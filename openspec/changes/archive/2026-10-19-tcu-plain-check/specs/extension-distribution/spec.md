## MODIFIED Requirements

### Requirement: Catalogue des commandes cohérent
Le skill `cm` SHALL afficher un tableau français concis avec Commande,
Utilisation et Description. Il SHALL présenter `$cm`, `$pllm`, `$tfl` et
`$tcu` avec leurs syntaxes documentées, dont le déclencheur `/TCU`. Il SHALL
NOT exécuter les commandes listées ni inventer de slash native. Toute évolution
autorisée des entrées SHALL actualiser les copies autonome et embarquée.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm est invoqué
- **THEN** le tableau contient `$cm`, `$pllm [active|MODE] [--tfl-catalog CHEMIN]`, `$tfl [auto|mode1|mode2]` et `$tcu [check]`
- **AND** la description TCU indique le déclencheur /TCU sans promettre une slash native
- **AND** aucune mise à jour ou évaluation n'est déclenchée
