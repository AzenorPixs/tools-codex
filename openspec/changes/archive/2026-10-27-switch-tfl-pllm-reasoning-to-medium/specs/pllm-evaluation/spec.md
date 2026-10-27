## MODIFIED Requirements

### Requirement: Politiques et sélection explicites
PLLM SHALL garder six priorités : payants Go 1/2, gratuits Go 3/4,
payants OpenRouter 5 et DeepSeek 6. Les comptes et références historiques
SHALL être conservés. Les modèles 1 à 5 SHALL provenir de TFL avec route,
fournisseur et date. Medium SHALL être l'effort demandé par défaut. La première
politique valide après sélection ordonnée de son candidat SHALL être
sélectionnée.

#### Scenario: Sélection selon la priorité
- **WHEN** plusieurs politiques sont valides
- **THEN** la première par priorité 1 à 6 est retenue indépendamment du débit des autres

#### Scenario: Authentification des modes renumérotés
- **WHEN** les modes sont évalués
- **THEN** les références existantes sont utilisées sans création ou déplacement de secret
- **AND** policy=mode1 sert à 1/3, policy=mode2 à 2/4, ancien policy=mode3 à 5 et ancien policy=mode4 à 6

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL garder les paliers 1024, 2048, 4096, 8192 et 120 s par requête.
Les contrôles applicables SHALL précéder chaque requête, sans quota en 3/4.
Un HTTP 400/429 SHALL arrêter le candidat sans repli vers un autre niveau
d'effort. La mémoire SHALL distinguer modèle, raisonnement et profil de débit,
garder les succès historiques sans les réutiliser pour un autre profil. Une
mémoire invalide SHALL NOT être écrasée ; un ancien succès SHALL NOT valider
l'invocation.

#### Scenario: Nouvelle politique gratuite
- **WHEN** mode3 ou mode4 est évalué pour la première fois après migration
- **THEN** son premier palier est 1024, sans réutiliser l'ancien OpenRouter ou DeepSeek
- **AND** la mémoire des anciens 3/4 est déplacée vers 5/6 lors du passage du schéma 1 au schéma 2

#### Scenario: Reprise de configuration connue
- **WHEN** une configuration possède un succès Medium mémorisé
- **THEN** son palier peut être repris avec des mesures actuelles et les contrôles applicables

#### Scenario: HTTP 400 ou 429
- **WHEN** un candidat reçoit ce refus
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
- **WHEN** une réussite Medium mémorisée correspond à la même configuration
- **THEN** l'évaluation peut reprendre à ce palier avec de nouveaux contrôles applicables
- **AND** un échec ne remplace pas la dernière réussite

#### Scenario: Configuration remplacée après HTTP 429
- **WHEN** un autre candidat autorisé remplace le modèle limité
- **THEN** ses paliers sont recalculés selon son identité
- **AND** sans réussite Medium correspondante, il commence à 1024 tokens
- **AND** l'épuisement des candidats reste un échec sans sélection valide

#### Scenario: HTTP 400 ou 429 au premier palier
- **WHEN** une requête reçoit HTTP 400 ou HTTP 429
- **THEN** aucun budget supérieur n'est testé pour ce candidat dans cette invocation
- **AND** les autres candidats autorisés gardent leurs propres contrôles et tests

#### Scenario: Troncature ou seuil mesuré non satisfait
- **WHEN** le candidat reçoit une réponse tronquée ou échoue sur un seuil mesuré
- **THEN** les paliers suivants restent disponibles après les contrôles applicables

#### Scenario: Repli d'effort après refus ciblé
- **WHEN** Medium reçoit HTTP 400 sur son paramètre d'effort
- **THEN** aucun repli vers HIGH ou XHIGH n'est autorisé
- **AND** HTTP 401/403/429, troncature ou seuil ne déclenchent aucun repli d'effort

#### Scenario: Nouveau profil après un ancien succès
- **WHEN** un succès utilise l'ancien débit entre fragments
- **THEN** il reste historique et n'amorce pas le nouveau protocole
- **AND** sans succès Medium du nouveau profil, le premier palier est 1024

#### Scenario: Réutilisation du nouveau profil
- **WHEN** une réussite Medium mémorisée correspond à la même configuration et au même profil de débit
- **THEN** son palier peut être repris avec des mesures actuelles

### Requirement: Contrat Medium propre au transport
PLLM SHALL exiger Medium avant génération, sélection et affichage.
`supported_efforts` avec `medium` ou `null` explicite suffit ; donnée absente,
invalide, booléen `reasoning`, budget seul ou liste sans `medium` SHALL exclure.
Envoyer `medium` selon transport : `reasoning_effort` (Chat Completions/DeepSeek),
`reasoning.effort` (Responses), `output_config.effort` (Messages). L'équivalence
documentée SHALL garder le protocole. Un refus SHALL NOT retenter HIGH/XHIGH.

#### Scenario: Gratuit OpenCode en Chat Completions
- **WHEN** un candidat OpenCode utilise chat_completions sans équivalence documentée
- **THEN** la requête contient reasoning_effort=medium sans thinking
- **AND** le modèle doit réussir ses mesures actuelles avant de devenir valide

#### Scenario: Autres transports et DeepSeek
- **WHEN** Responses, Messages ou DeepSeek direct sont évalués
- **THEN** leurs paramètres Medium propres au transport restent préservés

#### Scenario: HIGH absent et XHIGH annoncé
- **WHEN** les métadonnées annoncent HIGH/XHIGH sans Medium
- **THEN** le candidat est exclu et aucun niveau différent n'est demandé

#### Scenario: Aucun niveau autorisé
- **WHEN** Medium n'est pas pris en charge
- **THEN** le candidat est invalide sans requête de performance ni repli vers un autre effort
