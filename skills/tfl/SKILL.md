---
name: tfl
description: Générer un rapport autonome des LLM OpenCode Go puis OpenRouter, avec filtres de contexte, coût, multimédia, blacklist et code couleur communs. Utiliser pour /TFL, TFL ou « Test Fournisseur LLM ».
---

# TFL — Test Fournisseur LLM

Produire un rapport unifié en français avec deux tableaux fournisseurs,
OpenCode Go puis OpenRouter. OpenCode général est retiré : ne collecter ni
ses modèles, ni ses tarifs, ni ses métadonnées ; ne pas le tester ou le lister.
Le JSON contient uniquement les sections fournisseurs opencode_go et openrouter.

TFL est autonome : il interroge directement les catalogues et sources officielles, applique ses propres
règles et ne dépend pas des skills ou plugins TOCG/TLOLC.

## Exécution

L’exécution de TFL est obligatoirement effectuée hors sandbox, car le générateur
doit accéder aux APIs OpenCode Go et OpenRouter. Dans Codex, lancer la commande
avec une exécution autorisée hors sandbox (par exemple
`sandbox_permissions=require_escalated`). Cette règle s’applique aux invocations
directes, aux commandes `/TFL` et à tout plugin qui charge cette skill. Ne pas
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
les deux tableaux fournisseurs, les essais gratuits, la date d’actualisation, chemins des fichiers et messages d’erreur
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
- `data/tfl.md`, rapport complet dans l’ordre Go, OpenRouter, puis essais gratuits.

## Colonnes communes

Les deux tableaux fournisseurs gardent les huit colonnes suivantes : `Rang`, `Modèle /
ID`, `Contexte`, `Sortie`, `Entrée $/M`, `Sortie $/M`, `Coût moyen $/M` et `Code
couleur`. Les métadonnées propres à un fournisseur restent dans le JSON, mais
ne sont jamais ajoutées à un seul des tableaux.

Le coût moyen est `(prix d'entrée + prix de sortie) / 2`. Go affiche USD/M ;
OpenRouter affiche EUR/M après conversion BCE vérifiée. Le classement est
croissant. Les libellés tarifaires du tableau OpenRouter utilisent €/M.

Code couleur dans la devise affichée : 🟢 jusqu’à 0.20 $/M inclus, 🟡 au-delà de 0.20 jusqu’à
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
- Les exclusions par identifiant proviennent exclusivement de LM et restent
  auditables dans `excluded_models`.
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
`store=false` et `reasoning.effort=medium`. Pour `chat_completions`, il utilise
`messages` et `max_tokens`. Toute requête OpenCode Go de complétion doit porter
`x-opencode-session`. Une route absente ou inconnue doit être signalée et ne
doit pas être remplacée silencieusement par une autre.

## Règles OpenRouter

- Source API : `https://openrouter.ai/api/v1/models`.
- La sélection examine tous les modèles renvoyés par l'API, sans liste
  prédéfinie d'identifiants, filtre de catégorie ou limite artificielle du
  nombre de modèles. Les filtres TFL sont appliqués localement.
- Les modèles multimodaux en entrée sont conservés ; le tableau commun affiche
  uniquement la modalité de sortie. Les sorties non textuelles audio, vidéo,
  speech ou sound sont exclues.
- Le contexte doit être au moins de 1M et le coût moyen compris entre zéro et
  0.10 €/M inclus après conversion BCE vérifiée. Un gratuit vérifié reste admissible.
- Les payants sont conservés avec contexte/prix/modalités admissibles sans
  exiger Medium ; les gratuits doivent publier Medium et réussir le benchmark.
- La liste noire partagée LM s'applique sans liste propre à OpenRouter.
- Les modalités d’entrée/sortie, capacités (`tools`, `reasoning`, `JSON`),
  paramètres API et motifs d’exclusion restent dans la section OpenRouter du
  JSON.
- Un nouveau modèle admissible est classé automatiquement. La disparition
  d'un ancien modèle ne provoque pas d'échec si d'autres résultats sont
admissibles. Si aucun modèle ne satisfait les filtres, TFL publie la sélection
vide et ses exclusions sans interrompre les autres catalogues.

Les prix OpenRouter sont récupérés à chaque exécution dans `pricing.prompt`
et `pricing.completion`, puis convertis par million de tokens. Les prix de
cache et les éventuels paliers `overrides` sont conservés séparément dans le
JSON, avec leurs conditions de contexte ou de jours et horaires UTC ; le
classement conserve les prix API de base. Les prix négatifs, non
finis ou débordants ne sont pas exploitables.

## Robustesse et présentation

TFL affiche OpenCode Go puis OpenRouter, ses deux seuls catalogues. Une
erreur d’authentification, de réseau, de JSON ou de données indispensables fait
échouer la génération plutôt que de produire un classement partiel silencieux.
Une collecte valide sans modèle admissible reste un résultat publiable : les
autres catalogues continuent, même si les deux sélections sont vides. Chaque
tableau fournisseur garde ses huit colonnes et affiche « Aucun modèle
admissible » avec une synthèse des exclusions lorsqu'il est vide. Le JSON
conserve models vide, selection_status (available ou empty), exclusion_summary
(motif vers nombre), les compteurs, sources et exclusions détaillées courants.
Une publication valide retourne zéro, sans réutiliser d'ancien catalogue.

