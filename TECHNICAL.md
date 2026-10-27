# TECHNICAL.md — Tools Codex

## Objet

Ce document définit le cadre technique des extensions distribuées par Tools
Codex. Il complète `PROJECT.md`, `BUILD.md` et les règles de `AGENTS.md`.

## Compatibilité

Les extensions ciblent Codex et doivent rester compatibles avec les formats
de plugins pris en charge par Codex. Toute incompatibilité de version ou de
plateforme doit être documentée dans la spécification OpenSpec applicable.

Les outils utilisés pour le développement et la validation sont ceux déclarés
dans `DEVOPS.md`. Aucune dépendance supplémentaire ne doit être introduite
sans validation explicite du développeur.

La plage Python déclarée dans `pyproject.toml` est `>=3.13,<3.15` : branches
3.13 et 3.14, qualifiées par les contrôles hors ligne décrits ci-dessous.
Les versions antérieures à 3.13 et à partir de 3.15 sont explicitement hors
de cette plage. La version observée dans `DEVOPS.md` reste un inventaire
d'environnement, distinct des preuves de qualification.
`pyproject.toml` décrit les métadonnées et prérequis Python du dépôt ; aucun
packaging ni publication Python n'est ajouté. Sa métadonnée `project.version`
reprend exactement la release de `VERSION`, qui reste la source de vérité.

## Arborescence

Les commandes sources CM/PLLM/TFL/TCU/LM/PROMPT sont conservées dans :

```text
.codex/commands/
```

Les six fichiers canoniques sont CM.md, PLLM.md, TFL.md, TCU.md, LM.md et
PROMPT.md. Leurs déclencheurs sont /CM, /PLLM, /TFL, /TCU, /LM et /PROMPT ;
les anciennes graphies en minuscules restent des alias. Chaque skill déclare
son display_name en majuscules dans agents/openai.yaml, identique dans les
deux distributions. Les identifiants techniques, chemins de skills et
invocations $… restent en minuscules.

Les plugins sont placés à la racine du dépôt :

```text
plugins/<NOM_DU_PLUGIN>/
```

Les skills autonomes sont placés à la racine du dépôt :

```text
skills/<NOM_DU_SKILL>/
```

Le skill `cm` possède sa source d'édition dans `skills/cm/SKILL.md`. Le lien
symbolique relatif `.agents/skills/cm -> ../../skills/cm` l'expose dans
l'emplacement de découverte des skills du dépôt. Il reste dans le projet et
évite une copie supplémentaire pour la découverte locale. Le plugin embarque
un fichier identique dans `plugins/cm/skills/cm/SKILL.md`, sans lien vers
l'extérieur du paquet. Aucun fichier global Codex n'est modifié.

Le catalogue de la marketplace du dépôt est placé dans :

```text
.agents/plugins/marketplace.json
```

Les chemins des plugins déclarés dans ce catalogue sont relatifs à la racine
du dépôt et commencent par `./`.

## Version de release

`VERSION` est la source de vérité de la version de release de Tools Codex.
Chaque manifeste `plugins/<NOM_DU_PLUGIN>/.codex-plugin/plugin.json` publié
par la marketplace et `project.version` dans `pyproject.toml` doivent déclarer
exactement cette version.

## Structure des plugins actuels

Les plugins `cm`, `pllm`, `tfl`, `tcu`, `lm` et `prompt` possèdent un identifiant stable en kebab-case et
utilisent actuellement le manifeste de compatibilité Codex suivant :

```text
plugins/<NOM_DU_PLUGIN>/.codex-plugin/plugin.json
```

Le manifeste déclare le nom, la version, la présentation et le répertoire de
skills embarqués. Les six plugins embarquent chacun le skill du même nom.
PLLM et TFL incluent les scripts, références et données nécessaires à leur
exécution. CM conserve son catalogue et embarque aussi le bootstrap du planning
commun, comme les cinq autres plugins. Il ne déclare ni serveur MCP ni application.

TCU embarque `skills/tcu/SKILL.md` et `skills/tcu/scripts/update.py`. Les deux
copies autonomes et embarquées sont identiques. Le lien relatif
`.agents/skills/tcu -> ../../skills/tcu` assure la découverte dans ce projet.
Les deux distributions fournissent aussi `agents/openai.yaml` avec le nom
d'affichage `TCU` pour les listes et pastilles de skills.

Le plugin prompt embarque `skills/prompt/SKILL.md` et
`skills/prompt/scripts/resolve_prompt.py`, identiques aux sources autonomes.
Le lien `.agents/skills/prompt -> ../../skills/prompt` expose le skill local.

Le format portable avec un manifeste `plugin.json` à la racine peut être adopté
pour une évolution ultérieure validée. Il ne doit pas être ajouté uniquement
pour dupliquer le manifeste de compatibilité existant.

Une structure de plugin compatible avec l'état actuel est :

```text
plugins/<NOM_DU_PLUGIN>/
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   └── <NOM_DU_SKILL>/
│       ├── SKILL.md
│       ├── agents/
│       ├── scripts/
│       ├── references/
│       └── data/
```

Les répertoires `agents/`, `scripts/`, `references/` et `data/` sont
optionnels. Les skills intégrés à un plugin sont placés dans son répertoire
`skills/`.

## Commandes et skills autonomes

Chaque commande et skill autonome doit avoir une responsabilité unique, un nom
explicite et une documentation suffisante pour son usage. Les fichiers texte
sont encodés en UTF-8 avec des fins de ligne Unix.

Les skills autonomes sont stockés dans `skills/<NOM_DU_SKILL>/`. Leur structure
précise suit les conventions Codex applicables au moment de leur création. Une
extension ne doit pas dupliquer un comportement déjà fourni par un plugin ou
une commande existante sans nécessité documentée.

