## MODIFIED Requirements

### Requirement: Contrat Low propre au transport
Le contrat historique Low SHALL être remplacé par HIGH, puis XHIGH seulement
si HIGH est indisponible et XHIGH pris en charge. Chat Completions SHALL
utiliser reasoning_effort sauf équivalence documentée ; Responses reasoning.effort ;
Messages output_config.effort avec thinking adaptive ; DeepSeek thinking activé
et reasoning_effort. Chaque transport SHALL exiger une preuve publiée de HIGH
ou XHIGH ; un budget seul SHALL NOT suffire. Aucun repli vers un niveau
inférieur SHALL être effectué.

#### Scenario: Gratuit OpenCode en Chat Completions
- **WHEN** un candidat OpenCode utilise chat_completions sans équivalence documentée
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

## ADDED Requirements

### Requirement: Consommation des preuves et équivalences documentées
PLLM SHALL préserver les preuves TFL par fournisseur, modèle et protocole.
Il SHALL accepter HIGH/XHIGH officiellement reconnus même sans intensité
distincte et utiliser uniquement les paramètres équivalents documentés sur
sa route publiée. Un effort ou contexte encore invérifiable SHALL déclencher
le workflow d'investigation du LLM avant toute admission ; un contexte
invérifiable après investigation SHALL rester exclu.

#### Scenario: Équivalence de transport
- **WHEN** une preuve vérifiée autorise HIGH via thinking.type=enabled sur Chat Completions
- **THEN** PLLM utilise ce paramètre et trace HIGH et son équivalence sans modifier la route

#### Scenario: Preuve ou contexte absent
- **WHEN** aucun résultat d'investigation ne permet l'admission
- **THEN** le modèle n'atteint pas la génération et le motif reste auditable
