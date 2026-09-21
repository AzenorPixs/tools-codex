---
name: pllm
description: Évaluer en temps réel les modèles à chaque invocation de /pllm et déterminer la politique convergente de priorité des modèles LLM pour les agents de codage. Utiliser pour /pllm, PLLM ou une demande explicite de gestion de ses modes et conditions de validité.
---

# PLLM — Politique de priorité des modèles LLM

Présenter les entrées dans un tableau unique multi-colonnes avec cet ordre : Politique, Identifiant API, Fournisseur, TTFT, Tokens/s, État, Dernier palier réussi, Évalué le. Afficher ensuite les quotas et soldes sur une ligne dédiée par PLLM. L’état est `Valide` ou `Invalide` et dépend de la condition du mode.

## Mode 1

- Priorité : 1 (priorité la plus haute actuellement définie).
- Modèle : premier modèle du catalogue TFL OpenCode Go, classé par coût moyen croissant après application des filtres TFL.
- Raisonnement : Low.
- Fournisseur : OpenCode Go (`opencodego`).
- TTFT : évalué par le test, en secondes.
- Tokens/s : évalué par le test.
- Condition : `TTFT < 60 s ET Tokens/s > 15 ET utilisation_5h < 100 % ET utilisation_hebdomadaire < 100 % ET utilisation_mensuelle < 100 %`.
- État : `Valide` si tous les critères sont satisfaits ; `Invalide` si au moins un critère échoue.

Les seuils sont stricts : TTFT égal à 60 s, débit égal à 15 tokens/s ou utilisation égale à 100 % rendent le mode invalide.

### Référence du secret de l’hôte

La clé API est déclarée dans la base de secrets de l’hôte. Les attributs fournis sont :

```text
label = PLLM — Mode 1 — DeepSeek V4 Flash — OpenCode GMail
service = pllm
policy = mode1
provider = opencodego
account = anthony.demard44@gmail.com
```

Ces informations sont des métadonnées de recherche, pas la clé. Ne pas recréer le secret ni demander sa valeur dans le chat. Ne jamais afficher, recopier, journaliser ou enregistrer sa valeur dans le catalogue. Respecter les règles d’accès aux secrets de la session ; la déclaration de son emplacement n’autorise pas sa lecture par le modèle. Tout futur mécanisme d’authentification doit conserver la valeur hors du contexte du modèle et des sorties.

### Accès d’exécution requis

Chaque invocation réelle de `/pllm` doit pouvoir accéder au trousseau de
l’hôte via `secret-tool` et aux endpoints HTTPS des fournisseurs. Si une
exécution en bac à sable échoue avec `Operation not permitted`, `Could not
connect` ou une erreur équivalente lors de l’accès au trousseau ou au réseau,
relancer la même commande avec un accès d’exécution hors bac à sable (escalade
explicitement autorisée pour cette commande). Cette erreur ne doit pas être
interprétée comme une clé absente ou invalide. Limiter l’escalade au processus
d’évaluation nécessaire (`python3 scripts/evaluate.py` ou `python3
scripts/evaluate.py active`) et ne jamais afficher, copier dans un fichier ou
transmettre la valeur d’une clé.

### Compatibilité API OpenCode Go — modes 1 et 2

OpenCode Go exige l’en-tête `x-opencode-session` sur chaque requête de
complétion. Le testeur doit générer un identifiant stable par
évaluation de politique et le réutiliser pour tous les paliers et reprises de
cette évaluation. Cette règle s’applique aux modes 1 et 2, qui utilisent tous
les deux le fournisseur `opencodego`. Ne jamais publier la valeur de session.
Sans cet en-tête, l’API renvoie `HTTP 400` avec le type `MissingSessionID` avant
l’appel au modèle ; cette réponse ne doit pas être interprétée comme une panne
du modèle ou un quota épuisé.

Les routes vérifiées sont `GET /models` pour la liste des modèles et
`GET /usage` pour les quotas. Le routage de génération n’est pas uniforme :
TFL publie dans chaque modèle OpenCode Go les champs `api_endpoint`,
`api_protocol` et `endpoint_source`. PLLM doit les utiliser sans déduction
silencieuse depuis le nom du modèle.

