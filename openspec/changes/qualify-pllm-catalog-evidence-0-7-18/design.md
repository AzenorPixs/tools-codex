# Conception

## Chaîne des preuves

Les registres d'investigation restent liés au fournisseur, à l'identifiant et
au protocole. Pour OpenCode Go, TFL revalide l'empreinte de la documentation
officielle avant de réintégrer un candidat. Le rapport conserve les constats
et les motifs d'exclusion ; les prix, routes, disponibilités et performances
ne sont jamais édités manuellement.

Pour DeepSeek direct, PLLM consomme une preuve officielle pour
`deepseek-v4-flash` sur Chat Completions. La documentation précise que la
valeur demandée `medium` est mappée à `high`. Le mode7 reste donc invalide sous
le contrat Medium effectif et indique cette incompatibilité dans son état.
Aucune génération ne part pour ce mode avec un autre effort.

## Évaluation et publication

L'exécution produit d'abord un catalogue TFL frais. PLLM reçoit explicitement
ce catalogue et parcourt les sept politiques en mode normal. Les contrôles de
ressources restent séquentiels avant chaque requête ; les gratuits ne
consultent aucun quota ou solde. Les rapports locaux sont conservés sous
`reports/`, hors artefacts distribués.

Les résultats de génération restent distincts des preuves documentaires.
La validité reste déterminée par les mesures courantes, les ressources et les
seuils déjà spécifiés. Les candidats gratuits non présents, non accessibles
ou en échec restent invalides avec leur motif, sans élargissement de catégorie.

## Release

`0.7.18` est la prochaine version après `0.7.17`. `VERSION` reste la source
de vérité. La valeur est alignée dans la métadonnée Python, le README et les
six manifestes publiés. Les copies autonomes et embarquées des scripts,
skills et registres sont contrôlées pour leur parité.

## Sources officielles examinées

- Meta Model API — raisonnement Muse Spark :
  https://dev.meta.ai/docs/reasoning
- QwenCloud — Messages API, modèles Qwen3.8 et effort Medium :
  https://docs.qwencloud.com/api-reference/chat/anthropic
- DeepSeek — paramètres Chat Completions et mapping `medium` vers `high` :
  https://api-docs.deepseek.com/api/create-chat-completion/

Les contenus courants et empreintes seront recontrôlés au moment de la
constitution des registres. Ces sources n'établissent ni accès aux comptes ni
mesures de performance.
