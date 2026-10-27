## MODIFIED Requirements

### Requirement: Catalogue des commandes cohérent
Le skill CM SHALL afficher un tableau français avec Commande, Utilisation et
Description pour CM, PLLM, TFL, TCU et prompt. Les deux copies SHALL conserver
les syntaxes documentées, dont $prompt LIST ou CODE et les déclencheurs /prompt et /cm.
La consultation SHALL NOT exécuter les actions listées ni inventer une slash
native. Toute évolution autorisée SHALL actualiser les deux catalogues.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm ou /cm est invoqué
- **THEN** le tableau décrit les cinq invocations, dont $tcu [check] et $prompt LIST ou CODE
- **AND** aucune mise à jour, évaluation ou exécution de prompt n'est déclenchée

#### Scenario: Wrapper CM
- **WHEN** .codex/commands/cm.md est utilisé
- **THEN** il délègue au skill CM et conserve une seule entrée prompt dans chaque catalogue
- **AND** il ne lance pas le prompt et ne promet pas une slash native automatiquement enregistrée

### Requirement: Distribution du plugin TCU
La marketplace SHALL référencer ./plugins/tcu avec un manifeste de release
commune et skills: ./skills/. Elle SHALL conserver CM, PLLM, TFL et prompt.
Le projet SHALL fournir skills/tcu/, sa copie embarquée, le lien relatif
.agents/skills/tcu et .codex/commands/TCU.md. Les cinq manifestes, VERSION,
README et pyproject.toml SHALL déclarer la même release commune.

#### Scenario: Résolution TCU
- **WHEN** le catalogue et le paquet TCU sont vérifiés
- **THEN** les cinq plugins, les sources et le script embarqué sont présents et leurs versions alignées
- **AND** le paquet TCU copié isolément résout son script sans dépendre du dépôt