Le JSON conserve la source et la date de récupération tarifaire de chaque
fournisseur. Une source indispensable inaccessible, invalide ou de format
non reconnu fait échouer la collecte avant publication et préserve les
rapports précédents. Aucun prix historique n'est réutilisé silencieusement.
Une route de génération Go inconnue reste signalée sans protocole inventé.

Le rapport commence par `# TFL — Test Fournisseur LLM`, puis affiche les titres
`Rapport des LMM OpenCode Go les moins onéreux` et `Rapports des LMM OpenRouter les moins
onéreux`. Il restitue la date de récupération, les filtres appliqués,
les chemins des fichiers et les exclusions dans le JSON.

TFL mesure désormais la latence et le débit des seuls gratuits structurellement
admissibles. Les payants restent un catalogue tarifaire sans benchmark ni filtre Medium.
TFL ne mesure pas la qualité fonctionnelle du code généré. Les tarifs sont
des références fournisseur susceptibles d’évoluer. Le catalogue TFL est la
source à utiliser par `/PLLM` pour son modèle OpenRouter économique, via
`~/.codex/skills/tfl/data/tfl.json`, section `openrouter.models`.


## Qualification obligatoire des gratuits

Pour les deux catalogues, vérifier les prix d'entrée/sortie nuls et les
variantes compatibles, contexte ≥1M et les filtres existants. Tester chaque
candidat gratuit avec scripts/performance.py, moteur local embarqué identique
à PLLM. Exiger réponse complète, comptage fiable, TTFT <30 s ET débit >20
 tokens/s. Le débit Go inclut raisonnement et réponse ; OpenRouter
utilise la réponse seule. Aucune mesure commerciale ou historique ne valide
la collecte courante.

Tous les tests gratuits demandent exclusivement Medium, sans repli vers un autre effort. Chat Completions
utilise reasoning_effort, Responses reasoning.effort, Messages thinking
adaptive et output_config.effort. Une capacité Medium publiée peut établir son acceptation ; sinon, une réponse API complète à la requête Medium la prouve, même si le fournisseur convertit ou ignore l'effort en interne. Des métadonnées absentes ou différentes ne bloquent pas seules l'essai. Les payants OpenRouter ne demandent pas cette preuve. Un refus 400 propre à l'effort, comme
401/403/429, arrête le candidat. Les paliers sont 1024, 2048, 4096, 8192, 120 s par requête,
arrêt au premier succès. Le niveau effectif et les paramètres sont tracés.

Les tests gratuits n'appellent jamais quota, crédit ou solde. Go
utilise la clé de la politique TFL sélectionnée. Pour les générations
OpenRouter, utiliser la clé d'environnement existante, sinon le trousseau
historique service=pllm/policy=mode3/provider=openrouter du compte OpenRouter,
sans valeur transmise au modèle, en argument, dans les rapports ou journaux.
Un accès manquant exclut le gratuit avec sa cause ; ne créer aucun secret.

Retirer de models tous les gratuits échoués ou non mesurables. Conserver
leurs critères, dates, niveaux, tentatives, mesures disponibles et causes
filtrées dans excluded_models et free_performance_results. Une limitation
HTTP est un échec d'accès, jamais une mesure de TTFT/débit inventée. Recalculer
les rangs après exclusion, sans modifier le classement des payants.
Ajouter après les deux tableaux fournisseurs un tableau commun des essais
gratuits, avec fournisseur, modèle, TTFT, débit, raisonnement et état/cause.
Si une section devient vide après qualification, publier son état, ses
exclusions et les essais effectués, puis poursuivre les autres sections.
Ne pas confondre ce résultat daté et lié au
compte utilisé avec une indisponibilité permanente du fournisseur.


## Débit moyen — protocole 8

Utiliser la même mesure que PLLM : tokens de sortie Go, ou tokens de
réponse seuls OpenRouter, divisés par la durée complète non arrondie de la
requête. L'attente, le TTFT et le raisonnement sont inclus dans cette durée.
Il s'agit d'une moyenne côté client, sans extrapoler une rafale de fragments
ni soustraire le premier token, sans écrêtage ou plancher artificiel.
request_seconds porte le dénominateur exact ; duration_seconds est un affichage
arrondi ; generation_seconds reste un diagnostic entre fragments.
Une réponse complète en un bloc est mesurable ; une durée invalide ou un
comptage inexploitable exclut le gratuit avec une mesure indisponible.
Les rapports tracent throughput_metric=request_average_v1,
throughput_window=request_total et measurement_protocol_version=8.
Les seuils 30 s / 20 tokens/s restent stricts, mais le nouveau débit peut
modifier l'éligibilité. Les valeurs anciennes ne sont pas directement
comparables et ne sont pas réécrites. Relancer TFL puis PLLM après mise à jour
pour obtenir de nouvelles qualifications avec le protocole 8.