Les modèles Muse Spark 1.3, Muse Spark 1.2, GPT 5.6 Luna et Grok 4.6 utilisent
`POST /responses`, avec `input`, `max_output_tokens` et
`reasoning.effort=low`. Les modèles déclarés `chat_completions` utilisent
`POST /chat/completions` avec `messages` et `max_tokens`. Les modèles déclarés
`messages` utilisent `POST /messages`; ce protocole est documenté par TFL mais
est benchmarké par PLLM avec le parseur SSE Anthropic dédié.

Pour Muse, ne jamais envoyer une requête vers `/chat/completions` : le contrôle
réalisé renvoie HTTP 500, alors que `/responses` fonctionne. Une route absente
ou inconnue invalide le test avec une cause explicite. Le modèle est résolu
avant le contrôle de quota depuis le premier élément de
`~/.codex/skills/tfl/data/tfl.json`, section `opencode_go.models`.
Les détails du contrat, les champs récupérables et les routes de lecture
observées en 404 sont documentés dans
[references/opencode-go-api.md](references/opencode-go-api.md). Cette référence
reste indicative : les réponses en temps réel de l’API font autorité.

Pour Muse, le corps correct est celui de Responses : `input` structuré, `max_output_tokens`, `stream=true`, `store=false` et `reasoning.effort=low`, avec le User-Agent `PLLM-coding-agent/1.0` et un identifiant stable `x-opencode-session`.

Un `HTTP 429` portant `rate_limit_exceeded` est une limitation de service OpenCode Go avant génération. Ce résultat ne prouve ni une panne ni une mauvaise qualité de Muse ; il interdit toutefois de déclarer la politique valide, car TTFT et débit n’ont pas été mesurés. Pour les Modes 1 et 2, PLLM ne bascule pas immédiatement vers une politique de priorité inférieure : elle parcourt le catalogue TFL OpenCode Go par coût croissant et teste le premier modèle disponible dont le protocole est benchmarké (`responses` ou `chat_completions`). Les modèles `messages` sont benchmarkés avec le schéma Anthropic : en-tête `x-api-key`, corps `messages` et `max_tokens`, flux SSE `content_block_delta`/`message_delta`. Ce repli utilise l’identifiant, le point d’accès et le protocole publiés par TFL.

## Sous-commandes de forçage

Les commandes `PLLM Mode 1`, `PLLM Mode 2`, `PLLM Mode 3` et `PLLM Mode 4`
forcent l’évaluation de la politique correspondante avec son modèle par défaut.

Les suffixes `1`, `2` et `3` forcent le rang correspondant du tableau TFL :
`Mode 11`, `12`, `13` ciblent les rangs 1 à 3 OpenCode Go pour le Mode 1 ;
`Mode 21`, `22`, `23` ciblent les rangs 1 à 3 OpenCode Go pour le Mode 2 ;
`Mode 31`, `32`, `33` ciblent les rangs 1 à 3 OpenRouter pour le Mode 3.
`Mode 4` conserve DeepSeek V4 Flash. Une commande forcée n’évalue que la
politique demandée et ne déclenche pas le repli automatique vers un autre
moteur ; les contrôles de quotas et les paliers de performance restent
obligatoires. Les moteurs et leur protocole sont résolus dans le catalogue TFL
au moment de l’exécution.

## Modes 2, 3 et 4

Ces modes reprennent les politiques validées dans les conversations du 2 septembre 2026 ; le raisonnement est désormais `Low` pour tous. Les seuils de performance de PLLM sont communs : TTFT < 60 s et tokens/s > 15, après validation des quotas.

### Mode 2 — priorité 2

- Modèle : premier modèle du catalogue TFL OpenCode Go ; utiliser son identifiant exact et le coût minimal retenu par TFL.
- Raisonnement : `Low`.
- Fournisseur : OpenCode Go (`opencodego`).
- Attributs exacts du trousseau : `service=pllm`, `policy=mode2`, `provider=opencodego`, `account=az.github@pixs.fr`.
- Quotas : même endpoint et même contrôle des trois périodes que le Mode 1, avec la clé propre au Mode 2.
- Condition : TTFT < 60 s ET tokens/s > 15 ET utilisations 5 h, semaine et mois toutes < 100 %.

