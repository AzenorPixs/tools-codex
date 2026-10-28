## MODIFIED Requirements

### Requirement: Mesures concluantes du modèle sélectionné
Tous les modes SHALL exiger réponse complète, comptage fiable et
mesures actuelles. Contexte d'entrée ≥1M SHALL être vérifié sans benchmark
d'un million de tokens. Les gratuits 3/4/6 exigent TTFT <30 s et débit >20 ;
les payants benchmarkés 1/2/5/7 exigent TTFT <90 s et débit >15. Mode5 exige aussi candidat payant, contexte, coût ≤0,10 EUR/M et solde positif. Le protocole reste
inchangé pour les modes mesurés ; le parcours s'arrête au premier succès.

#### Scenario: Limites strictes distinctes
- **WHEN** un gratuit atteint TTFT 30 s ou débit 20 tokens/s, ou un payant atteint TTFT 90 s ou débit 15 tokens/s
- **THEN** ce candidat est invalide

#### Scenario: Seuil payant conservé
- **WHEN** un payant mesure TTFT 70,4 s et satisfait tous les autres critères
- **THEN** son seuil TTFT est satisfait ; ce même TTFT échoue pour un gratuit

#### Scenario: Mesure non concluante
- **WHEN** une réponse est tronquée, absente ou sans comptage fiable
- **THEN** elle ne constitue pas une réussite et aucun résultat historique ne la remplace

#### Scenario: Candidat limité ou incomplet
- **WHEN** un candidat échoue après ses paliers ou reçoit une limitation fournisseur
- **THEN** seul le candidat suivant admissible de la catégorie autorisée peut le remplacer
- **AND** ce remplaçant exige ses propres contrôles et mesures

#### Scenario: Limites strictes gratuites
- **WHEN** un mode 3/4/6 mesure TTFT ≥30 s ou débit ≤20 tokens/s
- **THEN** ce candidat reste invalide même si le quota du compte est disponible

#### Scenario: Gratuit valide
- **WHEN** un gratuit vérifié de contexte ≥1M donne une réponse complète à TTFT 29,9 s et débit 20,1 tokens/s
- **THEN** ses seuils sont satisfaits sans contrôle de quota

#### Scenario: Limites des autres modes
- **WHEN** un candidat payant de mode 1/2/5/7 mesure TTFT ≥90 s ou débit ≤15 tokens/s
- **THEN** son candidat reste invalide

#### Scenario: Limites strictes
- **WHEN** un candidat atteint TTFT 30 s ou débit 20 tokens/s pour un candidat gratuit, ou TTFT 90 s ou débit 15 tokens/s pour les candidats payants
- **THEN** ce candidat est invalide

#### Scenario: Repli après limitation fournisseur
- **WHEN** une limitation HTTP 429 conduit à choisir un autre modèle de la catégorie autorisée
- **THEN** ce candidat exige ses propres contrôles et mesures concluantes
- **AND** l'épuisement du dernier palier ne transforme pas le repli en réussite

#### Scenario: TTFT sous la nouvelle limite
- **WHEN** un candidat payant benchmarké de mode1/2/5/7 mesure 70,4 s et satisfait les autres critères
- **THEN** son seuil TTFT est satisfait ; ce même TTFT échoue pour un candidat gratuit

#### Scenario: Limite stricte de TTFT atteinte
- **WHEN** le TTFT atteint 30 s pour un candidat gratuit ou 90 s pour les candidats payants benchmarkés
- **THEN** le candidat reste invalide même avec un débit suffisant

### Requirement: Catégories payante et gratuite exclusives
Les modes 1/2 SHALL examiner exclusivement les payants Go. Les modes 3/4
SHALL examiner exclusivement les gratuits Go, et le mode6 SHALL examiner
exclusivement les gratuits OpenRouter, indépendamment des ressources. Mode5
SHALL examiner exclusivement les payants OpenRouter avec crédit positif,
contexte ≥1M et coût moyen ≤0,10 EUR/M, avec benchmark Medium payant.
Mode7 SHALL conserver DeepSeek direct. Les modes 1/2/5/7 SHALL NOT basculer
vers un candidat gratuit.

#### Scenario: Compte Go disponible ou épuisé
- **WHEN** les gratuits 3/4 sont évalués
- **THEN** leur catégorie reste gratuite indépendamment des ressources du compte

