## MODIFIED Requirements

### Requirement: Catalogue des commandes cohérent
Le skill `cm` SHALL afficher un tableau français concis avec Commande,
Utilisation et Description. Il SHALL présenter `$cm`, `$pllm`, `$tfl` et
`$tcu` avec leurs syntaxes documentées, dont le déclencheur `/TCU`. Il SHALL
NOT exécuter les commandes listées ni inventer de slash native. Toute évolution
autorisée des entrées SHALL actualiser les copies autonome et embarquée.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm est invoqué
- **THEN** le tableau contient `$cm`, `$pllm [active|MODE] [--tfl-catalog CHEMIN]`, `$tfl [auto|mode1|mode2]` et `$tcu [--check]`
- **AND** la description TCU indique le déclencheur /TCU sans promettre une slash native
- **AND** aucune mise à jour ou évaluation n'est déclenchée

### Requirement: Préservation des copies et qualification de distribution
Les copies autonomes et embarquées de CM, PLLM, TFL et TCU SHALL rester
cohérentes. Les skills et scripts TCU, ainsi que le skill CM, SHALL être
identiques dans les deux distributions. La qualification SHALL distinguer
les contrôles locaux d'une installation réelle dans une nouvelle session.
Les secrets et données personnelles SHALL rester hors des artefacts publiés.

#### Scenario: Mise à jour d'instructions communes
- **WHEN** une ressource commune distribuée est modifiée
- **THEN** les deux copies sont actualisées et comparées
- **AND** cette comparaison n'est pas présentée comme une installation réussie

#### Scenario: Vérification du paquet CM isolé
- **WHEN** le seul répertoire du plugin CM est copié hors du dépôt
- **THEN** son manifeste et son skill sont résolus sans source externe

## ADDED Requirements

### Requirement: Distribution du plugin TCU
La marketplace SHALL référencer `./plugins/tcu` avec un manifeste de release
commune et `skills: ./skills/`. Elle SHALL conserver les plugins CM/PLLM/TFL.
Le projet SHALL fournir `skills/tcu/`, sa copie embarquée, le lien relatif
`.agents/skills/tcu` et `.codex/commands/TCU.md`. Les quatre manifestes, VERSION,
README et pyproject.toml SHALL déclarer la même release commune.

#### Scenario: Résolution TCU
- **WHEN** le catalogue et le paquet TCU sont vérifiés
- **THEN** les quatre plugins, les sources et le script embarqué sont présents et leurs versions alignées
- **AND** le paquet TCU copié isolément résout son script sans dépendre du dépôt
