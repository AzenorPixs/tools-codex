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
payants OpenRouter 5 et DeepSeek 6. Les comptes et références historiques
SHALL être conservés. Les modèles 1 à 5 SHALL provenir de TFL avec route,
fournisseur et date. HIGH SHALL être le défaut, avec repli XHIGH pris en
charge lorsque HIGH est indisponible. La première politique valide après
sélection ordonnée de son candidat SHALL être sélectionnée.

#### Scenario: Sélection selon la priorité
- **WHEN** plusieurs politiques sont valides
- **THEN** la première par priorité 1 à 6 est retenue indépendamment du débit des autres

#### Scenario: Authentification des modes renumérotés
- **WHEN** les modes sont évalués
- **THEN** les références existantes sont utilisées sans création ou déplacement de secret
- **AND** policy=mode1 sert à 1/3, policy=mode2 à 2/4, ancien policy=mode3 à 5 et ancien policy=mode4 à 6

### Requirement: Quotas avant performance
Les modes 1/2/5/6 SHALL consulter leurs quotas ou soldes avant chaque
requête de performance. Une donnée absente, refusée ou incohérente SHALL
arrêter leur évaluation avant cette requête. Les modes 3/4 SHALL NOT consulter
quota ou solde ; ils SHALL publier ce contrôle comme non applicable.
L'authentification et les limitations fournisseur SHALL rester applicables.

#### Scenario: Gratuit sans contrôle de quota
- **WHEN** mode3 ou mode4 est évalué
- **THEN** aucune requête usage, credits ou balance n'est envoyée, même entre paliers
- **AND** les ressources du compte associé ne conditionnent pas sa validité

#### Scenario: Contrôle indispensable indisponible ou épuisé
- **WHEN** un contrôle des modes 1/2/5/6 est refusé, indisponible ou épuisé
- **THEN** la politique reste invalide sans génération correspondante ni repli gratuit

#### Scenario: Quota indispensable indisponible
- **WHEN** un contrôle des modes 1/2/5/6 échoue
- **THEN** la politique reste invalide sans test de performance correspondant

#### Scenario: Quota épuisé ou non disponible
- **WHEN** un contrôle de quota des modes 1/2/5/6 est indisponible ou refusé
- **THEN** la politique reste invalide sans performance ni repli gratuit

#### Scenario: Épuisement confirmé
- **WHEN** les ressources payantes sont confirmées épuisées
- **THEN** 1/2/5/6 restent invalides sans génération ni repli gratuit

### Requirement: Conditions de quota propres aux fournisseurs
Go payant (modes 1/2) SHALL exiger trois périodes disponibles, statut ok
et usage <100 %. Mode5 SHALL exiger un solde OpenRouter strictement positif
et SHALL NOT utiliser de candidat gratuit. DeepSeek (mode6) SHALL exiger
is_available=true et au moins un solde utilisable >0, sans addition de
devises. Un statut inconnu SHALL NOT prouver un épuisement.

#### Scenario: Go épuisé avant le premier test
- **WHEN** un quota de mode1 ou mode2 atteint 100 %
- **THEN** ce mode est invalide sans requête de génération payante ou gratuite

#### Scenario: Ressources épuisées pendant le parcours
- **WHEN** le contrôle avant un palier ou le candidat suivant après un échec constate l'épuisement
- **THEN** le mode s'arrête sans génération supplémentaire ni repli gratuit

#### Scenario: Crédit OpenRouter épuisé
- **WHEN** le solde de mode5 est nul ou négatif
- **THEN** le mode est invalide et aucun candidat payant ou gratuit n'est testé

#### Scenario: Réussite sans candidat suivant
- **WHEN** le premier candidat conforme réussit avec ses contrôles actuels
- **THEN** aucun contrôle ni test du candidat suivant n'est effectué dans ce mode

#### Scenario: Épuisement Go après une réussite
- **WHEN** le quota externe évolue après la réussite qui a terminé le mode
- **THEN** aucun candidat suivant ni contrôle supplémentaire n'est lancé dans ce mode
- **AND** la réussite reste datée de ses contrôles réels sans garantie de disponibilité permanente

#### Scenario: OpenRouter et DeepSeek renumérotés
- **WHEN** modes 5 et 6 sont évalués
- **THEN** les contrôles propres à leurs fournisseurs restent applicables

#### Scenario: Limite de quota atteinte
- **WHEN** un quota Go atteint 100 % ou le solde OpenRouter est épuisé
- **THEN** aucun candidat payant ou gratuit correspondant n'est testé

