## MODIFIED Requirements

### Requirement: Effort vérifiable avant admission
TFL SHALL tester Medium sur le transport publié pour les gratuits admissibles,
même si leurs métadonnées sont absentes ou ne déclarent pas cet effort. Une
réponse complète SHALL prouver l'acceptation du paramètre sans établir l'effort
interne. Contexte, gratuité, réponse complète, TTFT et débit restent requis.
TFL SHALL conserver les payants OpenRouter comme catalogue tarifaire sans benchmark ; PLLM mode5 SHALL vérifier Medium et ses performances lors de sa propre évaluation.

#### Scenario: Modèle benchmarké sans preuve
- **WHEN** un modèle gratuit n'a pas de métadonnée Medium avant test
- **THEN** TFL lui envoie le paramètre Medium sur le transport publié
- **AND** une réponse complète prouve l'acceptation du paramètre sous réserve des seuils de performance

#### Scenario: Payant OpenRouter sans preuve
- **WHEN** Medium est absent ou non pris en charge dans les métadonnées d'un modèle OpenRouter payant qui satisfait contexte/prix/modalités
- **THEN** le modèle est conservé dans OpenRouter sans benchmark ni investigation Medium bloquante

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie medium ou null explicite, ou qu'une requête Medium complète est acceptée par l'API
- **THEN** l'acceptation du paramètre satisfait le filtre d'effort sous réserve des autres critères
- **AND** un budget seul ou un booléen reasoning seul ne prouve pas l'acceptation

#### Scenario: Medium absent
- **WHEN** supported_efforts publie une liste sans medium
- **THEN** TFL essaie le paramètre Medium sur l'API et conserve l'exclusion seulement si l'API le refuse ou si un autre critère échoue

#### Scenario: Tous les efforts explicitement pris en charge
- **WHEN** supported_efforts publie explicitement null ou l'API accepte une requête complète en Medium
- **THEN** le candidat peut être qualifié sous réserve des autres critères

#### Scenario: Budget seul
- **WHEN** le modèle ne publie qu'un budget de raisonnement sans niveau Medium
- **THEN** le budget seul ne prouve pas l'acceptation, mais TFL peut établir celle-ci par une requête Medium réelle

