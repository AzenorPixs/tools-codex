---
name: tfl
description: Générer un rapport autonome et unifié des LLM OpenCode Go, du catalogue général OpenCode puis OpenRouter, avec filtres de contexte, coût, multimédia, blacklist et code couleur communs. Utiliser pour /tfl, TFL ou « Test Fournisseur LLM ».
---

# TFL — Test Fournisseur LLM

Produire un rapport unifié, en français, des modèles LLM retenus dans trois
catalogues. L’ordre est obligatoire :

1. OpenCode Go ;
2. catalogue général OpenCode ;
3. OpenRouter.

TFL est autonome : il interroge directement les catalogues et sources officielles, applique ses propres
règles et ne dépend pas des skills ou plugins TOCG/TLOLC.

## Exécution

L’exécution de TFL est obligatoirement effectuée hors sandbox, car le générateur
doit accéder aux APIs OpenCode Go, OpenCode général et OpenRouter. Dans Codex, lancer la commande
avec une exécution autorisée hors sandbox (par exemple
`sandbox_permissions=require_escalated`). Cette règle s’applique aux invocations
directes, aux commandes `/tfl` et à tout plugin qui charge cette skill. Ne pas
relancer TFL dans la sandbox si l’autorisation hors sandbox est refusée : arrêter
et restituer clairement l’erreur.

Depuis le dossier de ce skill :

```bash
python3 scripts/test_fournisseur_llm.py
python3 scripts/test_fournisseur_llm.py mode1
python3 scripts/test_fournisseur_llm.py mode2
python3 scripts/test_fournisseur_llm.py --policy auto
```

Lorsqu’une demande `/TFL`, `/tfl` ou « Test Fournisseur LLM » est exécutée
depuis la console, la sortie non sensible de la commande doit toujours être
restituée dans le message final visible de l’interface Codex, et pas seulement
dans la sortie technique d’un outil ou dans un message de progression :
les trois tableaux, date d’actualisation, chemins des fichiers et messages d’erreur
éventuels. Ne pas exécuter silencieusement la commande ni renvoyer uniquement
les liens vers les fichiers. Les clés et toute autre donnée sensible restent
exclues de la restitution.

`auto` recherche d’abord le secret OpenCode Go du mode 1, puis celui du mode 2
si le premier est inaccessible. La première clé accessible est utilisée pour
la requête API ; un refus d’authentification ou un échec de cette requête ne
déclenche pas de repli vers l’autre clé. La clé OpenRouter est lue depuis
`OPENROUTER_API_KEY`, puis `OPENROUTER_KEY`. Aucune clé ne doit apparaître dans
la sortie, les fichiers ou les journaux.

La commande écrit atomiquement :

- `data/tfl.json`, catalogue unifié et audit détaillé ;
- `data/tfl.md`, rapport complet dans l’ordre Go, OpenCode général, OpenRouter.

## Colonnes communes

Les trois tableaux utilisent exactement les mêmes colonnes : `Rang`, `Modèle /
ID`, `Contexte`, `Sortie`, `Entrée $/M`, `Sortie $/M`, `Coût moyen $/M` et `Code
couleur`. Les métadonnées propres à un fournisseur restent dans le JSON, mais
ne sont jamais ajoutées à un seul des tableaux.

Le coût moyen est `(prix d'entrée + prix de sortie) / 2`, en USD par million de
tokens, et le classement est croissant sur cette valeur.

Code couleur commun : 🟢 jusqu’à 0.20 $/M inclus, 🟡 au-delà de 0.20 jusqu’à
0.40 $/M inclus, 🟠 au-delà de 0.40 jusqu’à 0.50 $/M inclus, ⚪ coût non
vérifié, 🔴 au-delà du seuil.

## Règles OpenCode Go

- Source de disponibilité : `https://opencode.ai/zen/go/v1/models`.
- Source complémentaire : `https://models.dev/api.json`, fournisseur
  `opencode-go`, pour `limit.context`, `modalities.input/output` et le
  transport `npm`/`api` du fournisseur avec ses surcharges par modèle.
- Le contexte est strictement vérifié et doit être supérieur ou égal à 1M de
  tokens. Un contexte absent ou inférieur à 1M exclut le modèle.
- Le coût de référence hors pointe doit être vérifiable et sa moyenne doit être
  inférieure ou égale à 0.5 $/M. Les coûts inconnus ou supérieurs sont exclus.
- Les sorties audio, vidéo, speech et sound sont exclues. Une capacité
  multimodale uniquement en entrée reste admissible ; une sortie absente des
  sources reste `Non vérifié`. Les déclarations API et models.dev sont
  confrontées ; des modalités contradictoires font échouer la génération.
- `muse-spark-1.2-contributor` est une blacklist permanente et reste auditable
  dans `excluded_models`.
- Les tarifs pointe/hors pointe, estimations rolling/weekly/monthly, sources de
  contexte et motifs d’exclusion sont conservés dans le JSON, pas dans le
  tableau commun.