### Mode 3 — priorité 3

- Modèle : premier modèle de la section OpenRouter du catalogue TFL, résolu à chaque évaluation depuis `~/.codex/skills/tfl/data/tfl.json`, section `openrouter.models` ; conserver son identifiant exact et la date du catalogue dans le résultat.
- Raisonnement : `Low`.
- Fournisseur : OpenRouter (`openrouter`).
- Attributs exacts du trousseau : `service=pllm`, `policy=mode3`, `provider=openrouter`, `account=az.openrouter@pixs.fr`. Le libellé historique mentionnant Mode 2 était une coquille ; les attributs font autorité.
- Contrôle du solde : `GET https://openrouter.ai/api/v1/credits`, solde = `data.total_credits - data.total_usage`. Vérifier le contrat officiel lors de l’exécution. Respecter la devise de l’API : ne pas étiqueter arbitrairement les crédits en euros comme dans les anciens comptes rendus. Le critère est un solde strictement positif.
- Condition : solde > 0 ET TTFT < 60 s ET tokens/s > 15. Un accès au solde refusé rend le mode `Invalide` et interdit le test de performance.
- Si le catalogue est absent, invalide ou doit être actualisé, appliquer le skill TFL en exécutant obligatoirement le générateur hors sandbox pour permettre l’accès réseau. Ne pas substituer le deuxième modèle si le premier échoue : ce mode exige le premier modèle OpenRouter du catalogue TFL.

### Mode 4 — priorité 4

- Modèle : DeepSeek V4 Flash ; identifiant direct à vérifier auprès du fournisseur : `deepseek-v4-flash`. Ne pas utiliser le préfixe OpenRouter `deepseek/` pour l’API directe.
- Raisonnement : `Low`.
- Fournisseur : DeepSeek (`deepseek`).
- Attributs exacts du trousseau : `service=pllm`, `policy=mode4`, `provider=deepseek`, `account=az.deepseek@pixs.fr`.
- Contrôle : `GET https://api.deepseek.com/user/balance` ; vérifier `is_available` et les `total_balance` de `balance_infos`.
- Condition : `is_available=true` ET au moins un solde utilisable strictement positif ET TTFT < 60 s ET tokens/s > 15. Conserver séparément les devises, sans les additionner ni inventer une conversion en euros.
- Les crédits achetés et la consommation cumulée restent indisponibles si l’API ne les fournit pas ; ils ne remplacent pas le contrôle du solde.

Pour tous les modes, vérifier la prise en charge effective de `Low` et sa représentation API. Ne jamais remplacer silencieusement ce réglage par un niveau différent. Si le niveau demandé est incompatible, déclarer `Invalide` avec la cause. Ne pas reprendre les anciens soldes, quotas ou statuts comme résultats actuels.

## Évaluation et restitution

L’évaluation du modèle, de sa TTFT et de son débit en tokens/s repose sur un test réel effectué avec la clé API du modèle auprès du fournisseur du mode. Ne pas utiliser de valeurs commerciales ou de mesures d’un autre fournisseur comme résultats du test. La clé doit être injectée dans le processus de test depuis la base de secrets de l’hôte sans être transmise au modèle ni affichée. Si cet accès sécurisé n’est pas disponible, signaler que le test ne peut pas être exécuté.

Pour les modes OpenCode Go, conserver un user-agent propre au testeur,
ajouter `x-opencode-session` et sélectionner le corps de requête selon
`api_protocol`. Pour `responses`, mesurer le TTFT sur
`response.output_text.delta` et lire le comptage dans
`response.completed.response.usage.output_tokens`. Conserver dans
`performance_test` le protocole et le point d’accès, sans publier la valeur de
session.

