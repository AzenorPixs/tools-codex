---
name: pllm
description: Évaluer en temps réel les modèles à chaque invocation de /pllm et déterminer la politique convergente de priorité des modèles LLM pour les agents de codage. Utiliser pour /pllm, PLLM ou une demande explicite de gestion de ses modes et conditions de validité.
---

# PLLM — Politique de priorité des modèles LLM

Présenter les entrées dans un tableau unique multi-colonnes avec cet ordre : Politique, Identifiant API, Fournisseur, TTFT, Tokens/s, État, Dernier palier réussi, Évalué le. Afficher ensuite les quotas et soldes sur une ligne dédiée par PLLM. L’état est `Valide` ou `Invalide` et dépend de la condition du mode.

## Six politiques et catégories

Évaluer par priorité 1 à 6 : Go payant compte 1, Go payant compte 2,
gratuits Go et OpenCode général compte 1, mêmes gratuits compte 2,
OpenRouter, puis DeepSeek direct. Les modes 1/2 ne contiennent aucun gratuit :
un quota épuisé les rend `🔴 Invalide — Quota épuisé`, sans génération.
Les modes 3/4 n'appellent jamais de quota ni de solde, y compris entre paliers.
Ils restent gratuits indépendamment des ressources des comptes associés.

Les gratuits 3/4 exigent TTFT <30 s et débit >20 tokens/s. Les payants
1/2/5/6 gardent TTFT <90 s et débit >15 tokens/s. Tous exigent réponse complète,
comptage fiable, HIGH/XHIGH autorisé et filtres TFL. Le contexte d'entrée ≥1M
est vérifié pour les candidats du catalogue ; le benchmark n'envoie pas un
million de tokens. Les paliers et le protocole de mesure actuels sont conservés.

Hors forçage, essayer les payants 1/2/5 par coût moyen TFL croissant, avec ordre
stable TFL à prix égal. Utiliser la moyenne des prix d'entrée/sortie de
référence : hors pointe Go, prix de base OpenRouter. Conserver le coût vérifié
dans average_price_usd_per_million_tokens et prix/provenances dans model_source.
Essayer les gratuits 3/4 dans l'ordre TFL Go puis OpenCode général, sans tri
par performances historiques. Dans chaque mode, retenir le premier candidat
qui réussit les tests actuels et ne pas tester les suivants. Après un échec,
essayer le suivant sous réserve des contrôles bloquants. Le mode6 conserve
son candidat direct unique sans prix inventé.

Le mode5 est exclusivement payant. Un crédit épuisé le rend invalide sans
repli gratuit ; une nouvelle invocation relit le crédit. Une panne ou un
refus d'authentification ne prouve jamais un épuisement. Les modes 3/4 restent
gratuits : prix d'entrée et de sortie vérifiés nuls avec variantes compatibles,
jamais un nom free seul. Conserver modalités, blacklist et transport.

Go et général utilisent le débit raisonnement+réponse ; OpenRouter et DeepSeek
le débit réponse seule. Les priorités 1 à 6 priment sur les performances entre
modes. L'invocation normale passe à la politique suivante après sélection ;
active s'arrête à la première politique valide. Le JSON conserve catégories,
critères, candidats visités, exclusions, tentatives, routes et dates sans
mesures inventées pour les candidats non visités. Garder les huit colonnes.

État rend `🟢 Valide — gratuit` en 3/4 et les diagnostics sûrs d'authentification
ou d'accès refusés. Un refus d'authentification pendant un contrôle exécuté
invalide le mode courant. Ne publier ni corps d'erreur brut, compte, clé ou
identifiant de session et ne pas usurper une identité de client natif.

## Mode 1

- Priorité : 1 (priorité la plus haute actuellement définie).
- Modèle : premier candidat payant TFL OpenCode Go conforme, essayé par coût croissant.
- Raisonnement : HIGH.
- Fournisseur : OpenCode Go (`opencodego`).
- TTFT : évalué par le test, en secondes.
- Tokens/s : évalué par le test.
- Condition : `TTFT < 90 s ET Tokens/s > 15 ET quotas disponibles`.
- État : `Valide` si tous les critères sont satisfaits ; `Invalide` si au moins un critère échoue.

Les seuils de performance sont stricts. Une utilisation à 100 % rend ce mode invalide et rouge, sans repli gratuit.

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

### Compatibilité API OpenCode — modes 1 à 4

