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

Les commandes sources CM/PLLM/TFL/TCU/prompt sont conservées dans :

```text
.codex/commands/
```

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

Les plugins `cm`, `pllm`, `tfl`, `tcu` et `prompt` possèdent un identifiant stable en kebab-case et
utilisent actuellement le manifeste de compatibilité Codex suivant :

```text
plugins/<NOM_DU_PLUGIN>/.codex-plugin/plugin.json
```

Le manifeste déclare le nom, la version, la présentation et le répertoire de
skills embarqués. Les cinq plugins embarquent chacun le skill du même nom.
PLLM et TFL incluent les scripts, références et données nécessaires à leur
exécution. CM contient uniquement son manifeste et `skills/cm/SKILL.md` ; il
ne déclare ni script, ni serveur MCP, ni application ou service externe.

TCU embarque `skills/tcu/SKILL.md` et `skills/tcu/scripts/update.py`. Les deux
copies autonomes et embarquées sont identiques. Le lien relatif
`.agents/skills/tcu -> ../../skills/tcu` assure la découverte dans ce projet.

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
| `$prompt` (déclencheur `/prompt`) | `skills/prompt/` | `plugins/prompt/` |
| `$cgpt` | `skills/cgpt/` | — |
| `$coding-session-statistics` | `skills/coding-session-statistics/` | — |

Le catalogue de `$cm` doit rester synchronisé avec les noms, syntaxes et
responsabilités des entrées maison publiées. Sa consultation n'exécute pas
PLLM, TFL, TCU ou un prompt. Elle ne vérifie pas que ces skills sont installés localement.
Après une modification de sa source autonome, la copie embarquée doit être
synchronisée et comparée octet pour octet. Le chargement simultané du plugin
CM et du skill autonome peut afficher deux entrées ; la procédure de
distribution n'en supprime ou désactive aucune automatiquement.
La commande source `.codex/commands/cm.md` délègue au skill CM ; `/cm` est
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
| `pllm` | Python 3, `secret-tool` et accès au trousseau de l'hôte, accès réseau HTTPS et répertoire de données inscriptible. Le catalogue TFL est fourni par `--tfl-catalog CHEMIN` ou par le chemin voisin par défaut ; les quatre politiques sont initialisées si le fichier courant manque. | OpenCode Go, OpenRouter, DeepSeek et le service de taux de change de la BCE. |
| `cgpt` | Python 3, répertoire de données inscriptible et outil Codex `mcp__codex_app__get_usage_limits`. | Aucun accès HTTP direct. |
| `coding-session-statistics` | Historique persistant de la session. Le suivi de quota utilise `cgpt` ; les mesures de performance nécessitent une collecte planifiée dès le début de session. | Aucun accès HTTP direct obligatoire. |
| `$cm` | Skill découvert dans le projet ou installé dans un emplacement reconnu. | Aucun. |
| `$prompt` | Python 3.13/3.14, DEVOPS.md du projet courant et référentiel déclaré lisibles. | Aucun pour résoudre ; dépend ensuite du prompt choisi. |
| `$tcu` | Python 3.13/3.14, CLI Codex, racines identifiées inscriptibles pour appliquer. | GitHub public HTTPS et marketplace officielle. |

Les plugins `pllm` et `tfl` écrivent leurs rapports dans leur répertoire
`data/`. TFL accepte une redirection par `--output-dir` ; PLLM ne propose pas
d'option équivalente et exige que son propre répertoire `data/` soit
inscriptible. PLLM charge `data/pllm-current.json` avant l'évaluation ; si ce
fichier manque, les quatre politiques sont initialisées sans mesures ni
sélection historique. Un fichier courant invalide provoque un diagnostic et
reste préservé. Les contrôles de quotas et de performance restent obligatoires.

La résolution du catalogue par PLLM accepte `--tfl-catalog CHEMIN` pour
OpenCode Go, OpenRouter et les replis. Sans option, elle conserve
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
`tests/test_extension_qualification.py`, `tests/test_tcu_update.py` et
`tests/test_prompt_dispatch.py`, exécutables avec
`python3 -B -m unittest discover -s tests -v`. Elle couvre les deux
distributions, le catalogue explicite, l'initialisation, la préservation d'un
historique corrompu et les replis après HTTP 429. Chaque remplaçant recalcule
ses paliers et exige ses propres mesures avant de devenir valide.
TFL exclut les prix OpenRouter non finis et les débordements, puis prépare
une sérialisation JSON stricte avant publication. Ces tests isolés ne
qualifient pas les services externes. La compatibilité Python est contrôlée
sur les branches 3.13 et 3.14 avec la suite applicable, la compilation de tous les
scripts et tests, leurs imports et la résolution du fuseau Europe/Paris.
Les résultats et versions exactes sont consignés dans le change et son
rapport d'archive ; aucune compatibilité avec une autre branche n'est déduite.

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

Le wrapper issu de `.codex/commands/prompt.md` est déployé par défaut dans
CODEX_HOME/prompts, ou dans le premier --commands-dir explicite. Les autres
copies présentes sont actualisées. Son reçu dédié
`.tools-codex-prompt-origin.json` peut reprendre une preuve du reçu partagé
sans l’écraser. Les plans génériques ne gèrent plus prompt.md. Le wrapper
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