Ajouter `x-opencode-session` à chaque requête de complétion. En cas de
`MissingSessionID`, classer le test comme erreur de compatibilité du client,
corriger l’en-tête ou le transmettre avant de conclure sur la validité du
modèle. Conserver dans `performance_test` le nom de l’en-tête et le motif d’un
échec, sans conserver sa valeur.

Le test de génération ne suffit pas à établir les utilisations sur 5 heures, une semaine et un mois : obtenir ces valeurs auprès d’une source de quotas du fournisseur avant de conclure à la validité du mode. Pour les Modes 1 et 2, le test utilise le premier modèle OpenCode Go du catalogue TFL fraîchement actualisé.

Chaque invocation de `/pllm` déclenche une nouvelle évaluation réelle des modèles définis, authentifiée auprès de leur fournisseur. Ne pas se limiter à afficher la politique, proposer un test ultérieur ou réutiliser des résultats précédents comme mesures actuelles. L’invocation autorise les requêtes de test nécessaires ; ne pas redemander une confirmation de principe pour lancer le test.

Ordre obligatoire pour chaque modèle à chaque invocation :

1. Vérifier les accès nécessaires et consulter en temps réel tous les quotas applicables au mode, qu’il s’agisse de quotas temporels ou de solde/crédit. Appliquer les conditions définies pour ce mode, sans inventer de seuil de solde.
2. Si le contrôle des quotas rend le modèle `Invalide`, arrêter son évaluation avant toute requête de performance. Cela inclut un quota épuisé, un solde ne satisfaisant pas la condition du mode, ou un accès/une donnée de quota indispensable indisponible. Conserver l’état `Invalide` et indiquer la cause précise.
3. Seulement si tous les contrôles de quotas sont satisfaits, exécuter le test de performance en streaming, mesurer TTFT et tokens/s, puis appliquer les seuils du mode pour déterminer l’état final.

Ne jamais exécuter le contrôle des quotas et le test de performance en parallèle pour un même modèle. Si le test de performance est omis à cause des quotas, afficher `Non exécuté — contrôle des quotas Invalide` pour TTFT et tokens/s, sans reprendre des mesures antérieures.

Pour le Mode 1, consulter `GET https://opencode.ai/zen/go/v1/usage` avec l’authentification Bearer injectée en mémoire. Les champs `usage.rolling.percent`, `usage.weekly.percent` et `usage.monthly.percent` donnent les utilisations ; `status` et `resetsAt` donnent le statut et la réinitialisation de chaque période. Cet endpoint a été vérifié dans le code officiel et utilisé avec succès. Toute utilisation à 100 % ou plus invalide le Mode 1 avant le test de performance.

Présenter les résultats horodatés dans le tableau multi-colonnes unique. Si un prérequis empêche l’exécution (accès sécurisé au secret, endpoint vérifié, prise en charge du modèle ou de son raisonnement), attribuer `Invalide`, signaler précisément le blocage et distinguer un test non exécuté d’un test exécuté en échec. Ne jamais inventer de mesure, de quota ou d’état validé. Pour chaque évaluation réelle, indiquer la date, les mesures et les critères en échec.

Lorsqu’une mesure TTFT ou tokens/s n’a pas été exécutée ou n’est pas disponible, afficher uniquement `-` dans la cellule correspondante. Ne jamais afficher une phrase de diagnostic dans ces deux cellules ; la cause reste conservée dans le JSON.

Si un accès nécessaire manque (secret, authentification, API de test ou source de quotas), attribuer au modèle l’état `Invalide` et indiquer précisément la cause du manque. Si une mesure ou un quota nécessaire reste indisponible, attribuer également `Invalide` en précisant la donnée manquante. Distinguer cette impossibilité d’évaluation d’un seuil mesuré non satisfait ; ne jamais inventer une mesure pour justifier l’état.