OpenCode Go exige l’en-tête `x-opencode-session` sur chaque requête de
complétion. Le testeur doit générer un identifiant stable par
évaluation de politique et le réutiliser pour tous les paliers et reprises de
cette évaluation. Cette règle s’applique aux modes 1 à 4, avec leurs fournisseurs effectifs
`opencodego` ou `opencode`. Ne jamais publier la valeur de session.
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
`reasoning.effort=high`. Les modèles déclarés `chat_completions` utilisent
`POST /chat/completions` avec `messages` et `max_tokens`. Les modèles déclarés
`messages` utilisent `POST /messages`; ce protocole est documenté par TFL mais
est benchmarké par PLLM avec le parseur SSE Anthropic dédié.
Pour `chat_completions` OpenCode Go et général, HIGH est envoyé uniquement via
`reasoning_effort=high`, sans `thinking`. Ce paramètre reste réservé aux
contrats qui le requièrent : thinking adaptatif et output_config.effort de Messages et activation
thinking pour DeepSeek direct. Responses et OpenRouter gardent leurs propres
représentations HIGH ; ne pas déduire le corps du nom du modèle.

Pour Muse, ne jamais envoyer une requête vers `/chat/completions` : le contrôle
réalisé renvoie HTTP 500, alors que `/responses` fonctionne. Une route absente
ou inconnue invalide le test avec une cause explicite. Les candidats sont résolus depuis
`../tfl/data/tfl.json` relatif au dossier de ce skill, sections
`opencode_go.models` et, pour les gratuits 3/4, `opencode.models`, sauf chemin
fourni par `--tfl-catalog CHEMIN`. Le mode détermine une catégorie fixe : payante en 1/2/5/6, gratuite en 3/4.
Les détails du contrat, les champs récupérables et les routes de lecture
observées en 404 sont documentés dans
[references/opencode-go-api.md](references/opencode-go-api.md). Cette référence
reste indicative : les réponses en temps réel de l’API font autorité.

Pour Muse, le corps correct est celui de Responses : `input` structuré, `max_output_tokens`, `stream=true`, `store=false` et `reasoning.effort=high`, avec le User-Agent `PLLM-coding-agent/1.0` et un identifiant stable `x-opencode-session`.

Hors l'unique repli d'effort XHIGH autorisé, un HTTP 400 ou 429 arrête les paliers du candidat dans cette invocation.
Continuer les autres candidats de la catégorie autorisée après leurs contrôles.
Un HTTP 429 ne déplace jamais un candidat payant 1/2 vers les gratuits 3/4.
Conserver son Retry-After exploitable et afficher le réessai indiqué, sans
attendre une échéance longue, rejouer les budgets ni planifier une reprise.
Une échéance n'est pas une garantie de succès. Un HTTP 400 affiche le paramètre
connu refusé lorsqu'il est identifiable ; ne pas assimiler ce refus à un échec
de débit ou de budget de sortie.
Chaque candidat utilise le protocole et l'endpoint TFL. Les modèles `messages`
sont benchmarkés avec `x-api-key` et le parseur SSE Anthropic dédié.
Les deux catalogues OpenCode conservent `x-opencode-session`, une session stable
par évaluation de politique et le User-Agent propre à PLLM. Le compte du mode
reste la source d'authentification, même pour un gagnant `opencode`.
Le contrôle Go est réservé aux modes 1/2 ; aucun appel usage en 3/4.
La même clé du compte est utilisée seulement sur l'origine HTTPS OpenCode
validée. Un refus de cette clé ne crée ni nouveau secret ni configuration privée.


## Sous-commandes de forçage

`PLLM Mode 1` à `PLLM Mode 6` forcent le premier candidat admissible du mode,
sans remplacement automatique ni évaluation d'une autre politique.

- `11`, `12`, `13` et `21`, `22`, `23` gardent les rangs bruts TFL Go.
  Un rang gratuit est incompatible avec ces modes payants et échoue.
- `31`, `32`, `33` et `41`, `42`, `43` ciblent les rangs de la liste gratuite
  admissible Go puis OpenCode général des modes 3 et 4 respectivement.
- Les anciens rangs OpenRouter `31`, `32`, `33` deviennent `51`, `52`, `53`,
  avec les rangs bruts TFL OpenRouter, exclusivement payants.
- `6` conserve DeepSeek V4 Flash direct.

Un rang absent ou incompatible échoue sans substitution. Les contrôles de
ressources restent obligatoires en 1/2/5/6 et absents en 3/4 ; les tests de
performance restent obligatoires partout.

## Modes 2 à 6

### Mode 2 — priorité 2

- Premier payant TFL Go conforme dans l'ordre de coût croissant, HIGH, fournisseur `opencodego`.
- Référence existante : `service=pllm`, `policy=mode2`, `provider=opencodego`,
  `account=az.github@pixs.fr`.
- Contrôler les trois périodes Go avec ce compte avant chaque requête.
- Validité : quotas disponibles, réponse complète, TTFT <90 s et débit >15.
  Épuisement : rouge et invalide, sans candidat gratuit.

### Mode 3 — priorité 3 — gratuits du compte 1

