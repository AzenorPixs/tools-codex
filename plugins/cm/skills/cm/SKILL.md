---
name: cm
description: Afficher le catalogue des commandes maison Tools Codex avec leurs syntaxes. Utiliser pour $cm, /cm ou une demande de liste des commandes maison.
---

Affiche le catalogue ci-dessous en français, sous la forme d'un tableau concis
avec les colonnes `Commande`, `Utilisation` et `Description`. Conserve les
syntaxes indiquées et n'invente pas de commande. Cette consultation ne lance
ni PLLM, ni TFL, ni TCU, ni un prompt et ne charge pas leurs skills pour les exécuter.

| Commande | Utilisation | Description |
|---|---|---|
| `$cm` | `$cm` | Affiche le catalogue des commandes maison disponibles. |
| `$pllm` | `$pllm [active\|MODE] [--tfl-catalog CHEMIN]` | Évalue les politiques LLM ; accepte un mode forcé documenté et un catalogue TFL explicite. |
| `$tfl` | `$tfl [auto\|mode1\|mode2]` | Génère le rapport unifié des LLM fournisseurs, OpenCode Go en premier puis OpenRouter. |
| `$tcu` | `$tcu [check]` | Met à jour les briques installées et installe prompt si absent ; déclencheur `/TCU`, sans enregistrement d’une slash native. |
| `$prompt` | `$prompt LIST\|CODE` | Liste ou lance un prompt du projet ; arguments en MAJUSCULE, dont 1CISMP1 à 1CISMP8 ; déclencheur `/prompt`. |

Ces invocations désignent des skills disponibles après leur découverte ou leur
installation dans Codex. Le catalogue ne vérifie pas leur installation locale.
`/cm` est un déclencheur du même catalogue ; `.codex/commands/cm.md` délègue
au skill. Les fichiers de commande sources ne les enregistrent pas
automatiquement comme slash natives. `$cm` est directement pris en charge.

Lors d'une création, d'un renommage, d'une suppression ou d'un changement de
syntaxe autorisé d'une entrée publiée, actualise ce catalogue dans la source
autonome `skills/cm/SKILL.md` : nom, utilisation et description concise. Puis
synchronise `plugins/cm/skills/cm/SKILL.md` et vérifie que les deux fichiers
sont identiques. Le lien local `.agents/skills/cm` reste dirigé vers la source
autonome.
