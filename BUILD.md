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
dispose de Python 3, d'un accès HTTPS sortant et, pour `pllm` et `tfl`, de la
configuration locale nécessaire aux accès autorisés par l'utilisateur.

Installez `tfl` avec `pllm` : PLLM lit le catalogue produit par TFL. Les deux
plugins écrivent des rapports dans leur répertoire `data/`, qui doit être
inscriptible ou redirigé vers une sortie prise en charge.

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