- Tous les gratuits vérifiés TFL `opencode_go` puis `opencode`, HIGH.
- Utiliser exactement la référence de secret du mode 1, sans nouveau secret.
- Aucun appel de quota ou de solde. Quotas JSON `null`,
  `quota_status=not_applicable` et affichage `Non applicable`.
- Validité : gratuité vérifiée, contexte ≥1M, réponse complète, comptage fiable,
  TTFT <30 s ET débit >20 tokens/s, raisonnement+réponse.
- Les limitations et restrictions d'accès restent celles du fournisseur.

### Mode 4 — priorité 4 — gratuits du compte 2

- Même sélection gratuite et mêmes seuils stricts que mode3.
- Utiliser exactement la référence de secret du mode 2 ; aucun nouveau secret.
- Aucun appel de quota ou de solde, même avant un palier supplémentaire.

### Mode 5 — priorité 5 — ancien mode 3 OpenRouter

- Essayer exclusivement les payants TFL `openrouter` par coût moyen croissant,
  ordre TFL à prix égal. Retenir le premier succès aux tests actuels.
- Référence inchangée : `service=pllm`, `policy=mode3`, `provider=openrouter`,
  `account=az.openrouter@pixs.fr`. Le numéro de politique du trousseau reste historique.
- Contrôle avant chaque requête : `GET https://openrouter.ai/api/v1/credits`,
  solde = `data.total_credits - data.total_usage`. Garder la devise de l'API.
- Validité : solde >0, réponse complète, TTFT <90 s et débit réponse seule
  >15 tokens/s. Un crédit épuisé ou un contrôle refusé interdit le test,
  sans repli gratuit. Une invocation ultérieure relit le crédit.
- Utiliser les métadonnées OpenRouter actuelles pour HIGH/XHIGH autorisé.
  Si le catalogue doit être actualisé, appliquer TFL avec ses accès autorisés.

### Mode 6 — priorité 6 — ancien mode 4 DeepSeek direct

- DeepSeek V4 Flash, `deepseek-v4-flash`, HIGH, fournisseur `deepseek`.
- Référence inchangée : `service=pllm`, `policy=mode4`, `provider=deepseek`,
  `account=az.deepseek@pixs.fr` ; conserver ces attributs historiques.
- Contrôle : `GET https://api.deepseek.com/user/balance`,
  `is_available=true` ET au moins un `total_balance` utilisable >0.
- Garder les devises séparées. Validité : réponse complète, TTFT <90 s et
  débit réponse seule >15 tokens/s, en plus du solde utilisable.
- Les crédits achetés et la consommation cumulée indisponibles ne remplacent
  jamais le contrôle du solde.

Pour tous les modes, demander HIGH et vérifier sa représentation API ; XHIGH est le seul repli autorisé lorsqu'il est pris en charge. Ne jamais remplacer silencieusement ce réglage par un niveau différent. Si le niveau demandé est incompatible, déclarer `Invalide` avec la cause. Ne pas reprendre les anciens soldes, quotas ou statuts comme résultats actuels.

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

Pour 1/2, le test de génération ne suffit pas à établir les utilisations sur 5 heures, une semaine et un mois : obtenir ces valeurs de quotas avant de conclure. Ce contrôle ne s’applique jamais aux gratuits 3/4. Les modes 1/2 utilisent les payants Go ; les modes 3/4 les gratuits Go et OpenCode général du catalogue TFL actualisé.

Chaque invocation de `/pllm` déclenche une nouvelle évaluation réelle des modèles définis, authentifiée auprès de leur fournisseur. Ne pas se limiter à afficher la politique, proposer un test ultérieur ou réutiliser des résultats précédents comme mesures actuelles. L’invocation autorise les requêtes de test nécessaires ; ne pas redemander une confirmation de principe pour lancer le test.

Ordre obligatoire pour chaque modèle à chaque invocation :

1. Vérifier les accès et le catalogue. Pour 1/2/5/6, contrôler en temps réel
   les quotas ou soldes avant chaque requête. Pour 3/4, ne jamais les appeler.
2. Si un contrôle indispensable échoue, arrêter ce mode avant performance.
   Un épuisement invalide 1/2/5/6 sans test ni repli gratuit.
3. Tester les candidats de la catégorie autorisée, mesurer le flux et appliquer
   les seuils propres au mode. Les gratuits 3/4 restent admissibles sans quota.

Ne jamais exécuter le contrôle des quotas et le test de performance en parallèle pour un même modèle. Si le test est omis, afficher uniquement `-` pour TTFT et tokens/s, avec sa cause dans État et dans le JSON, sans mesure antérieure.

Pour le Mode 1, consulter `GET https://opencode.ai/zen/go/v1/usage` avec l’authentification Bearer injectée en mémoire. Les champs `usage.rolling.percent`, `usage.weekly.percent` et `usage.monthly.percent` donnent les utilisations ; `status` et `resetsAt` donnent le statut et la réinitialisation de chaque période. Cet endpoint a été vérifié dans le code officiel et utilisé avec succès. Toute utilisation à 100 % ou plus invalide 1/2 sans test ni repli gratuit. Ne jamais appeler cet endpoint en 3/4.

