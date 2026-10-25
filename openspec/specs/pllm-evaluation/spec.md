# pllm-evaluation Specification

## Purpose

Définir l’évaluation des politiques PLLM, leurs quotas et mesures, leur publication et la séparation des applications OpenCode autorisées.

## Requirements

### Requirement: Résolution explicite du catalogue TFL
PLLM SHALL accepter `--tfl-catalog CHEMIN` pour les modes OpenCode Go,
OpenRouter et les replis. Sans cette option, le chemin SHALL rester
`../tfl/data/tfl.json` relatif au skill PLLM. Un catalogue absent ou invalide
SHALL produire un diagnostic explicite sans sélection inventée.

#### Scenario: Plugins installés séparément
- **WHEN** le catalogue est fourni explicitement depuis un autre emplacement
- **THEN** la résolution utilise ce fichier pour le rang initial et les replis
- **AND** aucune recherche dans les configurations privées n'est nécessaire

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

### Requirement: Protocole des mesures traçable
Les mesures SHALL employer une horloge monotone et un flux réel ; le TTFT
SHALL porter sur le premier contenu visible. Le JSON SHALL conserver la
portée du débit : raisonnement et réponse pour Go et OpenCode général,
réponse seule pour OpenRouter et DeepSeek. Le classement interne SHALL
comparer uniquement des débits de même portée.

#### Scenario: Deux catalogues OpenCode
- **WHEN** les candidats gratuits Go et OpenCode général sont comparés
- **THEN** leurs débits utilisent la même portée raisonnement et réponse
- **AND** leurs fournisseurs, routes et comptages restent distincts

#### Scenario: Mesures provenant de fournisseurs différents
- **WHEN** des mesures OpenCode et OpenRouter sont restituées
- **THEN** le JSON conserve leur portée sans les présenter comme une mesure identique

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


### Requirement: Publication traçable
PLLM SHALL publier `pllm-current.json` et `pllm-current.md` par remplacement
atomique de chaque fichier, sans secret. Le JSON SHALL tracer les horodatages,
critères, résultats, causes, sélection et type de débit.

#### Scenario: Résultats publiés
- **WHEN** l'évaluation se termine et la publication réussit
- **THEN** les deux fichiers décrivent la même évaluation sans valeur secrète

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

### Requirement: Absence de sélection valide
L'absence de politique valide SHALL effacer l'ancienne sélection avec
`selected_mode=null` et `selection_status=no_valid_model`.

#### Scenario: Aucune politique valide
- **WHEN** aucune politique évaluée ne satisfait les critères
- **THEN** le résultat indique l'absence de politique valide sans conserver une ancienne sélection

### Requirement: Application OpenCode distincte et autorisée
Une simple évaluation PLLM SHALL NOT modifier la configuration OpenCode.
L'application à une session SHALL exiger une autorisation explicite et les
contrôles décrits par le skill, avec les secrets confinés au processus dédié.
Les réglages du développeur SHALL prévaloir sur les valeurs par défaut.

#### Scenario: Évaluation sans demande de bascule
- **WHEN** PLLM est invoquée uniquement pour évaluer ou publier une politique
- **THEN** elle ne modifie pas les agents ou l'authentification OpenCode

### Requirement: Continuité de session OpenCode et CAB
Une interdiction d'arrêter OpenCode SHALL préserver son processus et son
interface. Toute reprise sous CAB après une bascule autorisée SHALL
réconcilier la session et ses autorisations avant de poursuivre.

#### Scenario: Rechargement interne pendant une bascule autorisée
- **WHEN** le contexte est rechargé sans autorisation d'arrêter le processus
- **THEN** le processus et son interface sont préservés
- **AND** la session CAB est réconciliée avant la reprise des mandats

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

### Requirement: Classement interne par performances
Hors forçage, PLLM SHALL tester tous les candidats admissibles de la catégorie
autorisée. Les réussites SHALL être classées par débit décroissant, TTFT
croissant puis ordre stable TFL, Go avant général pour le repli modes 1/2.
Le premier de ce classement SHALL représenter le mode. Le JSON SHALL tracer
tous les candidats et leurs tentatives ; active SHALL s'arrêter uniquement
après classement complet du premier mode valide.

#### Scenario: Un candidat plus rapide après la première réussite
- **WHEN** deux candidats valides ont des débits distincts
- **THEN** celui au débit maximal est retenu indépendamment de son rang tarifaire

#### Scenario: Départage à débit égal
- **WHEN** plusieurs candidats ont le même débit valide
- **THEN** le TTFT minimal puis l'ordre TFL les départagent

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
