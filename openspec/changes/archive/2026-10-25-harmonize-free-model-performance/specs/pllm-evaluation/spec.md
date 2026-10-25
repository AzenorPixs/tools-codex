## MODIFIED Requirements

### Requirement: Politiques et sélection explicites
PLLM SHALL garder six priorités : payants Go 1/2, gratuits Go/général 3/4,
OpenRouter 5 et DeepSeek 6. Les comptes et références historiques SHALL être
conservés. Les modèles 1 à 5 SHALL provenir de TFL avec route, fournisseur et
date. HIGH SHALL être le défaut, avec repli XHIGH pris en charge lorsque HIGH
est indisponible. La première politique valide après classement SHALL être
sélectionnée.

#### Scenario: Sélection selon la priorité
- **WHEN** plusieurs politiques sont valides
- **THEN** la première par priorité 1 à 6 est retenue indépendamment du débit des autres

#### Scenario: Authentification des modes renumérotés
- **WHEN** les nouveaux modes sont évalués
- **THEN** les références existantes sont utilisées sans création ou déplacement de secret
- **AND** policy=mode1 sert à 1/3, policy=mode2 à 2/4, ancien policy=mode3 à 5 et ancien policy=mode4 à 6

### Requirement: Mesures concluantes du modèle sélectionné
Tous les modes SHALL exiger réponse complète, comptage fiable et mesures
actuelles du modèle retenu. Tous les candidats gratuits, y compris le repli OpenRouter de 5, SHALL exiger contexte ≥1M,
TTFT <30 s et débit >20 tokens/s. Les candidats payants des modes 1/2/5/6 SHALL conserver TTFT <90 s
et débit >15 tokens/s. Une troncature, erreur ou mesure absente SHALL NOT
être remplacée par un résultat historique. Tous les candidats admissibles
SHALL être comparés hors forçage.

#### Scenario: Limites strictes gratuites
- **WHEN** un mode 3/4 mesure TTFT ≥30 s ou débit ≤20 tokens/s
- **THEN** ce candidat reste invalide même si le quota du compte est disponible

#### Scenario: Gratuit valide
- **WHEN** un gratuit vérifié de contexte ≥1M donne une réponse complète à TTFT 29,9 s et débit 20,1 tokens/s
- **THEN** ses seuils sont satisfaits sans contrôle de quota

#### Scenario: Limites des autres modes
- **WHEN** un candidat payant de mode 1/2/5/6 mesure TTFT ≥90 s ou débit ≤15 tokens/s
- **THEN** son candidat reste invalide

#### Scenario: Mesure non concluante
- **WHEN** une réponse est tronquée, absente ou sans comptage fiable
- **THEN** le candidat reste invalide sans succès ni mesure inventés


#### Scenario: Candidat limité ou incomplet
- **WHEN** un candidat échoue après ses paliers ou reçoit une limitation fournisseur
- **THEN** seul un autre candidat de la catégorie autorisée peut le remplacer
- **AND** le remplaçant exige ses propres contrôles et mesures

#### Scenario: Limites strictes
- **WHEN** un candidat atteint TTFT 30 s ou débit 20 tokens/s pour un candidat gratuit, ou TTFT 90 s ou débit 15 tokens/s pour les candidats payants
- **THEN** ce candidat est invalide

#### Scenario: Repli après limitation fournisseur
- **WHEN** une limitation HTTP 429 conduit à choisir un autre modèle de la catégorie autorisée
- **THEN** ce candidat exige ses propres contrôles et mesures concluantes
- **AND** l'épuisement du dernier palier ne transforme pas le repli en réussite

#### Scenario: TTFT sous la nouvelle limite
- **WHEN** un candidat payant de mode1/2/5/6 mesure 70,4 s et satisfait les autres critères
- **THEN** son seuil TTFT est satisfait ; ce même TTFT échoue pour un candidat gratuit

#### Scenario: Limite stricte de TTFT atteinte
- **WHEN** le TTFT atteint 30 s pour un candidat gratuit ou 90 s pour les candidats payants
- **THEN** le candidat reste invalide même avec un débit suffisant

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL garder les paliers 1024, 2048, 4096, 8192 et 120 s par requête.
Les contrôles applicables SHALL précéder chaque requête, sans quota en 3/4.
Un HTTP 400/429 SHALL arrêter le candidat, hors unique repli d'effort XHIGH
autorisé. La mémoire SHALL garder les succès complets par configuration,
distinguer Low/HIGH/XHIGH et adapter le schéma 1 en 2. Une mémoire invalide
SHALL NOT être écrasée ; un palier mémorisé SHALL NOT valider l'invocation.

