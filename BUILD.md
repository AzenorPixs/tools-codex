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
| `pllm` | `pllm` | Évaluation et application contrôlée d'une politique LLM. |
| `tfl` | `tfl` | Rapport comparatif OpenCode Go puis OpenRouter. |

Les commandes de `.codex/commands/` et les skills autonomes de `skills/` sont
des sources du dépôt. Leur mise à disposition ne résulte pas, à elle seule, de
l'installation d'un plugin depuis la marketplace ; elle doit suivre le mode de
distribution Codex approprié à ces ressources.

## Skill catalogue cm

Le skill `cm` remplace l'ancienne commande `/cm`. Dans ce projet, la source
`skills/cm/SKILL.md` est exposée par le lien relatif
`.agents/skills/cm -> ../../skills/cm`. Utilisez `$cm` dans Codex pour afficher
les invocations maison et leurs syntaxes. La consultation du catalogue ne
lance ni PLLM ni TFL et ne vérifie pas leur installation.

Pour utiliser le catalogue dans un autre projet, copiez le dossier `skills/cm/`
dans `.agents/skills/cm/` de ce projet. Pour un usage personnel partagé entre
projets, installez ce dossier dans `~/.agents/skills/cm/`. Conservez son
`SKILL.md` ; une copie doit être actualisée depuis la source lors des mises à
jour. Ces installations hors du dépôt sont des actions distinctes.

Codex détecte les modifications de skills. Si `cm` n'apparaît pas, démarrez
une nouvelle session ou redémarrez Codex. Vérifiez alors que `$cm` affiche le
tableau français avec `$cm`, `$pllm` et `$tfl`, sans lancer d'évaluation. Le
contrôle local du lien ne remplace pas ce test effectif de découverte.

L'installation de PLLM ou TFL depuis la marketplace n'installe pas `cm`.
Les commandes sources restantes dans `.codex/commands/` n'enregistrent pas
automatiquement des commandes slash natives. Le mécanisme de skills et les
emplacements de découverte sont décrits dans la
[documentation officielle](https://learn.chatgpt.com/docs/build-skills).

## Installation

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
TFL accessible. Si le fichier courant PLLM manque, les quatre politiques sont
initialisées automatiquement, sans reprendre de résultats historiques.
Pour des plugins séparés, lancer depuis le skill PLLM :

```bash
python3 scripts/evaluate.py --tfl-catalog /chemin/vers/le/catalogue/tfl.json
```

Cette option accepte le fichier produit par TFL, y compris avec `--output-dir`.
Sans option, PLLM conserve le chemin voisin `../tfl/data/tfl.json`.
Les tests hors ligne couvrent des emplacements isolés ; un test réel
d'installation dans une nouvelle session Codex reste à effectuer avant
publication, conformément à `TECHNICAL.md`.

TFL doit être exécuté hors sandbox pour accéder à ses fournisseurs. Si un accès
OpenRouter est nécessaire, préparez-le localement sans jamais ajouter
d'information d'authentification au dépôt ou à la configuration de la
marketplace.

Les skills `cgpt` et `coding-session-statistics` requièrent respectivement
l'outil Codex de lecture des quotas et l'historique persistant de la session.
Ils ne sont pas installés automatiquement avec les plugins de la marketplace.

## Mise à jour

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

## Vérification avant publication

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
