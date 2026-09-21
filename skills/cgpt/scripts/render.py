#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent / 'data'

def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')

def color(remaining):
    return '🟢' if remaining >= 75 else '🟡' if remaining >= 50 else '🟠' if remaining >= 25 else '🔴'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('view', nargs='?', choices=['7u'])
    args = parser.parse_args()
    raw = json.load(sys.stdin)
    observed = datetime.fromisoformat(raw['observed_at']).astimezone(ZoneInfo('Europe/Paris')).isoformat(timespec='seconds')
    rows = []
    for item in raw['windows']:
        used = item.get('used_percent')
        if used is not None and (not isinstance(used, (int, float)) or not 0 <= used <= 100):
            raise ValueError('Pourcentage hors limites')
        remain = None if used is None else max(0, min(100, 100-used))
        reset = item.get('resets_at')
        rows.append({'bucket':item['bucket'], 'duration_minutes':item.get('duration_minutes'), 'used_percent':used, 'remaining_percent':remain,
                     'reset_paris':None if reset is None else datetime.fromtimestamp(reset, ZoneInfo('Europe/Paris')).isoformat(timespec='seconds')})
    data = {'schema_version':1, 'observed_at':observed, 'scope':'shared_account', 'windows':rows, 'error':raw.get('error'),
            'reset_credits_available':raw.get('reset_credits_available')}
    lines = ['| Compteur du compte | Fenêtre | Utilisé | Restant | Réinitialisation Europe/Paris | Consulté le |', '|---|---|---|---|---|---|']
    for r in rows:
        duration = r['duration_minutes']
        label = '7 jours' if duration == 10080 else '5 heures' if duration == 300 else str(duration)+' minutes' if duration is not None else 'Non disponible'
        remaining = 'Non disponible' if r['remaining_percent'] is None else color(r['remaining_percent'])+' '+str(r['remaining_percent'])+' %'
        values = [r['bucket'],label,'Non disponible' if r['used_percent'] is None else str(r['used_percent'])+' %',remaining,r['reset_paris'] or 'Non disponible',observed]
        lines.append('| '+' | '.join(map(cell,values))+' |')
    if not rows:
        lines.append('| Non disponible | — | — | — | '+cell(raw.get('error') or 'Source indisponible')+' | '+observed+' |')
    cutoff = datetime.fromisoformat(observed) - timedelta(days=7)
    history = []
    history_path = ROOT/'quota-history.jsonl'
    if history_path.exists():
        for line in history_path.read_text(encoding='utf-8').splitlines():
            point = json.loads(line)
            stamp = datetime.fromisoformat(point['observed_at'])
            if cutoff <= stamp <= datetime.fromisoformat(observed):
                history.append(point)
    history.sort(key=lambda point: point['observed_at'])
    stats = []
    if raw.get('reset_credits_available') is not None:
        stats.append(['Crédits de réinitialisation disponibles', str(raw['reset_credits_available']), 'Aucun crédit utilisé par cette commande'])
    stats.append(['Consultations enregistrées sur les 7 derniers jours', str(len(history)+1), 'Points de mesure, pas sessions de travail'])
    if history:
        stats.append(['Période effectivement observée', history[0]['observed_at']+' → '+observed, 'Historique local du compte ; ne mesure pas le temps actif'])
    for row in rows:
        if row['used_percent'] is None or row['reset_paris'] is None:
            continue
        baseline = None
        for point in reversed(history):
            previous = next((w for w in point['windows'] if w['bucket']==row['bucket'] and w['duration_minutes']==row['duration_minutes']), None)
            if previous is None:
                continue
            if previous['reset_paris'] != row['reset_paris'] or previous['used_percent'] is None:
                break
            baseline = (point, previous)
        if baseline:
            point, previous = baseline
            delta = row['used_percent'] - previous['used_percent']
            stats.append([row['bucket']+' — variation sur '+str(row['duration_minutes'])+' min', f'{delta:+g} points',
                          'Depuis '+point['observed_at']+' ; compteur à la précision fournie, sans attribution à cette tâche'])
    data['observed_statistics'] = stats
    if stats:
        lines += ['', '| Autre statistique du compte | Valeur | Portée |', '|---|---|---|']
        for stat in stats:
            lines.append('| '+' | '.join(map(cell,stat))+' |')
    ROOT.mkdir(exist_ok=True)
    for name, content in [('cgpt-current.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n'),('cgpt-current.md','\n'.join(lines)+'\n')]:
        p=ROOT/name; temp=p.with_name(p.name+'.tmp');temp.write_text(content,encoding='utf-8');temp.replace(p)
    with (ROOT/'quota-history.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(data,ensure_ascii=False)+'\n')
    if args.view == '7u':
        codex = next((row for row in rows if row['bucket'].casefold() == 'codex' and row['duration_minutes'] == 10080), None)
        print('Non disponible' if codex is None or codex['used_percent'] is None else f"{codex['used_percent']:g} %")
    else:
        print('\n'.join(lines))

if __name__ == '__main__':
    main()
