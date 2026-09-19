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

## Arborescence

Les commandes Codex sont placées dans :

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

Le catalogue de la marketplace du dépôt est placé dans :

```text
.agents/plugins/marketplace.json
```

Les chemins des plugins déclarés dans ce catalogue sont relatifs à la racine
du dépôt et commencent par `./`.

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

| Commande | Skill autonome | Plugin |
|---|---|---|
| `/cm` | — | — |
| `/pllm` | `skills/pllm/` | `plugins/pllm/` |
| `/tfl` | `skills/tfl/` | `plugins/tfl/` |
| — | `skills/cgpt/` | — |
| — | `skills/coding-session-statistics/` | — |

La commande `/cm` doit rester synchronisée avec les commandes effectivement
présentes dans `.codex/commands/`.

## Données générées

Les scripts de `cgpt`, `pllm` et `tfl` peuvent générer ou actualiser des
rapports locaux. Les données liées à un compte, aux quotas ou à l'historique
d'utilisation ne doivent jamais être ajoutées aux sources publiées. Les
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

Avant publication, chaque plugin doit être vérifié dans une nouvelle session
Codex après son installation depuis la marketplace. La validation couvre au
minimum le chargement du manifeste, la disponibilité des skills ou outils
déclarés et l'absence de dépendance ou de donnée sensible non documentée.

Les skills autonomes sont validés avec leur `SKILL.md` et leurs ressources
nécessaires. Les scripts Python sont vérifiés au minimum par compilation sans
écriture d'artefact ; les fichiers JSON sont analysés avant publication.

Les formats de manifeste, de catalogue et les règles de distribution suivent
la [documentation officielle OpenAI sur les plugins](https://developers.openai.com/plugins/build/plugins).