Un même skill peut être fourni à la fois de façon autonome et embarqué dans un
plugin lorsque les deux modes de distribution sont nécessaires.

Les correspondances actuellement publiées sont :

| Invocation de skill | Skill autonome | Plugin |
|---|---|---|
| `$cm` | `skills/cm/` | `plugins/cm/` |
| `$pllm` | `skills/pllm/` | `plugins/pllm/` |
| `$tfl` | `skills/tfl/` | `plugins/tfl/` |
| `$tcu` (déclencheur `/TCU`) | `skills/tcu/` | `plugins/tcu/` |
| `$lm` (déclencheur `/LM`) | `skills/lm/` | `plugins/lm/` |
| `$prompt` (déclencheur `/PROMPT`) | `skills/prompt/` | `plugins/prompt/` |
| `$cgpt` | `skills/cgpt/` | — |
| `$coding-session-statistics` | `skills/coding-session-statistics/` | — |

Le catalogue de `$cm` doit rester synchronisé avec les noms, syntaxes et
responsabilités des entrées maison publiées. Sa consultation n'exécute pas
PLLM, TFL, TCU, LM ou un prompt. Elle ne vérifie pas que ces skills sont installés localement.
La colonne `Commande` référence les skills disponibles avec leurs noms
lisibles, dont `TCU`, pour permettre leur présentation native dans Codex ;
les syntaxes `$…` restent dans `Utilisation`.
Après une modification de sa source autonome, la copie embarquée doit être
synchronisée et comparée octet pour octet. Le chargement simultané du plugin
CM et du skill autonome peut afficher deux entrées ; la procédure de
distribution n'en supprime ou désactive aucune automatiquement.
La commande source `.codex/commands/CM.md` délègue au skill CM ; `/CM` est
reconnu comme déclencheur du catalogue, qui garde une seule entrée prompt.
La présence de ces wrappers ne crée pas une slash native automatiquement
enregistrée dans Codex. `$cm` reste directement pris en charge.

## Prérequis d'exécution

Les prérequis suivants s'appliquent lors de l'utilisation des extensions. Ils
décrivent des mécanismes et des accès ; aucune valeur d'identification ne doit
être stockée dans ce dépôt.

| Composant | Prérequis locaux | Services externes nécessaires |
|---|---|---|
| `tfl` | Python 3, `secret-tool` et accès au trousseau de l'hôte, accès réseau HTTPS, exécution hors sandbox et répertoire de données inscriptible. Les accès aux fournisseurs sont configurés localement hors des sources. | OpenCode Go, models.dev et OpenRouter. |
| `pllm` | Python 3, `secret-tool` et accès au trousseau de l'hôte, accès HTTPS et `data/` inscriptible. Le catalogue TFL est fourni explicitement ou par le chemin voisin ; sept politiques sont initialisées si l'état courant manque. | OpenCode Go 1 à 4, OpenRouter payant 5 et gratuit 6, DeepSeek 7, BCE. |
| `cgpt` | Python 3, répertoire de données inscriptible et outil Codex `mcp__codex_app__get_usage_limits`. | Aucun accès HTTP direct. |
| `coding-session-statistics` | Historique persistant de la session. Le suivi de quota utilise `cgpt` ; les mesures de performance nécessitent une collecte planifiée dès le début de session. | Aucun accès HTTP direct obligatoire. |
| `$cm` | Skill découvert dans le projet ou installé dans un emplacement reconnu. | Aucun. |
| `$prompt` | Python 3.13/3.14, DEVOPS.md du projet courant et référentiel déclaré lisibles. | Aucun pour résoudre ; dépend ensuite du prompt choisi. |
| `$tcu` | Python 3.13/3.14, CLI Codex, racines identifiées inscriptibles pour appliquer. | GitHub public HTTPS et marketplace officielle. |
| Planning commun des six plugins | Python 3.13/3.14, CLI Codex, gestionnaire systemd utilisateur, TFL/PLLM installés et accès au trousseau de la session pour l'exécution. | Lecture des quotas Codex, puis services TFL/PLLM seulement si les conditions sont satisfaites. |

Les plugins `pllm` et `tfl` écrivent leurs rapports dans leur répertoire
`data/`. TFL accepte une redirection par `--output-dir` ; PLLM ne propose pas
d'option équivalente et exige que son propre répertoire `data/` soit
inscriptible. PLLM charge `data/pllm-current.json` avant l'évaluation ; si ce fichier
manque, sept politiques sont initialisées sans mesures ni sélection historique.
Un fichier courant invalide provoque un diagnostic et reste préservé. Les
contrôles de ressources applicables et les benchmarks des modes concernés
restent obligatoires ; les gratuits 3/4/6 ne consultent aucun quota.

PLLM définit sept priorités : 1/2 payants Go, 3/4 gratuits Go, 5 payants
OpenRouter sans benchmark, 6 gratuits OpenRouter benchmarkés et 7 DeepSeek
direct. Les modes 1/2 contrôlent les trois périodes Go ; mode5 consulte le
crédit OpenRouter, vérifie coût moyen ≤0,20 EUR/M et contexte ≥1M sans Medium
ni génération ; mode7 conserve le contrôle DeepSeek. Les gratuits 3/4/6 ne
consultent jamais quota ni solde et publient `quota_status=not_applicable`,
`quotas=null` et `Non applicable`. Ils exigent gratuité vérifiée, contexte
≥1M, Medium, TTFT <30 s et débit >20 tokens/s. Les modes benchmarkés payants
1/2/7 gardent TTFT <90 s et débit >15 tokens/s.

