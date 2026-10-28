# BUILD.md — Tools Codex

## Distribution des plugins

Les plugins de Tools Codex sont publiés via la marketplace GitHub suivante :

```text
https://github.com/AzenorPixs/tools-codex
```

La marketplace doit exposer un catalogue de plugins valide avant d'être
ajoutée dans Codex. Chaque plugin référencé par ce catalogue est stocké dans
`plugins/<NOM_DU_PLUGIN>/` à la racine du dépôt.

Le catalogue `.agents/plugins/marketplace.json` référence les plugins publiés
par cette marketplace. Toute évolution de la liste des plugins doit mettre à
jour ce catalogue et préserver des chemins relatifs à la racine du dépôt.

Les plugins destinés à la marketplace sont actuellement :

| Plugin | Skill embarqué | Fonction |
|---|---|---|
| `lm` | `lm` | Liste noire partagée des modèles exclus de TFL et PLLM. |
| **PROMPT** (`prompt`) | **PROMPT** (`prompt`) | Liste et lancement des prompts définis par le DEVOPS du projet. |
| `cm` | `cm` | Catalogue des commandes maison et de leurs syntaxes. |
| `tcu` | `tcu` | Mise à jour vérifiée des briques déjà installées. |
| `pllm` | `pllm` | Évaluation et application contrôlée d'une politique LLM. |
| `tfl` | `tfl` | Rapport OpenCode Go puis OpenRouter uniquement. |

Les commandes de `.codex/commands/` et les skills autonomes de `skills/` sont
des sources du dépôt. Leur mise à disposition ne résulte pas, à elle seule, de
l'installation d'un plugin depuis la marketplace ; elle doit suivre le mode de
distribution Codex approprié à ces ressources.

Les six commandes sources sont CM.md, PLLM.md, TFL.md, TCU.md, LM.md et
PROMPT.md, avec déclencheurs canoniques en majuscules. Les identifiants
techniques des plugins et skills restent en minuscules ; les anciens
déclencheurs restent des alias. Un lien personnel vers un ancien fichier
source en minuscules doit être réorienté vers le nouveau chemin lors de la
migration de cette installation ; la livraison des sources ne modifie pas
automatiquement ce profil.

## Skill catalogue cm

Le skill `cm` reconnaît `$cm` et `/CM`. Le wrapper `.codex/commands/CM.md`
délègue au même catalogue sans lancer les actions listées. Dans ce projet, la source
`skills/cm/SKILL.md` est exposée par le lien relatif
`.agents/skills/cm -> ../../skills/cm`. Utilisez `$cm` dans Codex pour afficher
les invocations maison et leurs syntaxes. La consultation du catalogue ne
lance ni PLLM, ni TFL, ni TCU, ni prompt et ne vérifie pas leur installation.

Le plugin `cm` embarque une copie identique dans
`plugins/cm/skills/cm/SKILL.md`. Une fois cette source disponible dans la
marketplace configurée, installez le catalogue avec :

```bash
codex plugin add cm@tools-codex
```

Cette commande installe le skill embarqué ; elle ne copie pas le dossier
autonome du dépôt. Le plugin ne requiert aucune connexion ni service externe.

Pour utiliser le catalogue dans un autre projet, copiez le dossier `skills/cm/`
dans `.agents/skills/cm/` de ce projet. Pour un usage personnel partagé entre
projets, installez ce dossier dans `~/.agents/skills/cm/`. Conservez son
`SKILL.md` ; une copie doit être actualisée depuis la source lors des mises à
jour. Ces installations hors du dépôt sont des actions distinctes.

Choisissez une distribution adaptée à votre usage : le chargement simultané
du plugin et du skill autonome peut afficher deux entrées CM. L'ajout du
plugin au catalogue conserve le skill autonome et le lien local ; aucune
installation existante n'est supprimée ou désactivée automatiquement.

Codex détecte les modifications de skills. Si `cm` n'apparaît pas, démarrez
une nouvelle session ou redémarrez Codex. Vérifiez alors que `$cm` affiche le
tableau français avec CM, PLLM, TFL, TCU, LM et PROMPT dans `Commande`, sous forme
de références aux skills disponibles, et leurs syntaxes `$…` dans `Utilisation`,
sans lancer les actions listées. Le
contrôle local du lien ne remplace pas ce test effectif de découverte.