Présenter les résultats horodatés dans le tableau multi-colonnes unique. Si un prérequis empêche l’exécution (accès sécurisé au secret, endpoint vérifié, prise en charge du modèle ou de son raisonnement), attribuer `Invalide`, signaler précisément le blocage et distinguer un test non exécuté d’un test exécuté en échec. Ne jamais inventer de mesure, de quota ou d’état validé. Pour chaque évaluation réelle, indiquer la date, les mesures et les critères en échec.

Lorsqu’une mesure TTFT ou tokens/s n’a pas été exécutée ou n’est pas disponible, afficher uniquement `-` dans la cellule correspondante. Ne jamais afficher une phrase de diagnostic dans ces deux cellules ; la cause reste conservée dans le JSON.

Si un accès nécessaire manque (secret, authentification, API de test ou source de quotas), attribuer au modèle l’état `Invalide` et indiquer précisément la cause du manque. Si une mesure ou un quota nécessaire reste indisponible, attribuer également `Invalide` en précisant la donnée manquante. Distinguer cette impossibilité d’évaluation d’un seuil mesuré non satisfait ; ne jamais inventer une mesure pour justifier l’état.

TTFT (Time To First Token) désigne le temps écoulé entre l’envoi de la requête et la réception du premier token de réponse. Mesurer côté client avec une horloge monotone et une réponse en streaming ; un événement vide ou contenant uniquement des métadonnées ne constitue pas un premier token. Cette mesure inclut la latence réseau et l’attente du fournisseur. Distinguer un éventuel flux de raisonnement du contenu de réponse et expliciter lequel est mesuré. En l’absence de protocole explicitement fourni, choisir un test de génération de code court et borné, indiquer le prompt, le budget de sortie et le nombre de requêtes utilisés, et garder ce protocole identique entre les modèles comparés. Ne pas bloquer une invocation uniquement pour demander ces paramètres. Mesurer le débit avec un comptage de tokens fiable, jamais avec le nombre de fragments de streaming ; signaler si le fournisseur ne permet pas de le déterminer. Les points d’accès, identifiants API et sources de quotas doivent être vérifiés avant toute exécution ; ne pas les déduire du nom commercial.

Les modes 1 à 6 sont définis, dans cet ordre de priorité. Ne pas inventer d’autres modes ni leurs priorités. La sélection entre politiques suit l’ordre de priorité explicite décrit ci-dessous ; dans un même mode, retenir le premier succès dans l'ordre de coût payant ou l'ordre gratuit TFL. Ne pas modifier la configuration des agents lors d’une simple présentation ou évaluation de PLLM.


## Publication de la politique en vigueur

Après chaque invocation, publier systématiquement les résultats, y compris si tous les modèles sont `Invalide`, dans le dossier `data/` de ce skill :

- `pllm-current.json` : catalogue de référence lisible par les futures commandes et agents.
- `pllm-current.md` : tableau Markdown multi-colonnes correspondant, à restituer à l’utilisateur.

Les deux fichiers décrivent la même évaluation. Le JSON contient `schema_version`, `published_at`, `evaluated_at`, `selection_status`, `selected_mode` et `models`. Chaque entrée contient aussi `performance_criteria` et `quota_status` ; elle contient `priority`, `selected`, `mode`, `model`, `reasoning`, `provider`, `ttft_seconds`, `tokens_per_second`, `condition`, `state`, `cause`, `quotas`, `performance_test` et `evaluated_at`. Utiliser `null` pour une mesure indisponible, jamais zéro. Horodater en ISO 8601 avec fuseau. Conserver le protocole et le motif d’un test omis ou échoué dans `performance_test`.
Les tentatives HTTP conservent `http_error` : statut, code reconnu, paramètre
connu, indicateurs de limitation et Retry-After filtré (`retry_after_seconds`,
`retry_at`). Lire au plus 64 Kio d'erreur en mémoire et fermer la réponse.
Les secondes entières et les dates HTTP avec fuseau sont acceptées ; une valeur
absente, invalide ou hors plage reste indisponible. Ne conserver ni corps brut,
message libre, en-têtes privés, compte, clé ou identifiant de session.

Le rapport utilisateur contient un seul tableau Markdown multi-colonnes, avec une ligne par politique et les colonnes Politique, Identifiant API, Fournisseur, TTFT (s), Tokens/s, État, Dernier palier réussi et Évalué le. Les quotas et soldes sont affichés sous le tableau, sur une ligne par PLLM. Sous ces six lignes, afficher en grand et en gras la PLLM active, son fournisseur et son modèle. Les colonnes Modèle, Raisonnement, Priorité, Mode, Cause, Sélectionné, Quotas / solde et Condition ne sont pas ajoutées. Le diagnostic figure dans État. Ces champs restent disponibles dans le JSON pour la sélection et la traçabilité. Ne jamais y inclure de clé, d’en-tête d’authentification ou de compte personnel.

