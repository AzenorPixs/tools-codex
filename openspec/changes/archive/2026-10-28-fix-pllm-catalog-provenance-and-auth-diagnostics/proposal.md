# Provenance TFL et diagnostics d'authentification PLLM

## Why
L'évaluation du 28 octobre 2026 à 11:28 a consommé le catalogue du plugin daté du 14 septembre, alors qu'une collecte autonome du même jour retient des gratuits Go et OpenRouter. Les modes 3/4/6 annoncent une absence sans identifier cette source. Le mode2 échoue séparément sur le contrôle des quotas avec HTTP 401.

## What Changes
- Tracer chemin, date, âge et avertissements du catalogue utilisé, sans seuil arbitraire de péremption et sans collecte TFL implicite.
- Distinguer l'absence de gratuit dans ce catalogue, les exclusions locales et les refus de ressources ; identifier phase, endpoint et statut HTTP filtré.
- Documenter la sélection explicite de la collecte TFL réellement produite.
- Qualifier les deux distributions, effectuer les contrôles réels bornés et aligner la release commune sur 0.7.23.
- Exclure de Git les trois fichiers de résultats/mémoire PLLM régénérables afin que les contrôles réels ne publient pas les quotas ni l'historique ; préserver leurs copies locales.

## Impact
Évaluateurs et skills PLLM autonome/embarqué, commande PLLM, tests, README, TECHNICAL, BUILD, CHANGELOG et métadonnées de release. Aucun changement de seuil, effort, compte, secret, priorité, timer ou configuration OpenCode. Un refus fournisseur persistant reste un blocage externe identifié, pas une réussite inventée.
