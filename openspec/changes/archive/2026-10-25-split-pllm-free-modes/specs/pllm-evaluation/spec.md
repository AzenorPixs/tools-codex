## MODIFIED Requirements

### Requirement: Initialisation sans historique
PLLM SHALL initialiser six modes de priorités 1 à 6 si le fichier courant
manque, sans quota, mesure ni sélection historique. Un historique valide à
quatre modes SHALL être adapté au schéma 2 : anciens 1/2 conservés, ancien 3
vers 5, ancien 4 vers 6, nouveaux 3/4 initialisés. La conversion SHALL effacer
la sélection et marquer toutes les lignes non évaluées dans cette invocation.
Un historique invalide SHALL produire un diagnostic et SHALL NOT être écrasé.

#### Scenario: Première évaluation
- **WHEN** aucun fichier courant n'existe
- **THEN** six politiques sans résultats inventés sont initialisées

#### Scenario: Historique de quatre modes
- **WHEN** un historique valide de schéma 1 est chargé
- **THEN** OpenRouter et DeepSeek sont déplacés vers 5 et 6 sans sélection courante
- **AND** les nouveaux modes 3/4 n'héritent pas de mesures valides

#### Scenario: Historique illisible
- **WHEN** les politiques, le schéma ou le JSON sont invalides
- **THEN** le fichier reste préservé et la publication est arrêtée

### Requirement: Politiques et sélection explicites
PLLM SHALL évaluer six modes de priorités 1 à 6 : Go payant compte 1,
Go payant compte 2, gratuits Go/général compte 1, mêmes gratuits compte 2,
OpenRouter, DeepSeek direct. Les modèles des modes 1 à 5 SHALL provenir de TFL
avec fournisseur, route et date propres. Low SHALL rester le défaut. Les
références d'authentification historiques SHALL être conservées. La première
politique valide après classement SHALL être sélectionnée.

#### Scenario: Sélection selon la priorité
- **WHEN** plusieurs politiques sont valides
- **THEN** la première par priorité 1 à 6 est retenue indépendamment du débit des autres

#### Scenario: Authentification des modes renumérotés
- **WHEN** les nouveaux modes sont évalués
- **THEN** les références existantes sont utilisées sans création ou déplacement de secret
- **AND** policy=mode1 sert à 1/3, policy=mode2 à 2/4, ancien policy=mode3 à 5 et ancien policy=mode4 à 6

### Requirement: Quotas avant performance
Les modes 1/2/5/6 SHALL consulter leurs quotas ou soldes avant chaque
requête de performance. Une donnée absente, refusée ou incohérente SHALL
arrêter leur évaluation avant cette requête. Les modes 3/4 SHALL NOT consulter
quota ou solde ; ils SHALL publier ce contrôle comme non applicable, sans
valeur ni disponibilité inventée. L'authentification et les limitations
fournisseur SHALL rester applicables à tous les modes.

#### Scenario: Gratuit sans contrôle de quota
- **WHEN** mode3 ou mode4 est évalué avec un accès de génération fonctionnel
- **THEN** aucune requête usage, credits ou balance n'est envoyée, même entre paliers
- **AND** un quota épuisé ou inaccessible sur le compte associé ne conditionne pas sa validité

#### Scenario: Quota indispensable indisponible
- **WHEN** un contrôle des modes 1/2/5/6 échoue
- **THEN** la politique reste invalide sans test de performance correspondant


#### Scenario: Quota épuisé ou non disponible
- **WHEN** un contrôle de quota des modes 1/2/5/6 est indisponible ou refusé
- **THEN** la politique reste invalide sans performance ni repli gratuit

#### Scenario: Épuisement confirmé
- **WHEN** les ressources sont confirmées épuisées
- **THEN** les modes 1/2 restent invalides sans repli ; seul mode5 peut tester ses gratuits OpenRouter
### Requirement: Conditions de quota propres aux fournisseurs
Go payant (modes 1/2) SHALL exiger trois périodes disponibles, statut ok
et usage <100 %. Un épuisement SHALL rendre le mode invalide et rouge sans
candidat gratuit. OpenRouter (mode5) SHALL exiger un solde >0 pour les payants ;
son repli gratuit SHALL exiger un épuisement confirmé. DeepSeek (mode6) SHALL
exiger is_available=true et au moins un solde utilisable >0, sans addition de
devises. Un statut inconnu SHALL NOT prouver un épuisement.

#### Scenario: Go épuisé avant le premier test
- **WHEN** un quota de mode1 ou mode2 atteint 100 %
- **THEN** ce mode est rouge et invalide sans requête de génération payante ou gratuite

#### Scenario: Épuisement Go après une réussite
- **WHEN** un contrôle avant le candidat suivant établit l'épuisement
- **THEN** le mode est invalidé sans conserver son ancien gagnant et sans repli gratuit