Écrire chaque fichier via un fichier temporaire dans le même dossier puis remplacement atomique. Le JSON fait autorité ; le Markdown est sa représentation. Signaler toute erreur de publication et ne pas annoncer une actualisation réussie si l’écriture a échoué.

### Contrat pour les futures commandes

Lire `data/pllm-current.json` dans le dossier du skill PLLM effectivement utilisé en priorité. Vérifier sa version et son horodatage : il décrit la politique évaluée à cette date, pas une garantie de disponibilité permanente. Une demande d’actualisation exige une nouvelle invocation de `/pllm`, avec contrôles applicables avant performance, sans quota en 3/4. Une simple lecture du catalogue ne lance pas de test.

Classer `models` et les lignes du tableau par `priority` croissante : 1 est la priorité la plus haute. Les priorités doivent être explicites et uniques ; ne pas les déduire du coût ou des performances. Les modes 1 à 6 ont respectivement les priorités 1 à 6. Toute future entrée doit recevoir une priorité définie par l’utilisateur.

Sélectionner le premier modèle dont `state` vaut `Valide` dans cet ordre. Lui attribuer `selected: true` ; toutes les autres entrées ont `selected: false`. `selected_mode` contient son mode et `selection_status` vaut `selected`. Garder visibles les autres modèles, y compris ceux de priorité supérieure qui sont `Invalide`, avec leurs causes dans le JSON.

Si aucun modèle n’est `Valide`, `selected_mode` vaut `null`, `selection_status` vaut `no_valid_model` et aucune entrée n’est sélectionnée. Ne jamais sélectionner une entrée `Invalide`. Le rapport multi-colonnes affiche `Aucune politique valide`.

Les futures commandes utilisent cette sélection comme premier choix. Si les priorités sont absentes, ambiguës ou si le catalogue est illisible, signaler une politique indisponible plutôt qu’inventer une sélection.

La sélection publiée indique le modèle éligible pour les commandes consommatrices ; elle ne prouve pas que la configuration d’un agent a été modifiée. Toute commande appliquant cette sélection doit respecter le modèle, le raisonnement et le fournisseur de l’entrée sélectionnée.

### Application à une session OpenCode

Cette procédure s’applique uniquement lorsqu’une session de codage OpenCode est
explicitement autorisée à adopter la PLLM publiée. Une simple invocation ou
présentation de `/pllm` ne modifie jamais OpenCode.

Une interdiction de fermer ou redémarrer OpenCode concerne son processus et
l’interface visible du développeur. Elle n’interdit pas le chargement d’une
clé fournisseur ni le rechargement interne du contexte. Une restriction
distincte sur le stockage des secrets doit être respectée lorsqu’elle est
explicitement imposée ; ne pas l’inventer à partir de la règle de cycle de vie.
Le modèle et le raisonnement explicitement demandés par le développeur
prévalent sur les valeurs par défaut du mode ; les contrôles réels doivent
porter sur cette configuration exacte.

Lorsqu’un changement de fournisseur est requis, ou lorsque la politique
sélectionnée utilise une autre clé pour le fournisseur déjà sélectionné,
l’agent doit appliquer cette séquence avant de changer les agents `plan` et
`build` :

1. Résoudre le secret du mode sélectionné depuis le trousseau avec ses
   attributs PLLM historiques : 1/3 utilisent policy=mode1, 2/4 policy=mode2,
   avec provider=opencodego même pour une destination opencode ; 5 conserve
   policy=mode3/provider=openrouter et 6 policy=mode4/provider=deepseek. Utiliser son identifiant
   fournisseur effectif pour la destination, puis l’envoyer directement à `PUT /auth/<provider-id>` de
   l’API locale OpenCode, avec le schéma d’authentification API. La valeur ne
   doit jamais être affichée, journalisée, passée dans
   un argument de commande ni transmise au modèle.
   L’API standard peut la stocker dans le fichier d’authentification privé
   d’OpenCode, hors dépôt, rapports, indexation et lecture des agents. Ce
   stockage local est permis sauf restriction explicite du développeur ;
   aucune copie manuelle supplémentaire n’est autorisée.
2. À la fin du mandat courant, sans permission ni opération en attente,
   appeler `POST /instance/dispose`. Cette opération réinitialise le contexte
   du projet et l’état de fournisseur mémorisé sans fermer l’interface ni
   arrêter ou redémarrer le processus OpenCode. Elle peut interrompre les
   connexions MCP ; conserver la session et réconcilier ses échanges avant
   toute reprise. Ne pas remplacer cette opération par un arrêt du processus.