#### Scenario: Candidat au nom free mais payant
- **WHEN** le nom contient free mais les prix vérifiés ne sont pas tous nuls
- **THEN** ce candidat n'est pas admissible en 3/4

#### Scenario: Gratuit OpenRouter forcé en mode payant
- **WHEN** un rang OpenRouter explicitement demandé en mode5 désigne un gratuit
- **THEN** il échoue comme catégorie incompatible sans substitution ni génération

#### Scenario: Candidat payant au nom free
- **WHEN** un candidat porte free dans son nom mais ses prix ne sont pas tous nuls
- **THEN** il n'est pas admissible en 3/4 et sa catégorie payante exige les contrôles correspondants

#### Scenario: Retour au payant après repli général
- **WHEN** un historique ancien désigne un gratuit général en mode1/2 puis les quotas Go reviennent
- **THEN** seuls les payants Go peuvent représenter 1/2 après leurs nouveaux contrôles ; les gratuits sont en 3/4

#### Scenario: Crédit épuisé et modèle payant au nom free
- **WHEN** le solde OpenRouter est nul et un nom free porte un prix non nul
- **THEN** le mode5 reste invalide sans génération payante ou gratuite

#### Scenario: Ancien catalogue général payant
- **WHEN** un ancien catalogue contient des payants généraux admissibles, avec ou sans candidat Go
- **THEN** les modes 1/2, forcés ou ordinaires, ne sélectionnent et ne testent que les payants opencode_go
- **AND** aucun résultat historique général ne remplace un candidat Go absent ou invalide

#### Scenario: Ancien catalogue général gratuit
- **WHEN** un ancien catalogue contient des gratuits généraux admissibles, avec ou sans candidat Go
- **THEN** les modes 3/4, forcés ou ordinaires, ne sélectionnent et ne testent que les gratuits opencode_go
- **AND** l'échec ou l'absence des gratuits Go ne déclenche aucun repli général

### Requirement: Gratuité vérifiable et retour au payant
La gratuité des modes 3/4/6 SHALL exiger prix publiés d'entrée et de sortie
nuls avec variantes compatibles, jamais un nom seul. Contexte ≥1M, filtres
TFL, accès et transport SHALL être préservés ; Medium SHALL être exigé par
tous les modes benchmarkés, y compris le mode5. Les
catégories SHALL rester fixes pendant l'invocation. Les ressources des modes
payants SHALL être relues à chaque nouvelle invocation, sans résultat hérité.

#### Scenario: Ressources rétablies
- **WHEN** les quotas Go, le crédit OpenRouter ou les soldes DeepSeek évoluent à une nouvelle invocation
- **THEN** les modes payants consultent à nouveau leurs contrôles applicables
- **AND** les modes gratuits 3/4/6 restent sans contrôle de ressources

#### Scenario: Ancien résultat gratuit OpenRouter
- **WHEN** un historique valide contient un ancien gagnant OpenRouter gratuit en mode5
- **THEN** il reste lisible mais ne valide pas l'évaluation actuelle et aucun test gratuit n'est lancé

#### Scenario: Crédit OpenRouter rétabli pendant le repli
- **WHEN** le crédit revient après l'arrêt du mode5 pour épuisement
- **THEN** aucune transition gratuite n'est effectuée et une nouvelle invocation relit le crédit avant de tester ses payants

#### Scenario: Quotas rétablis pendant les tests gratuits
- **WHEN** les ressources reviennent pendant les tests gratuits 3/4
- **THEN** ces modes restent gratuits sans contrôle de ressources et mode5 conserve sa catégorie payante

### Requirement: Invariants du classement tarifaire
Les priorités 1 à 7 SHALL respecter les seuils benchmarkés gratuits/payants,
les quotas, le raisonnement, les forçages et le protocole 8. Le mode5 SHALL
refuser les candidats gratuits et benchmarker les payants selon les seuils payants.
Le JSON SHALL tracer les candidats visités et leurs contrôles ;
active SHALL s'arrêter au premier mode valide. Le rapport SHALL conserver
ses huit colonnes.

