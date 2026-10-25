"""Débit moyen sur requête complète : rafales, fiabilité et mémoire du protocole."""
import io
import itertools
import json
import unittest
from unittest.mock import patch

from test_extension_qualification import PLLM, TFL, load_script
import test_pllm_free_fallback as fixtures
import test_free_performance as free_tests


def stream(events, done=True):
    return io.BytesIO(b''.join(b'data: '+json.dumps(event).encode()+b'\n' for event in events)
                      +(b'data: [DONE]\n' if done else b''))


def chat_events(count=100, reasoning_tokens=0, chunks=1, finish='stop', thinking=False):
    events=[{'choices':[{'delta':{'reasoning':'thinking'}}]}] if thinking else []
    events += [{'choices':[{'delta':{'content':'code'}}]} for _ in range(chunks)]
    events[-1]['choices'][0]['finish_reason']=finish
    events[-1]['usage']={'completion_tokens':count,
                         'completion_tokens_details':{'reasoning_tokens':reasoning_tokens}}
    return events


def response_events(count):
    return [{'type':'response.output_text.delta','delta':'code'},
            {'type':'response.output_text.delta','delta':'more'},
            {'type':'response.completed','response':{'status':'completed','usage':{'output_tokens':count}}}]


class ThroughputMeasurementTests(unittest.TestCase):
    workspace=fixtures.PllmFreeFallbackTests.workspace
    run_evaluation=fixtures.PllmFreeFallbackTests.run_evaluation

    def run_stream(self, script, events, ticks, provider='openrouter', protocol='chat_completions', done=True, model=None):
        engine=load_script(script).performance
        model=model if model is not None else {}
        model.update(provider=provider,model_id='measurement-fixture',reasoning='high',
                     api_protocol=protocol,api_endpoint='https://opencode.ai/zen/v1/'+protocol)
        with patch.object(engine,'request',return_value=stream(events,done)) as request, \
             patch.object(engine.time,'monotonic',side_effect=ticks), \
             patch.object(engine.signal,'alarm'):
            complete=engine.benchmark(model,'offline-fixture',1024,
                                      {'reasoning':{'supported_efforts':['high']}},session_id='private-session')
        return complete,model,request

    def test_mercury_burst_uses_full_request_instead_of_microsecond_span(self):
        for script in (*PLLM,*TFL):
            events=chat_events(715,462,chunks=2,thinking=True)
            ticks=(0,1.2,1.7748,1.7748+252/2147441.04,1.7750,1.7751)
            complete,model,_=self.run_stream(script,events,ticks)
            self.assertTrue(complete)
            self.assertEqual(model['tokens_per_second'],142.527)
            self.assertEqual(model['performance_test']['request_seconds'],1.7751)
            self.assertEqual(model['performance_test']['generation_seconds'],0.0001)
            self.assertEqual(model['throughput_window'],'request_total')
            self.assertEqual(model['measurement_protocol_version'],8)

    def test_fragment_coalescing_does_not_change_full_request_average(self):
        schedules=((1,(0,1.5,1.8,2)),
                   (2,(0,1.5,1.500001,1.8,2)),
                   (3,(0,.5,1,1.5,1.8,2)))
        for script in (*PLLM,*TFL):
            values=[]
            for chunks,ticks in schedules:
                complete,model,_=self.run_stream(script,chat_events(100,chunks=chunks),ticks)
                self.assertTrue(complete)
                values.append(model['tokens_per_second'])
            self.assertEqual(values,[50,50,50])

    def test_complete_single_block_can_have_zero_inter_fragment_duration(self):
        for script in (*PLLM,*TFL):
            complete,model,_=self.run_stream(script,chat_events(),(0,1,1.5,2))
            self.assertTrue(complete)
            self.assertEqual(model['performance_test']['generation_seconds'],0)
            self.assertEqual(model['tokens_per_second'],50)

    def test_unrounded_request_duration_is_the_denominator(self):
        for script in (*PLLM,*TFL):
            _,model,_=self.run_stream(script,chat_events(),(0,.5,1,1.23456))
            self.assertEqual(model['performance_test']['duration_seconds'],1.2346)
            self.assertEqual(model['performance_test']['request_seconds'],1.23456)
            self.assertEqual(model['tokens_per_second'],round(100/1.23456,3))
            self.assertNotEqual(model['tokens_per_second'],round(100/1.2346,3))

    def test_chat_response_only_count_excludes_reasoning_without_minus_one(self):
        for script in (*PLLM,*TFL):
            for provider in ('openrouter','deepseek'):
                _,model,_=self.run_stream(script,chat_events(101,80,thinking=True),
                                          (0,.2,1,1.5,2),provider=provider)
                self.assertEqual(model['tokens_per_second'],10.5)
                self.assertEqual(model['throughput_scope'],'response_only')

    def test_responses_keeps_global_count_and_first_visible_ttft(self):
        for script in (*PLLM,*TFL):
            for provider in ('opencodego','opencode'):
                events=[{'type':'response.reasoning_text.delta','delta':'think'},*response_events(101)]
                _,model,request=self.run_stream(script,events,(0,.1,1,1.5,1.8,2),
                                                provider=provider,protocol='responses',done=False)
                self.assertEqual(model['tokens_per_second'],50.5)
                self.assertEqual(model['ttft_seconds'],1)
                self.assertEqual(model['performance_test']['ttft_reasoning_seconds'],.1)
                self.assertEqual(model['throughput_scope'],'reasoning_and_response')
                self.assertEqual(request.call_args.args[2]['reasoning'],{'effort':'high'})
                self.assertNotIn('private-session',json.dumps(model))

    def test_messages_uses_the_same_total_window(self):
        for script in (*PLLM,*TFL):
            events=[{'type':'message_start','message':{'usage':{'output_tokens':0}}},
                    {'type':'content_block_delta','delta':{'type':'thinking_delta','thinking':'think'}},
                    {'type':'content_block_delta','delta':{'type':'text_delta','text':'code'}},
                    {'type':'message_delta','delta':{'stop_reason':'end_turn'},'usage':{'output_tokens':101}},
                    {'type':'message_stop'}]
            _,model,request=self.run_stream(script,events,(0,.1,.2,1,1.5,1.8,2),
                                            provider='opencode',protocol='messages',done=False)
            self.assertEqual(model['tokens_per_second'],50.5)
            self.assertEqual(request.call_args.args[2]['output_config'],{'effort':'high'})
            self.assertNotIn('stream_options',request.call_args.args[2])

    def test_invalid_total_duration_never_publishes_a_rate_or_stale_measure(self):
        for script in (*PLLM,*TFL):
            for end in (0,-1,float('nan'),float('inf')):
                model={'tokens_per_second':9999999,'ttft_seconds':5}
                with self.subTest(script=script,end=end), self.assertRaisesRegex(RuntimeError,'Durée totale'):
                    self.run_stream(script,chat_events(),(0,0,0,end),model=model)
                self.assertIsNone(model['tokens_per_second'])
                self.assertIsNone(model['ttft_seconds'])
                json.dumps(model,allow_nan=False)

    def test_invalid_api_token_counts_are_not_replaced_with_fragment_counts(self):
        for script in (*PLLM,*TFL):
            for count,reasoning in ((None,0),(True,0),(101.0,0),(0,0),(-5,0),
                                     (101,102),(101,-1),(101,True),(101,'80')):
                model={'tokens_per_second':9999999}
                with self.subTest(count=count,reasoning=reasoning), self.assertRaisesRegex(RuntimeError,'Comptage'):
                    self.run_stream(script,chat_events(count,reasoning),(0,1,1.5,2),model=model)
                self.assertIsNone(model['tokens_per_second'])

    def test_truncated_or_incomplete_stream_does_not_keep_an_old_rate(self):
        for script in (*PLLM,*TFL):
            model={'tokens_per_second':9999999}
            complete,model,_=self.run_stream(script,chat_events(finish='length'),(0,1,1.5,2),model=model)
            self.assertFalse(complete)
            self.assertIsNone(model['tokens_per_second'])
            with self.assertRaisesRegex(RuntimeError,'Réponse absente'):
                self.run_stream(script,chat_events(finish=None),(0,1,2),done=False,model=model)
            self.assertIsNone(model['tokens_per_second'])

    def test_ranking_uses_request_average_instead_of_the_fastest_received_burst(self):
        for script in PLLM:
            module,path,_=self.workspace(script)
            def behavior(model,budget):
                burst=model['model_id']=='paid-a'
                ticks=(0,9.99,9.990001,9.999,10) if burst else (0,.1,.9,.99,1)
                with patch.object(module.performance,'request',return_value=stream(response_events(1000 if burst else 400),False)), \
                     patch.object(module.performance.time,'monotonic',side_effect=ticks), \
                     patch.object(module.performance.signal,'alarm'):
                    return module.performance.benchmark(model,'offline-fixture',budget,{},session_id='fixture')
            data,_,_=self.run_evaluation(module,path,benchmark_behavior=behavior,active=True)
            self.assertEqual(data['models'][0]['model_id'],'paid-b')
            self.assertEqual(data['models'][0]['tokens_per_second'],400)
            self.assertEqual([m['tokens_per_second'] for m in data['models'][0]['candidate_results']],[100,400])

    def test_tfl_excludes_free_burst_that_fails_the_average_threshold(self):
        for script in TFL:
            module=load_script(script)
            def request(url,key,body,extra_headers=None):
                return stream(response_events(300 if body['model']=='good' else 100),False)
            audit=[];excluded=[]
            with patch.object(module.performance,'request',side_effect=request), \
                 patch.object(module.performance.time,'monotonic',side_effect=itertools.cycle((0,9.99,9.990001,9.999,10))), \
                 patch.object(module.performance.signal,'alarm'):
                rows=module.qualify_free_models([free_tests.candidate('good'),free_tests.candidate('bad')],
                                                excluded,'opencode_go','offline-fixture',audit)
            self.assertEqual([row['id'] for row in rows],['good'])
            self.assertEqual(rows[0]['tokens_per_second'],30)
            self.assertEqual(excluded[0]['tokens_per_second'],10)
            self.assertEqual(len(excluded[0]['performance_test']['attempts']),4)
            self.assertEqual(excluded[0]['throughput_metric'],'request_average_v1')

    def test_old_high_memory_is_preserved_but_new_profile_starts_fresh_and_is_reusable(self):
        for script in PLLM:
            module,path,_=self.workspace(script)
            old=module.load_current()['models'][2]
            old.update(model_id='free-go',throughput_scope='reasoning_and_response',api_protocol='responses',
                       api_endpoint='https://opencode.ai/zen/go/v1/responses')
            legacy=module.identity(old)
            for field in ('throughput_metric','throughput_window','measurement_protocol_version'):
                legacy.pop(field)
            module.MEMORY_PATH.parent.mkdir()
            module.MEMORY_PATH.write_text(json.dumps({'schema_version':2,'policies':{'mode3':{
                'identity':legacy,'last_successful_max_tokens':8192}}}))
            def behavior(model,budget):
                model.update(ttft_seconds=1,tokens_per_second=40)
                return budget>=2048
            first,events,_=self.run_evaluation(module,path,benchmark_behavior=behavior,forced={'mode':'mode3'})
            self.assertEqual([e[3] for e in events if e[0]=='benchmark'],[1024,2048])
            self.assertEqual(first['models'][2]['throughput_metric'],'request_average_v1')
            memory=module.load_memory()['policies']['mode3']
            self.assertEqual(len(memory['configurations']),2)
            self.assertIn(json.dumps(legacy,sort_keys=True),memory['configurations'])
            _,events,_=self.run_evaluation(module,path,benchmark_behavior=behavior,forced={'mode':'mode3'})
            self.assertEqual([e[3] for e in events if e[0]=='benchmark'],[2048])

    def test_tfl_and_pllm_publish_the_new_metric_without_changing_numeric_limits(self):
        for script in (*PLLM,*TFL):
            engine=load_script(script).performance
            self.assertEqual(engine.FREE_CRITERIA,{'minimum_context_tokens':1000000,'ttft_lt_seconds':30,'tokens_per_second_gt':20})
            self.assertEqual(engine.limits({'mode':'mode1','is_free':False}),(90,15))
            self.assertEqual(engine.limits({'mode':'mode5','is_free':True}),(30,20))
        for script in PLLM:
            module,path,_=self.workspace(script)
            data,_,text=self.run_evaluation(module,path,forced={'mode':'mode3'})
            self.assertEqual(data['protocol_version'],8)
            self.assertIn('Débit moyen sur la requête complète',text)
            self.assertEqual(data['models'][2]['measurement_protocol_version'],8)


if __name__=='__main__':
    unittest.main()