TTFT (Time To First Token) désigne le temps écoulé entre l’envoi de la requête et la réception du premier token de réponse. Mesurer côté client avec une horloge monotone et une réponse en streaming ; un événement vide ou contenant uniquement des métadonnées ne constitue pas un premier token. Cette mesure inclut la latence réseau et l’attente du fournisseur. Distinguer un éventuel flux de raisonnement du contenu de réponse et expliciter lequel est mesuré. En l’absence de protocole explicitement fourni, choisir un test de génération de code court et borné, indiquer le prompt, le budget de sortie et le nombre de requêtes utilisés, et garder ce protocole identique entre les modèles comparés. Ne pas bloquer une invocation uniquement pour demander ces paramètres. Mesurer le débit avec un comptage de tokens fiable, jamais avec le nombre de fragments de streaming ; signaler si le fournisseur ne permet pas de le déterminer. Les points d’accès, identifiants API et sources de quotas doivent être vérifiés avant toute exécution ; ne pas les déduire du nom commercial.

Les Modes 1 à 4 sont définis, dans cet ordre de priorité. Ne pas inventer d’autres modes ni leurs priorités. La sélection suit l’ordre de priorité explicite décrit ci-dessous. Ne pas modifier la configuration des agents lors d’une simple présentation ou évaluation de PLLM.


## Publication de la politique en vigueur

Après chaque invocation, publier systématiquement les résultats, y compris si tous les modèles sont `Invalide`, dans le dossier `data/` de ce skill :

- `pllm-current.json` : catalogue de référence lisible par les futures commandes et agents.
- `pllm-current.md` : tableau Markdown multi-colonnes correspondant, à restituer à l’utilisateur.

Les deux fichiers décrivent la même évaluation. Le JSON contient `schema_version`, `published_at`, `evaluated_at`, `selection_status`, `selected_mode` et `models`. Chaque entrée contient `priority`, `selected`, `mode`, `model`, `reasoning`, `provider`, `ttft_seconds`, `tokens_per_second`, `condition`, `state`, `cause`, `quotas`, `performance_test` et `evaluated_at`. Utiliser `null` pour une mesure indisponible, jamais zéro. Horodater en ISO 8601 avec fuseau. Conserver le protocole et le motif d’un test omis ou échoué dans `performance_test`.

Le rapport utilisateur contient un seul tableau Markdown multi-colonnes, avec une ligne par politique et les colonnes Politique, Identifiant API, Fournisseur, TTFT (s), Tokens/s, État, Dernier palier réussi et Évalué le. Les quotas et soldes sont affichés sous le tableau, sur une ligne par PLLM. Sous ces quatre lignes, afficher en grand et en gras la PLLM active, son fournisseur et son modèle. Les lignes ou colonnes Modèle, Raisonnement, Priorité, Mode, Cause, Sélectionné, Quotas / solde et Condition ne sont pas affichées. Ces champs restent disponibles dans le JSON pour la sélection et la traçabilité. Ne jamais y inclure de clé, d’en-tête d’authentification ou de compte personnel.

Écrire chaque fichier via un fichier temporaire dans le même dossier puis remplacement atomique. Le JSON fait autorité ; le Markdown est sa représentation. Signaler toute erreur de publication et ne pas annoncer une actualisation réussie si l’écriture a échoué.

### Contrat pour les futures commandes

Lire `~/.codex/skills/pllm/data/pllm-current.json` en priorité. Vérifier sa version et son horodatage : il décrit la politique évaluée à cette date, pas une garantie de disponibilité permanente. Une demande d’actualisation exige une nouvelle invocation de `/pllm`, avec contrôle des quotas avant toute performance. Une simple lecture du catalogue ne lance pas de test.

Classer `models` et les lignes du tableau par `priority` croissante : 1 est la priorité la plus haute. Les priorités doivent être explicites et uniques ; ne pas les déduire du coût ou des performances. Les Modes 1, 2, 3 et 4 ont respectivement les priorités 1, 2, 3 et 4. Toute future entrée doit recevoir une priorité définie par l’utilisateur.

Sélectionner le premier modèle dont `state` vaut `Valide` dans cet ordre. Lui attribuer `selected: true` ; toutes les autres entrées ont `selected: false`. `selected_mode` contient son mode et `selection_status` vaut `selected`. Garder visibles les autres modèles, y compris ceux de priorité supérieure qui sont `Invalide`, avec leurs causes dans le JSON.

