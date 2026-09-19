---
description: Générer le rapport unifié des fournisseurs LLM, OpenCode Go puis OpenRouter
---

Utilise obligatoirement la skill `tfl` installée par Tools Codex.

L’exécution de TFL DOIT toujours être effectuée hors sandbox pour permettre
l’accès réseau aux APIs OpenCode Go et OpenRouter. Dans Codex, demande une
exécution autorisée hors sandbox ; si cette autorisation est refusée, arrête la
commande et restitue l’erreur sans tenter de repli sandboxé.

À chaque invocation, exécute réellement le générateur autonome :

- sans argument : `python3 scripts/test_fournisseur_llm.py` ;
- avec `mode1`, `mode2` ou `auto` : transmet cet argument au générateur ;
- avec `--policy mode1`, `--policy mode2` ou `--policy auto` : transmet cette option au générateur.

Exécute la commande depuis le répertoire du skill TFL installé. Le tableau OpenCode Go
DOIT être produit et affiché en premier, puis le tableau OpenRouter en second.
Restitue intégralement la sortie produite par le générateur, sans masquer les
lignes de rapport ni les codes couleur. Les clés API ne doivent jamais être
affichées.

Argument reçu : `$ARGUMENTS`
