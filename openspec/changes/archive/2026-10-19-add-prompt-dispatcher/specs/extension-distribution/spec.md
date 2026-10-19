## MODIFIED Requirements

### Requirement: Catalogue des commandes cohérent
Le skill CM SHALL afficher un tableau français avec Commande, Utilisation et
Description pour CM, PLLM, TFL, TCU et prompt. Les deux copies SHALL conserver
les syntaxes documentées, dont $prompt LIST ou CODE et le déclencheur /prompt.
La consultation SHALL NOT exécuter les actions listées ni inventer une slash
native. Toute évolution autorisée SHALL actualiser les deux catalogues.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm est invoqué
- **THEN** le tableau décrit les cinq invocations, dont $tcu [check] et $prompt LIST ou CODE
- **AND** aucune mise à jour, évaluation ou exécution de prompt n'est déclenchée

### Requirement: Préservation des copies et qualification de distribution
Les copies autonomes et embarquées de CM, PLLM, TFL, TCU et prompt SHALL rester
cohérentes. Les skills et scripts TCU et prompt, ainsi que le skill CM, SHALL
être identiques dans les deux distributions. La qualification SHALL distinguer
contrôles locaux et exécution réelle d'un prompt ou installation dans une
nouvelle session. Les secrets et données personnelles SHALL rester exclus.

#### Scenario: Mise à jour d'instructions communes
- **WHEN** une ressource commune distribuée est modifiée
- **THEN** les deux copies sont actualisées et comparées sans prétendre à une installation réelle

#### Scenario: Vérification du paquet CM isolé
- **WHEN** le seul répertoire du plugin CM est copié hors du dépôt
- **THEN** son manifeste et son skill sont résolus sans source externe

## ADDED Requirements

### Requirement: Distribution du plugin prompt
La marketplace SHALL référencer ./plugins/prompt, avec un manifeste de release
commune et skills: ./skills/. Le projet SHALL fournir skills/prompt/, sa copie
embarquée, .codex/commands/prompt.md et le lien relatif .agents/skills/prompt.
Le paquet SHALL contenir son résolveur mais SHALL NOT embarquer les prompts
du référentiel externe. Les cinq plugins SHALL partager la release du projet.

#### Scenario: Paquet autonome
- **WHEN** le paquet prompt est copié isolément
- **THEN** son script fonctionne avec un projet explicite contenant DEVOPS.md
- **AND** aucun fichier du dépôt Tools Codex n'est nécessaire hors du paquet