Les références des secrets sont conservées : policy=mode1 pour 1/3,
policy=mode2 pour 2/4, ancien policy=mode3 pour 5/6 et ancien policy=mode4
pour 7. Aucune migration de secret n'est nécessaire. Les états/mémoires
passent au schéma 3 : les succès anciens Go restent associés, l'ancien mode5
est réinitialisé, DeepSeek devient mode7 et le mode6 gratuit ne reprend aucun
apprentissage. La sélection est effacée lors de l'adaptation. Les fichiers
invalides ne sont pas écrasés. Le schéma 3 n'est pas lisible par l'ancien
évaluateur ; préserver une copie avant retour de version.

Les routes et fournisseurs de chaque section sont conservés. Les candidats
OpenCode Go utilisent la clé du compte associé au mode uniquement sur l'origine
HTTPS OpenCode validée, un User-Agent PLLM et une session stable. Une restriction
de client natif ou un refus de clé reste explicite ; le testeur ne fabrique pas
une identité native et ne crée pas de secret. La configuration OpenCode reste
inchangée. L'état historique accepte `opencode` pour les anciens 1/2 et les gratuits 3/4 ;
les candidats courants 1/2 restent exclusivement payants Go et 3/4 gratuits Go,
y compris lorsque les catalogues ou historiques contiennent opencode.

Les tests déterminent l'admissibilité des modes benchmarkés. Les payants Go 1/2 sont essayés par coût moyen croissant. Le mode5 sélectionne le payant OpenRouter admissible le moins cher au prix courant, sans génération. Les gratuits 3/4/6 sont parcourus dans l'ordre TFL de leur section et retiennent le premier succès. Le mode7 garde son unique candidat DeepSeek sans tarif inventé. Les forçages de rang conservent
leur cible, avec refus des gratuits en mode5 désormais exclusivement payant.
Le coût vérifié est conservé dans average_price_usd_per_million_tokens et les
prix/provenances dans model_source. Les moyennes décimales égales conservent
leur égalité sans artefact d'addition binaire ; un prix non vérifiable reste
exclu et aucun prix antérieur n'est hérité. Le contexte d'entrée ≥1M est une
capacité TFL vérifiée ; le test borné n'envoie pas un million de tokens.
Go comptent la sortie raisonnement+réponse ; OpenRouter/DeepSeek la
réponse seule. Le protocole 8 divise ce comptage par la durée complète non
arrondie de la requête, attente et TTFT inclus. Aucun premier token n'est
soustrait. Une réponse complète en un bloc reste mesurable ; les durées ou
comptages invalides rendent le débit indisponible. Les priorités restent fixes.
Les rapports exposent request_seconds, throughput_metric=request_average_v1,
throughput_window=request_total et measurement_protocol_version=8.
duration_seconds est un affichage arrondi ; generation_seconds reste la
fenêtre diagnostique entre fragments. Ces deux affichages ne servent pas de
dénominateur. Aucun plafond ou minimum de durée artificiel ne corrige la valeur.
La mémoire inclut ce profil dans l'identité : les anciennes réussites restent
historiques sans amorcer le nouveau protocole. Un nouveau succès de même
profil peut réutiliser son palier. Les anciens débits ne sont pas comparables ;
les seuils numériques conservés peuvent produire un autre classement et une
autre éligibilité.
Le JSON additif conserve catégorie, exclusions, candidats et tentatives, ainsi
que les quotas réels. La mémoire garde les succès par configuration ; un
palier d'un autre candidat n'est pas affiché. Les erreurs HTTP/SSE sont filtrées
et rendues dans État sans corps brut. active s'arrête silencieusement après
le premier succès du premier mode valide ; les forçages gardent un seul candidat.

Les benchmarks PLLM hors mode5 et les gratuits TFL demandent exclusivement Medium,
sans repli vers un autre effort. Chat Completions
utilise reasoning_effort ; Responses reasoning.effort ; Messages thinking
adaptive et output_config.effort ; DeepSeek thinking activé et reasoning_effort.
Les gratuits OpenRouter du mode6 exigent une déclaration vérifiable de Medium ; les payants OpenRouter du mode5 en sont exemptés. Aucun autre niveau n'est utilisé. Le niveau effectif est tracé et
participe à l'identité de mémoire ; une réussite mesurée avec un autre effort
n'amorce pas un test Medium. Un refus 400 propre à l'effort arrête le candidat ; 401/403/429
conservent leur traitement propre.
Les erreurs HTTP sont lues au plus sur 64 Kio, fermées et filtrées sans corps
brut, compte ou secret. Le diagnostic est réutilisable sans relire le corps.

scripts/performance.py embarque le même moteur dans les quatre distributions
PLLM/TFL : seuils, gratuité vérifiable, paramètres et mesure streaming. Les
plugins restent autonomes et leurs paquets isolés contiennent ce module.
Les dépendances réseau/horloge sont injectées dans le parseur pour les tests.
TFL teste tous les gratuits structurellement admissibles des deux catalogues,
sans appel de quota, crédit ou solde. Il utilise la clé Go de sa politique
pour Go et la clé OpenRouter existante (environnement, sinon trousseau
historique du mode 5). Les valeurs restent en mémoire et hors des sorties.
Les gratuits échoués sont retirés de models et conservés dans excluded_models
et free_performance_results avec critères, dates, niveaux et tentatives.
Les deux tableaux fournisseurs Go puis OpenRouter conservent huit colonnes ; un tableau
commun des essais gratuits est ajouté. Une section vide après qualification
est publiée avec son état et ses exclusions, sans bloquer les autres sections.
Le filtre dépend du compte
TFL utilisé : un autre compte peut avoir un accès différent, sans que PLLM
réintègre automatiquement un candidat exclu du catalogue.

