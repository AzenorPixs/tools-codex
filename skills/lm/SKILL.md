---
name: lm
description: Gérer la liste noire commune des modèles LLM exclus des sélections et tests TFL et PLLM. Utiliser pour $lm, /LM ou une modification explicite de cette liste.
---

Depuis le dossier de ce skill, exécute le script avec les arguments demandés :

```text
python3 -B scripts/lm.py
python3 -B scripts/lm.py LIST
python3 -B scripts/lm.py ADD identifiant
python3 -B scripts/lm.py REMOVE identifiant
```

Sans argument, affiche la liste sans écriture. ADD et REMOVE correspondent à
une demande explicite d'ajout ou de retrait ; une simple consultation ou une
explication n'autorise pas une mutation. Restitue le résultat ou l'erreur en
français. Ne lance pas TFL ou PLLM pour consulter ou modifier la liste.

Les distributions utilisent CODEX_HOME/lm/blacklist.json, avec ~/.codex comme
CODEX_HOME par défaut. Sans fichier, mimo-v2.5 et muse-spark-1.2-contributor
sont exclus en mémoire ; LIST ne
crée pas ce fichier. Les modifications sont atomiques et idempotentes.
Une liste vide explicite reste vide. Une liste illisible ou invalide bloque
sans écrasement ni réinitialisation. Ne répare pas silencieusement son contenu.

L'identifiant est comparé sans distinction de casse, après retrait du préfixe
fournisseur et des suffixes :free ou -free. mimo-v2.5 exclut ainsi
xiaomi/mimo-v2.5:free ; mimo-v2.50 et mimo-v2.5-pro restent distincts.
LM est l'unique liste noire de TFL et PLLM. Toute entrée, y compris
muse-spark-1.2-contributor, est retirable avec REMOVE ; aucune exclusion
permanente ne subsiste. TFL et PLLM relisent la liste à leur prochaine invocation ;
LM ne réécrit pas les anciens rapports et ne configure pas OpenCode.

Maintenir scripts/model_blacklist.py identique dans les distributions
autonomes et embarquées de LM, TFL et PLLM. Les paquets restent indépendants.
Le stockage utilisateur hors cache est préservé lors des mises à jour TCU.

`/LM` est un déclencheur du skill et une commande source ; ce fichier
n'enregistre pas automatiquement une slash native. `$lm` est directement
invocable après découverte ou installation du skill.

La commande canonique est `/LM` ; `/lm` reste
un alias compatible. L’identifiant technique du skill reste en minuscules.
