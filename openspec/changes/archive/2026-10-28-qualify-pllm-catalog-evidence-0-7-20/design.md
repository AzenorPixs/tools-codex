# Conception

## Chaîne des preuves

Les registres d'investigation restent liés au fournisseur, à l'identifiant et
au protocole. Pour OpenCode Go, TFL revalide l'empreinte de la documentation
officielle avant de réintégrer un candidat. Le rapport conserve les constats
et les motifs d'exclusion ; les prix, routes, disponibilités et performances
ne sont jamais édités manuellement.

Les pages HTML peuvent changer leurs scripts ou leur balisage sans modifier
leur contenu documentaire. L'empreinte est calculée sur leur texte visible
normalisé en UTF-8 NFC avec les espaces consécutifs réduits. Les sources non
HTML gardent leur empreinte SHA-256 des octets reçus. Chaque entrée précise la
méthode afin que TFL et PLLM appliquent le même recontrôle.

Pour DeepSeek direct, PLLM consomme une preuve officielle pour
`deepseek-v4-flash` sur Chat Completions. La documentation précise que la
valeur demandée `medium` est acceptée comme alias puis mappée à `high`. Selon
la décision du développeur du 28 octobre 2026, cette acceptation suffit à
satisfaire l'exigence de paramètre. PLLM envoie `medium`, conserve le mapping
documenté et mesure toujours réponse, TTFT et débit réels ; aucun résultat de
benchmark n'est hérité.

## Évaluation et publication

L'exécution produit d'abord un catalogue TFL frais. PLLM reçoit explicitement
ce catalogue et parcourt les sept politiques en mode normal. Les contrôles de
ressources restent séquentiels avant chaque requête ; les gratuits ne
consultent aucun quota ou solde. Les rapports locaux sont conservés sous
`reports/`, hors artefacts distribués.

Les résultats de génération restent distincts des preuves documentaires.
La validité reste déterminée par les mesures courantes, les ressources et les
seuils déjà spécifiés. Le plafond moyen de base OpenRouter payant est fixé à
0,10 EUR/M après conversion BCE, recalculé par TFL à la collecte et par PLLM
mode5 à la sélection, y compris pour les anciens catalogues et rangs forcés.
Les candidats gratuits non présents, non accessibles
ou en échec restent invalides avec leur motif, sans élargissement de catégorie.

Le moteur TFL/PLLM doit conserver `copy` pour copier la preuve d'acceptation
Medium de la réponse complète, puis poursuivre jusqu'au calcul du débit. La
régression valide ce chemin dans les copies autonomes et embarquées ; le
diagnostic d'exécution précédent ne contenait pas de traceback exploitable.

## Release

`0.7.20` est la prochaine version après `0.7.19`. `VERSION` reste la source
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