#### Scenario: OpenRouter et DeepSeek renumérotés
- **WHEN** modes 5 et 6 sont évalués
- **THEN** les contrôles propres à leurs fournisseurs restent applicables


#### Scenario: Limite de quota atteinte
- **WHEN** un quota Go atteint 100 % ou le solde OpenRouter est épuisé
- **THEN** aucun payant correspondant n'est testé ; seul mode5 autorise son repli gratuit mesuré
### Requirement: Mesures concluantes du modèle sélectionné
Tous les modes SHALL exiger réponse complète, comptage fiable et mesures
actuelles du modèle retenu. Les modes gratuits 3/4 SHALL exiger contexte ≥1M,
TTFT <30 s et débit >20 tokens/s. Les modes 1/2/5/6 SHALL conserver TTFT <90 s
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
- **WHEN** un mode 1/2/5/6 mesure TTFT ≥90 s ou débit ≤15 tokens/s
- **THEN** son candidat reste invalide

#### Scenario: Mesure non concluante
- **WHEN** une réponse est tronquée, absente ou sans comptage fiable
- **THEN** le candidat reste invalide sans succès ni mesure inventés


#### Scenario: Candidat limité ou incomplet
- **WHEN** un candidat échoue après ses paliers ou reçoit une limitation fournisseur
- **THEN** seul un autre candidat de la catégorie autorisée peut le remplacer
- **AND** le remplaçant exige ses propres contrôles et mesures

#### Scenario: Limites strictes
- **WHEN** un candidat atteint TTFT 30 s ou débit 20 tokens/s en 3/4, ou TTFT 90 s ou débit 15 tokens/s dans les autres modes
- **THEN** ce candidat est invalide

#### Scenario: Repli après limitation fournisseur
- **WHEN** une limitation HTTP 429 conduit à choisir un autre modèle de la catégorie autorisée
- **THEN** ce candidat exige ses propres contrôles et mesures concluantes
- **AND** l'épuisement du dernier palier ne transforme pas le repli en réussite

#### Scenario: TTFT sous la nouvelle limite
- **WHEN** un candidat de mode1/2/5/6 mesure 70,4 s et satisfait les autres critères
- **THEN** son seuil TTFT est satisfait ; ce même TTFT échoue en 3/4

#### Scenario: Limite stricte de TTFT atteinte
- **WHEN** le TTFT atteint 30 s en 3/4 ou 90 s dans les autres modes
- **THEN** le candidat reste invalide même avec un débit suffisant
### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL garder les paliers 1024, 2048, 4096 et 8192 tokens, 120 s par
requête, et arrêter un candidat sur HTTP 400/429. Les contrôles applicables
SHALL précéder chaque requête, sans quota en 3/4. La mémoire SHALL garder les
seuls succès complets par configuration et adapter le schéma 1 en 2 sans
apprentissage initial en 3/4. Une mémoire invalide SHALL NOT être écrasée.
Un palier mémorisé SHALL NOT valider une invocation.

#### Scenario: Nouvelle politique gratuite
- **WHEN** mode3 ou mode4 est évalué pour la première fois après migration
- **THEN** son premier palier est 1024, sans réutiliser l'ancien OpenRouter ou DeepSeek
- **AND** la mémoire des anciens 3/4 est déplacée vers 5/6 lors du passage du schéma 1 au schéma 2

#### Scenario: Reprise de configuration connue
- **WHEN** une configuration possède un succès mémorisé
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
- **WHEN** une réussite mémorisée correspond à la même configuration
- **THEN** l'évaluation peut reprendre à ce palier avec de nouveaux contrôles applicables
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
- **THEN** les paliers suivants restent disponibles après les contrôles applicables
### Requirement: Invocation normale et mode active silencieux
L'invocation normale SHALL évaluer les six modes et restituer un tableau
à six lignes et leurs ressources ou mention non applicable. active SHALL
classer tous les candidats du premier mode valide puis s'arrêter et publier
sans sortie console ou conversationnelle. Les modes non visités SHALL garder
evaluated_this_run=false et SHALL NOT être sélectionnés depuis l'historique.

#### Scenario: active s'arrête sur le premier gratuit valide
- **WHEN** les modes 1/2 sont invalides et mode3 est valide
- **THEN** les modes 4/5/6 ne sont pas évalués et la publication reste silencieuse


#### Scenario: Mode active avec politiques non visitées
- **WHEN** le mode `active` sélectionne une politique et s'arrête
- **THEN** les politiques non visitées sont signalées par `evaluated_this_run=false`
- **AND** leurs résultats historiques ne sont pas présentés comme des contrôles actuels ni sélectionnés
- **AND** les fichiers sont publiés sans restitution console ou conversationnelle
### Requirement: Invocation forcée sans repli automatique
Un forçage SHALL limiter l'évaluation au mode et au candidat demandés.
Les commandes 1 à 6 SHALL cibler le premier candidat admissible de ce mode.
11–13 et 21–23 SHALL garder les rangs bruts Go ; 31–33 et 41–43 SHALL cibler
les rangs de la liste gratuite admissible Go puis général ; 51–53 SHALL
reprendre les rangs bruts OpenRouter. 6 SHALL garder DeepSeek direct. Un
rang indisponible ou incompatible SHALL échouer sans substitution.