- La source tarifaire de référence est `https://opencode.ai/docs/go/`.

Les tarifs sont récupérés dans les tableaux de cette documentation à chaque
exécution, sans table tarifaire statique ni repli sur un ancien catalogue.
Les noms publiés sont rapprochés des identifiants disponibles sans recherche
approximative. Une correspondance absente exclut le modèle avec son motif ;
une ambiguïté ou des prix contradictoires font échouer la génération.
Les prix barrés sont ignorés. Les variantes et les prix de cache sont conservés
dans le JSON. Pour plusieurs paliers de contexte, le classement utilise le
coût moyen hors pointe maximal, afin de ne pas appliquer un prix réservé aux
contextes courts. Les estimations de requêtes non collectées restent `N/A`
(`null` dans les champs numériques JSON).

La clé est recherchée avec `service=pllm`, `policy=mode1|mode2`,
`provider=opencodego` et le compte associé, sans afficher sa valeur.

### Routage API par modèle

OpenCode Go ne fournit pas un protocole de génération uniforme. TFL publie
`api_endpoint`, `api_protocol` et `endpoint_source` à partir des métadonnées
courantes, sans liste de modèles ni déduction par famille ou nom. Une route
explicite API prime ; sinon le SDK et la base API publiés par models.dev sont
résolus avec les surcharges du modèle sur le fournisseur. Un modèle absent
des métadonnées de transport ne reçoit aucun routage par défaut inventé.

Les contrats génériques reconnus sont `@ai-sdk/openai-compatible` pour
`chat_completions`, `@ai-sdk/openai` pour `responses` et `@ai-sdk/anthropic`
pour `messages`. Un protocole explicitement publié est conservé lorsqu'il
est reconnu. Un SDK/protocole inconnu ou une base absente restent signalés.
Ces règles décrivent les transports, jamais une liste d'identifiants de modèles.

Les bases et endpoints publiés doivent être HTTPS, de la même origine
OpenCode, sans identifiants utilisateur, query ou fragment. Une URL non sûre
bloque la publication. Le JSON conserve les sources et dates dans
`modalities_metadata` et `routing_metadata`. Le statut de route `documented`
indique une résolution de métadonnées ; `generation_tested=false` ne doit
jamais être présenté comme un appel de génération réussi. Un gratuit retenu
après une génération complète reçoit generation_tested=true avec ses preuves.

Pour `responses`, le corps utilise `input`, `max_output_tokens`, `stream=true`,
`store=false` et `reasoning.effort=high`. Pour `chat_completions`, il utilise
`messages` et `max_tokens`. Toute requête OpenCode Go de complétion doit porter
`x-opencode-session`. Une route absente ou inconnue doit être signalée et ne
doit pas être remplacée silencieusement par une autre.

## Règles du catalogue général OpenCode

- Disponibilité : `https://opencode.ai/zen/v1/models`, par GET public sans
  Authorization ni emprunt du secret Go.
- Tarifs : `https://opencode.ai/v2/docs/console/models/`, collectés à chaque
  exécution, sans table statique ni repli sur un ancien catalogue.
- Métadonnées : fournisseur `opencode` de `https://models.dev/api.json`,
  indépendant de `opencode-go` pour contexte, modalités et transport.
- Contexte vérifié ≥ 1M tokens ; moyenne des prix d'entrée/sortie comprise
  entre zéro et 0,50 USD/M inclus. Le prix de classement est le maximum des
  moyennes des variantes publiées, paliers et périodes compris ; les prix
  de cache restent séparés. Go conserve sa référence hors pointe.
- Les sorties audio/vidéo/speech/sound et `muse-spark-1.2-contributor` sont
  exclues. Une entrée multimodale reste admissible ; l'inconnu reste explicite.
- La section JSON `opencode` conserve sources, dates, variantes, modèles et
  exclusions. Un même ID dans Go et le catalogue général garde ses données
  propres dans chaque section, sans emprunt de prix, contexte ou route.

Les variantes gratuites de contexte inférieur à 1M restent exclues. Le
catalogue général possède son propre classement et les mêmes huit colonnes.
Les sections `opencode_go` et `openrouter` restent compatibles avec PLLM ;
l'ajout du catalogue général ne change pas ses politiques de sélection.

## Règles OpenRouter

- Source API : `https://openrouter.ai/api/v1/models`.
- La sélection examine tous les modèles renvoyés par l'API, sans liste
  prédéfinie d'identifiants, filtre de catégorie ou limite artificielle du
  nombre de modèles. Les filtres TFL sont appliqués localement.
- Les modèles multimodaux en entrée sont conservés ; le tableau commun affiche
  uniquement la modalité de sortie. Les sorties non textuelles audio, vidéo,
  speech ou sound sont exclues.
- Le contexte doit être au moins de 1M et le coût moyen compris entre zéro et
  0.5 $/M inclus. Un modèle gratuit vérifié reste admissible.
