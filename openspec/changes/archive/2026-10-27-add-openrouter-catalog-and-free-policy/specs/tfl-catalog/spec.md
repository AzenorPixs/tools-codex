## MODIFIED Requirements

### Requirement: Seuils de sélection vérifiables
TFL SHALL vérifier contexte ≥1M, coût moyen ≤0,50 USD/M Go et ≤0,20 EUR/M
OpenRouter au taux BCE. Prix/contexte inconnus sont exclus. Les payants
OpenRouter satisfaisant contexte, coût, modalités et LM restent admissibles
sans Medium. Les gratuits vérifiés SHALL réussir réponse complète en Medium,
TTFT <30 s et débit >20 tokens/s avant inclusion ; échecs et preuves restent
dans excluded_models.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte ou le coût d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

#### Scenario: Gratuit échoué ou non mesurable
- **WHEN** le gratuit échoue sur un seuil, l'effort Medium, l'accès, HTTP ou la mesure
- **THEN** il est exclu de models avec sa cause, ses tentatives et ses mesures disponibles

#### Scenario: Payant sans Medium
- **WHEN** un payant OpenRouter vérifie contexte ≥1M, coût ≤0,20 EUR/M, modalités et liste noire, mais ne publie pas Medium
- **THEN** il reste dans models avec ses métadonnées d'effort, sans investigation Medium bloquante

#### Scenario: Seuils gratuits stricts
- **WHEN** le TTFT atteint 30 s ou le débit atteint au plus 20 tokens/s
- **THEN** le gratuit est exclu même si ses prix, contexte et effort Medium sont admissibles

### Requirement: Effort vérifiable avant admission
TFL SHALL exiger une capacité Medium vérifiable avant classement et benchmark
des modèles gratuits, y compris OpenRouter. Les payants OpenRouter peuvent être
classés selon contexte/prix/modalités sans preuve Medium, car PLLM mode5 ne
benchmarke pas. Les autres modèles sans preuve SHALL rester auditables dans le
JSON et SHALL NOT apparaître dans les tableaux de benchmark gratuit.

#### Scenario: Modèle benchmarké sans preuve
- **WHEN** Medium n'est pas vérifiable pour un candidat gratuit ou Go
- **THEN** le modèle est exclu avant génération et motivé dans le JSON

#### Scenario: Payant OpenRouter sans preuve
- **WHEN** Medium est absent ou non pris en charge pour un modèle OpenRouter payant qui satisfait contexte/prix/modalités
- **THEN** le modèle est conservé dans la section OpenRouter sans benchmark ni investigation Medium bloquante

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie une liste contenant medium, ou null explicite signifiant tous les efforts
- **THEN** le candidat satisfait le filtre d'effort sous réserve des autres critères
- **AND** une clé absente, une valeur invalide, un booléen reasoning ou supports_max_tokens seul reste exclu

#### Scenario: Medium absent
- **WHEN** supported_efforts publie une liste qui ne contient pas medium
- **THEN** le candidat est exclu avant le test

#### Scenario: Tous les efforts explicitement pris en charge
- **WHEN** supported_efforts publie explicitement null
- **THEN** le candidat peut être testé en Medium sous réserve des autres critères

#### Scenario: Budget seul
- **WHEN** le modèle ne publie qu'un budget de raisonnement sans preuve d'effort Medium
- **THEN** il est exclu sans équivalence de niveau inventée

### Requirement: Effort courant exclusivement Medium pour les benchmarks
TFL SHALL benchmarker les gratuits uniquement en Medium, transmettre cet
effort selon le protocole et exclure un refus sans repli. Les payants OpenRouter
ne sont pas benchmarkés et ne requièrent pas Medium pour leur admission au
mode5. D'autres capacités publiées ne changent pas l'effort demandé.

#### Scenario: Plusieurs capacités publiées

- **WHEN** les métadonnées d'un candidat déclarent Medium et d'autres capacités
- **THEN** TFL demande Medium et n'envoie aucune autre valeur d'effort
- **AND** seul un benchmark réussi avec Medium peut entrer dans le catalogue

#### Scenario: Medium indisponible ou refusé

- **WHEN** Medium n'est pas vérifiable, n'est pas pris en charge ou est refusé
  par le transport
- **THEN** le candidat est exclu du catalogue avec sa cause
- **AND** aucune requête de repli n'est effectuée