Hors l'unique repli d'effort autorisé, HTTP 400 et HTTP 429 arrêtent les paliers de ce candidat, puis les autres
candidats autorisés continuent avec leurs contrôles. Retry-After accepte
secondes entières et dates HTTP avec fuseau ; une valeur inexploitable reste
indisponible. Le JSON conserve http_error, délai et échéance ; État affiche
le refus ou le réessai disponible en heure de Paris. Aucune attente jusqu'à
un quota journalier ni reprise planifiée n'est créée. Les troncatures et les
seuils mesurés continuent de permettre les paliers habituels, sans réduire le niveau requis.

La résolution du catalogue par PLLM accepte `--tfl-catalog CHEMIN` pour
OpenCode Go, les gratuits 3/4 et OpenRouter 5. Sans option, elle conserve
`../tfl/data/tfl.json` relatif au skill PLLM. Pour des plugins installés
séparément, fournir explicitement le catalogue produit par TFL. Les tests
hors ligne qualifient des emplacements séparés ; ils ne prouvent pas une
installation réelle dans Codex ni l'accès aux fournisseurs.

Les accès aux fournisseurs sont préparés localement, hors des sources. Aucune
information d'authentification, valeur de configuration sensible ou sortie de
stockage sécurisé ne doit être enregistrée dans les rapports, affichée ou
ajoutée aux sources. Le stockage privé standard d'une clé fournisseur par
OpenCode est permis hors du dépôt et hors de la lecture des agents, sauf
restriction explicite du développeur. Une interdiction de fermer ou redémarrer
son processus n'interdit pas ce chargement ni le rechargement interne de son
contexte, qui doit préserver l'interface et être suivi d'une réconciliation MCP
et CAB.

## Données générées

Les reçus et sauvegardes TCU restent dans les installations utilisateur,
hors des sources versionnées. Ils ne doivent jamais être ajoutés au dépôt.

Les scripts de `cgpt`, `pllm` et `tfl` peuvent générer ou actualiser des
rapports locaux. Les données liées aux quotas ou à l'historique d'utilisation
ne doivent jamais être ajoutées aux sources publiées. Les
catalogues fournisseurs et les rapports inclus dans un plugin doivent être
contrôlés avant publication : ils ne doivent contenir ni secret ni information
personnelle.

## Sécurité et exécution

Les extensions ne doivent contenir aucun secret, identifiant, jeton, clé ou
certificat. Les configurations requérant une donnée sensible doivent utiliser
un mécanisme externe au dépôt et documenter uniquement le nom de la variable
ou le prérequis attendu.

Les scripts embarqués doivent être compatibles avec les versions Debian prises
en charge. Les scripts Bash sont vérifiés au minimum avec `bash -n` et
`shellcheck` lorsqu'ils sont disponibles.

Les hooks et serveurs MCP déclarés par un plugin doivent limiter leurs accès
aux seules ressources nécessaires et gérer explicitement les erreurs.

## Validation

Lors du diagnostic du 10 octobre 2026, `src/` et `tests/` étaient vides.
Aucune suite de tests automatisés distincte des générateurs n'a été identifiée
dans ces répertoires, dans les scripts des skills ou dans `pyproject.toml`.
`test_fournisseur_llm.py` est le générateur TFL, pas une suite de tests.
La lecture des sources, les contrôles documentaires et la validation OpenSpec
ne prouvent ni le fonctionnement fournisseur ni l'installation des plugins.
La suite hors ligne actuelle comprend `tests/test_pllm_ttft.py`,
`tests/test_pllm_free_fallback.py`,
`tests/test_pllm_http_diagnostics.py`, `tests/test_pllm_six_modes.py`, `tests/test_pllm_price_priority.py`, `tests/test_free_performance.py`, `tests/test_throughput_measurement.py`,
`tests/test_extension_qualification.py`, `tests/test_tcu_update.py` et
`tests/test_prompt_dispatch.py`, exécutables avec
`python3 -B -m unittest discover -s tests -v`. Elle couvre les deux
distributions, le catalogue explicite, l'initialisation, la préservation d'un
historique corrompu et les remplacements après HTTP 429, les sept modes, leurs comptes, les
seuils stricts 3/4, les forçages et les migrations de schéma. Chaque remplaçant recalcule
ses paliers et exige ses propres mesures avant de devenir valide.
TFL exclut les prix OpenRouter non finis et les débordements, puis prépare
une sérialisation JSON stricte avant publication. Ces tests isolés ne
qualifient pas les services externes. La compatibilité Python est contrôlée
sur les branches 3.13 et 3.14 avec la suite applicable, la compilation de tous les
scripts et tests, leurs imports et la résolution du fuseau Europe/Paris.
Les résultats et versions exactes sont consignés dans le change et son
rapport d'archive ; aucune compatibilité avec une autre branche n'est déduite.

Les tarifs OpenCode Go sont collectés à chaque génération depuis les tableaux
officiels de `https://opencode.ai/docs/go/`, par HTMLParser et urllib de la
bibliothèque standard. L'unité par million, les montants courants, les
correspondances et les doublons Go/Go Plus sont vérifiés ; les anciens prix
barrés sont ignorés. Les variantes, prix de cache, source, date et empreinte
de la documentation restent dans `opencode_go.pricing_reference`. Le prix
de classement est le maximum des moyennes hors pointe entre les paliers de
contexte disponibles. Les estimations de requêtes non collectées sont `null`
avec un statut N/A ; aucun historique tarifaire ou d'estimation n'est repris.

Les modalités Go sont collectées dans les déclarations API et dans
`modalities.input/output` de models.dev, sans liste de modèles connus. Les
déclarations concordantes utilisent la provenance API lorsqu'elle existe ;
des déclarations contradictoires bloquent la publication. Une absence reste
non vérifiée. Les sources et dates sont conservées dans `modalities_metadata`.
Les filtres de sortie s'appliquent aux modalités ainsi récupérées.