#### Scenario: Publication et priorités préservées
- **WHEN** plusieurs politiques valides ont été évaluées selon leurs règles
- **THEN** la première par priorité 1 à 7 est sélectionnée avec huit colonnes inchangées
- **AND** son prix courant et les preuves des candidats visités restent auditables

### Requirement: Effort vérifiable indépendant du catalogue et de l'historique
PLLM SHALL demander le paramètre `medium` pour tout candidat benchmarké,
y compris OpenRouter payant au mode5 et DeepSeek direct au mode7. L'acceptation courante de l'API SHALL suffire même si le
fournisseur convertit ou ignore l'effort ; elle ne mesure pas l'effort interne.
Un refus SHALL invalider le candidat sans autre niveau. Les exclus SHALL rester
non sélectionnés et conserver leur motif et leurs preuves JSON ; les sept
politiques SHALL rester présentes.

#### Scenario: Mapping Medium vers High
- **WHEN** une source officielle prouve que l'API accepte Medium comme alias de High
- **THEN** le candidat satisfait l'exigence d'acceptation du paramètre, sous réserve des ressources, du contexte, de la réponse et des seuils de performance
- **AND** le rapport conserve le mapping sans prétendre que l'effort interne est Medium

#### Scenario: Paramètre Medium refusé par l'API
- **WHEN** un appel réel avec le paramètre Medium reçoit un refus de compatibilité reconnu
- **THEN** le candidat reste invalide sans reprise avec un autre effort
- **AND** le diagnostic précis et les preuves filtrées restent dans les exclusions JSON

#### Scenario: Nettoyage d'une exclusion historique
- **WHEN** le nettoyage de publication retire un candidat qui n'a aucune preuve d'acceptation du paramètre
- **THEN** le rapport conserve le motif dans la cause de la politique et dans les exclusions JSON
- **AND** l'identifiant du candidat reste absent des colonnes utilisateur

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie medium, null explicite, ou une requête courante avec medium est acceptée par l'API
- **THEN** le candidat satisfait le critère d'acceptation du paramètre sous réserve des autres critères
- **AND** une métadonnée absente ou invalide seule ne prouve pas l'acceptation, mais ne bloque pas un test réel

#### Scenario: Ancien catalogue ou résultat historique
- **WHEN** un candidat benchmarké précédemment retenu n'a pas de preuve d'effort admissible
- **THEN** il ne peut être sélectionné, généré ou affiché malgré son historique
- **AND** le mode5 sans benchmark antérieur reste invalide jusqu'à une nouvelle mesure concluante

#### Scenario: Cible forcée sans effort vérifiable
- **WHEN** un rang forcé désigne un modèle sans preuve Medium
- **THEN** seule la candidate forcée est testée avec le paramètre medium, sans substitution
- **AND** elle reste invalide si l'API refuse ce paramètre
- **AND** un rang du mode5 exige aussi solde positif, Medium et benchmark payant concluant

#### Scenario: Candidat direct sans preuve
- **WHEN** le modèle DeepSeek direct n'a pas de capacité Medium vérifiable
- **THEN** PLLM envoie medium sur la route directe publiée et vérifie la réponse réelle
- **AND** une réponse API complète établit l'acceptation, même si le fournisseur mappe ou ignore medium

#### Scenario: Preuve publiée liée au transport
- **WHEN** un candidat TFL publie une preuve d'acceptation Medium pour son identifiant et son protocole courants
- **THEN** PLLM recontrôle cette source avant génération et conserve le résultat dans l'audit
- **AND** l'absence ou l'inaccessibilité de cette preuve déclenche un essai API avec medium, sans conclure à un refus

### Requirement: Consommation des preuves et équivalences documentées
PLLM SHALL préserver les preuves TFL par fournisseur, modèle et protocole.
Les modes benchmarkés SHALL admettre uniquement Medium après vérification et
utiliser les paramètres documentés sur leur route publiée, y compris le mode5 payant OpenRouter. Un contexte encore invérifiable SHALL déclencher
le workflow d'investigation du LLM avant toute admission ; un contexte
invérifiable après investigation SHALL rester exclu.

#### Scenario: Équivalence de transport
- **WHEN** une preuve vérifiée établit une équivalence Medium vers thinking.type=enabled sur Chat Completions
- **THEN** PLLM utilise ce paramètre et trace son équivalence sans modifier la route