### Requirement: Mesures concluantes du modèle sélectionné
Tous les modes SHALL exiger réponse complète, comptage fiable et mesures
actuelles. Les candidats TFL SHALL avoir un contexte d'entrée ≥1M, sans
envoi d'un million de tokens. Les gratuits 3/4 SHALL respecter TTFT <30 s
et débit >20 tokens/s ; les payants 1/2/5/6, <90 s et >15 tokens/s. Les
paliers, HIGH/XHIGH et le protocole actuels SHALL rester inchangés. Hors
forçage, le parcours SHALL s'arrêter au premier succès selon l'ordre du mode.

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
- **WHEN** un mode 3/4 mesure TTFT ≥30 s ou débit ≤20 tokens/s
- **THEN** ce candidat reste invalide même si le quota du compte est disponible

#### Scenario: Gratuit valide
- **WHEN** un gratuit vérifié de contexte ≥1M donne une réponse complète à TTFT 29,9 s et débit 20,1 tokens/s
- **THEN** ses seuils sont satisfaits sans contrôle de quota

#### Scenario: Limites des autres modes
- **WHEN** un candidat payant de mode 1/2/5/6 mesure TTFT ≥90 s ou débit ≤15 tokens/s
- **THEN** son candidat reste invalide

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
Les mesures SHALL utiliser une horloge monotone. Le TTFT SHALL porter sur
le premier contenu visible. Le débit SHALL être le comptage de sortie divisé
par la durée totale non arrondie de la requête, TTFT inclus : global pour
Go/général, réponse seule pour OpenRouter/DeepSeek. Une réponse complète en
un bloc SHALL être mesurable. Durée ou comptage invalides SHALL produire
une mesure indisponible. Le JSON SHALL tracer profil, formule et durées.

#### Scenario: Deux catalogues OpenCode
- **WHEN** les candidats gratuits Go et OpenCode général sont comparés
- **THEN** leurs débits utilisent la même portée raisonnement et réponse
- **AND** leurs fournisseurs, routes et comptages restent distincts

#### Scenario: Mesures provenant de fournisseurs différents
- **WHEN** des mesures OpenCode et OpenRouter sont restituées
- **THEN** le JSON conserve leur portée sans les présenter comme une mesure identique

#### Scenario: Fragments reçus en rafale
- **WHEN** un flux complet est reçu sur une fenêtre de contenu très courte
- **THEN** les tokens/s utilisent la durée complète de la requête sans extrapolation entre fragments

#### Scenario: Un bloc complet
- **WHEN** une réponse complète est reçue en un seul bloc avec compteur et durée fiables
- **THEN** le débit moyen est calculé sans exiger plusieurs fragments

#### Scenario: Durée invalide
- **WHEN** la durée totale est nulle, négative ou non finie
- **THEN** aucun débit n'est fabriqué et le candidat reste invalide avec cause explicite

#### Scenario: Durée non arrondie
- **WHEN** l'affichage arrondit la durée
- **THEN** le calcul utilise encore la durée monotone non arrondie

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL garder les paliers 1024, 2048, 4096, 8192 et 120 s par requête.
Les contrôles applicables SHALL précéder chaque requête, sans quota en 3/4.
Un HTTP 400/429 SHALL arrêter le candidat, hors repli XHIGH autorisé.
La mémoire SHALL distinguer modèle, raisonnement et profil de débit, garder
les succès historiques sans les réutiliser pour un autre profil. Une mémoire
invalide SHALL NOT être écrasée ; un ancien succès SHALL NOT valider l'invocation.

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

#### Scenario: Nouveau profil après un ancien succès
- **WHEN** un succès utilise l'ancien débit entre fragments
- **THEN** il reste historique et n'amorce pas le nouveau protocole
- **AND** sans succès du nouveau profil, le premier palier est 1024

#### Scenario: Réutilisation du nouveau profil
- **WHEN** une réussite mémorisée correspond à la même configuration et au même profil de débit
- **THEN** son palier peut être repris avec des mesures actuelles

### Requirement: Publication traçable
PLLM SHALL publier pllm-current.json et pllm-current.md atomiquement par
fichier, sans secret. Le JSON SHALL tracer horodatages, critères, causes,
sélection, comptages, profil de débit et durée totale non arrondie utilisée.
Les rapports SHALL indiquer que le débit moyen inclut l'attente et le TTFT.
Les anciens débits SHALL NOT être présentés comme comparables ou actuels.

#### Scenario: Résultats publiés
- **WHEN** l'évaluation se termine et la publication réussit
- **THEN** les deux fichiers décrivent la même évaluation sans valeur secrète

### Requirement: Invocation normale et mode active silencieux
L'invocation normale SHALL évaluer les six modes et restituer un tableau
à six lignes et leurs ressources ou mention non applicable. Chaque mode
SHALL arrêter son parcours au premier candidat valide. active SHALL s'arrêter
à la première politique valide et publier sans sortie console ou
conversationnelle. Les modes non visités SHALL garder evaluated_this_run=false
et SHALL NOT être sélectionnés depuis l'historique.

