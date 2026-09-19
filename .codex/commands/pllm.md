---
description: Évaluer en temps réel les politiques PLLM et sélectionner le premier modèle valide
---

Utilise obligatoirement la skill `pllm` installée par Tools Codex.

À chaque invocation, exécute réellement le script d’évaluation :

- sans argument : `python3 scripts/evaluate.py`
- avec l’argument `active` : `python3 scripts/evaluate.py active`

Exécute la commande depuis le répertoire du skill PLLM installé. Ne remplace pas cette exécution par une lecture des anciens fichiers `data/pllm-current.*`. Le script contrôle les quotas avant les tests, publie les résultats et ne doit jamais afficher de secret.

Restitue exactement la sortie produite par le script, sans ajouter de titre, commentaire, légende ou conclusion. Si l’exécution échoue, indique l’erreur réelle et ne présente pas les fichiers comme actualisés.

Argument reçu : `$ARGUMENTS`