L'installation de PLLM ou TFL depuis la marketplace n'installe pas `cm`.
Les commandes sources restantes dans `.codex/commands/` n'enregistrent pas
automatiquement des commandes slash natives. Le mécanisme de skills et les
emplacements de découverte sont décrits dans la
[documentation officielle](https://learn.chatgpt.com/docs/build-skills).

## Installation

Pour PLLM, la release du paquet ne détermine pas la fraîcheur des données TFL.
Avant une évaluation manuelle, identifier la collecte réellement produite et
transmettre son chemin avec --tfl-catalog si les distributions sont séparées.
La mise à jour des scripts ne synchronise pas les catalogues utilisateur.
Le JSON publié indique source, date et compteurs ; une sélection gratuite vide
doit être interprétée selon cette source. Un HTTP 401 au quota nécessite de
vérifier l'accès du compte correspondant hors des rapports ; ne pas remplacer
automatiquement sa clé ou emprunter celle d'un autre compte. Aucun nouveau
planning ni changement OpenCode n'est requis par ce correctif.

Le plugin `prompt` s'installe, une fois sa version disponible dans la
marketplace configurée, avec `codex plugin add prompt@tools-codex`. Le skill
autonome `skills/prompt/` conserve le même résolveur. Dans ce projet, le lien
`.agents/skills/prompt` pointe vers cette source. Choisir une distribution
adaptée évite deux entrées du même skill dans le sélecteur.

Ajoutez la marketplace à Codex avec la commande suivante :

```bash
codex plugin marketplace add AzenorPixs/tools-codex
```

Vérifiez que la marketplace est enregistrée :

```bash
codex plugin marketplace list
```

Dans Codex CLI, ouvrez ensuite l'explorateur de plugins avec `/plugins`,
sélectionnez la marketplace Tools Codex et installez le plugin souhaité.
Démarrez une nouvelle session Codex avant d'utiliser les skills ou les outils
fournis par le plugin.

## Prérequis avant installation et test

Avant d'installer et d'exécuter un plugin, assurez-vous que l'environnement
dispose de Python 3.13 ou 3.14, d'un accès HTTPS sortant et, pour `pllm` et `tfl`, de la
configuration locale nécessaire aux accès autorisés par l'utilisateur.
Ces deux composants utilisent `secret-tool` et nécessitent un accès au
trousseau de l'hôte. Leur présence et cet accès doivent être vérifiés dans
l'environnement réel ; aucune installation de dépendance n'est implicite.
La plage déclarée est `>=3.13,<3.15`, conformément à `pyproject.toml` et
`TECHNICAL.md`. La métadonnée Python reprend la release de `VERSION` ; elle
n'ajoute ni procédure de packaging ni publication d'un paquet Python.

Installez `tfl` avec `pllm` : PLLM lit le catalogue produit par TFL. Les deux
plugins écrivent des rapports dans leur répertoire `data/`. TFL accepte
`--output-dir` ; PLLM exige son propre répertoire inscriptible et un catalogue
TFL accessible. Si le fichier courant PLLM manque, les sept politiques sont
initialisées automatiquement, sans reprendre de résultats historiques.
Pour des plugins séparés, lancer depuis le skill PLLM :

```bash
python3 scripts/evaluate.py --tfl-catalog /chemin/vers/le/catalogue/tfl.json
```

Cette option accepte le fichier produit par TFL, y compris avec `--output-dir`.
Sans option, PLLM conserve le chemin voisin `../tfl/data/tfl.json`.
Ce catalogue fournit les payants Go pour 1/2, les gratuits Go pour 3/4, les payants OpenRouter pour 5, les gratuits OpenRouter pour 6 et DeepSeek direct pour 7.
Les modes 1/2 épuisés deviennent rouges et invalides sans essai gratuit.
Les modes gratuits 3/4/6 ne consultent aucun quota ou solde ; ils exigent
contexte ≥1M, Medium, réponse complète, TTFT <30 s et débit >20 tokens/s.
Le mode5 exige un crédit OpenRouter positif, contexte ≥1M et coût moyen
≤0,10 EUR/M ; aucun benchmark ni effort Medium n'est requis. Le mode7 conserve
le contrôle DeepSeek et les seuils payants. Les références de trousseau restent
historiques, sans création ni migration de clé.
Les historiques des schémas 1/2 sont adaptés au schéma 3 : l'ancien mode5 est réinitialisé, DeepSeek passe au mode7, le mode6 gratuit est neuf et aucune sélection courante n'est héritée. Les succès OpenRouter antérieurs ne sont pas
transférés au mode5 ; la mémoire DeepSeek est déplacée au mode7. Un ancien
évaluateur ne lit pas le schéma3 : sauvegarder ses données avant retour.

PLLM récupère une mémoire sans `schema_version` uniquement si elle contient
`policies` vide ou le seul `mode7` DeepSeek Medium avec identité, profil de
débit du protocole 8 et succès cohérents. Le chargement conserve le fichier
intact ; le prochain succès publie atomiquement le schéma 3. Les mémoires
ambiguës ou corrompues restent refusées et préservées. L'écriture valide et
normalise sa mémoire avant publication pour garantir sa relecture.

Aucun historique invalide n'est écrasé. Les payants Go 1/2 sont essayés par
coût moyen croissant. Mode5 sélectionne le payant OpenRouter admissible le
moins cher au taux BCE courant, sans génération. Les gratuits 3/4/6 sont
essayés dans l'ordre TFL de leur section et arrêtent au premier succès benchmarké.
Après un échec, essayer le suivant admissible avec ses propres contrôles ;
une erreur bloquante d'authentification ou de ressources arrête le mode.
Le contexte ≥1M est une capacité d'entrée vérifiée, sans requête d'un million
de tokens. Les seuils des benchmarks sont préservés ; Medium est exigé pour tous les modes mesurés, mais pas le mode5. L'invocation normale poursuit les sept politiques ; active s'arrête à la première valide. Les rangs forcés restent ciblés : les rangs 51–53 visent les payants OpenRouter, 61–63 les gratuits OpenRouter et 7 DeepSeek. Les priorités 1 à 7 sont fixes. Les restrictions
fournisseur restent applicables aux gratuits ; les tests hors ligne ne prouvent pas l'accès réel.
Les diagnostics HTTP 400/429 et le Retry-After disponible figurent dans les
rapports PLLM sans corps d'erreur brut. Les refus HTTP 400/429 n'entraînent plus d'essais aux
budgets supérieurs ; une limitation conserve ses contraintes fournisseur.
Un alias Medium mappé par le fournisseur vers High reste invalide ; le
diagnostic exact et la preuve d'exclusion restent dans le JSON. Le mode7
recontrôle son registre DeepSeek avant toute génération.
Les champs JSON de diagnostic restent conservés ; l'adaptation des historiques
PLLM est automatique et ne nécessite aucun nouveau secret.
Les tests hors ligne couvrent des emplacements isolés ; un test réel
d'installation dans une nouvelle session Codex reste à effectuer avant
publication, conformément à `TECHNICAL.md`.

TFL doit être exécuté hors sandbox pour accéder à ses fournisseurs. Si un accès
OpenRouter est nécessaire, préparez-le localement sans jamais ajouter
d'information d'authentification au dépôt ou à la configuration de la
marketplace.

TFL nécessite également l'accès HTTPS à la documentation tarifaire officielle
OpenCode Go : ses tableaux sont relus à chaque exécution. Une page inaccessible,
une unité ou un format non reconnu, ou des prix contradictoires bloquent la
collecte avant publication, sans repli sur un catalogue ancien. Le JSON trace
la provenance, la date et les variantes tarifaires Go et OpenRouter. Les
estimations Go non collectées restent N/A. Ces changements n'ajoutent aucune
dépendance Python ni étape d'installation. Le script et le SKILL.md autonome
et embarqué doivent rester identiques ; une modification des sources ne met
pas à jour les copies déjà installées dans le profil Codex.
La sélection OpenRouter lit désormais tout le catalogue API et applique les
filtres localement, sans liste prédéfinie d'identifiants ni catégorie imposée.
Les modèles gratuits vérifiables sont admissibles aux mêmes conditions de
contexte et de sortie. Un changement du catalogue ou des tarifs peut donc
modifier les modèles retenus sans nouvelle release du générateur.
models.dev fournit aussi les modalités et le transport Go courant, avec
surcharges SDK/base API par modèle. TFL ne contient aucune liste de modèles
pour ces résolutions. Une information inconnue reste signalée ; une
contradiction ou une URL non sûre bloque la publication. La route documentée
n'est pas une qualification de génération. Les tests de compatibilité avec
PLLM ne lancent ni quotas ni benchmarks ; aucune dépendance SDK n'est installée.
TFL ne collecte ni ne teste plus OpenCode général. Le JSON ne publie que
opencode_go et openrouter et le rapport affiche leurs deux tableaux, huit
colonnes chacun, puis les essais gratuits. Contexte ≥1M reste obligatoire ; Go ≤0,50 USD/M et OpenRouter ≤0,10 EUR/M au taux BCE vérifié. Medium est requis pour les candidats benchmarkés et gratuits, pas pour les payants OpenRouter du mode5.
PLLM ignore les anciennes sections opencode pour tous les modes 1 à 4,
y compris leurs rangs forcés. Les erreurs de sources indispensables restent bloquantes.

Les skills `cgpt` et `coding-session-statistics` requièrent respectivement
l'outil Codex de lecture des quotas et l'historique persistant de la session.
Ils ne sont pas installés automatiquement avec les plugins de la marketplace.

## Utilisation de PROMPT

Le seul référentiel est le dossier et l'index indiqués par le DEVOPS.md du
projet courant. Les sources restent externes au plugin et ne sont pas copiées.
Les arguments sont en MAJUSCULE ; ils ne comportent pas de tirets :

```text
/PROMPT LIST
/PROMPT CISMP3
/PROMPT 1CISMP3
```

Les mêmes actions sont disponibles avec `$prompt LIST`, `$prompt CISMP3` et
`$prompt 1CISMP3`. `/PROMPT` est une commande source et un déclencheur du skill,
sans enregistrement automatique d'une slash native.

| Arguments | Source et effet |
|---|---|
| LIST | Affiche la table réelle de l'index, sans lire les corps ni lancer un prompt. |
| ACSP, ACSM, ACSMP, CGP, CISM | Charge le fichier du même nom et exécute son processus. |
| DOP, DOPP, EDP, ISM, ISMP | Charge le fichier du même nom et exécute son processus. |
| GCM, GCMP | Alias validés de GSCM.md et GSCMP.md, avec leurs entrées dans l'index. |
| PPSC, PPSCP, RCAM, RCAMP | Charge le fichier du même nom et exécute son processus. |
| SPCM, SPCMP, RSM, RSMP, SCM, SCMP | Charge le fichier du même nom et exécute son processus. |
| CISMPx | Charge CISMP.md avec le RUN CISMPn et son cycle normal. |
| 1CISMPx | Même RUN, un change complet, archivage, statistiques puis arrêt de la session de codage. |

Les codes directs, CISMPx, 1CISMPx et LIST sont résolus à chaque appel.
Le suffixe x est un entier décimal ASCII strictement positif sans zéro initial,
sans borne supérieure applicative. Un nom
inconnu ou en minuscules, un suffixe de RUN invalide, une déclaration absente/ambiguë,
un fichier manquant ou une sortie du dossier déclaré provoquent un blocage
explicite. Aucun autre référentiel n'est recherché.

Le résolveur s'appelle depuis une installation quelconque avec le projet
explicitement fourni :

```text
python3 -B <skill>/scripts/resolve_prompt.py LIST --project-root <projet>
```

Pour une action, il prépare le texte et l'instruction, puis le skill lit et
exécute réellement le processus du prompt. Les validations, préconditions et
conditions imposant de rendre la main restent applicables. Pour 1CISMPn, la
directive borne la sélection après un change ; les clôtures requises sont
effectuées avant l'arrêt et aucun deuxième change n'est engagé.

## Mise à jour

TCU automatise la mise à jour des briques déjà installées. Une fois son plugin
publié dans la marketplace configurée, installez-le avec
`codex plugin add tcu@tools-codex`, ou utilisez le skill autonome `skills/tcu/`.
Dans ce projet, `.agents/skills/tcu` pointe vers cette source. `$tcu` lance la
mise à jour ; `/TCU` est son déclencheur et sa commande source, sans
enregistrement automatique d'une slash native.

```text
$tcu check
$tcu
```

Depuis le répertoire du skill installé, les équivalents sont :

```bash
python3 -B scripts/update.py check
python3 -B scripts/update.py --apply
```

Le script seul contrôle sans écriture par défaut. Il nécessite le CLI Codex,
Python 3.13/3.14 et HTTPS public GitHub, sans nouvelle dépendance Python ni
secret. Il rafraîchit uniquement la marketplace officielle tools-codex,
vérifie les versions et préserve les données générées prises en charge.

Les copies autonomes présentes sont actualisées depuis le dépôt officiel,
à un SHA identifié. Les emplacements par défaut sont CODEX_HOME/skills,
~/.agents/skills, CODEX_HOME/prompts et CODEX_HOME/commands, avec ~/.codex pour
CODEX_HOME par défaut. Pour une installation spécifique, transmettez
`--skills-dir CHEMIN` ou `--commands-dir CHEMIN`. Les liens et checkouts de
développement sont signalés sans modification ; TCU ne met pas à jour le
checkout de travail par git pull. Seul le composant prompt absent est
installé automatiquement : plugin via le CLI, skill et résolveur embarqués
vérifiés contre la source GitHub, puis wrapper de commande. Un composant
incomplet est signalé ; aucun wrapper trompeur n’est écrit. Les autres plugins
absents ne sont pas installés, ni une seconde copie autonome du skill.

Le wrapper provient de `.codex/commands/PROMPT.md` ; sa cible par défaut est
CODEX_HOME/prompts/PROMPT.md, ou le premier --commands-dir explicite. Les
autres copies présentes sont mises à jour. Son reçu dédié
`.tools-codex-prompt-origin.json` peut reprendre une preuve existante sans
écraser le reçu partagé. Le contenu des prompts métier n’est jamais copié :
le skill résout exclusivement leur référentiel depuis DEVOPS.md.
`$tcu check` décrit ces opérations sans installation ni écriture.

Une ancienne copie prompt.md reste actualisée à son emplacement, sans création
d'un doublon PROMPT.md. Si les deux noms existent, TCU vérifie leurs empreintes
dans le même plan et reçu de composant. Les autres commandes en minuscules
déjà installées reçoivent aussi leur source canonique, sans changement de nom.
Les liens et modifications locales restent des conflits préservés. Une ancienne
release avec source prompt.md reste contrôlable ; les retours de version
conservent leurs gardes habituelles.

Une copie sans reçu et différente de la source est ambiguë. Après examen du
contrôle, `--adopt` permet explicitement son adoption avec sauvegarde. Cette
option ne force jamais une source suivie modifiée. Les reçus gardent les
empreintes et la release ; les sauvegardes restent dans CODEX_HOME/tcu-backups.
Les données, configurations personnelles et fichiers retirés en amont restent
préservés. Les anciens fichiers conservés ne sont pas purgés automatiquement.

En cas d'échec autonome, les fichiers remplacés sont restaurés et la
sauvegarde reste disponible. Le rafraîchissement CLI peut déjà avoir réussi :
le bilan distingue chaque canal, les versions connues et les états inconnus.
Un conflit local préserve sa cible et laisse continuer les opérations
indépendantes de marketplace et les plans locaux valides. Une erreur de source,
de sauvegarde ou de vérification CLI reste bloquante pour les sources non sûres.
Le bilan distingue plugin, skill embarqué et commande prompt.
Il retourne un code non nul sur conflit ou échec ; aucun succès complet n'est
déduit d'un simple téléchargement. Une nouvelle session charge les skills
actualisés. La livraison et les tests locaux n'installent pas TCU dans le profil
réel et ne publient pas la release distante.

Les commandes manuelles de rafraîchissement restent disponibles :

Rafraîchissez toutes les marketplaces configurées, y compris Tools Codex :

```bash
codex plugin marketplace upgrade
```

Pour mettre à jour uniquement cette marketplace, relevez son nom dans la
sortie de `codex plugin marketplace list`, puis exécutez :

```bash
codex plugin marketplace upgrade <NOM_DE_LA_MARKETPLACE>
```

Après la mise à jour, ouvrez `/plugins` pour vérifier les versions et les
plugins proposés, puis démarrez une nouvelle session avant toute utilisation.

Le rafraîchissement inclut désormais le plugin CM lorsqu'il est installé
depuis cette marketplace. Les copies autonomes restent à actualiser depuis
`skills/cm/` ; la copie embarquée du dépôt doit rester identique à cette
source. Une modification locale non publiée n'est pas récupérée par une
marketplace distante. La vérification du paquet en local ne remplace pas son
installation réelle et l'invocation de `$cm` dans une nouvelle session.

## Vérification avant publication

Pour prompt, valider le paquet isolé avec une racine de projet explicite,
sa parité avec le skill autonome et LIST depuis le vrai DEVOPS en lecture
seule. La disponibilité locale du plugin ne démontre pas une installation
dans un profil ni l'exécution d'un RUN ; ces étapes restent distinctes.

Avant de publier ou de mettre à jour la marketplace :

* vérifiez la validité du catalogue et des manifestes de plugin ;
* vérifiez les skills et les scripts inclus ;
* contrôlez qu'aucune donnée liée aux quotas, historiques ou informations
  d'authentification
  n'est ajoutée à la publication ;
* installez chaque plugin depuis la marketplace et testez-le dans une nouvelle
  session Codex.

## Références

Les commandes de gestion de marketplace et le redémarrage d'une session après
l'installation sont conformes à la [documentation officielle OpenAI sur la
distribution des plugins](https://developers.openai.com/plugins/build/plugins).


## Qualification gratuite TFL et moteur commun

Chaque paquet PLLM/TFL contient son scripts/performance.py ; les quatre copies
sont identiques et ne dépendent pas d'un autre plugin installé. Conserver ce
fichier lors de la distribution autonome ou d'un paquet isolé.
TFL génère désormais des réponses pour ses seuls gratuits admissibles en
Medium exclusivement, sans repli vers un autre effort. Exiger
contexte ≥1M, prix nuls vérifiés, réponse complète, TTFT <30 s et débit >20.
Les paliers sont 1024→2048→4096→8192 et 120 s par requête. Une invocation TFL
peut donc durer plus longtemps et rencontrer les limites gratuites fournisseur.
Aucun quota ou solde n'est consulté pour ces tests ; les clés existantes sont
injectées en mémoire. OpenRouter utilise l'environnement existant, sinon la
référence historique PLLM de ce compte dans le trousseau.
Les gratuits échoués sortent de models ; leurs preuves restent dans les
exclusions et le tableau commun des tests. Une section devenue vide est
publiée avec ses motifs sans bloquer les autres sections. La qualification est datée
et dépend du compte choisi par TFL, même si un autre compte pourrait réussir.
Les payants TFL ne sont pas benchmarkés. Une nouvelle invocation PLLM reteste
ses candidats retenus avec ses propres comptes et le raisonnement Medium.
Les anciens résultats mesurés avec un autre effort ne sont pas des réussites
Medium. Cette livraison
locale est qualifiée hors ligne et n'exécute aucun benchmark fournisseur réel.


## Protocole 8 de débit moyen

Distribuer les quatre copies identiques de performance.py avec les scripts
PLLM/TFL de la même release 0.7.6. Le débit utilise désormais le comptage API
sur la durée totale non arrondie de la requête, attente et TTFT inclus.
Les rafales et réponses en un bloc ne sont plus extrapolées sur la fenêtre
entre fragments. Les durées invalides produisent une mesure indisponible,
sans plafond ou plancher artificiel. Le JSON conserve les diagnostics et le
profil request_average_v1/request_total, protocole 8.
Les seuils et interfaces sont conservés, mais la signification du débit change :
classement et qualification peuvent changer. Les anciens succès de mémoire
restent présents et ne sont pas utilisés pour amorcer ce profil ; une réussite
courante est nécessaire. Aucune migration destructive ni réécriture des
rapports utilisateur pendant cette livraison. Après installation distincte,
relancer TFL puis PLLM pour obtenir des résultats sous la nouvelle méthode.

## Distribution et utilisation de LM

Le plugin lm est déclaré dans la marketplace. Une fois publié, il peut être
installé avec `codex plugin add lm@tools-codex`. La copie autonome est
skills/lm/ ; .agents/skills/lm la découvre dans ce projet. Choisir un mode
d'installation évite deux entrées LM. Une nouvelle session chargera les
ressources installées ; cette livraison locale ne réalise pas l'installation.

```text
/LM
/LM LIST
/LM ADD mimo-v2.5
/LM REMOVE mimo-v2.5
$lm LIST
```

Le script équivalent est `python3 -B scripts/lm.py` depuis le skill, suivi
de ADD ou REMOVE et de l'identifiant si nécessaire. LIST n'écrit rien.
Le stockage commun est CODEX_HOME/lm/blacklist.json, avec ~/.codex par défaut.
Sans fichier, mimo-v2.5 et muse-spark-1.2-contributor sont exclus et retirables.
Les paquets TFL/PLLM embarquent le module
identique et appliquent cette liste même sans plugin LM installé.
Une erreur de politique bloque sans réinitialisation. Les anciens rapports
restent inchangés jusqu'à leur prochaine génération. Les variantes fournisseur
et gratuites sont normalisées. LM est l'unique liste noire, sans exclusion permanente.
TCU préserve le fichier utilisateur et ne crée pas un composant LM absent.
Les tests isolés ne prouvent ni chargement dans une nouvelle session ni
performance fournisseur. Pour revenir à une ancienne release, tenir compte
du fait que 0.7.5 ignore la politique LM.

## Planning utilisateur TFL puis PLLM

Depuis 0.7.8, les plugins proposent un hook SessionStart. Codex demande de revoir et
d'approuver sa définition avant de l'exécuter ; l'installation du plugin
seule ne prouve donc pas que le timer est actif. Après cette approbation, le
bootstrap enregistre le planning à l'ouverture d'une session. TCU depuis 0.7.8 et
les releases suivantes exécutent le même bootstrap lors de `--apply`, sans lancer TFL/PLLM.
Une première mise à jour lancée avec un ancien TCU ne possède pas ce nouveau
code : utiliser ensuite le hook approuvé ou le TCU actualisé.

TFL et PLLM doivent déjà être présents, sous forme autonome ou comme plugins
activés de la marketplace. Le bootstrap ne les installe pas et ignore les
checkouts de développement. Pour une installation autonome copiée, exécuter
une fois depuis le skill installé, dans la session de l'utilisateur :

```bash
python3 -B scripts/scheduler.py install
python3 -B scripts/scheduler.py check
```

`--skills-root CHEMIN` permet d'indiquer une racine autonome spécifique, sans
figer une version de cache. Les paquets présents restent résolus à chaque
passage. Les hooks de plusieurs plugins et les mises à jour partagent une
installation, avec reçu et empreintes ; aucun autre planning n'est modifié.
Python 3.13/3.14, le CLI Codex, un gestionnaire systemd utilisateur actif et
les accès fournisseur existants de la session sont nécessaires. Aucune
connexion fournisseur ni secret supplémentaire n'est créé.

Le timer utilisateur exécute la chaîne à **00 h et 12 h Europe/Paris**,
sans rattrapage. Codex doit être ouvert pour ce même utilisateur. Une lecture
fraîche des quotas Codex précède chaque étape ; un restant nul ou un quota
inconnu empêche son démarrage. Aucun quota Spark ou historique n'est utilisé
comme remplacement. Si TFL échoue ou ne publie pas de catalogue frais, PLLM
ne démarre pas. PLLM est exécuté sans `active`, avec les sept modes habituels
et le catalogue TFL explicite. Les invocations manuelles restent inchangées.

Contrôler l'activation réelle avec :

```bash
systemctl --user status tools-codex-llm-refresh.timer
systemctl --user list-timers tools-codex-llm-refresh.timer
```

Le dernier état filtré est `CODEX_HOME/llm-refresh/state.json`. Les rapports
restent dans les dossiers `data/` des skills effectivement utilisés. L'absence
de session systemd ou une cible modifiée produit un diagnostic, sans faux
succès d'activation. Pour retirer uniquement le planning reconnu, depuis le
skill installé :

```bash
python3 -B scripts/scheduler.py remove
```

Les rapports et les autres unités sont conservés. Un hook toujours approuvé
ou une nouvelle application TCU peut réinstaller le planning ; désactiver ce
hook dans Codex si ce retrait doit durer. Une livraison locale et ses profils
de test ne prouvent ni approbation des hooks, ni activation du profil réel,
ni exécution observée à une échéance. Ces preuves restent distinctes.


## Admission stricte Medium

Tout candidat benchmarké doit publier une capacité Medium vérifiable avant test, sélection et affichage. Le mode5 payant OpenRouter n’exige pas Medium. Une liste supported_efforts contenant
medium ou un null explicitement publié (tous les efforts) est admissible. Une
clé absente, une valeur invalide, un booléen reasoning, une liste sans medium
ou un budget seul ne suffit pas. Aucun autre effort n'est autorisé.
Les exclus restent dans les audits JSON, sans apparaître dans les tableaux.
Les anciens catalogues, historiques et rangs forcés ne contournent pas ce
filtre ; DeepSeek direct exige aussi une preuve. Une section TFL vide est
publiée explicitement sans réintégrer de modèle exclu.


## Contrat TFL/PLLM 0.7.14 et conversion OpenRouter

TFL ne collecte ni ne publie plus OpenCode général. Le JSON contient seulement
opencode_go et openrouter. PLLM 1/2 ne sélectionne que les payants Go et 3/4
les gratuits Go, même si un ancien catalogue ou historique contient opencode.
Le rapport affiche Go en USD/M puis OpenRouter en EUR/M, huit colonnes chacun,
puis les essais gratuits ayant une preuve Medium. Aucun modèle exclu
pour son effort ne figure dans les tableaux ; les motifs restent dans le JSON.
Le moteur commun collecte le dernier taux BCE USD par EUR publié depuis
https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml. EUR = USD / taux ;
le plafond OpenRouter est 0,10 EUR/M inclus avant arrondi. Le JSON conserve
prix USD/EUR, source, date du cours et date de récupération. TFL bloque avant
publication si le cours est invérifiable ; PLLM refait le contrôle à la sélection
et à la frontière de génération, y compris pour les anciens catalogues et
les rangs forcés. Un budget seul n’équivaut plus à Medium.
Go garde 0,50 USD/M. Une sélection vide après filtrage ou essais
gratuits n'empêche plus les autres collectes et leur publication. Les tableaux
vides gardent leurs huit colonnes avec « Aucun modèle admissible » et une
synthèse des exclusions. Le JSON ajoute selection_status (available ou empty)
et exclusion_summary (motif vers nombre) aux deux sections et conserve les
sources, compteurs et motifs détaillés. Même deux sélections vides valides
sont publiées avec un code zéro ; les erreurs réelles préservent les anciens
rapports. Le planning garde les mêmes horaires et contrôles ; il exige seulement les
deux listes models Go/OpenRouter non vides pour lancer PLLM. Les tests de cette release sont hors ligne, sans mise
à jour de profil, activation du planning ni benchmark réel.

## Preuves supplémentaires et investigations

Livrer model_evidence.py avec chacun des quatre moteurs TFL/PLLM, le guide
references/model-evidence.md et le registre de référence TFL. Les niveaux
reasoning_options de models.dev sont normalisés. Une preuve Medium suffit
même sans intensité distincte. Une preuve historique qui ne couvre pas Medium
reste historique et déclenche une nouvelle recherche ; elle ne prouve pas cet effort.
Une métadonnée de contexte ou d'effort inconnue exige une recherche du LLM
dans les sources officielles pour les deux catalogues. Le registre du
répertoire de rapport, model-evidence.json, complète les preuves livrées.
TFL vérifie leurs sources courantes ; PLLM les recontrôle avant génération.
Le CLI seul marque investigation_status=required et le rapport provisoire ;
il ne prétend pas effectuer l'analyse du LLM. Un contexte encore invérifiable
après investigation exclut le modèle. Les commandes sources et skills
imposent ce workflow. Les politiques, seuils et règles du planning sont conservés.
Les lectures documentaires ne qualifient ni accès, ni génération, ni débit.


## Libellés PROMPT dans les bilans

Le plugin, le skill et la commande sont présentés sous le libellé **PROMPT**.
Le bilan JSON TCU ajoute `libelle: PROMPT` à chacune de ces ressources ; la
restitution utilise ce libellé. Les clés techniques `brique` et `composant`,
les chemins historiques et l’invocation `$prompt` restent compatibles.
