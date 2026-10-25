---
description: Générer le rapport LLM OpenCode Go, OpenCode général puis OpenRouter
---

Utilise obligatoirement la skill `tfl` installée par Tools Codex.

L’exécution de TFL DOIT toujours être effectuée hors sandbox pour permettre
l’accès réseau aux APIs OpenCode Go, OpenCode général et OpenRouter. Dans Codex, demande une
exécution autorisée hors sandbox ; si cette autorisation est refusée, arrête la
commande et restitue l’erreur sans tenter de repli sandboxé.

À chaque invocation, exécute réellement le générateur autonome :

- sans argument : `python3 scripts/test_fournisseur_llm.py` ;
- avec `mode1`, `mode2` ou `auto` : transmet cet argument au générateur ;
- avec `--policy mode1`, `--policy mode2` ou `--policy auto` : transmet cette option au générateur.

Exécute la commande depuis le répertoire du skill TFL installé. Le tableau OpenCode Go
DOIT être produit et affiché en premier, puis le catalogue général OpenCode,
puis OpenRouter. Les trois tableaux DOIVENT conserver les mêmes colonnes.
Tester les gratuits des trois catalogues en HIGH, puis XHIGH si HIGH est
indisponible et XHIGH pris en charge, sans contrôle de quota. Exiger contexte
≥1M, gratuité vérifiée, réponse complète, TTFT <30 s et débit >20 tokens/s.
Exclure les échecs de models, conserver leurs preuves et afficher le tableau
commun des essais gratuits après les trois tableaux fournisseurs.
Restitue intégralement la sortie produite par le générateur, sans masquer les
lignes de rapport ni les codes couleur. Les clés API ne doivent jamais être
affichées.

Argument reçu : `$ARGUMENTS`
