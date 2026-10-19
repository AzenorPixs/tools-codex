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

Les commandes sources PLLM/TFL sont conservées dans :

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

Le skill `cm` possède une source unique dans `skills/cm/SKILL.md`. Le lien
symbolique relatif `.agents/skills/cm -> ../../skills/cm` l'expose dans
l'emplacement de découverte des skills du dépôt. Il reste dans le projet et
évite une copie du catalogue. Aucun fichier global Codex n'est modifié.

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

Les plugins `pllm` et `tfl` possèdent un identifiant stable en kebab-case et
utilisent actuellement le manifeste de compatibilité Codex suivant :

```text
plugins/<NOM_DU_PLUGIN>/.codex-plugin/plugin.json
```

Le manifeste déclare le nom, la version, la présentation et le répertoire de
skills embarqués. Les deux plugins embarquent chacun le skill du même nom,
ainsi que les scripts, références et données nécessaires à son exécution.

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
| `$cm` | `skills/cm/` | — |
| `$pllm` | `skills/pllm/` | `plugins/pllm/` |
| `$tfl` | `skills/tfl/` | `plugins/tfl/` |
| `$cgpt` | `skills/cgpt/` | — |
| `$coding-session-statistics` | `skills/coding-session-statistics/` | — |

Le catalogue de `$cm` doit rester synchronisé avec les noms, syntaxes et
responsabilités des entrées maison publiées. Sa consultation n'exécute pas
PLLM ou TFL. Elle ne vérifie pas que ces skills sont installés localement.
La commande source `.codex/commands/cm.md` est supprimée : `/cm` est remplacé
par `$cm`. Les fichiers sources PLLM/TFL restent inchangés ; leur présence
n'enregistre pas automatiquement des commandes slash natives dans Codex.

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
La suite hors ligne actuelle comprend `tests/test_pllm_ttft.py` et
`tests/test_extension_qualification.py`, exécutables avec
`python3 -B -m unittest discover -s tests -v`. Elle couvre les deux
distributions, le catalogue explicite, l'initialisation, la préservation d'un
historique corrompu et les replis après HTTP 429. Chaque remplaçant recalcule
ses paliers et exige ses propres mesures avant de devenir valide.
TFL exclut les prix OpenRouter non finis et les débordements, puis prépare
une sérialisation JSON stricte avant publication. Ces tests isolés ne
qualifient pas les services externes. La compatibilité Python est contrôlée
sur les branches 3.13 et 3.14 avec ces 19 tests, la compilation de tous les
scripts et tests, leurs imports et la résolution du fuseau Europe/Paris.
Les résultats et versions exactes sont consignés dans le change et son
rapport d'archive ; aucune compatibilité avec une autre branche n'est déduite.

Avant publication, chaque plugin doit être vérifié dans une nouvelle session
Codex après son installation depuis la marketplace. La validation couvre au
minimum le chargement du manifeste, la disponibilité des skills ou outils
déclarés et l'absence de dépendance ou de donnée sensible non documentée.

Les skills autonomes sont validés avec leur `SKILL.md` et leurs ressources
nécessaires. Pour `cm`, le format, le lien de découverte et le catalogue sont
contrôlés localement. Une invocation effective de `$cm` dans une nouvelle
session Codex est une preuve distincte ; la résolution du lien seule ne la
démontre pas. Les scripts Python sont vérifiés au minimum par compilation sans
écriture d'artefact ; les fichiers JSON sont analysés avant publication.

Les formats de manifeste, de catalogue et les règles de distribution suivent
la [documentation officielle OpenAI sur les plugins](https://developers.openai.com/plugins/build/plugins).
