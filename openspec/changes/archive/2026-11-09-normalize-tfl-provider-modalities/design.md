# Conception — TFL07

## Résolution des modalités

Comparer des catégories canoniques plutôt que les chaînes de transport.
Les types `image/*`, `audio/*` et `video/*` se résolvent vers leur type
principal ; `text/*` vers `text` ; `application/pdf` vers `pdf`. Les valeurs
déjà canoniques gardent leur catégorie. Les types inconnus restent normalisés
en casse et espaces uniquement, sans être supprimés ni attribués à une
catégorie supposée.

Les différentes déclarations d’une même source sont cohérentes si leurs
ensembles canoniques sont égaux. La comparaison entre API et models.dev suit
la même règle. Une différence réelle d’ensembles demeure une erreur explicite
avant publication. Les données restituées aux filtres restent canoniques afin
que les catégories `audio`, `video`, `speech` et `sound` continuent d’exclure
les sorties correspondantes.

## Audit et compatibilité

Le JSON conserve, pour chaque direction, les valeurs observées par l’API et
models.dev en plus des catégories résolues, de la source et de la date déjà
publiées. Les champs de routage et les huit colonnes de rapport ne changent
pas. Aucun repli historique ou par identifiant de modèle n’est ajouté.