#### Scenario: Preuve ou contexte absent
- **WHEN** aucun résultat d'investigation ne permet l'admission
- **THEN** le modèle n'atteint pas la génération et le motif reste auditable

### Requirement: Effort demandé exclusivement Medium
PLLM SHALL demander exclusivement le paramètre `medium` pour les politiques
benchmarkées, y compris le mode5, les forçages de rang et chaque transport. Une réponse API complète SHALL
établir l'acceptation du paramètre même si l'effort interne est converti,
ignoré ou non appliqué. Un refus de Medium SHALL invalider le candidat sans
repli vers un autre effort.

#### Scenario: Demande forcée ou transport non compatible
- **WHEN** une cible forcée ou un transport refuse le paramètre medium
- **THEN** le candidat est déclaré invalide sans génération à un autre effort

### Requirement: Historique limité aux résultats Medium
PLLM SHALL NOT valider un résultat historique benchmarké dont le paramètre
`medium` demandé ou son acceptation API n'est pas explicitement établi. PLLM SHALL
invalider ces résultats avant affichage et sélection, conserver leur motif
dans les exclusions et ne pas réutiliser leurs paliers. Une mesure historique
ne prouve pas l'acceptation API courante. Cette règle s'applique aussi aux anciens résultats non benchmarkés du mode5.

#### Scenario: Historique incompatible malgré une capacité Medium
- **WHEN** le résultat ou une de ses tentatives historiques n'enregistre pas explicitement la demande medium et son acceptation API
- **THEN** PLLM l'invalide avant affichage et sélection
- **AND** conserve le motif d'exclusion sans réutiliser son palier

## ADDED Requirements

### Requirement: Benchmark payant du mode5 et parcours des candidats
Le mode5 SHALL exiger réponse complète, comptage fiable, TTFT <90 s et débit réponse seule >15 tokens/s au protocole 8 avec Medium. Hors forçage, il SHALL parcourir les payants par coût courant croissant et ordre TFL à prix égal. Le premier succès SHALL arrêter le parcours ; les tentatives et mesures SHALL rester auditables sans secret.

#### Scenario: Premier payant conforme
- **WHEN** le premier payant admissible réussit le benchmark Medium avec solde positif
- **THEN** il est retenu avec ses mesures et son palier et aucun candidat suivant n'est testé

#### Scenario: Échec puis succès
- **WHEN** le moins cher échoue aux quatre paliers ou reçoit un refus non bloquant et le suivant réussit
- **THEN** le suivant est retenu avec ses propres contrôles et mesures et les tentatives du premier restent auditées

#### Scenario: Rang forcé en échec
- **WHEN** le candidat payant explicitement forcé échoue au benchmark
- **THEN** le mode reste invalide sans substituer un autre rang

### Requirement: Paliers et contrôles du benchmark mode5
Le mode5 SHALL contrôler le solde avant chaque requête et utiliser les paliers 1024, 2048, 4096, 8192 avec 120 s maximum par requête. Il SHALL commencer au dernier succès de même identité ou à 1024. Une erreur d'authentification ou de ressources SHALL arrêter le mode. Un HTTP 400 ou 429 SHALL arrêter le candidat sans autre effort ni attente programmée.

#### Scenario: Authentification ou ressources bloquantes
- **WHEN** le contrôle du solde échoue ou l'authentification est refusée avant ou pendant les essais
- **THEN** le mode reste invalide sans génération supplémentaire ni substitution gratuite

#### Scenario: Reprise du palier mémorisé
- **WHEN** une nouvelle invocation retrouve une réussite de même identité Medium au protocole 8
- **THEN** son premier essai reprend ce palier après un nouveau contrôle du solde

### Requirement: Invalidation du mode5 non benchmarké
PLLM SHALL invalider les anciens résultats mode5 sans benchmark Medium concluant avant affichage ou sélection. Ils SHALL NOT amorcer un palier ni remplacer les mesures courantes. Le chargement SHALL préserver les fichiers historiques jusqu'à la publication normale.

#### Scenario: Ancienne validation sans benchmark
- **WHEN** un historique mode5 valide uniquement prix, contexte et solde
- **THEN** il ne peut ni représenter un succès benchmarké ni amorcer un palier et reste invalide jusqu'à une nouvelle évaluation conforme