3. Attendre que `GET /global/health` confirme le retour de l’instance, puis
   vérifier que le fournisseur et le modèle sélectionnés sont publiés par
   `GET /provider`.
4. Créer une session temporaire sans outils ni accès aux fichiers et exécuter
   une requête bornée avec le fournisseur, le modèle et le raisonnement
   effectivement demandés. Supprimer cette seule session après le contrôle.
5. Seulement si une réponse du modèle est observée, mettre à jour `plan` et
   `build`, puis relire `GET /agent` afin de confirmer le fournisseur, le
   modèle et le niveau de raisonnement effectifs.

Si l’injection, la disposition, le contrôle de santé ou le test échoue,
conserver la configuration des agents inchangée et signaler la cause. La
disposition interrompt les échanges en cours : elle doit donc être exécutée
uniquement dans le cadre de la bascule explicitement autorisée.
Sous CAB, recontrôler `/mcp`, appeler réellement `broker_readiness` dans la
session persistante, puis réussir le test CAB avant de reprendre les mandats.


## Catalogue explicite et première évaluation

Pour des plugins installés séparément, transmettre le catalogue produit par TFL :

```bash
python3 scripts/evaluate.py --tfl-catalog /chemin/vers/tfl.json
python3 scripts/evaluate.py active --tfl-catalog /chemin/vers/tfl.json
python3 scripts/evaluate.py 3 --tfl-catalog /chemin/vers/tfl.json
```

Le chemin explicite est utilisé pour Go, les gratuits Go/général 3/4 et OpenRouter 5.
TFL retire désormais de models les gratuits échoués à ses tests HIGH/XHIGH,
avec leurs preuves dans excluded_models. Le catalogue dépend du compte TFL
utilisé ; un échec avec ce compte peut rendre un candidat absent pour un autre
compte jusqu'à une nouvelle collecte TFL. PLLM ne réintègre pas les exclus et
reteste toujours ses candidats retenus avec la clé propre à son mode.
Sans option, le chemin voisin `../tfl/data/tfl.json` est conservé. Un catalogue
absent ou invalide produit un diagnostic ; ne pas chercher dans les
configurations privées pour le remplacer.

Si `data/pllm-current.json` manque, initialiser six politiques sans quota,
mesure ni sélection historique. Le schéma courant vaut 2 : un ancien historique
à quatre modes est validé puis adapté en mémoire (ancien 3→5, ancien 4→6,
nouveaux 3/4 initialisés), sans sélection ni évaluation actuelle héritées.
La mémoire de schéma 1 est adaptée en 2 avec les mêmes déplacements ; les
nouveaux 3/4 n'héritent d'aucun succès. Les anciens fichiers restent intacts
jusqu'à la publication normale ou à une nouvelle réussite. Un ancien évaluateur
ne lit pas le schéma 2 : conserver ses données avant un retour de version. Un fichier existant invalide bloque avant publication et reste
préservé. Les répertoires nécessaires sont créés lors de la publication ou de
la mémorisation d'une réussite.

Après un repli HTTP 429, recalculer les paliers pour la nouvelle configuration :
sans réussite mémorisée correspondante, commencer à 1 024 tokens. Effectuer les contrôles applicables avant sa requête, sans quota en 3/4. Le dernier palier et l'épuisement des candidats
ne permettent jamais de déclarer valide un modèle sans mesures concluantes.

## Protocole de performance reproductible — version 8

À chaque invocation, exécuter `python3 scripts/evaluate.py`, chemin relatif au dossier de ce skill. Le script contrôle les quotas applicables avant chaque test (jamais en 3/4), mesure les réponses en streaming et publie le JSON et le Markdown. Il parcourt les candidats jusqu'au premier succès de chaque mode ; une invocation forcée ne remplace jamais son candidat.

Le test utilise le même prompt de tri fusion Python et de trois assertions pour tous les modes. Les paliers autorisés sont exactement **1 024 → 2 048 → 4 096 → 8 192 tokens**, raisonnement et réponse compris. Sans réussite mémorisée pour cette configuration, commencer à 1 024. Après une troncature ou un seuil mesuré non satisfait, passer au palier suivant après les contrôles applicables, sans quota en 3/4. Hors l'unique repli d'effort XHIGH autorisé, HTTP 400 et 429 arrêtent ce candidat sans augmenter son budget ; les règles 401/403 restent applicables. Si un contrôle indispensable échoue, arrêter sans lancer ce test ; un épuisement interdit 1/2/5/6 sans repli gratuit. Arrêter le mode au premier succès du candidat ; après son échec à 8 192 ou un refus compatible avec la poursuite, essayer le candidat suivant autorisé. Aucun palier à 8 912 ni tentative supplémentaire. Chaque requête est limitée à 120 secondes ; le TTFT requis reste <30 s pour les gratuits et <90 s pour les payants.