#### Scenario: Invocation normale après une réussite
- **WHEN** un candidat valide est retenu dans un mode
- **THEN** les candidats suivants de ce mode ne sont pas testés et la politique suivante est évaluée

#### Scenario: active s'arrête sur le premier gratuit valide
- **WHEN** modes 1/2 sont invalides et le premier gratuit conforme de mode3 réussit
- **THEN** les modes 4/5/6 ne sont pas évalués et la publication reste silencieuse

#### Scenario: Politiques non visitées
- **WHEN** active retient une politique
- **THEN** les autres modes gardent evaluated_this_run=false et ne sont pas sélectionnés depuis leurs résultats historiques

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
soit la disponibilité du compte associé. Mode5 SHALL examiner exclusivement
les payants OpenRouter avec crédit positif. Mode6 SHALL conserver DeepSeek
direct. Les modes 1/2/5 SHALL NOT basculer vers un candidat gratuit.

#### Scenario: Compte Go disponible ou épuisé
- **WHEN** les gratuits 3/4 sont évalués
- **THEN** leur catégorie reste gratuite indépendamment des ressources du compte

#### Scenario: Candidat au nom free mais payant
- **WHEN** le nom contient free mais les prix vérifiés ne sont pas tous nuls
- **THEN** ce candidat n'est pas admissible en 3/4

#### Scenario: Gratuit OpenRouter forcé
- **WHEN** le rang explicitement demandé en mode5 désigne un gratuit
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

### Requirement: Gratuité vérifiable et retour au payant
La gratuité des modes 3/4 SHALL exiger prix publiés d'entrée et de sortie
nuls avec variantes compatibles, jamais un nom seul. Contexte ≥1M, filtres
TFL, accès, transport et HIGH/XHIGH autorisé SHALL être préservés. Les
catégories SHALL rester fixes pendant l'invocation. Les ressources des modes
payants SHALL être relues à chaque nouvelle invocation, sans résultat hérité.

#### Scenario: Ressources rétablies
- **WHEN** les quotas Go ou le crédit OpenRouter redeviennent disponibles à une nouvelle invocation
- **THEN** 1/2/5 peuvent redevenir valides après leurs propres contrôles et mesures payantes
- **AND** 3/4 restent gratuits avec leurs seuils propres

#### Scenario: Ancien résultat gratuit OpenRouter
- **WHEN** un historique valide contient un ancien gagnant gratuit en mode5
- **THEN** il reste lisible mais ne valide pas l'évaluation actuelle et aucun test gratuit n'est lancé

#### Scenario: Crédit OpenRouter rétabli pendant le repli
- **WHEN** le crédit revient après l'arrêt du mode5 pour épuisement
- **THEN** aucune transition gratuite n'est effectuée et une nouvelle invocation relit le crédit avant de tester ses payants

#### Scenario: Quotas rétablis pendant les tests gratuits
- **WHEN** les ressources reviennent pendant les tests gratuits 3/4
- **THEN** ces modes restent gratuits sans contrôle de ressources et mode5 conserve sa catégorie payante

### Requirement: Diagnostic visible et sûr
Le rapport SHALL garder huit colonnes et les diagnostics dans État, sans
secret ni compte. Les modes 1/2/5 épuisés SHALL afficher rouge et Invalide
avec leur cause. Les réussites 3/4 SHALL afficher Valide et gratuit, avec
ressources non applicables. Le JSON SHALL conserver causes, candidats
évalués, exclusions, tentatives et quotas réels sans mesure fabriquée pour
un candidat non visité.

#### Scenario: Ressources gratuites
- **WHEN** le rapport des modes 3/4 est publié
- **THEN** leurs ressources indiquent Non applicable et leurs quotas JSON sont null

#### Scenario: Authentification refusée
- **WHEN** un contrôle ou un flux exécuté renvoie HTTP 401
- **THEN** le mode est invalide avec le diagnostic sûr d'authentification refusée

#### Scenario: Paramètre refusé et message sensible
- **WHEN** un HTTP 400 désigne un paramètre connu avec un corps privé
- **THEN** seuls le statut, le code reconnu et le paramètre connu sont publiés, sans corps brut

#### Scenario: Arrêt sans mesure inventée
- **WHEN** un candidat valide met fin au parcours du mode
- **THEN** candidate_results contient uniquement les candidats effectivement visités

#### Scenario: Authentification ou limitation gratuite
- **WHEN** mode3 ou mode4 reçoit HTTP 401, 403 ou 429
- **THEN** le diagnostic reste visible sans quota inventé ni attente indéfinie