## Liste noire partagée LM

Charger scripts/model_blacklist.py, embarqué dans ce paquet, avant les appels
fournisseur. Le script applique la liste CODEX_HOME/lm/blacklist.json,
avec ~/.codex comme CODEX_HOME par défaut. Sans fichier, mimo-v2.5 et
muse-spark-1.2-contributor sont exclus ; les deux entrées sont retirables par LM.
Une liste invalide bloque sans écrasement. Utiliser $lm ou /LM pour LIST,
ADD identifiant ou REMOVE identifiant ; ce stockage reste hors des caches.
Les préfixes fournisseur, la casse et les suffixes :free/-free ne permettent
pas de contourner une exclusion. LM est l'unique liste noire ; aucune exclusion
permanente ou liste interne TFL ne subsiste. Une liste explicite vide reste vide.
Les modèles interdits sont absents des listes retenues et des tests ; seules
les traces d'exclusion les mentionnent. Un ancien catalogue ou historique ne
valide pas un modèle interdit et une cible forcée interdite reste refusée.
Maintenir ce module identique dans les six distributions LM/TFL/PLLM.

## Planning utilisateur TFL puis PLLM

Le hook SessionStart approuvé et TCU --apply peuvent enregistrer le timer
utilisateur à 00 h et 12 h Europe/Paris. Pour une installation autonome
explicitement demandée, utiliser `python3 -B scripts/scheduler.py install`.
Une simple invocation TFL ne demande pas l'installation d'un planning.
Le runner exige Codex ouvert et un quota Codex frais disponible avant TFL
puis PLLM normal ; un quota nul ou inconnu bloque l'étape. PLLM reçoit le
catalogue fraîchement publié, sans repli sur un ancien fichier en cas d'échec.
Les passages manqués ne sont pas rattrapés. Cette coordination ne change ni
les filtres TFL, ni les seuils gratuits, ni LM, ni les invocations manuelles.
Le contrôle du planning reste inchangé : une section Go ou OpenRouter models vide dans un
rapport manuel valide empêche encore le lancement planifié de PLLM ; aucune
section générale opencode n’est exigée.


## Admission stricte Medium pour les candidats benchmarkés

Tout candidat gratuit ou Go payant doit publier une capacité Medium vérifiable
avant test, sélection et affichage. Une liste supported_efforts contenant
medium ou un null explicitement publié (tous les efforts) est admissible. Une
clé absente, une valeur invalide, un booléen reasoning, une liste sans medium
ou un budget seul ne suffit pas. Aucun autre effort n'est autorisé.
Les exclus restent dans les audits JSON, sans apparaître dans les tableaux.
Les anciens catalogues, historiques et rangs forcés ne contournent pas ce
filtre pour les candidats benchmarkés ; DeepSeek direct exige aussi une preuve.
Les payants OpenRouter sont conservés même sans Medium. Une section TFL vide est
publiée explicitement avec ses exclusions et ne bloque pas les autres sections.

Les niveaux publiés dans `reasoning_options` (type=effort, values) sont des
preuves. Medium officiellement accepté reste admissible même sans intensité
distincte : tracer l'équivalence et envoyer les paramètres documentés du
protocole utilisé, comme thinking.type=enabled pour une équivalence documentée.
Une preuve historique qui ne couvre pas Medium ne remplace pas une requête
courante acceptée. Une valeur absente, un budget ou un interrupteur seul
n'invente pas cette preuve.

## Investigation obligatoire des efforts et contextes

Un contexte non vérifiable impose une analyse et une recherche du LLM dans les
sources officielles. Pour un effort Medium inconnu, envoyer la requête Medium
sur le transport publié et utiliser une réponse complète comme preuve de son
acceptation. Suivre [le protocole de preuve](references/model-evidence.md),
compléter les conclusions sourcées dans le répertoire du rapport et relancer
le générateur. Le JSON marque les investigations de contexte `required` ; le
rapport reste provisoire jusqu'à leur résolution ou à un blocage explicite.
Si le contexte reste invérifiable après investigation, le modèle est écarté.
Les seuils restent inchangés.


## Plafond OpenRouter en euros

Collecter le dernier taux USD par EUR publié par la BCE à
https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml à chaque invocation.
Calculer EUR = USD / taux et comparer la moyenne non arrondie à 0,10 EUR/M
inclus. Une source, une date ou un taux absent, invalide ou inaccessible bloque
la publication sans repli historique. Conserver prix natifs USD, prix EUR,
source, date de publication et date de récupération dans le JSON. Les prix
OpenRouter affichés sont en €/M ; le taux daté accompagne le tableau.
Go garde le plafond 0,50 USD/M. Le filtre Medium s’applique aux gratuits et
aux payants Go benchmarkés ; les payants OpenRouter n’en dépendent pas. Les
exclus d’effort sont absents des tableaux des gratuits mais restent dans les audits JSON.

La commande canonique est `/TFL` ; `/tfl` reste
un alias compatible. L’identifiant technique du skill reste en minuscules.