Le transport Go utilise une route API explicitement publiée ou les champs
`npm`/`api` de models.dev, avec surcharge du modèle sur le fournisseur. Les
contrats génériques reconnus sont openai-compatible → chat_completions,
openai → responses (fabrique par défaut) et anthropic → messages. Aucun nom
ni famille de modèle ne détermine le protocole ou l'endpoint. Un modèle non
documenté, un SDK inconnu ou une base absente restent signalés sans repli.
HTTPS, origine OpenCode, port HTTPS, absence d'identifiants utilisateur,
query et fragment sont vérifiés avant publication des URL. Une URL non sûre
ou une route explicite contradictoire avec son protocole bloque la génération.
Les champs consommés par PLLM restent présents ; `routing_metadata` conserve
source, date, SDK, portée des surcharges et référence du contrat de protocole.
`routing_status=documented` et `generation_tested=false` distinguent la preuve
documentaire d'un appel réel. `tests/test_tfl_go_metadata.py` couvre ces cas
sur les deux distributions et vérifie la lecture des métadonnées par PLLM,
sans quota ni benchmark.

TFL collecte exclusivement Go et OpenRouter. Les collecteurs historiques
OpenCode général ne sont plus appelés ; aucun modèle général, investigation,
essai ou section opencode n'est publié. models.dev reste la source des seules
métadonnées opencode-go utilisées pour Go. Les helpers de lecture historiques
restent isolés et ne participent pas au parcours main.
PLLM ne consomme que opencode_go pour les modes 1 à 4 : payants en 1/2,
gratuits en 3/4. Une ancienne section opencode, même admissible, malformée ou
seule disponible, n'est jamais un repli ; les rangs forcés restent bornés à Go.
Les tests test_tfl_opencode_catalog.py et test_pllm_six_modes.py couvrent la
publication à deux sections et l'absence d'appels généraux, y compris anciens
résultats sélectionnés. Les sections Go/OpenRouter valides mais vides restent
publiables avec leur état et leurs exclusions. Les seuils restent conservés.

OpenRouter conserve la collecte `pricing.prompt/completion` et le classement
sur les prix API de base, avec conversion par million. Les caches et les
paliers `overrides` sont conservés dans `pricing_details`, y compris les
conditions de contexte et les jours/horaires UTC publiés. Aucun seuil de
contexte n'est inventé pour une variante temporelle. La requête modèles
interroge tout le catalogue sans filtre de catégorie, modalité ni limite
artificielle de nombre. La sélection est dynamique, sans liste d'identifiants :
contexte ≥1M, moyenne API de base ≤0,20 EUR/M au taux BCE vérifié, modalités
de sortie et blacklist. Medium s'applique aux gratuits OpenRouter benchmarkés, pas aux payants du mode5. Les prix négatifs, non finis ou débordants
sont non exploitables. La provenance tarifaire des deux fournisseurs est
horodatée. Une source indispensable invalide ou des tarifs Go contradictoires
font échouer la génération avant publication ; les rapports existants restent
intacts. Aucun repli statique ou historique n'existe. Une correspondance
tarifaire absente exclut le modèle avec son motif ; une route de génération
Go inconnue est signalée sans protocole déduit. `tests/test_tfl_pricing.py`
couvre ces comportements sur les deux distributions, hors réseau et trousseau.
Cette suite couvre aussi l'arrivée et la disparition de modèles, les prix
gratuits et les bornes, l'audit des exclusions et un catalogue de plus de
1 000 modèles. Le JSON désigne cette sélection par
`live-api-context-cost-modalities`. L'absence d'un ancien modèle n'est plus
bloquante ; l'absence de tout résultat admissible est publiée explicitement
avec ses exclusions et ne bloque plus les autres catalogues.

Avant publication, chaque plugin doit être vérifié dans une nouvelle session
Codex après son installation depuis la marketplace. La validation couvre au
minimum le chargement du manifeste, la disponibilité des skills ou outils
déclarés et l'absence de dépendance ou de donnée sensible non documentée.

Les skills autonomes sont validés avec leur `SKILL.md` et leurs ressources
nécessaires. Pour `cm`, le format des deux skills, leur parité, le lien de
découverte, le catalogue et la résolution du paquet copié isolément sont
contrôlés localement. Une invocation effective de `$cm` dans une nouvelle
session Codex est une preuve distincte ; la résolution du lien seule ne la
démontre pas. Les scripts Python sont vérifiés au minimum par compilation sans
écriture d'artefact ; les fichiers JSON sont analysés avant publication.