#### Scenario: Ancien forçage OpenRouter
- **WHEN** le rang OpenRouter 1 est demandé après renumérotation
- **THEN** la commande est 51 ; 31 cible désormais le premier gratuit du compte 1

#### Scenario: Gratuit forcé
- **WHEN** 3, 4, 31 ou 41 est demandé
- **THEN** seul le candidat gratuit correspondant est testé sans appel de quota


#### Scenario: Échec d'une politique forcée
- **WHEN** la politique explicitement forcée échoue
- **THEN** PLLM ne teste pas un autre moteur pour remplacer celui demandé
### Requirement: Catégories payante et gratuite exclusives
Les modes 1/2 SHALL examiner exclusivement les payants Go. Les modes 3/4
SHALL examiner exclusivement les gratuits Go puis OpenCode général, quelle que
soit la disponibilité du compte associé. Mode5 SHALL conserver payants
OpenRouter avec crédit, gratuits après épuisement confirmé. Mode6 SHALL
conserver DeepSeek direct. Aucun candidat payant SHALL être appelé en 3/4.

#### Scenario: Compte Go disponible ou épuisé
- **WHEN** les gratuits 3/4 sont évalués
- **THEN** leur catégorie reste gratuite indépendamment des ressources du compte

#### Scenario: Candidat payant au nom free
- **WHEN** un candidat porte free dans son nom mais ses prix ne sont pas tous nuls
- **THEN** il n'est pas admissible en 3/4 ni au repli gratuit de 5


#### Scenario: Retour au payant après repli général
- **WHEN** un historique ancien désigne un gratuit général en mode1/2 puis les quotas Go reviennent
- **THEN** seuls les payants Go peuvent représenter 1/2 après leurs nouveaux contrôles ; les gratuits sont en 3/4

#### Scenario: Crédit épuisé et modèle payant au nom free
- **WHEN** le solde OpenRouter est nul et qu'un nom free porte un prix non nul
- **THEN** ce candidat est exclu du repli gratuit
- **AND** aucun candidat payant n'est appelé
### Requirement: Gratuité vérifiable et retour au payant
La gratuité SHALL exiger prix publiés d'entrée et de sortie nuls avec
variantes compatibles, jamais un nom seul. Contexte ≥1M, filtres TFL, accès,
transport et Low SHALL être préservés. Le retour au payant et les transitions
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
### Requirement: Diagnostic visible et sûr
État SHALL conserver les diagnostics HTTP/SSE filtrés sans corps brut,
secret ou compte. Les modes 1/2 épuisés SHALL afficher rouge et Invalide avec
la cause Quota épuisé. Les réussites 3/4 SHALL afficher Valide et gratuit,
sans mention de repli ou quota disponible. Mode5 gratuit SHALL garder Valide
et repli gratuit avec solde réel. Le JSON SHALL conserver causes, candidats,
exclusions, tentatives, seuils par politique et mesures null si absentes.

#### Scenario: Authentification ou limitation gratuite
- **WHEN** mode3 ou mode4 reçoit HTTP 401, 403 ou 429
- **THEN** le diagnostic reste visible sans quota inventé ni attente indéfinie

#### Scenario: Ressources non applicables
- **WHEN** le rapport des modes 3/4 est publié
- **THEN** leur ligne indique quota non applicable et leurs quotas restent null

#### Scenario: Corps d'erreur sensible
- **WHEN** un refus contient des informations privées
- **THEN** seuls les champs autorisés filtrés sont conservés

#### Scenario: Authentification refusée
- **WHEN** le contrôle ou un flux renvoie un refus d'authentification HTTP 401
- **THEN** la ligne affiche Invalide et Authentification refusée (HTTP 401)
- **AND** aucun ancien gagnant ni repli gratuit ne masque ce refus

#### Scenario: Réussite gratuite avec quota épuisé
- **WHEN** mode3/4 satisfait ses seuils gratuits ou que le repli gratuit de mode5 réussit
- **THEN** 3/4 affichent Valide et gratuit avec quota non applicable ; 5 affiche repli gratuit et son solde réel épuisé

#### Scenario: Paramètre refusé et message sensible
- **WHEN** un HTTP 400 désigne un paramètre connu avec un corps contenant des données privées
- **THEN** seuls le statut, le code reconnu et le paramètre connu sont publiés
- **AND** aucune donnée privée ni message brut n'est conservé
