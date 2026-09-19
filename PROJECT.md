# PROJECT.md — Tools Codex

## Objectif

Tools Codex rassemble des extensions internes destinées à enrichir Codex :

* des plugins maison ;
* des skills maison ;
* des commandes maison.

Le projet centralise ces ressources afin qu'elles puissent être versionnées,
maintenues et distribuées de manière cohérente.

## Périmètre

Le projet contient uniquement les ressources d'extension propres à Codex et
leur documentation associée. Chaque ressource conserve un périmètre explicite
et indépendant afin de limiter les dépendances entre extensions.

## Organisation

Les commandes maison sont stockées dans :

```text
.codex/commands/
```

Les plugins maison sont stockés dans des répertoires dédiés :

```text
plugins/<NOM_DU_PLUGIN>/
```

Les skills maison autonomes sont stockés dans des répertoires dédiés :

```text
skills/<NOM_DU_SKILL>/
```

Un plugin peut également embarquer ses propres skills dans son répertoire
`skills/`, selon les conventions applicables de Codex.

## Catalogue actuel

| Type | Nom | Rôle |
|---|---|---|
| Plugin | `pllm` | Évalue une politique de modèles LLM et l'applique à une session OpenCode autorisée. |
| Plugin | `tfl` | Produit le rapport comparatif des fournisseurs OpenCode Go et OpenRouter. |
| Skill | `cgpt` | Affiche les quotas Codex disponibles. |
| Skill | `coding-session-statistics` | Produit un bilan auditable d'une session de codage ou de pilotage. |
| Skill | `pllm` | Expose la politique PLLM également en dehors du plugin. |
| Skill | `tfl` | Expose le rapport TFL également en dehors du plugin. |
| Commande | `/cm` | Affiche le catalogue des commandes maison publiées. |
| Commande | `/pllm` | Lance l'évaluation PLLM. |
| Commande | `/tfl` | Lance le rapport TFL. |

Les skills `pllm` et `tfl` sont volontairement fournis sous forme autonome et
embarquée afin de couvrir les deux modes de distribution. Le skill
`coding-session-statistics` s'appuie sur `cgpt` pour les relevés de quota
hebdomadaires lorsqu'ils sont demandés.

## Principes

Les extensions doivent privilégier :

* une responsabilité claire ;
* la compatibilité avec Codex ;
* la documentation des comportements et prérequis ;
* l'absence de secrets dans les sources ;
* une évolution indépendante et traçable de chaque plugin, skill ou commande.

Les évolutions fonctionnelles du projet sont décrites et validées dans
OpenSpec avant leur implémentation, conformément aux règles du dépôt.
