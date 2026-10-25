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
| `prompt` | `prompt` | Liste et lancement des prompts définis par le DEVOPS du projet. |
| `cm` | `cm` | Catalogue des commandes maison et de leurs syntaxes. |
| `tcu` | `tcu` | Mise à jour vérifiée des briques déjà installées. |
| `pllm` | `pllm` | Évaluation et application contrôlée d'une politique LLM. |
| `tfl` | `tfl` | Rapport OpenCode Go, catalogue général OpenCode puis OpenRouter. |

Les commandes de `.codex/commands/` et les skills autonomes de `skills/` sont
des sources du dépôt. Leur mise à disposition ne résulte pas, à elle seule, de
l'installation d'un plugin depuis la marketplace ; elle doit suivre le mode de
distribution Codex approprié à ces ressources.

## Skill catalogue cm

Le skill `cm` reconnaît `$cm` et `/cm`. Le wrapper `.codex/commands/cm.md`
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
tableau français avec CM, PLLM, TFL, TCU et Prompt dans `Commande`, sous forme
de références aux skills disponibles, et leurs syntaxes `$…` dans `Utilisation`,
sans lancer les actions listées. Le
contrôle local du lien ne remplace pas ce test effectif de découverte.

L'installation de PLLM ou TFL depuis la marketplace n'installe pas `cm`.
Les commandes sources restantes dans `.codex/commands/` n'enregistrent pas
automatiquement des commandes slash natives. Le mécanisme de skills et les
emplacements de découverte sont décrits dans la
[documentation officielle](https://learn.chatgpt.com/docs/build-skills).

## Installation

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
TFL accessible. Si le fichier courant PLLM manque, les six politiques sont
initialisées automatiquement, sans reprendre de résultats historiques.
Pour des plugins séparés, lancer depuis le skill PLLM :

```bash
python3 scripts/evaluate.py --tfl-catalog /chemin/vers/le/catalogue/tfl.json
```

Cette option accepte le fichier produit par TFL, y compris avec `--output-dir`.
Sans option, PLLM conserve le chemin voisin `../tfl/data/tfl.json`.
Ce catalogue fournit les payants Go pour 1/2, les gratuits Go et OpenCode
général pour 3/4, et OpenRouter pour 5 ; 6 conserve DeepSeek direct.
Les modes 1/2 épuisés deviennent rouges et invalides sans essai gratuit.
Les modes 3/4 utilisent les comptes de 1/2 respectivement sans consulter de
quota ou solde. Ils exigent prix nuls vérifiés, contexte ≥1M, réponse complète,
TTFT <30 s et débit >20 tokens/s. Tous les gratuits, y compris le repli OpenRouter de 5, utilisent ces seuils.
Les payants gardent leurs seuils <90 s et >15 tokens/s et leurs contrôles de ressources ; seul 5 conserve le
repli gratuit OpenRouter après crédit épuisé. Les références de trousseau
restent celles des anciens comptes, sans nouveau secret ni migration de clé.
Les historiques à quatre modes sont adaptés au schéma 2 (ancien 3→5, ancien
4→6, nouveaux 3/4 initialisés), sans résultat courant ni sélection hérités.
La mémoire suit ce déplacement sans apprentissage pour les nouveaux 3/4.
Un ancien évaluateur ne lit pas le schéma 2 : sauvegarder ses données avant
un retour de version. Aucun historique invalide n'est écrasé.
Le gagnant payant de 1/2 et de la catégorie payante de 5 est le moins cher
parmi les candidats qualifiés, selon le coût moyen de référence TFL (hors
pointe Go, prix de base OpenRouter). À prix égal seulement, départager par
débit maximal, TTFT minimal puis ordre TFL stable. Les gratuits 3/4 et le repli
gratuit de 5 restent classés par performances ; 6 garde son candidat unique.
Les priorités entre politiques 1 à 6 restent inchangées. Tous les benchmarks demandent HIGH, puis XHIGH seulement si HIGH est
indisponible et XHIGH pris en charge ; aucun repli inférieur. Les restrictions
fournisseur restent applicables aux gratuits ; les tests hors ligne ne prouvent pas l'accès réel.
Les diagnostics HTTP 400/429 et le Retry-After disponible figurent dans les
rapports PLLM sans corps d'erreur brut. Hors le repli d'effort XHIGH autorisé, ils n'entraînent plus d'essais aux
budgets supérieurs ; une limitation conserve ses contraintes fournisseur.
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
Le catalogue général ajoute un accès public à `https://opencode.ai/zen/v1/models`
et à ses tarifs Console officiels, sans secret Go ni nouvelle dépendance.
Les métadonnées proviennent de `opencode` dans models.dev. Les trois tableaux
s'affichent dans l'ordre Go, OpenCode général, OpenRouter, avec mêmes colonnes
et seuils 1M/0,50 USD/M. Une source indispensable en échec empêche la publication.
La section JSON `opencode` est additive ; PLLM l'utilise pour les gratuits autonomes 3/4, sans changer le classement tarifaire de TFL.

Les skills `cgpt` et `coding-session-statistics` requièrent respectivement
l'outil Codex de lecture des quotas et l'historique persistant de la session.
Ils ne sont pas installés automatiquement avec les plugins de la marketplace.

## Utilisation de prompt

Le seul référentiel est le dossier et l'index indiqués par le DEVOPS.md du
projet courant. Les sources restent externes au plugin et ne sont pas copiées.
Les arguments sont en MAJUSCULE ; ils ne comportent pas de tirets :

```text
/prompt LIST
/prompt CISMP3
/prompt 1CISMP3
```

Les mêmes actions sont disponibles avec `$prompt LIST`, `$prompt CISMP3` et
`$prompt 1CISMP3`. `/prompt` est une commande source et un déclencheur du skill,
sans enregistrement automatique d'une slash native.

| Arguments | Source et effet |
|---|---|
| LIST | Affiche la table réelle de l'index, sans lire les corps ni lancer un prompt. |
| ACSP, ACSM, ACSMP, CGP, CISM | Charge le fichier du même nom et exécute son processus. |
| DOP, DOPP, EDP, ISM, ISMP | Charge le fichier du même nom et exécute son processus. |
| GCM, GCMP | Alias validés de GSCM.md et GSCMP.md, avec leurs entrées dans l'index. |
| PPSC, PPSCP, RCAM, RCAMP | Charge le fichier du même nom et exécute son processus. |
| SPCM, SPCMP, RSM, RSMP, SCM, SCMP | Charge le fichier du même nom et exécute son processus. |
| CISMP1 à CISMP8 | Charge CISMP.md avec le RUN CISMPn et son cycle normal. |
| 1CISMP1 à 1CISMP8 | Même RUN, un change complet, archivage, statistiques puis arrêt de la session de codage. |

Les 38 arguments d'exécution et LIST sont résolus à chaque appel. Un nom
inconnu ou en minuscules, un RUN hors bornes, une déclaration absente/ambiguë,
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

Le wrapper provient de `.codex/commands/prompt.md` ; sa cible par défaut est
CODEX_HOME/prompts/prompt.md, ou le premier --commands-dir explicite. Les
autres copies présentes sont mises à jour. Son reçu dédié
`.tools-codex-prompt-origin.json` peut reprendre une preuve existante sans
écraser le reçu partagé. Le contenu des prompts métier n’est jamais copié :
le skill résout exclusivement leur référentiel depuis DEVOPS.md.
`$tcu check` décrit ces opérations sans installation ni écriture.

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
HIGH, avec XHIGH comme seul repli autorisé lorsque pris en charge. Exiger
contexte ≥1M, prix nuls vérifiés, réponse complète, TTFT <30 s et débit >20.
Les paliers sont 1024→2048→4096→8192 et 120 s par requête. Une invocation TFL
peut donc durer plus longtemps et rencontrer les limites gratuites fournisseur.
Aucun quota ou solde n'est consulté pour ces tests ; les clés existantes sont
injectées en mémoire. OpenRouter utilise l'environnement existant, sinon la
référence historique PLLM de ce compte dans le trousseau.
Les gratuits échoués sortent de models ; leurs preuves restent dans les
exclusions et le tableau commun des tests. Une section devenue vide bloque
la publication et préserve les anciens rapports. La qualification est datée
et dépend du compte choisi par TFL, même si un autre compte pourrait réussir.
Les payants TFL ne sont pas benchmarkés. Une nouvelle invocation PLLM reteste
ses candidats retenus avec ses propres comptes et le raisonnement HIGH/XHIGH.
Les anciens résultats Low ne sont pas des réussites HIGH. Cette livraison
locale est qualifiée hors ligne et n'exécute aucun benchmark fournisseur réel.


## Protocole 8 de débit moyen

Distribuer les quatre copies identiques de performance.py avec les scripts
PLLM/TFL de la même release 0.7.4. Le débit utilise désormais le comptage API
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
