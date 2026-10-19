## Why

La demande `/tcu check` doit fonctionner sans tirets. Le script et les exemples
exposent seulement --check, ce qui rend cette utilisation ambiguë.

## What Changes

- Accepter check comme argument de contrôle ; conserver --check compatible.
- Refuser check combiné avec --apply avant toute opération.
- Aligner skills, commande, catalogue CM et documentation dans les deux copies.
- Conserver la release 0.3.0 et les règles de contrôle sans écriture.

## Capabilities

### Modified Capabilities

- tools-codex-update : syntaxe et absence de mutation en contrôle.
- extension-distribution : syntaxe du catalogue CM.

## Impact

Correction demandée dans le périmètre TCU déjà validé. Aucun changement des
canaux, destinations ou règles de conflit. Le contrôle réel demandé est lu
sans application ; le conflit du lien de prompts reste signalé sans correction
hors périmètre. Les archives précédentes sont préservées.
