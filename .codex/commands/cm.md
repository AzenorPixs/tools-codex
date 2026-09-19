---
description: Afficher le résumé de toutes les Commandes Maison Codex
---

Affiche le catalogue des Commandes Maison Codex ci-dessous sous la forme d'un tableau concis avec les colonnes `Commande`, `Utilisation` et `Description`.

Réponds en français. N'invente pas de commande et conserve les syntaxes indiquées.

## Catalogue des Commandes Maison

| Commande | Utilisation | Description |
|---|---|---|
| `/cm` | `/cm` | Affiche le résumé de toutes les Commandes Maison disponibles. |
| `/pllm` | `/pllm [quotas et soldes]` | Actualise les politiques LLM et sélectionne automatiquement le mode disponible de plus haute priorité. |
| `/tfl` | `/tfl [auto\|mode1\|mode2]` | Génère le rapport unifié des LLM fournisseurs, OpenCode Go en premier puis OpenRouter. |

## Règle de maintenance

Lors de la création d'une nouvelle Commande Maison dans `.codex/commands/`, modifie aussi ce fichier afin d'ajouter immédiatement au catalogue :

1. le nom de la commande ;
2. sa syntaxe d'utilisation ;
3. une description concise.

Lors du renommage ou de la suppression d'une Commande Maison, mets également ce catalogue à jour.
