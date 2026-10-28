"""Qualification gratuite commune en Medium, sans réseau ni trousseau réel."""
from contextlib import ExitStack
import copy
import io
import json
from eur_fixtures import FX
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_extension_qualification import ROOT, PLLM, TFL, load_script
import test_pllm_free_fallback as fixtures
from test_pllm_http_diagnostics import failure


def candidate(name, section='opencode_go', free=True):
    row = fixtures.row(name, section, free)
    row.update(name=name, rank=1, output_label='Texte')
    if section != 'openrouter':
        prices = row['reference_pricing_usd_per_million_tokens']
        prices['average' if section == 'opencode' else 'average_off_peak'] = 0 if free else .1
    else:
        row['average'] = 0 if free else .1
    row['reasoning_capabilities'] = {'supported_efforts': ['medium', 'high', 'xhigh']}
    return row


class FreePerformanceTests(unittest.TestCase):
    workspace = fixtures.PllmFreeFallbackTests.workspace
    run_evaluation = fixtures.PllmFreeFallbackTests.run_evaluation

    def successful_benchmark(self, model, key, budget, metadata, session_id=None):
        self.assertEqual(model['reasoning'], 'medium')
        acceptance = {'status': 'accepted', 'parameter': 'medium',
                      'verified_by': 'completed_api_response'}
        model.update(ttft_seconds=1, tokens_per_second=40,
                     reasoning_acceptance=acceptance,
                     performance_test={'status': 'completed', 'max_tokens': budget,
                                        'reasoning_acceptance': acceptance})
        return True

    def test_four_embedded_engines_are_identical(self):
        engines=[p.with_name('performance.py') for p in (*PLLM, *TFL)]
        self.assertEqual(len({p.read_bytes() for p in engines}), 1)

    def test_tfl_strict_free_thresholds_on_all_catalogs(self):
        for script in TFL:
            module=load_script(script)
            for section in ('opencode_go', 'opencode', 'openrouter'):
                for ttft, throughput, valid in ((29.999,20.001,True),(30,21,False),
                                                (1,20,False),(30.001,40,False)):
                    with self.subTest(section=section, ttft=ttft, throughput=throughput):
                        rows=[candidate('free',section),candidate('paid',section,False)]
                        excluded=[]; audit=[]

                        def bench(model,key,budget,metadata,session_id=None):
                            model.update(ttft_seconds=ttft,tokens_per_second=throughput,
                                         performance_test={'status':'completed','max_tokens':budget})
                            return True

                        with patch.object(module.performance,'benchmark',side_effect=bench) as benchmark, \
                             patch.object(module.performance,'request',side_effect=AssertionError('Réseau interdit')), \
                             patch.object(module.performance,'get',side_effect=AssertionError('Aucun quota')):
                            retained=module.qualify_free_models(rows,excluded,section,'offline-key',audit)
                        self.assertEqual([r['id'] for r in retained],['free','paid'] if valid else ['paid'])
                        self.assertEqual(benchmark.call_count,1 if valid else 4)
                        self.assertEqual(len(excluded),int(not valid))
                        self.assertEqual(audit[0]['state'],'Valide' if valid else 'Invalide')
                        self.assertEqual(audit[0]['quota_status'],'not_applicable')
                        if not valid:
                            self.assertIn('Seuil gratuit',excluded[0]['reason'])

    def test_tfl_http_errors_are_excluded_without_more_budgets(self):
        for script in TFL:
            module=load_script(script)
            for status in (400,401,403,429):
                audit=[]; excluded=[]
                with patch.object(module.performance,'benchmark',side_effect=failure(status,{'error':{'message':'private-body'}})) as bench:
                    retained=module.qualify_free_models([candidate('free')],excluded,'opencode_go','offline-key',audit)
                self.assertEqual(retained,[])
                self.assertEqual(bench.call_count,1)
                self.assertIn('HTTP '+str(status),excluded[0]['reason'])
                self.assertNotIn('private-body',json.dumps(excluded))
                self.assertIsNone(audit[0]['ttft_seconds'])

    def test_tfl_truncation_advances_and_only_a_full_response_is_valid(self):
        for script in TFL:
            module=load_script(script)
            calls=[]
            def bench(model,key,budget,metadata,session_id=None):
                calls.append(budget)
                self.successful_benchmark(model,key,budget,metadata,session_id)
                return budget==4096
            excluded=[]; audit=[]
            with patch.object(module.performance,'benchmark',side_effect=bench):
                retained=module.qualify_free_models([candidate('free')],excluded,'opencode_go','offline-key',audit)
            self.assertEqual(calls,[1024,2048,4096])
            self.assertEqual(len(retained),1)
            self.assertEqual(excluded,[])

    def test_absent_key_blocks_but_high_only_metadata_can_be_proved_by_medium_response(self):
        for script in TFL:
            module=load_script(script)
            row=candidate('free','openrouter')
            excluded=[]
            with patch.object(module.performance,'benchmark') as benchmark:
                retained=module.qualify_free_models([row],excluded,'openrouter','',[])
            self.assertEqual(retained,[])
            benchmark.assert_not_called()
            self.assertTrue(excluded[0]['reason'])

            row=candidate('free','openrouter')
            row['reasoning_capabilities']={'supported_efforts':['high','xhigh']}
            excluded=[]; audit=[]
            with patch.object(module.performance,'benchmark',side_effect=self.successful_benchmark) as benchmark:
                retained=module.qualify_free_models([row],excluded,'openrouter','offline-key',audit)
            self.assertEqual([item['id'] for item in retained],['free'])
            benchmark.assert_called_once()
            self.assertEqual(audit[0]['reasoning_acceptance']['status'],'accepted')

    def test_medium_metadata_and_transport_contracts(self):
        for script in (*PLLM,*TFL):
            engine=load_script(script).performance
            for provider,protocol,field in (('opencodego','responses','reasoning'),
                                             ('opencode','chat_completions','reasoning_effort'),
                                             ('opencodego','messages','output_config')):
                model={'provider':provider,'api_protocol':protocol}
                options=engine.reasoning(model,1024,{'reasoning':{'supported_efforts':['medium']}})
                self.assertEqual(model['reasoning'],'medium')
                self.assertEqual(options[field],'medium' if field=='reasoning_effort' else {'effort':'medium'})
            self.assertEqual(engine.reasoning({'provider':'openrouter'},1024,
                                              {'reasoning':{'supports_max_tokens':True}}),
                             {'reasoning': {'effort': 'medium'}})
            self.assertEqual(engine.reasoning({'provider':'deepseek'},1024,{'reasoning': {'supported_efforts': ['medium']}}),
                             {'reasoning_effort':'medium','thinking':{'type':'enabled'}})
            for unsupported in (['low'], ['high'], ['xhigh'], ['high', 'xhigh']):
                self.assertEqual(engine.reasoning(
                    {'provider':'openrouter'},1024,{'reasoning':{'supported_efforts':unsupported}}),
                    {'reasoning': {'effort': 'medium'}})

    def test_pllm_free_modes_use_strict_limits_router_paid_skips_benchmark(self):
        for script in PLLM:
            module,path,_=self.workspace(script)
            def behavior(model,budget):
                model.update(ttft_seconds=40,tokens_per_second=18)
                return True
            free,_,_=self.run_evaluation(module,path,exhausted=True,benchmark_behavior=behavior,forced={'mode':'mode3'})
            self.assertEqual(free['models'][2]['state'],'Invalide')
            self.assertEqual(free['models'][2]['performance_criteria'],{'ttft_lt_seconds':30,'tokens_per_second_gt':20})
            paid,_,_=self.run_evaluation(module,path,benchmark_behavior=behavior,forced={'mode':'mode5'})
            self.assertEqual(paid['models'][4]['state'],'Valide')
            self.assertIsNone(paid['models'][4]['reasoning'])
            self.assertIsNone(paid['models'][4]['performance_criteria'])
            self.assertEqual(paid['models'][4]['performance_test']['status'],'not_required')

    def test_pllm_medium_rejection_does_not_retry_another_effort_or_tier(self):
        for script in PLLM:
            module,path,catalog=self.workspace(script)
            catalog['opencode_go']['models'][0]['reasoning_capabilities']={'supported_efforts':['medium','high','xhigh']}
            path.write_text(json.dumps(catalog))
            calls=[]
            def behavior(model,budget):
                calls.append((model['reasoning'],budget))
                raise failure(400,{'error':{'code':'invalid_value','param':'reasoning_effort'}})
            data,_,_=self.run_evaluation(module,path,benchmark_behavior=behavior,forced={'mode':'mode3'})
            self.assertEqual(calls,[('medium',1024)])
            self.assertEqual(data['models'][2]['state'],'Invalide')
            self.assertEqual(data['models'][2]['reasoning'],'medium')

    def test_tfl_medium_rejection_does_not_retry_another_effort_or_tier(self):
        for script in TFL:
            module=load_script(script)
            calls=[]
            def bench(model,key,budget,metadata,session_id=None):
                calls.append((model['reasoning'],budget))
                raise failure(400,{'error':{'code':'unsupported_parameter','param':'reasoning_effort'}})
            audit=[]
            with patch.object(module.performance,'benchmark',side_effect=bench):
                rows=module.qualify_free_models([candidate('free')],[],'opencode_go','offline-key',audit)
            self.assertEqual(calls,[('medium',1024)])
            self.assertEqual(rows,[])
            self.assertEqual(len(audit[0]['performance_test']['attempts']),1)

    def test_price_variants_cannot_be_misclassified_as_free(self):
        for script in (*PLLM,*TFL):
            engine=load_script(script).performance
            row=candidate('looks-free','openrouter')
            self.assertTrue(engine.is_free(row,'openrouter'))
            row['pricing_details']={'overrides':[{'prompt':1,'completion':0}]}
            self.assertFalse(engine.is_free(row,'openrouter'))
            row['pricing_details']={'unverified_fields':['overrides[0].prompt']}
            self.assertFalse(engine.is_free(row,'openrouter'))

    def test_tfl_full_publication_filters_failed_free_and_audits_it(self):
        for script in TFL:
            module=load_script(script)
            with tempfile.TemporaryDirectory(prefix='free-publication-',dir=ROOT/'tests') as directory:
                output=Path(directory)
                def bench(model,key,budget,metadata,session_id=None):
                    if model['model_id']=='fail':
                        raise failure(429,{'error':{'code':'FreeUsageLimitError','message':'private-body'}})
                    self.assertEqual(key,'router-offline' if model['provider']=='openrouter' else 'go-offline')
                    return self.successful_benchmark(model,key,budget,metadata,session_id)
                go=[candidate('pass'),candidate('fail'),candidate('paid',free=False)]
                router=[candidate('router','openrouter')]
                with ExitStack() as stack:
                    stack.enter_context(patch.object(module.performance, "fetch_eur_rates", return_value=FX))
                    stack.enter_context(patch.object(module,'parse_args',return_value=SimpleNamespace(policy_option=None,policy='auto',timeout=1,output_dir=output)))
                    stack.enter_context(patch.dict(module.os.environ,{'CODEX_HOME':str(output/'codex-profile')},clear=True))
                    stack.enter_context(patch.object(module,'select_secret',return_value=('mode2','go-offline')))
                    stack.enter_context(patch.object(module,'openrouter_secret',return_value='router-offline'))
                    for name in ('fetch_models','fetch_opencode_models','fetch_openrouter_models'):
                        stack.enter_context(patch.object(module,name,return_value={'data':[]}))
                    for name in ('fetch_go_metadata','fetch_opencode_metadata','fetch_go_pricing','fetch_opencode_pricing'):
                        stack.enter_context(patch.object(module,name,return_value={}))
                    stack.enter_context(patch.object(module,'build_rows',return_value=(go,[])))
                    stack.enter_context(patch.object(module,'build_openrouter_rows',return_value=(router,[])))
                    stack.enter_context(patch.object(module.performance,'benchmark',side_effect=bench))
                    stack.enter_context(patch.object(module.performance,'request',side_effect=AssertionError('Réseau interdit')))
                    stack.enter_context(patch('sys.stdout',new_callable=io.StringIO))
                    self.assertEqual(module.main(),0)
                data=json.loads((output/'tfl.json').read_text())
                self.assertNotIn('opencode',data)
                self.assertEqual([r['id'] for r in data['opencode_go']['models']],['pass','paid'])
                self.assertEqual(data['opencode_go']['excluded_models'][0]['id'],'fail')
                self.assertEqual(len(data['free_performance_results']),3)
                self.assertEqual(data['measurement_protocol_version'],8)
                self.assertEqual(data['throughput_metric'],'request_average_v1')
                self.assertEqual(data['throughput_window'],'request_total')
                markdown=(output/'tfl.md').read_text()
                self.assertIn('Tests de performance des modèles gratuits',markdown)
                self.assertIn('HTTP 429',markdown)
                self.assertNotIn('go-offline',json.dumps(data)+markdown)
                self.assertNotIn('router-offline',json.dumps(data)+markdown)
                self.assertNotIn('private-body',json.dumps(data)+markdown)

    def test_isolated_tfl_package_resolves_its_own_engine(self):
        for script in TFL:
            with tempfile.TemporaryDirectory(prefix='isolated-engine-',dir=ROOT/'tests') as directory:
                installed=Path(directory)/'scripts'/script.name
                installed.parent.mkdir()
                for source in (script,script.with_name('performance.py'),script.with_name('model_blacklist.py'),
                               script.with_name('model_evidence.py')):
                    installed.with_name(source.name).write_bytes(source.read_bytes())
                module=load_script(installed)
                self.assertEqual(module.performance.FREE_CRITERIA['ttft_lt_seconds'],30)

    def test_tfl_insufficient_context_never_reaches_generation(self):
        for script in TFL:
            module=load_script(script)
            row=candidate('short-free'); row['context_length']=999999
            excluded=[]
            with patch.object(module.performance,'benchmark') as bench:
                self.assertEqual(module.qualify_free_models([row],excluded,'opencode_go','offline-key',[]),[])
            bench.assert_not_called()
            self.assertIn('Contexte',excluded[0]['reason'])

    def test_nonfinite_or_missing_measurements_are_excluded_without_invalid_json(self):
        for script in TFL:
            module=load_script(script)
            for value in (None,float('nan'),float('inf')):
                def bench(model,key,budget,metadata,session_id=None):
                    model.update(ttft_seconds=value,tokens_per_second=40,
                                 performance_test={'status':'completed','max_tokens':budget})
                    return True
                excluded=[];audit=[]
                with patch.object(module.performance,'benchmark',side_effect=bench):
                    self.assertEqual(module.qualify_free_models([candidate('free')],excluded,'opencode_go','offline-key',audit),[])
                self.assertIsNone(audit[0]['ttft_seconds'])
                self.assertIn('Mesure de performance',excluded[0]['reason'])
                json.dumps(excluded,allow_nan=False)

    def test_invalid_reasoning_metadata_is_not_silently_ignored(self):
        for script in (*PLLM,*TFL):
            engine=load_script(script).performance
            for options in ({'supported_efforts':'high'}, {'supported_efforts':[1]}, {'supports_max_tokens':'yes'}):
                model={'provider':'opencodego','api_protocol':'chat_completions'}
                self.assertFalse(engine.effort_allowed({'reasoning':options}))
                self.assertEqual(engine.reasoning(model,1024,{'reasoning':options}),
                                 {'reasoning_effort':'medium'})

    def test_old_effort_memory_cannot_start_medium_benchmark_at_an_old_tier(self):
        for script in PLLM:
            module,path,_=self.workspace(script)
            previous=module.load_current()['models'][2]
            previous.update(model_id='free-go',provider='opencodego',reasoning='low',
                            throughput_scope='reasoning_and_response',api_protocol='responses',
                            api_endpoint='https://opencode.ai/zen/go/v1/responses')
            module.MEMORY_PATH.parent.mkdir()
            module.MEMORY_PATH.write_text(json.dumps({'schema_version':2,'policies':{'mode3':{
                'identity':module.identity(previous),'last_successful_max_tokens':8192}}}))
            data,events,_=self.run_evaluation(module,path,forced={'mode':'mode3'})
            self.assertEqual([event[3] for event in events if event[0]=='benchmark'],[1024])
            self.assertEqual(data['models'][2]['reasoning'],'medium')

    def test_tfl_sections_emptied_by_free_tests_are_published_without_blocking_others(self):
        for script in TFL:
            module=load_script(script)
            for failed_ids in (('free',), ('router',), ('free', 'router')):
                with self.subTest(script=script, failed_ids=failed_ids), tempfile.TemporaryDirectory(prefix='free-empty-',dir=ROOT/'tests') as directory:
                    output=Path(directory)
                    for name in ('tfl.json','tfl.md'):
                        (output/name).write_text('preserved')
                    def bench(model,key,budget,metadata,session_id=None):
                        if model['model_id'] in failed_ids:
                            raise failure(429)
                        return self.successful_benchmark(model,key,budget,metadata,session_id)
                    with ExitStack() as stack:
                        stack.enter_context(patch.object(module.performance, "fetch_eur_rates", return_value=FX))
                        stack.enter_context(patch.object(module,'parse_args',return_value=SimpleNamespace(policy_option=None,policy='auto',timeout=1,output_dir=output)))
                        stack.enter_context(patch.dict(module.os.environ,{'CODEX_HOME':str(output/'codex-profile')},clear=True))
                        stack.enter_context(patch.object(module,'select_secret',return_value=('mode1','offline-key')))
                        stack.enter_context(patch.object(module,'openrouter_secret',return_value='router-offline'))
                        for name in ('fetch_models','fetch_opencode_models','fetch_openrouter_models'):
                            stack.enter_context(patch.object(module,name,return_value={'data':[]}))
                        for name in ('fetch_go_metadata','fetch_opencode_metadata','fetch_go_pricing','fetch_opencode_pricing'):
                            stack.enter_context(patch.object(module,name,return_value={}))
                        stack.enter_context(patch.object(module,'build_rows',return_value=([candidate('free')],[])))
                        stack.enter_context(patch.object(module,'build_openrouter_rows',return_value=([candidate('router','openrouter')],[])))
                        benchmark=stack.enter_context(patch.object(module.performance,'benchmark',side_effect=bench))
                        stdout=stack.enter_context(patch('sys.stdout',new_callable=io.StringIO))
                        self.assertEqual(module.main(),0)
                        self.assertEqual(benchmark.call_count,2)
                    catalog=json.loads((output/'tfl.json').read_text())
                    for section,model_id in (('opencode_go','free'),('openrouter','router')):
                        current=catalog[section]
                        self.assertEqual(current['selection_status'],'empty' if model_id in failed_ids else 'available')
                        self.assertEqual(bool(current['models']),model_id not in failed_ids)
                        if model_id in failed_ids:
                            self.assertEqual(current['excluded_models'][0]['id'],model_id)
                            self.assertEqual(sum(current['exclusion_summary'].values()),1)
                    self.assertEqual(len(catalog['free_performance_results']),2)
                    self.assertNotIn('opencode',catalog)
                    self.assertIn('HTTP 429',stdout.getvalue())
                    self.assertNotIn('preserved',(output/'tfl.md').read_text())


if __name__=='__main__':
    unittest.main()