#### Scenario: Nouvelle politique gratuite
- **WHEN** mode3 ou mode4 est évalué pour la première fois après migration
- **THEN** son premier palier est 1024, sans réutiliser l'ancien OpenRouter ou DeepSeek
- **AND** la mémoire des anciens 3/4 est déplacée vers 5/6 lors du passage du schéma 1 au schéma 2

#### Scenario: Reprise de configuration connue
- **WHEN** une configuration possède un succès mémorisé
- **THEN** son palier peut être repris avec des mesures actuelles et les contrôles applicables

#### Scenario: HTTP 400 ou 429
- **WHEN** un candidat reçoit ce refus sans repli d'effort XHIGH autorisé
- **THEN** aucun budget supérieur n'est tenté pour ce candidat
- **AND** les autres candidats admissibles gardent leurs propres tests

#### Scenario: Troncature ou seuil non satisfait
- **WHEN** le résultat est incomplet ou hors seuil
- **THEN** le palier suivant reste possible après les contrôles applicables


#### Scenario: Plusieurs candidats et retour à une configuration connue
- **WHEN** plusieurs configurations ont été évaluées avec succès
- **THEN** leurs paliers mémorisés sont distincts et réutilisables par configuration
- **AND** un candidat changé sans réussite correspondante repart à 1024

#### Scenario: Réutilisation d'un palier réussi
- **WHEN** une réussite mémorisée correspond à la même configuration
- **THEN** l'évaluation peut reprendre à ce palier avec de nouveaux contrôles applicables
- **AND** un échec ne remplace pas la dernière réussite

#### Scenario: Configuration remplacée après HTTP 429
- **WHEN** un autre candidat autorisé remplace le modèle limité
- **THEN** ses paliers sont recalculés selon son identité
- **AND** sans réussite correspondante, il commence à 1024 tokens
- **AND** l'épuisement des candidats reste un échec sans sélection valide

#### Scenario: HTTP 400 ou 429 au premier palier
- **WHEN** une requête reçoit HTTP 400 ou HTTP 429 sans repli d'effort XHIGH autorisé
- **THEN** aucun budget supérieur n'est testé pour ce candidat dans cette invocation
- **AND** les autres candidats autorisés gardent leurs propres contrôles et tests

#### Scenario: Troncature ou seuil mesuré non satisfait
- **WHEN** le candidat reçoit une réponse tronquée ou échoue sur un seuil mesuré
- **THEN** les paliers suivants restent disponibles après les contrôles applicables

#### Scenario: Repli d'effort après refus ciblé
- **WHEN** HIGH reçoit HTTP 400 sur son paramètre d'effort et XHIGH est annoncé
- **THEN** un seul repli XHIGH est autorisé avec ses propres paliers
- **AND** HTTP 401/403/429, troncature ou seuil ne déclenchent aucun repli d'effort


### Requirement: Contrat Low propre au transport
Le contrat historique Low SHALL être remplacé par HIGH, puis XHIGH seulement
si HIGH est indisponible et XHIGH pris en charge. Chat Completions SHALL
utiliser reasoning_effort ; Responses reasoning.effort ; Messages
output_config.effort avec thinking adaptive ; DeepSeek thinking activé et
reasoning_effort. OpenRouter SHALL suivre ses métadonnées ou le budget HIGH
80 % documenté. Aucun repli vers un niveau inférieur SHALL être effectué.

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

### Requirement: Gratuité vérifiable et retour au payant
La gratuité SHALL exiger prix publiés d'entrée et de sortie nuls avec
variantes compatibles, jamais un nom seul. Contexte ≥1M, filtres TFL, accès,
transport et le raisonnement HIGH/XHIGH autorisé SHALL être préservés. Le retour au payant et les transitions
de catégorie bornées SHALL concerner uniquement le mode5. Les modes 3/4
SHALL rester gratuits sans transition de quota.

#### Scenario: Ressources rétablies
- **WHEN** les ressources du compte Go reviennent
- **THEN** 1/2 peuvent redevenir valides après leurs propres contrôles et mesures
- **AND** 3/4 restent gratuits avec leurs seuils propres

#### Scenario: Crédit OpenRouter rétabli pendant le repli
- **WHEN** mode5 constate un crédit disponible avant une tentative gratuite
- **THEN** seuls ses payants peuvent le représenter et ses transitions restent bornées


#### Scenario: Quotas rétablis pendant les tests gratuits
- **WHEN** mode5 retrouve du crédit pendant ses tests gratuits OpenRouter
- **THEN** seuls ses payants peuvent représenter ce mode et les oscillations restent bornées