Les formats de manifeste, de catalogue et les règles de distribution suivent
la [documentation officielle OpenAI sur les plugins](https://developers.openai.com/plugins/build/plugins).

## Mise à jour TCU

Le script utilise la bibliothèque standard Python. Sans option ou avec
`check` (alias compatible `--check`), il lit les versions et un instantané GitHub identifié par SHA sans
écriture. Le skill transforme une demande explicite sans option en `--apply`.
Les réponses et archives sont bornées ; chemins, release et sources Python
sont vérifiés sans exécuter le code téléchargé. `data/` est exclu des sources
autonomes à remplacer.

Les racines par défaut sont CODEX_HOME/skills, ~/.agents/skills,
CODEX_HOME/prompts et CODEX_HOME/commands, avec ~/.codex par défaut pour
CODEX_HOME. `--skills-dir` et `--commands-dir` désignent des racines explicites.
Seul prompt absent peut être installé via le CLI après validation de la
source et du catalogue. Le manifeste, le skill et le résolveur installés sont
vérifiés contre l’instantané GitHub. Un cache incomplet peut être réparé via
le CLI ; aucun wrapper n’est écrit si cette vérification échoue. Les autres
plugins absents et skills autonomes absents ne sont pas créés.

Le wrapper issu de `.codex/commands/PROMPT.md` est déployé par défaut dans
CODEX_HOME/prompts/PROMPT.md, ou dans le premier --commands-dir explicite.
TCU accepte encore la source prompt.md d'une release antérieure si la source
canonique manque. Une copie prompt.md existante reste mise à jour sous son
nom actuel, sans doublon créé ni renommage. Si les deux graphies existent,
elles sont vérifiées dans le même plan. Son reçu dédié
`.tools-codex-prompt-origin.json` peut reprendre une preuve du reçu partagé
sans l’écraser. Les plans génériques ignorent les deux graphies de PROMPT.
Pour les autres commandes, une source canonique actualise également les
copies historiques en minuscules présentes, avec leurs reçus et sans créer
les commandes absentes. Le wrapper
délègue au skill sans copier le référentiel métier désigné dans DEVOPS.md.
Liens et checkouts de développement restent en conflit sans modification ;
aucun git pull ni redémarrage de service.

Le reçu `.tools-codex-origin.json` suit dépôt, SHA, release et empreintes. Une
copie différente sans reçu exige `--adopt`, jamais ajouté implicitement. Une
source suivie modifiée reste en conflit avec ou sans adoption. Les fichiers
retirés en amont sont conservés. Ni jeton ni configuration de connexion ne
sont chargés. Les sauvegardes restent sous CODEX_HOME/tcu-backups, sans purge,
dans un répertoire par exécution accessible au seul utilisateur (mode 0700).

Le verrou CODEX_HOME/tcu.lock exclut deux applications simultanées. Les données
JSON/Markdown des plugins sont sauvegardées avant le CLI puis restituées dans
le cache vérifié ; une autre donnée bloque le rafraîchissement. Versions et
activation sont relues après l'opération. Une divergence avec la release
GitHub bloque les sources autonomes. Le code du cache reste géré par Codex.

Chaque remplacement autonome est atomique ; une erreur restaure les sources
déjà remplacées et conserve la sauvegarde. Le cycle CLI n'est pas une
transaction commune : succès partiels et états inconnus sont rapportés sans
promesse d'annulation globale. Le bilan distingue cible et version observée,
avec trois lignes distinctes pour le plugin, le skill embarqué et la commande
prompt, et un code non nul sur conflit ou échec. Un conflit local ne bloque
pas les canaux indépendants ni les plans locaux valides. Une erreur de
source, de sauvegarde ou de cohérence CLI bloque les opérations non sûres.
La suite TCU simule réseau et CLI et
utilise des profils temporaires sous tests ; elle ne qualifie pas une mise à
jour du profil réel ni une publication GitHub.

## Résolution et lancement de prompts

Le résolveur Python lit uniquement DEVOPS.md dans la racine de projet fournie
par `--project-root`. Le skill relève cette racine dans le contexte de la tâche
avant de lancer le script, indépendamment de son installation. Les chemins
relatifs déclarés sont résolus depuis ce projet. Il n'existe pas de recherche
de repli dans le répertoire parent ou les dossiers globaux de Codex.

Les deux déclarations Dossier des prompts et Index des prompts sont uniques.
La table Sigle/Prompt/Fichier de l'index constitue le catalogue. Ses chemins
sont relatifs au dossier déclaré et restent dans celui-ci après résolution
des liens. Les liens déclarés et internes peuvent être lus sans être modifiés.
Doublon, déclaration ambiguë, sortie de dossier ou source invalide produisent
une erreur explicite. Les textes sont bornés à 1 Mio et lus en UTF-8.

LIST retourne les entrées et disponibilités sans lire les corps. Une action
retourne un état `ready`, le texte complet, le chemin et l'instruction à suivre.
Le résolveur n'exécute pas ce texte : le skill le lit intégralement puis conduit
son processus. Une résolution réussie ne vaut pas preuve de fin de RUN.

Les 38 actions sont en MAJUSCULE. GCM et GCMP sélectionnent les entrées GSCM et
GSCMP de l'index. CISMPn et 1CISMPn, pour n de 1 à 8, conservent exactement
le RUN CISMPn. Les variantes préfixées 1 portent `max_changes=1` et l'ordre
change complet, archivage, statistiques, arrêt de la session de codage. Cette
directive borne la boucle de sélection après le premier change sans supprimer
les validations, clôtures ou conditions imposant une décision. Le bilan ne
prétend pas terminer tous les changes du dépôt.

La suite `test_prompt_dispatch.py` utilise des projets et référentiels
temporaires. Elle couvre les 38 correspondances, l'isolation des projets,
les variantes de RUN, LIST, les liens lus sans modification et les erreurs.
Les paquets isolés et LIST réel sont contrôlés séparément ; aucun RUN piloté
ou prompt à effets réels n'est lancé pendant cette qualification.

## Liste noire LM

LM fournit un skill autonome et embarqué, le même module model_blacklist.py
que TFL/PLLM, la commande source .codex/commands/LM.md et la découverte
.agents/skills/lm -> ../../skills/lm. CM présente LM avec LIST, ADD et REMOVE.
Le nom d'affichage est LM ; aucune slash native n'est automatiquement créée.

Le fichier commun CODEX_HOME/lm/blacklist.json (repli ~/.codex) porte
schema_version=1 et models, liste d'identifiants canoniques uniques.
Sans fichier, mimo-v2.5 et muse-spark-1.2-contributor sont exclus en mémoire,
sans écriture ; une liste vide
valide reste vide. LIST ne modifie rien. ADD/REMOVE utilisent un verrou
fcntl non bloquant et un remplacement atomique en UTF-8/LF. Les identifiants
ASCII sont bornés à 256 caractères ; la casse, le préfixe fournisseur et
les seuls suffixes :free/-free sont normalisés. Pas de rapprochement par
sous-chaîne : mimo-v2.5-pro et mimo-v2.50 restent distincts.
Un unique `~` initial est accepté devant un segment fournisseur valide suivi
de `/`, comme `~unbiased/pareto-latest`. Il disparaît avec le préfixe lors de
la canonicalisation : `~xiaomi/mimo-v2.5:free` reste exclu. La limite de 256
caractères inclut ce marqueur ; `~model`, `~~vendor/model` et `vendor/~model`
restent invalides. Les noms finaux différents restent des identités distinctes.
Une politique illisible, dupliquée ou de schéma invalide bloque avant appel
fournisseur et reste préservée. LM est l'unique liste noire ; toutes les
entrées, y compris muse-spark, sont retirables. Le module est identique dans
les six distributions LM/TFL/PLLM, sans dépendance entre plugins installés.

TFL retire les interdits avant tri et tests gratuits dans ses deux sections,
avec cause dans excluded_models et politique dans lm_blacklist.
PLLM filtre aussi ses sélecteurs, replis, mode6 et frontières de génération,
y compris un catalogue ancien ou un succès mémorisé. Les forçages interdits
restent invalides sans remplacement ; les historiques interdits sont invalidés
avant publication et absents des listes de candidats. La mémoire historique
n'est pas détruite. LM ne réécrit pas les anciens rapports : l'effet concerne
les prochaines invocations. Les priorités, ressources, seuils et protocole 8
restent inchangés.

TCU découvre LM via le catalogue et actualise ses copies présentes sans
installer LM absent. Le fichier utilisateur hors cache reste préservé.
Les tests test_lm_blacklist.py et les cas TCU utilisent des profils isolés,
sans accès fournisseur ni installation réelle. Un retour vers 0.7.5 ignore
la politique LM et ne conserve donc pas sa garantie d'exclusion.

## Planning utilisateur TFL puis PLLM

Chaque plugin déclare `hooks: ./hooks/hooks.json`. Son SessionStart lance
`python3 "${PLUGIN_ROOT}/skills/<nom>/scripts/scheduler.py" install --hook`,
en arrière-plan, avec délai de 60 s. Les six modules autonomes et leurs six
copies embarquées sont identiques et sans effet à l'import. La confiance du
hook est une décision native Codex, jamais ajoutée ou contournée par le code.
Un bootstrap concurrent déjà occupé reste silencieux ; les autres erreurs
conservent un diagnostic filtré. Aucun modèle n'est appelé à l'installation.

TCU valide les déclarations et ressources des hooks dans l'instantané, sans
exécuter le code téléchargé. `--apply` utilise son module local chargé pour
le bootstrap ; `check` décrit seulement l'opération. Le bilan ajoute
`llm-refresh`, canal `session_utilisateur`, sans version de plugin inventée.
Des composants manquants restent en attente sans installation implicite.
Un conflit local sur TFL ou PLLM préserve aussi le planning sans l'armer.
Une erreur du planning produit un échec visible, même après une mise à jour
de sources réussie. Le CLI continue à gérer lui-même le cache des plugins.

Le timer `tools-codex-llm-refresh.timer` et son service sont dans
`XDG_CONFIG_HOME/systemd/user` (repli `~/.config/systemd/user`). Le calendrier
est `*-*-* 00,12:00:00 Europe/Paris`, `Persistent=false`, précision 1 s.
Le runner stable, sa configuration, son reçu et son état sont conservés sous
`CODEX_HOME/llm-refresh`. Les fichiers cibles ne sont remplacés que si leur
empreinte correspond au reçu ; les liens et propriétaires étrangers sont
refusés. Le retrait explicite ne touche que les fichiers reconnus et conserve
les rapports. Les erreurs d'installation restaurent les fichiers précédents,
sans promettre une transaction globale avec systemd.

À chaque échéance : détecter l'application ou un CLI interactif Codex du même
UID, lire le bucket `codex`, exécuter TFL, vérifier son nouveau catalogue,
relire présence et quota, puis lancer PLLM normal avec `--tfl-catalog`.
L'interface unifiée ChatGPT est reconnue seulement avec son backend Codex
enfant vivant ; l'application générique seule ne prouve pas Codex ouvert.
Les daemons, `codex exec`, helpers Electron et autres utilisateurs ne prouvent
pas cette présence. Le runner ne démarre pas Codex et ne rattrape pas les
passages manqués. Un verrou exclusif interdit deux séquences ; un verrou
partagé `tcu.lock` empêche une application TCU pendant les deux étapes.

Le quota est lu avec un client JSONL dédié : `initialize`, `initialized`, puis
`account/rateLimits/read` sur `codex app-server --stdio`. Aucun appel de
conversation, génération, connexion, achat ou réinitialisation n'est effectué.
Le processus natif accède à ses propres identifiants ; le runner ne lit pas
leur stockage. `rateLimitsByLimitId.codex` prime sur la vue historique ;
Spark et les observations anciennes ne le remplacent pas. Une fenêtre à
100 % utilisés ou plus bloque ; une fenêtre non exploitable produit un état
inconnu et bloque aussi. Le processus de lecture est borné à 30 s et 1 Mio.

Les étapes TFL et PLLM sont bornées à 3 600 s chacune, avec un budget service
de 7 500 s. Leurs sorties brutes ne vont pas au journal ; les rapports usuels
restent produits par leurs générateurs. `state.json` conserve seulement
statut, date, étape et code/diagnostic fixe. Un catalogue absent, invalide ou
non actualisé empêche PLLM. Les modes, seuils, paliers, transports et LM
manuels restent inchangés. Les tests `test_llm_schedule.py` isolent profils,
processus et fournisseurs et vérifient les unités avec les outils systemd.

Références officielles : [paquets et hooks](https://developers.openai.com/plugins/build/plugins),
[cycle des hooks](https://learn.chatgpt.com/docs/hooks),
[lecture des quotas](https://learn.chatgpt.com/docs/app-server).


## Admission stricte Medium

Tout candidat benchmarké doit publier une capacité Medium vérifiable avant test, sélection et affichage. Le mode5 payant OpenRouter n’exige pas Medium. Une liste supported_efforts contenant
medium ou un null explicitement publié (tous les efforts) est admissible. Une
clé absente, une valeur invalide, un booléen reasoning, une liste sans medium
ou un budget seul ne suffit pas. Aucun autre effort n'est autorisé.
Les niveaux publiés par models.dev dans `reasoning_options`, entrée
`type=effort` et liste `values`, sont normalisés vers `supported_efforts`.
Une liste vide, un budget, un interrupteur ou une déclaration ambiguë ne
prouve aucun niveau ; `values=null` ne signifie pas tous les efforts.
Une acceptation officielle de Medium reste admissible même sans intensité
distincte. Une équivalence documentée peut utiliser thinking.type=enabled
sur Chat Completions OpenCode, avec protocole et sémantique tracés. Une preuve
historique qui ne couvre pas Medium seule n'établit pas sa prise en charge.
Les exclus restent dans les audits JSON, sans apparaître dans les tableaux.
Les anciens catalogues, historiques et rangs forcés ne contournent pas ce
filtre ; DeepSeek direct exige aussi une preuve. Une section TFL vide est
publiée explicitement sans réintégrer de modèle exclu.


## Contrat TFL/PLLM 0.7.14 et conversion OpenRouter

TFL ne collecte ni ne publie plus OpenCode général. Le JSON contient seulement
opencode_go et openrouter. PLLM 1/2 sélectionne les payants Go, 3/4 les gratuits Go, 5 les payants OpenRouter sans benchmark, 6 les gratuits OpenRouter benchmarkés et 7 DeepSeek direct, même si un ancien catalogue ou historique contient opencode.
Le rapport affiche Go en USD/M puis OpenRouter en EUR/M, huit colonnes chacun,
puis les essais gratuits ayant une preuve Medium. Aucun modèle exclu
pour son effort ne figure dans les tableaux ; les motifs restent dans le JSON.
Le moteur commun collecte le dernier taux BCE USD par EUR publié depuis
https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml. EUR = USD / taux ;
le plafond OpenRouter est 0,20 EUR/M inclus avant arrondi. Le JSON conserve
prix USD/EUR, source, date du cours et date de récupération. TFL bloque avant
publication si le cours est invérifiable ; PLLM refait le contrôle à la sélection, y compris pour les anciens catalogues et les rangs forcés ; mode5 ne génère pas. Un budget seul n’équivaut plus à Medium.
Go garde 0,50 USD/M. Les capacités absentes peuvent vider une
section sans bloquer les autres collectes ni la publication. Chaque section
conserve models, compteurs, sources et exclusions, avec selection_status
(available ou empty) et exclusion_summary (motif vers nombre). Les tableaux
vides gardent huit colonnes, annoncent « Aucun modèle admissible » et donnent
la synthèse des exclusions, sans ligne de modèle fictive. Le taux BCE daté
reste affiché même si OpenRouter est vide. Deux sélections vides issues de
collectes valides produisent des fichiers frais et un code zéro ; aucune
qualification historique n'est reprise. Les erreurs réelles restent bloquantes.
Le planning conserve ses horaires et gardes ; son contrôle exige les deux
listes models Go/OpenRouter non vides avant PLLM, sans exiger opencode. Les tests de cette release sont hors ligne, sans mise à jour
de profil, activation du planning ni benchmark réel.

## Investigation des métadonnées

model_evidence.py est identique dans les quatre paquets TFL/PLLM. Le guide
references/model-evidence.md définit la recherche obligatoire du LLM lorsque
le contexte ou l'effort est invérifiable pour Go ou
OpenRouter. Le registre de référence TFL est complété par
<répertoire-du-rapport>/model-evidence.json : fournisseur, ID exact, champ,
protocole, conclusion, sources officielles HTTPS, dates et empreintes SHA-256.
Les preuves ne sont pas empruntées entre fournisseurs ou transports.
TFL vérifie le contenu courant des sources avant admission ; PLLM le
recontrôle à la frontière de génération. Une source différente ou inaccessible
exige une nouvelle investigation ; le hash ne prouve pas l'interprétation
sémantique du LLM. Une preuve documentaire ne vaut ni génération ni benchmark.
Le JSON conserve model_investigations et investigation_status. Un statut
required laisse le rapport provisoire et exige l'analyse de l'agent avant
restitution définitive ou un blocage explicite. Une investigation complète
sans contexte vérifiable exclut le modèle, sans inventer de limite.
tests/test_model_evidence.py couvre les deux catalogues, les conclusions,
les sources changées, le mapping MiMo et le recontrôle PLLM ; les scénarios
de déploiement isolé incluent désormais ce module dans chaque paquet.

Le registre PLLM de référence peut aussi contenir le fournisseur `deepseek`
pour l'identifiant direct du mode7. Une preuve `unsupported` est conservée
dans les exclusions et sa conclusion apparaît dans la cause de la politique ;
elle empêche le benchmark. Un alias demandé Medium mais appliqué en High
reste invalide. Le récupérateur suit uniquement les redirections HTTPS de
même origine ; toute redirection de confiance différente est refusée.
