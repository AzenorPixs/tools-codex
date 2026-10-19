# PROJECT.md — Tools Codex

## Objectif

Tools Codex rassemble des extensions internes destinées à enrichir Codex :

* des plugins maison ;
* des skills maison ;
* des commandes maison.

Le projet centralise ces ressources afin qu'elles puissent être versionnées,
maintenues et distribuées de manière cohérente.

## Version de release

La version de release de Tools Codex est déclarée dans `VERSION`. Les plugins
publiés par la marketplace doivent déclarer la même version de release dans
leur manifeste.

## Périmètre

Le projet contient uniquement les ressources d'extension propres à Codex et
leur documentation associée. Chaque ressource conserve un périmètre explicite
et indépendant afin de limiter les dépendances entre extensions.

Les archives OpenSpec relatives à CAB présentes dans ce dépôt constituent un
historique distinct du catalogue actuel ci-dessous. Leur provenance n'est pas
qualifiée par les cadrages actuels ; leur présence ne signifie pas que Tools
Codex distribue aujourd'hui CAB. Elles sont conservées inchangées et ne
constituent ni des changes actifs ni une liste de fonctionnalités à réimplémenter.

## Organisation

Les commandes sources PLLM/TFL sont conservées dans :

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

Le skill `cm`, invocable avec `$cm`, fournit le catalogue des commandes maison.
Il est découvert dans ce projet via le lien relatif `.agents/skills/cm` vers
`skills/cm/`. Les fichiers de `.codex/commands/` ne sont pas enregistrés
automatiquement comme commandes slash natives. L'installation autonome hors
du projet est décrite dans `BUILD.md`.

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
| Skill | `cm` (`$cm`) | Affiche le catalogue des invocations `$cm`, `$pllm` et `$tfl`. |
| Commande source | `/pllm` | Instructions historiques de lancement de l'évaluation PLLM ; skill invocable avec `$pllm`. |
| Commande source | `/tfl` | Instructions historiques de lancement du rapport TFL ; skill invocable avec `$tfl`. |

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