Si aucun modèle n’est `Valide`, `selected_mode` vaut `null`, `selection_status` vaut `no_valid_model` et aucune entrée n’est sélectionnée. Ne jamais sélectionner une entrée `Invalide`. Le rapport multi-colonnes affiche `Aucune politique valide`.

Les futures commandes utilisent cette sélection comme premier choix. Si les priorités sont absentes, ambiguës ou si le catalogue est illisible, signaler une politique indisponible plutôt qu’inventer une sélection.

La sélection publiée indique le modèle éligible pour les commandes consommatrices ; elle ne prouve pas que la configuration d’un agent a été modifiée. Toute commande appliquant cette sélection doit respecter le modèle, le raisonnement et le fournisseur de l’entrée sélectionnée.

### Application à une session OpenCode

Cette procédure s’applique uniquement lorsqu’une session de codage OpenCode est
explicitement autorisée à adopter la PLLM publiée. Une simple invocation ou
présentation de `/pllm` ne modifie jamais OpenCode.

Lorsqu’un changement de fournisseur est requis, ou lorsque la politique
sélectionnée utilise une autre clé pour le fournisseur déjà sélectionné,
l’agent doit appliquer cette séquence avant de changer les agents `plan` et
`build` :

1. Résoudre le secret du mode sélectionné depuis le trousseau avec ses
   attributs PLLM, puis l’envoyer directement à `PUT /auth/<provider-id>` de
   l’API locale OpenCode, avec le schéma d’authentification API. La valeur ne
   doit jamais être affichée, journalisée, écrite dans un fichier, passée dans
   un argument de commande ni transmise au modèle.
2. Appeler immédiatement `POST /instance/dispose`. Cette disposition recrée
   l’instance OpenCode et invalide l’état de fournisseur mémorisé ; elle est
   obligatoire après la mise à jour d’authentification et ne requiert pas un
   redémarrage du conteneur.
3. Attendre que `GET /global/health` confirme le retour de l’instance, puis
   vérifier que le fournisseur et le modèle sélectionnés sont publiés par
   `GET /provider`.
4. Créer une session temporaire sans outils ni accès aux fichiers et exécuter
   une requête bornée avec le fournisseur, le modèle et le raisonnement `Low`
   sélectionnés. Supprimer cette session après le contrôle.
5. Seulement si une réponse du modèle est observée, mettre à jour `plan` et
   `build`, puis relire `GET /agent` afin de confirmer le fournisseur, le
   modèle et le niveau de raisonnement effectifs.

Si l’injection, la disposition, le contrôle de santé ou le test échoue,
conserver la configuration des agents inchangée et signaler la cause. La
disposition interrompt les échanges en cours : elle doit donc être exécutée
uniquement dans le cadre de la bascule explicitement autorisée.


## Protocole de performance reproductible — version 4

À chaque invocation, exécuter `python3 scripts/evaluate.py`, chemin relatif au dossier de ce skill. Le script contrôle les quotas avant chaque test, mesure les réponses en streaming et publie le JSON et le Markdown. Il ne remplace pas le modèle du Mode 3.

Le test utilise le même prompt de tri fusion Python et de trois assertions pour tous les modes. Les paliers autorisés sont exactement **1 024 → 2 048 → 4 096 → 8 192 tokens**, raisonnement et réponse compris. Sans réussite mémorisée pour cette configuration, commencer à 1 024. Après tout échec du test de performance, passer au palier suivant, uniquement après un nouveau contrôle des quotas. Si les quotas sont invalides, arrêter sans lancer ce test. Arrêter au premier succès, ou après l’échec à 8 192. Aucun palier à 8 912 ni tentative supplémentaire. Chaque requête est limitée à 120 secondes ; le TTFT requis reste strictement inférieur à 60 secondes.

