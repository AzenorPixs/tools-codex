## MODIFIED Requirements

### Requirement: Catalogue des commandes cohérent
Le skill CM SHALL afficher un tableau français avec Commande, Utilisation et
Description pour CM, PLLM, TFL, TCU, LM et PROMPT. Les deux copies SHALL
conserver les invocations $…, les arguments documentés et les déclencheurs
canoniques en majuscules, avec alias en minuscules. La consultation SHALL NOT
exécuter les actions listées ni inventer une slash native. Toute évolution
autorisée SHALL actualiser les deux catalogues.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm, /CM ou son alias /cm est invoqué
- **THEN** le tableau décrit les six invocations avec les libellés en majuscules
- **AND** aucune mise à jour, évaluation ou exécution de prompt n'est déclenchée

#### Scenario: Wrapper CM
- **WHEN** .codex/commands/CM.md est utilisé
- **THEN** il délègue au skill CM et conserve une seule entrée PROMPT dans chaque catalogue
- **AND** il ne lance pas le prompt et ne promet pas une slash native automatiquement enregistrée

### Requirement: Présentation native des commandes
CM SHALL référencer le SKILL.md réel de chaque skill disponible, avec le
libellé CM, PLLM, TFL, TCU, LM ou PROMPT dans Commande. Les syntaxes $… SHALL
rester dans Utilisation. Sans référence, CM SHALL afficher le nom seul, sans
URI ou icône inventée. Les six skills SHALL déclarer leur display_name en
majuscules dans agents/openai.yaml avec des copies identiques dans les deux
distributions.

#### Scenario: Présentation uniforme
- **WHEN** un des six skills est disponible dans la session lors de la consultation
- **THEN** sa première cellule porte son libellé en majuscules et référence son SKILL.md réel
- **AND** sa syntaxe $… reste dans Utilisation et aucune action n'est exécutée

#### Scenario: Présentation uniforme de TCU
- **WHEN** le skill TCU est disponible dans la session lors de la consultation
- **THEN** sa première cellule porte le libellé TCU et référence son SKILL.md réel, selon la même règle que les autres entrées
- **AND** $tcu [check] reste dans Utilisation et aucune mise à jour n'est exécutée

### Requirement: Distribution du plugin prompt
La marketplace SHALL référencer ./plugins/prompt, avec un manifeste de release
commune et skills: ./skills/. Le projet SHALL fournir skills/prompt/, sa copie
embarquée, .codex/commands/PROMPT.md et le lien relatif .agents/skills/prompt.
Le manifeste et le skill SHALL afficher PROMPT. Le paquet SHALL contenir son
résolveur mais SHALL NOT embarquer les prompts du référentiel externe. Les
six plugins SHALL partager la release du projet.

#### Scenario: Paquet autonome
- **WHEN** le paquet prompt est copié isolément
- **THEN** son script fonctionne avec un projet explicite contenant DEVOPS.md
- **AND** aucun fichier du dépôt Tools Codex n'est nécessaire hors du paquet

## ADDED Requirements

### Requirement: Déclarations canoniques des six commandes en majuscules
Tools Codex SHALL fournir exactement les six commandes sources CM.md, PLLM.md,
TFL.md, TCU.md, LM.md et PROMPT.md sous .codex/commands/. Les commandes SHALL
documenter /CM, /PLLM, /TFL, /TCU, /LM et /PROMPT comme déclencheurs canoniques.
Les identifiants techniques, chemins de skills et invocations $… SHALL rester
inchangés. Les déclarations SHALL NOT promettre une slash native automatiquement
enregistrée.

#### Scenario: Qualification du catalogue distribué
- **WHEN** les commandes, skills, métadonnées et manifestes de la release sont contrôlés
- **THEN** les six noms de commande et d'affichage sont en majuscules dans les deux distributions
- **AND** les identifiants techniques et les arguments restent inchangés

#### Scenario: Ancienne invocation
- **WHEN** une ancienne invocation /cm, /pllm, /tfl ou /prompt est reçue par le skill
- **THEN** elle conserve le comportement documenté de la commande canonique correspondante
- **AND** la consultation de CM ne lance aucune action
