## MODIFIED Requirements

### Requirement: Catalogue des commandes cohérent
Le skill CM SHALL afficher un tableau français avec Commande, Utilisation et
Description pour CM, PLLM, TFL, TCU, LM et prompt. Les deux copies SHALL conserver
les syntaxes documentées, dont $prompt LIST ou CODE et les déclencheurs /prompt et /cm.
LM SHALL documenter $lm [LIST|ADD identifiant|REMOVE identifiant] et /LM.
La consultation SHALL NOT exécuter les actions listées ni inventer une slash
native. Toute évolution autorisée SHALL actualiser les deux catalogues.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm ou /cm est invoqué
- **THEN** le tableau décrit les six invocations, dont $tcu [check] et $prompt LIST ou CODE
- **AND** aucune mise à jour, évaluation ou exécution de prompt n'est déclenchée

#### Scenario: Wrapper CM
- **WHEN** .codex/commands/cm.md est utilisé
- **THEN** il délègue au skill CM et conserve une seule entrée prompt dans chaque catalogue
- **AND** il ne lance pas le prompt et ne promet pas une slash native automatiquement enregistrée

### Requirement: Présentation native des commandes
CM SHALL référencer le SKILL.md réel de chaque skill disponible, avec le
libellé CM, PLLM, TFL, TCU, LM ou Prompt dans Commande. Les syntaxes $… SHALL
rester dans Utilisation. Sans référence, CM SHALL afficher le nom seul, sans
URI ou icône inventée. Les deux distributions TCU SHALL déclarer
display_name: TCU dans agents/openai.yaml avec un contenu identique.

#### Scenario: Présentation uniforme de TCU
- **WHEN** le skill TCU est disponible dans la session lors de la consultation
- **THEN** sa première cellule porte le libellé TCU et référence son SKILL.md réel, selon la même règle que les autres entrées
- **AND** $tcu [check] reste dans Utilisation et aucune mise à jour n'est exécutée

### Requirement: Préservation des copies et qualification de distribution
Les copies autonomes et embarquées de CM, PLLM, TFL, TCU, LM et prompt SHALL rester
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

### Requirement: Distribution du plugin TCU
La marketplace SHALL référencer ./plugins/tcu avec un manifeste de release
commune et skills: ./skills/. Elle SHALL conserver CM, PLLM, TFL, LM et prompt.
Le projet SHALL fournir skills/tcu/, sa copie embarquée, le lien relatif
.agents/skills/tcu et .codex/commands/TCU.md. Les six manifestes, VERSION,
README et pyproject.toml SHALL déclarer la même release commune.

#### Scenario: Résolution TCU
- **WHEN** le catalogue et le paquet TCU sont vérifiés
- **THEN** les six plugins, les sources et le script embarqué sont présents et leurs versions alignées
- **AND** le paquet TCU copié isolément résout son script sans dépendre du dépôt

### Requirement: Distribution du plugin prompt
La marketplace SHALL référencer ./plugins/prompt, avec un manifeste de release
commune et skills: ./skills/. Le projet SHALL fournir skills/prompt/, sa copie
embarquée, .codex/commands/prompt.md et le lien relatif .agents/skills/prompt.
Le paquet SHALL contenir son résolveur mais SHALL NOT embarquer les prompts
du référentiel externe. Les six plugins SHALL partager la release du projet.

#### Scenario: Paquet autonome
- **WHEN** le paquet prompt est copié isolément
- **THEN** son script fonctionne avec un projet explicite contenant DEVOPS.md
- **AND** aucun fichier du dépôt Tools Codex n'est nécessaire hors du paquet

## ADDED Requirements

### Requirement: Distribution LM dans la marketplace et découverte locale
La marketplace SHALL référencer ./plugins/lm, manifeste de release commune,
skills: ./skills/ et skill lm embarqué. Le projet SHALL fournir skills/lm/,
sa copie embarquée identique, .codex/commands/LM.md et le lien relatif
.agents/skills/lm vers ../../skills/lm. agents/openai.yaml SHALL afficher LM.
La commande source SHALL déléguer au skill sans promettre une slash native.
Les versions VERSION, pyproject.toml, README et six plugins SHALL être 0.7.6
pour cette livraison.

#### Scenario: Catalogue CM et paquet LM
- **WHEN** le catalogue CM et le paquet LM isolé sont contrôlés
- **THEN** LM et ses syntaxes sont présents dans les deux CM et le paquet résout ses scripts
- **AND** les six plugins partagent la release commune sans installation globale