Mémoriser par politique dans `data/pllm-performance-memory.json` le dernier palier ayant satisfait **tous** les critères de performance après contrôle des quotas, avec date et identité modèle/fournisseur/raisonnement/type de débit. Lors de l’invocation suivante, commencer à ce palier puis augmenter en cas d’échec. Ne pas remplacer la dernière réussite par un échec. Si le modèle ou sa configuration change (notamment le premier modèle OpenRouter du catalogue TFL), repartir à 1 024 ; ne pas réutiliser un palier appris pour une autre configuration. Cette mémoire ne remplace jamais les nouveaux contrôles en temps réel. Afficher `last_successful_max_tokens` dans le catalogue et le tableau. Enregistrer atomiquement chaque réussite dès qu’elle est obtenue.

La nouvelle mémoire est initialement vide : aucun ancien résultat n’est transformé artificiellement en apprentissage du nouveau protocole.

Pour OpenRouter, consulter les métadonnées du modèle : utiliser `reasoning.effort=low` si ce niveau est exposé. Ne pas imposer `provider.require_parameters=true` : laisser OpenRouter choisir un fournisseur admissible et disponible, afin qu’un rate limit amont ne soit pas confondu avec une incapacité du modèle. Si seul `supports_max_tokens=true` est exposé, traduire Low par `reasoning.max_tokens=floor(max_tokens/5)` (204 pour 1 024 ; 409 pour 2 048 ; 819 pour 4 096 ; 1 638 pour 8 192), selon la correspondance d’environ 20 % documentée par OpenRouter. Ne pas envoyer simultanément effort et budget. Publier les paramètres réellement envoyés. Source : https://openrouter.ai/docs/guides/best-practices/reasoning-tokens . Cette traduction est un budget demandé, pas la preuve d’un nombre exact de tokens de réflexion produit.

La TTFT porte sur le premier contenu visible de réponse ; le premier événement de raisonnement est chronométré séparément. Conserver le comptage de sortie et de raisonnement fourni par l’API même en cas de troncature. Pour OpenCode Go (Modes 1 et 2), utiliser le débit global : `(completion_tokens - 1) / (instant_dernier_token_généré - instant_premier_token_généré)`, raisonnement et réponse compris. Les instants doivent correspondre à du texte généré, pas à des événements vides ou à des métadonnées. Le compteur séparé de raisonnement n’est pas requis. Conserver `throughput_scope=reasoning_and_response` et afficher « global » à côté du débit. Pour OpenRouter et DeepSeek direct, conserver le débit de réponse seul, hors raisonnement, avec `throughput_scope=response_only` et l’étiquette « réponse ». Les seuils restent > 15 tokens/s pour le type de débit ainsi défini ; ne pas comparer directement les deux types de débit comme une mesure identique. La sélection suit la priorité, pas le débit le plus élevé. Une absence de comptage fiable rend le résultat non mesurable ; ne pas remplacer des tokens par des fragments de flux.

Après le dernier palier, une réponse encore tronquée reste `Invalide` faute de mesure concluante, avec la cause `Budget du test épuisé`, sans présenter cela comme une panne du modèle. Distinguer cette cause des erreurs HTTP et des seuils de performance réellement non satisfaits.


## Code couleur

Présenter quatre couleurs selon la disponibilité restante : 🟢 vert à partir de 75 %, 🟡 jaune de 50 % inclus à 75 % exclu, 🟠 orange de 25 % inclus à 50 % exclu, 🔴 rouge sous 25 %. Pour les quotas temporels, calculer `restant = 100 - utilisé` et afficher les deux valeurs. Borner la disponibilité à 0–100 % pour la couleur.

Pour les soldes, la référence interne est 20 EUR : 🟢 à partir de 15 EUR (y compris 20 EUR et plus), 🟡 de 10 EUR inclus à 15 EUR exclu, 🟠 de 5 EUR inclus à 10 EUR exclu, 🔴 sous 5 EUR. Un solde nul est rouge. L’affichage utilisateur ne montre que le montant restant en `$` ; il ne montre ni la devise native ni la référence `/ 20 EUR`. Pour les devises autres que USD, appliquer un taux de conversion EUR vérifié et horodaté avant de déterminer la couleur. Ne jamais appliquer un seuil EUR à un montant USD sans conversion. Si la conversion est indisponible, afficher le montant avec ⚪ et signaler que la couleur EUR ne peut pas être calculée.

