## ADDED Requirements

### Requirement: Effort vérifiable indépendant du catalogue et de l'historique
PLLM SHALL exiger une capacité HIGH ou XHIGH vérifiable pour tout candidat,
y compris DeepSeek direct. HIGH SHALL être préféré, XHIGH le seul repli.
Un exclu SHALL NOT être généré, sélectionné ou affiché dans les tableaux ;
son motif SHALL rester dans le JSON. Un forçage exclu SHALL échouer sans
substitution. Les six politiques SHALL rester présentes dans l'état interne.

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie une liste contenant high ou xhigh, ou null explicite signifiant tous les efforts
- **THEN** le candidat satisfait le filtre d'effort sous réserve des autres critères
- **AND** une clé absente, une valeur invalide, un booléen reasoning ou supports_max_tokens seul reste exclu

#### Scenario: Ancien catalogue ou résultat historique
- **WHEN** un modèle précédemment retenu n'a pas de preuve d'effort admissible
- **THEN** il ne peut être sélectionné, généré ou affiché malgré son historique

#### Scenario: Cible forcée sans effort vérifiable
- **WHEN** un rang forcé désigne un modèle sans preuve HIGH/XHIGH
- **THEN** il est refusé sans génération ni substitution

#### Scenario: Candidat direct sans preuve
- **WHEN** le modèle DeepSeek direct n'a pas de capacité HIGH/XHIGH vérifiable
- **THEN** il est exclu avant génération et son identité n'apparaît pas dans les tableaux

### Requirement: Plafond EUR OpenRouter réappliqué
PLLM SHALL vérifier le coût moyen de base OpenRouter au plafond inclusif de
0,20 EUR/M avec le dernier taux BCE publié vérifié. Il SHALL recalculer depuis
les prix USD natifs sans faire confiance à une moyenne EUR historique et
SHALL conserver la provenance. Une conversion invérifiable SHALL empêcher
l'admission de ces candidats, y compris les rangs forcés et anciens catalogues.
Les priorités, catégories, contrôles de ressources et seuils de performance
SHALL rester inchangés.

#### Scenario: Ancien catalogue dépassant le nouveau plafond
- **WHEN** un candidat OpenRouter dépasse 0,20 EUR/M au taux courant
- **THEN** il est exclu avant génération même si son ancien catalogue le retenait

#### Scenario: Gratuit général après retrait du tableau
- **WHEN** les modes 3/4 lisent un catalogue TFL publié sans tableau général
- **THEN** ils peuvent toujours consommer les gratuits opencode admissibles du JSON

## MODIFIED Requirements

### Requirement: Contrat Low propre au transport
Le contrat historique Low SHALL être remplacé par HIGH, puis XHIGH seulement
si HIGH est indisponible et XHIGH pris en charge. Chat Completions SHALL
utiliser reasoning_effort ; Responses reasoning.effort ; Messages
output_config.effort avec thinking adaptive ; DeepSeek thinking activé et
reasoning_effort. Chaque transport SHALL exiger une preuve publiée de HIGH ou XHIGH ; un budget seul SHALL NOT suffire. Aucun repli vers un niveau inférieur SHALL être effectué.

#### Scenario: Gratuit OpenCode en Chat Completions
- **WHEN** un candidat OpenCode utilise chat_completions
- **THEN** la requête contient reasoning_effort=high sans thinking
- **AND** le modèle doit réussir ses mesures actuelles avant de devenir valide

#### Scenario: Autres transports et DeepSeek
- **WHEN** Responses, Messages ou DeepSeek direct sont évalués
- **THEN** leurs paramètres HIGH ou XHIGH effectif propres restent préservés

#### Scenario: HIGH absent et XHIGH annoncé
- **WHEN** les métadonnées excluent HIGH et annoncent XHIGH
- **THEN** seul XHIGH est demandé et le niveau effectif est tracé

#### Scenario: Aucun niveau autorisé
- **WHEN** ni HIGH ni XHIGH ne sont pris en charge
- **THEN** le candidat est invalide sans requête de performance ni repli inférieur