Le parseur streaming et les seuils sont fournis par scripts/performance.py,
embarqué et identique dans PLLM et TFL. Les imports n'effectuent aucun appel réseau.

Mémoriser par politique dans `data/pllm-performance-memory.json` le dernier palier ayant satisfait **tous** les critères de performance après les contrôles applicables, avec date et identité modèle/fournisseur/raisonnement/type et profil de débit. Lors de l’invocation suivante, commencer à ce palier puis augmenter en cas d’échec. Ne pas remplacer la dernière réussite par un échec. Si le modèle ou sa configuration change sans réussite correspondante mémorisée, repartir à 1 024 ; ne pas réutiliser un palier appris pour une autre configuration. Cette mémoire ne remplace jamais les nouveaux contrôles en temps réel. Afficher `last_successful_max_tokens` dans le catalogue et le tableau. Enregistrer atomiquement chaque réussite dès qu’elle est obtenue.

La nouvelle mémoire est initialement vide : aucun ancien résultat n’est transformé artificiellement en apprentissage du nouveau protocole.

Pour OpenRouter, suivre les supported_efforts publiés : HIGH en priorité,
XHIGH si HIGH est absent et XHIGH annoncé. Si seul supports_max_tokens=true
est exposé, HIGH utilise floor(0,80 × max_tokens), XHIGH floor(0,95 × max_tokens)
lorsque ce contrat l'autorise. Ne jamais envoyer effort et budget ensemble.
Un HTTP 400 précisément lié à l'effort permet au plus un passage à XHIGH
annoncé ; aucun repli sur 401/403/429, seuil, troncature ou autre paramètre.
Le palier est recalculé pour la configuration XHIGH, sans mémoire Low/HIGH
empruntée. Aucun niveau inférieur n'est autorisé. Les paramètres demandés et
le niveau effectif sont tracés, sans promettre une profondeur interne mesurée.
Source : https://openrouter.ai/docs/guides/best-practices/reasoning-tokens .

La TTFT porte toujours sur le premier contenu visible ; le premier raisonnement
est chronométré séparément. Le protocole 8 mesure un débit moyen côté client
sur la requête complète, attente et TTFT inclus :

- Go et OpenCode général : completion_tokens / request_seconds, raisonnement
  et réponse compris ; throughput_scope=reasoning_and_response.
- OpenRouter et DeepSeek : (completion_tokens - reasoning_tokens) /
  request_seconds, réponse seule au numérateur ; throughput_scope=response_only.

request_seconds est la durée monotone non arrondie, avant ouverture HTTP
jusqu'à la fin du flux et la libération de la réponse. Ne jamais utiliser la
valeur arrondie duration_seconds pour le calcul, ni soustraire le premier token.
La fenêtre generation_seconds entre fragments reste un diagnostic ; elle ne
détermine plus les tokens/s. Une réponse complète reçue en un bloc est
mesurable si durée et compteurs sont fiables. Une durée nulle, négative ou
non finie, un comptage incohérent ou un flux incomplet ne produit aucun débit
inventé ou valeur historique reprise. Aucun écrêtage ni plancher arbitraire.

Tracer throughput_metric=request_average_v1, throughput_window=request_total
et measurement_protocol_version=8 sur les mesures et les configurations de
mémoire. Les anciens succès restent historiques ; sans réussite du même
profil, commencer à 1024. Ce débit n'est pas une vitesse intrinsèque fournisseur
et n'est pas directement comparable à l'ancien débit entre fragments.
Les seuils numériques restent >20 tokens/s pour les gratuits et >15 pour les
payants, mais classement et éligibilité peuvent changer. Les portées de
comptage restent distinctes ; les priorités entre modes restent inchangées.

Après le dernier palier, une réponse encore tronquée reste `Invalide` faute de mesure concluante, avec la cause `Budget du test épuisé`, sans présenter cela comme une panne du modèle. Distinguer cette cause des erreurs HTTP et des seuils de performance réellement non satisfaits.


## Code couleur

Présenter quatre couleurs selon la disponibilité restante : 🟢 vert à partir de 75 %, 🟡 jaune de 50 % inclus à 75 % exclu, 🟠 orange de 25 % inclus à 50 % exclu, 🔴 rouge sous 25 %. Pour les quotas temporels, calculer `restant = 100 - utilisé`, afficher le restant et conserver l'utilisation dans les quotas bruts du JSON. Borner la disponibilité à 0–100 % pour la couleur.

