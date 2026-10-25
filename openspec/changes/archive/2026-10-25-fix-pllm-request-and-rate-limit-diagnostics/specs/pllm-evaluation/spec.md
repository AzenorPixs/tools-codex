## MODIFIED Requirements

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL utiliser les paliers 1024, 2048, 4096 et 8192 tokens, 120 s par
requête. Sans succès mémorisé de même configuration, commencer à 1024.
Les reprises SHALL contrôler les quotas avant chaque requête. Un HTTP 400
ou 429 SHALL arrêter les paliers du candidat. La mémoire SHALL enregistrer
seulement les succès complets par configuration, sans les remplacer par un
échec ni afficher un palier d'un autre modèle.

#### Scenario: Plusieurs candidats et retour à une configuration connue
- **WHEN** plusieurs configurations ont été évaluées avec succès
- **THEN** leurs paliers mémorisés sont distincts et réutilisables par configuration
- **AND** un candidat changé sans réussite correspondante repart à 1024

#### Scenario: Réutilisation d'un palier réussi
- **WHEN** une réussite mémorisée correspond à la même configuration
- **THEN** l'évaluation peut reprendre à ce palier avec de nouveaux contrôles
- **AND** un échec ne remplace pas la dernière réussite

#### Scenario: Configuration remplacée après HTTP 429
- **WHEN** un autre candidat autorisé remplace le modèle limité
- **THEN** ses paliers sont recalculés selon son identité
- **AND** sans réussite correspondante, il commence à 1024 tokens
- **AND** l'épuisement des candidats reste un échec sans sélection valide

#### Scenario: HTTP 400 ou 429 au premier palier
- **WHEN** une requête reçoit HTTP 400 ou HTTP 429
- **THEN** aucun budget supérieur n'est testé pour ce candidat dans cette invocation
- **AND** les autres candidats autorisés gardent leurs propres contrôles et tests

#### Scenario: Troncature ou seuil mesuré non satisfait
- **WHEN** le candidat reçoit une réponse tronquée ou échoue sur un seuil mesuré
- **THEN** les paliers suivants restent disponibles après contrôle des quotas

### Requirement: Diagnostic visible et sûr
État SHALL afficher le diagnostic sûr sur la ligne de politique sans colonne
supplémentaire. Les erreurs HTTP/SSE SHALL être distinguées sans corps brut,
secret ou compte. Un succès gratuit SHALL afficher Valide et repli gratuit,
avec quotas réels. Le JSON SHALL garder cause, preuves, mesures null si
absentes et détails HTTP filtrés : statut, code connu, paramètre connu,
délai et échéance Retry-After disponibles.

#### Scenario: Authentification refusée
- **WHEN** le contrôle ou un flux renvoie un refus d'authentification HTTP 401
- **THEN** la ligne affiche Invalide et Authentification refusée (HTTP 401)
- **AND** aucun ancien gagnant ni repli gratuit ne masque ce refus

#### Scenario: Réussite gratuite avec quota épuisé
- **WHEN** le meilleur candidat gratuit satisfait tous les critères
- **THEN** la ligne affiche Valide — repli gratuit et ses mesures actuelles
- **AND** le quota ou solde épuisé reste affiché sans être rendu disponible

#### Scenario: Paramètre refusé et message sensible
- **WHEN** un HTTP 400 désigne un paramètre connu avec un corps contenant des données privées
- **THEN** seuls le statut, le code reconnu et le paramètre connu sont publiés
- **AND** aucune donnée privée ni message brut n'est conservé

## ADDED Requirements

### Requirement: Contrat Low propre au transport
Chat Completions OpenCode Go et général SHALL envoyer reasoning_effort=low
sans thinking. Responses SHALL garder reasoning.effort=low et Messages son
budget thinking défini. DeepSeek direct SHALL conserver thinking activé et
reasoning_effort=low. OpenRouter SHALL garder sa résolution documentée.
PLLM SHALL NOT réduire Low ni déduire le contrat d'un nom de modèle.

#### Scenario: Gratuit OpenCode en Chat Completions
- **WHEN** un candidat OpenCode utilise chat_completions
- **THEN** la requête contient reasoning_effort=low sans thinking
- **AND** le modèle doit réussir ses mesures actuelles avant de devenir valide

#### Scenario: Autres transports et DeepSeek
- **WHEN** Responses, Messages ou DeepSeek direct sont évalués
- **THEN** leurs paramètres Low propres restent préservés

### Requirement: Retry-After filtré et sans attente indéfinie
PLLM SHALL lire au plus 64 Kio d'erreur HTTP et conserver uniquement des
champs filtrés. Retry-After SHALL accepter secondes entières ou date HTTP
avec fuseau, sans date inventée en cas d'absence ou d'erreur. Un HTTP 429
SHALL publier l'attente disponible sans rejouer les paliers ni planifier
une reprise. L'échéance SHALL NOT garantir un succès futur.

#### Scenario: Délai ou date HTTP exploitable
- **WHEN** un HTTP 429 contient un Retry-After valide
- **THEN** le JSON contient le délai et une échéance avec fuseau
- **AND** État indique la reprise sans attendre son échéance dans cette invocation

#### Scenario: En-tête ou corps inexploitable
- **WHEN** Retry-After ou le corps est absent, invalide ou hors plage
- **THEN** le statut reste explicite sans information inventée ni fuite du contenu brut
- **AND** la réponse HTTP est fermée et le candidat reste invalide