#### Scenario: Ressources non applicables
- **WHEN** le rapport des modes 3/4 est publié
- **THEN** leur ligne indique quota non applicable et leurs quotas restent null

#### Scenario: Corps d'erreur sensible
- **WHEN** un refus contient des informations privées
- **THEN** seuls les champs autorisés filtrés sont conservés

#### Scenario: Réussite gratuite avec quota épuisé
- **WHEN** mode3/4 satisfait ses seuils gratuits avec le quota Go associé épuisé
- **THEN** il affiche Valide et gratuit avec ressources non applicables ; un crédit OpenRouter épuisé laisse mode5 invalide

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

### Requirement: Classement interne par prix des payants et performances des gratuits
Hors forçage, PLLM SHALL essayer les payants 1/2/5 par coût moyen TFL
croissant et SHALL retenir le premier candidat qui satisfait tous les tests
actuels. Un candidat suivant SHALL être essayé seulement après échec du
précédent, sous réserve des contrôles bloquants. À prix égal, l'ordre stable
TFL SHALL être conservé sans test supplémentaire pour départager les débits.

#### Scenario: Catalogue désordonné
- **WHEN** le catalogue place un payant à 0,21 USD/M avant un payant à 0,15 USD/M
- **THEN** le payant à 0,15 USD/M est essayé en premier
- **AND** s'il réussit, le payant à 0,21 USD/M n'est pas testé

#### Scenario: Payant moins cher invalide
- **WHEN** le moins cher échoue à ses tests sans blocage global de ressources ou d'authentification
- **THEN** le suivant par prix est essayé avec ses propres contrôles jusqu'au premier succès

#### Scenario: Prix égaux
- **WHEN** deux payants ont le même coût moyen vérifié
- **THEN** le premier dans l'ordre TFL est essayé d'abord et sa réussite arrête le mode

#### Scenario: Payant moins cher et moins rapide
- **WHEN** le premier payant par prix à 0,15 USD/M réussit à 113 tokens/s
- **THEN** il représente le mode sans tester un payant plus cher même potentiellement plus rapide

### Requirement: Coût vérifié de classement PLLM
Le coût SHALL être la moyenne des prix d'entrée/sortie TFL : hors pointe
pour Go et prix de base pour OpenRouter. Les égalités tarifaires SHALL
résister aux erreurs d'addition binaire et conserver l'ordre TFL. Les prix
non vérifiables SHALL rester exclus. Le JSON SHALL tracer prix et provenance
sans héritage périmé. Mode6 SHALL garder son candidat unique sans tarif inventé.

#### Scenario: Moyennes égales calculées différemment
- **WHEN** les prix 0,1/0,2 et 0,15/0,15 sont publiés pour deux candidats
- **THEN** leurs moyennes égales à 0,15 conservent l'ordre TFL initial

#### Scenario: Prix absent ou invalide
- **WHEN** un candidat payant n'a pas de prix vérifiable
- **THEN** il est exclu avec sa cause avant génération

### Requirement: Classement des gratuits par performances
Les modes 3/4 SHALL parcourir les gratuits admissibles dans l'ordre TFL,
Go avant OpenCode général, et SHALL retenir le premier succès aux tests
gratuits actuels. Ils SHALL NOT tester les candidats suivants pour chercher
un débit supérieur. Après échec d'un gratuit, le suivant SHALL conserver
ses propres mesures et les seuils stricts <30 s et >20 tokens/s.

#### Scenario: Premier gratuit valide
- **WHEN** le premier gratuit Go satisfait tous les critères
- **THEN** il est retenu et aucun autre gratuit Go ou général n'est testé

#### Scenario: Repli vers le gratuit suivant
- **WHEN** les gratuits Go échouent sans blocage d'authentification et un gratuit général réussit
- **THEN** le premier gratuit général conforme est retenu sans contrôle de quota ni de solde

#### Scenario: Gratuit plus performant
- **WHEN** un gratuit conforme précède un autre candidat potentiellement plus performant
- **THEN** le premier succès est retenu et le suivant n'est pas testé

### Requirement: Invariants du classement tarifaire
Les priorités 1 à 6, seuils payants et gratuits, quotas, raisonnement,
forçages de rang et protocole 8 SHALL rester inchangés. Le mode5 SHALL
refuser les rangs gratuits conformément à sa catégorie exclusivement
payante. Le JSON SHALL tracer les candidats visités et leurs tentatives ;
active SHALL s'arrêter au premier mode valide. Le rapport SHALL conserver
ses huit colonnes.

#### Scenario: Publication et priorités préservées
- **WHEN** plusieurs politiques valides ont été évaluées selon leurs règles
- **THEN** la première par priorité 1 à 6 est sélectionnée avec huit colonnes inchangées
- **AND** son prix courant et les preuves des candidats visités restent auditables
