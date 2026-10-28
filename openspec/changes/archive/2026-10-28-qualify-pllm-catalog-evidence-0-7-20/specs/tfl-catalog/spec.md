## MODIFIED Requirements

### Requirement: Effort vérifiable avant admission
TFL SHALL tester Medium sur le transport publié pour les gratuits admissibles,
même si leurs métadonnées sont absentes ou ne déclarent pas cet effort. Une
réponse complète SHALL prouver l'acceptation du paramètre sans établir l'effort
interne. Contexte, gratuité, réponse complète, TTFT, débit, prix et LM restent
requis. Le mode5 payant OpenRouter n'exige ni Medium ni benchmark.

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

### Requirement: Efforts publiés et équivalences documentées
TFL SHALL normaliser reasoning_options et conserver la preuve Medium par
fournisseur, modèle et protocole. Un alias ou une réponse complète acceptant
`medium` satisfait le critère de paramètre, sans prouver l'effort interne. Seul
le paramètre Medium du transport publié SHALL être envoyé.

#### Scenario: Medium équivaut au raisonnement activé
- **WHEN** les sources officielles ou une réponse API complète établissent l'acceptation de Medium sur le protocole utilisé
- **THEN** Medium est admissible et le paramètre documenté du protocole est envoyé
- **AND** les autres critères, contrôles et seuils restent obligatoires

### Requirement: Effort courant exclusivement Medium pour les benchmarks
TFL SHALL demander exclusivement le paramètre `medium` pour ses benchmarks
gratuits. Une réponse API complète établit son acceptation même si le fournisseur
la convertit ou l'ignore ; cette preuve ne SHALL NOT être décrite comme une
mesure de l'effort interne. Un refus de Medium SHALL exclure le candidat sans
repli vers un autre effort. Les payants OpenRouter ne sont pas benchmarkés.

#### Scenario: Plusieurs capacités publiées
- **WHEN** les métadonnées d'un candidat déclarent Medium et d'autres capacités
- **THEN** TFL demande Medium et n'envoie aucune autre valeur d'effort
- **AND** seul un benchmark réussi avec la requête Medium peut entrer dans le catalogue

#### Scenario: Medium indisponible ou refusé
- **WHEN** le transport refuse Medium ou ne fournit aucune réponse complète à la requête
- **THEN** le candidat est exclu avec la cause filtrée
- **AND** aucune requête de repli n'est effectuée

### Requirement: Investigation des preuves manquantes
Pour Go et OpenRouter, un contexte inconnu SHALL déclencher une recherche
officielle. Le JSON SHALL tracer fournisseur, ID exact, champ, sources, dates,
méthode d'empreinte et conclusion. Le HTML est empreint sur son texte visible
normalisé ; les autres sources le sont sur les octets reçus. Medium inconnu
se vérifie sur la route publiée ; une réponse complète prouve l'acceptation du
paramètre, pas l'effort interne. Un contexte invérifiable reste exclu.

#### Scenario: Contexte encore invérifiable
- **WHEN** l'investigation ne permet pas de vérifier le contexte
- **THEN** le modèle reste exclu avec les sources examinées et la conclusion
- **AND** aucun contexte ni seuil plus faible n'est inventé

#### Scenario: Source devenue différente ou inaccessible
- **WHEN** une preuve supplémentaire ne correspond plus à sa source courante
- **THEN** elle ne permet aucune admission et une nouvelle investigation est requise

#### Scenario: Balisage HTML volatil sans changement documentaire
- **WHEN** une source HTML change son balisage ou ses scripts sans modifier son texte visible
- **THEN** son empreinte normalisée reste identique
- **AND** une modification du texte visible déclenche une nouvelle investigation

#### Scenario: Effort inconnu éprouvé par appel réel
- **WHEN** Medium n'est pas publié dans les métadonnées mais une réponse complète suit la requête avec ce paramètre
- **THEN** TFL enregistre l'acceptation API et continue d'appliquer les seuils de performance
- **AND** le rapport ne prétend pas que le fournisseur a utilisé un niveau interne Medium