Pour les soldes, la référence interne est 20 EUR : 🟢 à partir de 15 EUR (y compris 20 EUR et plus), 🟡 de 10 EUR inclus à 15 EUR exclu, 🟠 de 5 EUR inclus à 10 EUR exclu, 🔴 sous 5 EUR. Un solde nul est rouge. L’affichage utilisateur ne montre que le montant restant en `$` ; il ne montre ni la devise native ni la référence `/ 20 EUR`. Pour les devises autres que USD, appliquer un taux de conversion EUR vérifié et horodaté avant de déterminer la couleur. Ne jamais appliquer un seuil EUR à un montant USD sans conversion. Si la conversion est indisponible, afficher le montant avec ⚪ et signaler que la couleur EUR ne peut pas être calculée.

Pour tous les gratuits, un TTFT ≥30 s ou un débit ≤20 tokens/s est rouge ; les autres couleurs restent informatives. Pour les autres modes et les valeurs gratuites admissibles, appliquer pour la TTFT : 🟢 < 30 s, 🟡 de 30 s inclus à 45 s exclu, 🟠 de 45 s inclus à 90 s exclu, 🔴 ≥ 90 s. Pour tokens/s, appliquer : 🟢 > 30, 🟡 de 20 inclus à 30 inclus, 🟠 de 15 exclu à 20 exclu, 🔴 ≤ 15. Conserver le type de débit dans le JSON, mais ne pas ajouter d’étiquette `(global)` ou `(réponse)` dans le tableau. Une mesure indisponible ou non exécutée s’affiche `-` sans symbole de remplacement.

Les couleurs sont informatives, indépendantes de la validité : un solde rouge mais positif peut satisfaire le contrôle de solde. L’état doit toujours porter 🟢 `Valide` ou 🔴 `Invalide`, avec gratuit en 3/4 ou le diagnostic dans cette même cellule. Enregistrer les informations d’affichage dans `quota_display` sans écraser les quotas bruts.


## Sortie utilisateur limitée à un tableau multi-colonnes

Lors d’une invocation normale de `/pllm`, restituer un seul tableau Markdown multi-colonnes avec une ligne par politique dans l’ordre de priorité 1 à 6. Le Markdown est obligatoire car l’interface échappe le HTML brut. Les colonnes sont `Politique`, `Identifiant API`, `Fournisseur`, `TTFT (s)`, `Tokens/s`, `État`, `Dernier palier réussi` et `Évalué le`. Afficher ensuite six lignes de ressources (non applicables en 3/4), une pour chaque PLLM.

Les colonnes `Modèle`, `Raisonnement`, `Priorité`, `Mode`, `Cause`, `Sélectionné`, `Quotas / solde` et `Condition` ne sont pas ajoutées ; le diagnostic figure dans `État`. La condition reste disponible dans le JSON et peut être fournie sur demande. Les cellules TTFT et tokens/s valent `-` si le test n’a pas été exécuté ou si la mesure est indisponible. Afficher TTFT et tokens/s avec une seule décimale. Afficher l’horodatage sous la forme `DD-MM-YY HH:mm`. L’état reste coloré par 🟢 `Valide` ou 🔴 `Invalide`, complété dans la même cellule par gratuit en 3/4 ou le diagnostic sûr.

Pour `/pllm active`, le fichier Markdown contient uniquement la ligne de la première politique valide, sa ligne de quotas / solde et l’encart actif, ou `Aucune politique valide` si aucune politique n’est valide. Cette publication reste silencieuse : aucun tableau n’est restitué dans la conversation. Le JSON conserve `selected_mode`, `selection_status`, `selected` et `condition` pour les commandes consommatrices et les demandes détaillées.


## Argument `active` — sélection silencieuse

`/pllm active` exécute `python3 scripts/evaluate.py active`. Évaluer les politiques par priorité croissante avec les contrôles et paliers mémorisés habituels. Après le premier candidat conforme du mode, arrêter dès la première politique `Valide` : ne consulter ni quotas ni performances des politiques suivantes.

Actualiser `pllm-current.json` et `pllm-current.md` sans sortie console ni tableau dans la conversation. En mode active, le Markdown contient uniquement la ligne de la politique sélectionnée, sa ligne de quotas / solde et l’encart actif pour les autres commandes. Si aucune politique ne satisfait les conditions, publier « Aucune politique valide » et `selected_mode=null` ; ne pas conserver une ancienne sélection.

Le JSON conserve les lignes historiques des politiques non visitées, avec leur ancien horodatage et `evaluated_this_run=false`. Elles ne représentent pas des contrôles actuels et ne doivent jamais être sélectionnées sur cette base. Les politiques visitées ont `evaluated_this_run=true`. `evaluation_mode` distingue `active` et `all`. L’invocation sans argument continue à contrôler tous les modes et afficher le tableau unique, ses six lignes de ressources (non applicables en 3/4) et l’encart de la PLLM active.

L’exécution planifiée demandée est quotidienne à 00:00, 06:00, 12:00 et 18:00, heure de Paris. Elle doit utiliser le skill actif, sans figer un ancien nom d’utilisateur Unix, et rester silencieuse en fonctionnement normal.