Pour la TTFT, appliquer : 🟢 < 30 s, 🟡 de 30 s inclus à 45 s exclu, 🟠 de 45 s inclus à 60 s exclu, 🔴 ≥ 60 s. Pour tokens/s, appliquer : 🟢 > 30, 🟡 de 20 inclus à 30 inclus, 🟠 de 15 exclu à 20 exclu, 🔴 ≤ 15. Conserver le type de débit dans le JSON, mais ne pas ajouter d’étiquette `(global)` ou `(réponse)` dans le tableau. Une mesure indisponible ou non exécutée s’affiche `-` sans symbole de remplacement.

Les couleurs sont informatives, indépendantes de la validité : un solde rouge mais positif peut satisfaire le contrôle de solde. L’état doit toujours être affiché en 🟢 `Valide` ou 🔴 `Invalide`. Enregistrer les informations d’affichage dans `quota_display` sans écraser les quotas bruts.


## Sortie utilisateur limitée à un tableau multi-colonnes

Lors d’une invocation normale de `/pllm`, restituer un seul tableau Markdown multi-colonnes avec une ligne par politique dans l’ordre de priorité 1 à 4. Le Markdown est obligatoire car l’interface échappe le HTML brut. Les colonnes sont `Politique`, `Identifiant API`, `Fournisseur`, `TTFT (s)`, `Tokens/s`, `État`, `Dernier palier réussi` et `Évalué le`. Afficher ensuite quatre lignes de quotas / soldes, une pour chaque PLLM.

Les lignes ou colonnes `Modèle`, `Raisonnement`, `Priorité`, `Mode`, `Cause`, `Sélectionné`, `Quotas / solde` et `Condition` sont supprimées de l’affichage. La condition reste disponible dans le JSON et peut être fournie sur demande. Les cellules TTFT et tokens/s valent `-` si le test n’a pas été exécuté ou si la mesure est indisponible. Afficher TTFT et tokens/s avec une seule décimale. Afficher l’horodatage sous la forme `DD-MM-YY HH:mm`. L’état est toujours coloré par 🟢 `Valide` ou 🔴 `Invalide`.

Pour `/pllm active`, ne publier que la ligne de la première politique valide dans le même tableau multi-colonnes, sa ligne de quotas / solde et l’encart actif ; si aucune politique n’est valide, publier `Aucune politique valide`. Le JSON conserve `selected_mode`, `selection_status`, `selected` et `condition` pour les commandes consommatrices et les demandes détaillées.


## Argument `active` — sélection silencieuse

`/pllm active` exécute `python3 scripts/evaluate.py active`. Évaluer les politiques par priorité croissante avec les contrôles et paliers mémorisés habituels. Arrêter immédiatement dès la première politique `Valide` : ne consulter ni quotas ni performances des politiques suivantes.

Actualiser `pllm-current.json` et `pllm-current.md` sans sortie console ni tableau dans la conversation. En mode active, le Markdown contient uniquement la ligne de la politique sélectionnée, sa ligne de quotas / solde et l’encart actif pour les autres commandes. Si aucune politique ne satisfait les conditions, publier « Aucune politique valide » et `selected_mode=null` ; ne pas conserver une ancienne sélection.

Le JSON conserve les lignes historiques des politiques non visitées, avec leur ancien horodatage et `evaluated_this_run=false`. Elles ne représentent pas des contrôles actuels et ne doivent jamais être sélectionnées sur cette base. Les politiques visitées ont `evaluated_this_run=true`. `evaluation_mode` distingue `active` et `all`. L’invocation sans argument continue à contrôler tous les modes et afficher le tableau unique, ses quatre lignes de quotas / soldes et l’encart de la PLLM active.

L’exécution planifiée demandée est quotidienne à 00:00, 06:00, 12:00 et 18:00, heure de Paris. Elle doit utiliser le skill actif, sans figer un ancien nom d’utilisateur Unix, et rester silencieuse en fonctionnement normal.