- `meta/muse-spark-1.2-contributor` est une blacklist permanente.
- Les modalités d’entrée/sortie, capacités (`tools`, `reasoning`, `JSON`),
  paramètres API et motifs d’exclusion restent dans la section OpenRouter du
  JSON.
- Un nouveau modèle admissible est classé automatiquement. La disparition
  d'un ancien modèle ne provoque pas d'échec si d'autres résultats sont
  admissibles. Si aucun modèle ne satisfait les filtres, TFL échoue explicitement.

Les prix OpenRouter sont récupérés à chaque exécution dans `pricing.prompt`
et `pricing.completion`, puis convertis par million de tokens. Les prix de
cache et les éventuels paliers `overrides` sont conservés séparément dans le
JSON, avec leurs conditions de contexte ou de jours et horaires UTC ; le
classement conserve les prix API de base. Les prix négatifs, non
finis ou débordants ne sont pas exploitables.

## Robustesse et présentation

TFL affiche OpenCode Go, puis le catalogue général OpenCode, puis OpenRouter. Une
erreur d’authentification, de réseau, de JSON ou de filtre fait échouer la
génération plutôt que de produire un classement partiel silencieux.

Le JSON conserve la source et la date de récupération tarifaire de chaque
fournisseur. Une source indispensable inaccessible, invalide ou de format
non reconnu fait échouer la collecte avant publication et préserve les
rapports précédents. Aucun prix historique n'est réutilisé silencieusement.
Une route de génération Go inconnue reste signalée sans protocole inventé.

Le rapport commence par `# TFL — Test Fournisseur LLM`, puis affiche les titres
`Rapport des LMM OpenCode Go les moins onéreux`, `Rapport des LMM du catalogue
général OpenCode les moins onéreux` et `Rapports des LMM OpenRouter les moins
onéreux`. Il restitue la date de récupération, les filtres appliqués,
les chemins des fichiers et les exclusions dans le JSON.

TFL mesure désormais la latence et le débit des seuls gratuits structurellement
admissibles. Les payants restent un catalogue tarifaire sans benchmark.
TFL ne mesure pas la qualité fonctionnelle du code généré. Les tarifs sont
des références fournisseur susceptibles d’évoluer. Le catalogue TFL est la
source à utiliser par `/pllm` pour son modèle OpenRouter économique, via
`~/.codex/skills/tfl/data/tfl.json`, section `openrouter.models`.


## Qualification obligatoire des gratuits

Pour les trois catalogues, vérifier les prix d'entrée/sortie nuls et les
variantes compatibles, contexte ≥1M et les filtres existants. Tester chaque
candidat gratuit avec scripts/performance.py, moteur local embarqué identique
à PLLM. Exiger réponse complète, comptage fiable, TTFT <30 s ET débit >20
 tokens/s. Le débit Go/général inclut raisonnement et réponse ; OpenRouter
utilise la réponse seule. Aucune mesure commerciale ou historique ne valide
la collecte courante.

Tous les tests demandent HIGH ; XHIGH est le seul repli autorisé si HIGH est
indisponible et XHIGH publié. Chat Completions utilise reasoning_effort,
Responses reasoning.effort, Messages thinking adaptive et output_config.effort.
OpenRouter utilise ses métadonnées, ou un budget HIGH de 80 % lorsque seul
max_tokens est disponible. Aucun repli Low/Medium. Un refus 400 propre à l'effort
permet au plus un passage XHIGH annoncé, avec recalcul des paliers ; 401/403/429
arrêtent le candidat. Les paliers sont 1024, 2048, 4096, 8192, 120 s par requête,
arrêt au premier succès. Le niveau effectif et les paramètres sont tracés.

Les tests gratuits n'appellent jamais quota, crédit ou solde. Go et général
utilisent la clé de la politique TFL sélectionnée. Pour les générations
OpenRouter, utiliser la clé d'environnement existante, sinon le trousseau
historique service=pllm/policy=mode3/provider=openrouter du compte OpenRouter,
sans valeur transmise au modèle, en argument, dans les rapports ou journaux.
Un accès manquant exclut le gratuit avec sa cause ; ne créer aucun secret.

Retirer de models tous les gratuits échoués ou non mesurables. Conserver
leurs critères, dates, niveaux, tentatives, mesures disponibles et causes
filtrées dans excluded_models et free_performance_results. Une limitation
HTTP est un échec d'accès, jamais une mesure de TTFT/débit inventée. Recalculer
les rangs après exclusion, sans modifier le classement des payants.
Ajouter après les trois tableaux fournisseurs un tableau commun des essais
gratuits, avec fournisseur, modèle, TTFT, débit, raisonnement et état/cause.
Si une section devient vide après qualification, arrêter avant publication et
préserver les rapports existants. Ne pas confondre ce résultat daté et lié au
compte utilisé avec une indisponibilité permanente du fournisseur.
