## MODIFIED Requirements

### Requirement: Initialisation sans historique
PLLM SHALL initialiser sept priorités et utiliser le schéma 3. Sans état, les
politiques commencent sans mesures ni sélection. Les historiques des schémas
1/2 SHALL être adaptés en mémoire : anciens modes Go conservés, ancien
OpenRouter 5 réinitialisé, DeepSeek mode 4/6 déplacé en mode7 et mode6 gratuit
OpenRouter neuf. La sélection SHALL être effacée ; les états invalides SHALL
rester préservés.
Un historique invalide SHALL produire un diagnostic et SHALL NOT être écrasé.

#### Scenario: Première évaluation
- **WHEN** aucun fichier courant n'existe
- **THEN** sept politiques sans résultats inventés sont initialisées

#### Scenario: Historique de quatre modes
- **WHEN** un historique valide de schéma 1 ou 2 est chargé
- **THEN** DeepSeek devient mode 7, l'ancien OpenRouter mesuré est réinitialisé et le mode 6 gratuit est neuf
- **AND** aucune sélection courante n'est héritée

#### Scenario: Historique illisible
- **WHEN** les politiques, le schéma ou le JSON sont invalides
- **THEN** le fichier reste préservé et la publication est arrêtée

### Requirement: Politiques et sélection explicites
PLLM SHALL garder sept priorités : payants Go 1/2, gratuits Go 3/4,
OpenRouter payé 5, OpenRouter gratuit 6 et DeepSeek direct 7. Les comptes et
références historiques SHALL être conservés. Les modes 1 à 6 SHALL provenir du
catalogue TFL avec route, fournisseur et date. Medium SHALL être demandé
partout où un benchmark est exécuté. La première politique valide par priorité
SHALL être sélectionnée.

#### Scenario: Sélection selon la priorité
- **WHEN** plusieurs politiques sont valides
- **THEN** la première par priorité 1 à 7 est retenue indépendamment du débit des autres

#### Scenario: Authentification des modes renumérotés
- **WHEN** les modes sont évalués
- **THEN** les références existantes sont utilisées sans création ou déplacement de secret
- **AND** policy=mode1 sert à 1/3, policy=mode2 à 2/4, ancien policy=mode3 à 5/6 et ancien policy=mode4 à 7

### Requirement: Quotas avant performance
Les modes 1/2/5/7 SHALL consulter leurs quotas ou soldes avant toute
évaluation nécessitant un accès fournisseur. Une donnée absente, refusée ou
incohérente SHALL arrêter leur évaluation. Les modes 3/4/6 SHALL NOT consulter
quota ou solde ; ils SHALL publier ce contrôle comme non applicable.
L'authentification et les limitations fournisseur SHALL rester applicables.

#### Scenario: Gratuit sans contrôle de quota
- **WHEN** mode3 ou mode4 est évalué
- **THEN** aucune requête usage, credits ou balance n'est envoyée, même entre paliers
- **AND** les ressources du compte associé ne conditionnent pas sa validité

#### Scenario: Contrôle indispensable indisponible ou épuisé
- **WHEN** un contrôle des modes 1/2/5/7 est refusé, indisponible ou épuisé
- **THEN** la politique reste invalide sans génération correspondante ni repli gratuit

#### Scenario: Quota indispensable indisponible
- **WHEN** un contrôle des modes 1/2/5/7 échoue
- **THEN** la politique reste invalide sans test de performance correspondant

#### Scenario: Quota épuisé ou non disponible
- **WHEN** un contrôle de quota des modes 1/2/5/7 est indisponible ou refusé
- **THEN** la politique reste invalide sans performance ni repli gratuit

#### Scenario: Épuisement confirmé
- **WHEN** les ressources payantes sont confirmées épuisées
- **THEN** 1/2/5/7 restent invalides sans génération ni repli gratuit

### Requirement: Conditions de quota propres aux fournisseurs
Go payant (modes 1/2) SHALL exiger trois périodes disponibles, statut ok
et usage <100 %. Mode5 SHALL exiger un solde OpenRouter strictement positif
et SHALL NOT utiliser de candidat gratuit. Le mode6 gratuit SHALL NOT consulter
de solde. DeepSeek (mode7) SHALL exiger
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
- **WHEN** modes 5, 6 et 7 sont évalués
- **THEN** les contrôles propres à leurs fournisseurs restent applicables

#### Scenario: Limite de quota atteinte
- **WHEN** un quota Go atteint 100 % ou le solde OpenRouter est épuisé
- **THEN** aucun candidat payant ou gratuit correspondant n'est testé

### Requirement: Mesures concluantes du modèle sélectionné
Tous les modes sauf 5 SHALL exiger réponse complète, comptage fiable et
mesures actuelles. Contexte d'entrée ≥1M SHALL être vérifié sans benchmark
d'un million de tokens. Les gratuits 3/4/6 exigent TTFT <30 s et débit >20 ;
les payants benchmarkés 1/2/7 exigent TTFT <90 s et débit >15. Mode5 vérifie
seulement paid, contexte, coût ≤0,20 EUR/M et solde positif. Le protocole reste
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
- **WHEN** un candidat payant de mode 1/2/7 mesure TTFT ≥90 s ou débit ≤15 tokens/s
- **THEN** son candidat reste invalide

#### Scenario: Limites strictes
- **WHEN** un candidat atteint TTFT 30 s ou débit 20 tokens/s pour un candidat gratuit, ou TTFT 90 s ou débit 15 tokens/s pour les candidats payants
- **THEN** ce candidat est invalide

#### Scenario: Repli après limitation fournisseur
- **WHEN** une limitation HTTP 429 conduit à choisir un autre modèle de la catégorie autorisée
- **THEN** ce candidat exige ses propres contrôles et mesures concluantes
- **AND** l'épuisement du dernier palier ne transforme pas le repli en réussite

#### Scenario: TTFT sous la nouvelle limite
- **WHEN** un candidat payant benchmarké de mode1/2/7 mesure 70,4 s et satisfait les autres critères
- **THEN** son seuil TTFT est satisfait ; ce même TTFT échoue pour un candidat gratuit

#### Scenario: Limite stricte de TTFT atteinte
- **WHEN** le TTFT atteint 30 s pour un candidat gratuit ou 90 s pour les candidats payants benchmarkés
- **THEN** le candidat reste invalide même avec un débit suffisant

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL garder les paliers 1024, 2048, 4096, 8192 et 120 s par requête.
Les contrôles applicables SHALL précéder chaque requête, sans quota en 3/4/6.
Un HTTP 400/429 SHALL arrêter le candidat sans repli vers un autre niveau
d'effort. La mémoire SHALL distinguer modèle, raisonnement et profil de débit,
garder les succès historiques sans les réutiliser pour un autre profil. Une
mémoire invalide SHALL NOT être écrasée ; un ancien succès SHALL NOT valider
l'invocation.

#### Scenario: Nouvelle politique gratuite
- **WHEN** un mode gratuit 3/4/6 est évalué pour la première fois après migration
- **THEN** son premier palier est 1024, sans réutiliser l'ancien OpenRouter ou DeepSeek
- **AND** les apprentissages OpenRouter/DeepSeek incompatibles avec le nouveau schéma ne valident pas les modes 5/6/7

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
- **THEN** aucun repli vers un autre effort n'est autorisé
- **AND** HTTP 401/403/429, troncature ou seuil ne déclenchent aucun repli d'effort

#### Scenario: Nouveau profil après un ancien succès
- **WHEN** un succès utilise l'ancien débit entre fragments
- **THEN** il reste historique et n'amorce pas le nouveau protocole
- **AND** sans succès Medium du nouveau profil, le premier palier est 1024

#### Scenario: Réutilisation du nouveau profil
- **WHEN** une réussite Medium mémorisée correspond à la même configuration et au même profil de débit
- **THEN** son palier peut être repris avec des mesures actuelles

### Requirement: Invocation normale et mode active silencieux
L'invocation normale SHALL évaluer les sept modes et restituer un tableau
à sept lignes et leurs ressources ou mention non applicable. Chaque mode
SHALL arrêter son parcours au premier candidat valide. active SHALL s'arrêter
à la première politique valide et publier sans sortie console ou
conversationnelle. Les modes non visités SHALL garder evaluated_this_run=false
et SHALL NOT être sélectionnés depuis l'historique.

#### Scenario: Invocation normale après une réussite
- **WHEN** un candidat valide est retenu dans un mode
- **THEN** les candidats suivants de ce mode ne sont pas testés et la politique suivante est évaluée

#### Scenario: active s'arrête sur le premier gratuit valide
- **WHEN** les modes 1/2 sont invalides et le premier gratuit conforme de mode3 réussit
- **THEN** les modes 4/5/6/7 ne sont pas évalués et la publication reste silencieuse

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
Les commandes 1 à 7 SHALL cibler le premier candidat admissible de ce mode.
11–13 et 21–23 SHALL garder les rangs bruts Go ; 31–33 et 41–43 SHALL cibler
les rangs de la liste gratuite admissible Go ; 51–53 SHALL
reprendre les rangs bruts OpenRouter. 61–63 SHALL viser les rangs gratuits
OpenRouter admissibles. 7 SHALL garder DeepSeek direct. Un
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
SHALL examiner exclusivement les gratuits Go, et le mode6 SHALL examiner
exclusivement les gratuits OpenRouter, indépendamment des ressources. Mode5
SHALL examiner exclusivement les payants OpenRouter avec crédit positif,
contexte ≥1M et coût moyen ≤0,20 EUR/M, sans benchmark ni exigence Medium.
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
les modes benchmarkés mais pas par le mode5. Les
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

### Requirement: Diagnostic visible et sûr
Le rapport SHALL garder huit colonnes et les diagnostics dans État, sans
secret ni compte. Les modes payants épuisés SHALL être rouges et invalides.
Mode5 SHALL afficher `-` pour les mesures et indiquer l'absence de benchmark.
Les gratuits valides SHALL porter la mention gratuit et ressources non
applicables. Le JSON conserve causes, candidats, exclusions, tentatives et
quotas sans inventer de mesure pour un candidat non visité.

#### Scenario: Ressources gratuites
- **WHEN** le rapport des modes 3/4/6 est publié
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
- **WHEN** un mode gratuit reçoit HTTP 401, 403 ou 429
- **THEN** le diagnostic reste visible sans quota inventé ni attente indéfinie

#### Scenario: Ressources non applicables
- **WHEN** le rapport des modes 3/4/6 est publié
- **THEN** leur ligne indique quota non applicable et leurs quotas restent null

#### Scenario: Corps d'erreur sensible
- **WHEN** un refus contient des informations privées
- **THEN** seuls les champs autorisés filtrés sont conservés

#### Scenario: Réussite gratuite avec quota épuisé
- **WHEN** mode3/4 satisfait ses seuils gratuits avec le quota Go associé épuisé
- **THEN** il affiche Valide et gratuit avec ressources non applicables ; un crédit OpenRouter épuisé laisse mode5 invalide

### Requirement: Invariants du classement tarifaire
Les priorités 1 à 7 SHALL respecter les seuils benchmarkés gratuits/payants,
les quotas, le raisonnement, les forçages et le protocole 8. Le mode5 SHALL
refuser les candidats gratuits, sans benchmark, selon sa catégorie payante.
Le JSON SHALL tracer les candidats visités et leurs contrôles ;
active SHALL s'arrêter au premier mode valide. Le rapport SHALL conserver
ses huit colonnes.

#### Scenario: Publication et priorités préservées
- **WHEN** plusieurs politiques valides ont été évaluées selon leurs règles
- **THEN** la première par priorité 1 à 7 est sélectionnée avec huit colonnes inchangées
- **AND** son prix courant et les preuves des candidats visités restent auditables

### Requirement: Classement des gratuits par performances
Les modes 3/4 SHALL parcourir les gratuits admissibles Go exclusivement et
le mode6 SHALL parcourir les gratuits OpenRouter ; chaque mode SHALL garder
l'ordre TFL et retenir le premier succès aux tests
gratuits actuels. Ils SHALL NOT tester les candidats suivants pour chercher
un débit supérieur. Après échec d'un gratuit, le suivant SHALL conserver
ses propres mesures et les seuils stricts <30 s et >20 tokens/s.

#### Scenario: Premier gratuit valide
- **WHEN** le premier candidat gratuit du fournisseur de ce mode satisfait les critères
- **THEN** il est retenu et aucun autre candidat du mode n'est testé

#### Scenario: Repli vers le gratuit suivant
- **WHEN** un gratuit Go ou OpenRouter échoue sans blocage d'authentification et le suivant réussit
- **THEN** le premier gratuit conforme est retenu sans contrôle de quota ni de solde

#### Scenario: Gratuit plus performant
- **WHEN** un gratuit conforme précède un autre candidat potentiellement plus performant
- **THEN** le premier succès est retenu et le suivant n'est pas testé

### Requirement: Exclusion LM indépendante des catalogues et historiques
PLLM SHALL charger LM avant tout appel fournisseur et exclure les modèles
interdits de tout test et sélection : candidats TFL, rangs, replis, mode7
et frontière de génération, même avec un ancien catalogue ou une mémoire.
Une cible forcée interdite SHALL être refusée sans substitution.

#### Scenario: Candidat interdit
- **WHEN** un candidat figure dans LM avant sa génération
- **THEN** aucune requête de génération ni sélection n'est effectuée

### Requirement: Effort vérifiable indépendant du catalogue et de l'historique
PLLM SHALL exiger une capacité Medium vérifiable pour tout candidat
benchmarké, y compris DeepSeek direct au mode7. Le mode5 est exempté de cette
exigence et de toute génération. Seul Medium SHALL être demandé et admis pour
les autres modes. Un exclu SHALL NOT
être généré, sélectionné ou affiché dans les tableaux ;
son motif SHALL rester dans le JSON. Un forçage exclu SHALL échouer sans
substitution. Les sept politiques SHALL rester présentes dans l'état interne.

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie une liste contenant medium, ou null explicite signifiant tous les efforts
- **THEN** le candidat satisfait le filtre d'effort sous réserve des autres critères
- **AND** une clé absente, une valeur invalide, un booléen reasoning ou supports_max_tokens seul reste exclu

#### Scenario: Ancien catalogue ou résultat historique
- **WHEN** un candidat benchmarké précédemment retenu n'a pas de preuve d'effort admissible
- **THEN** il ne peut être sélectionné, généré ou affiché malgré son historique
- **AND** cette exigence ne s'applique pas au mode5, qui ne benchmarke pas

#### Scenario: Cible forcée sans effort vérifiable
- **WHEN** un rang forcé désigne un modèle sans preuve Medium
- **THEN** il est refusé dans les modes benchmarkés sans génération ni substitution
- **AND** un rang du mode5 reste soumis seulement au plafond de coût et au contexte

#### Scenario: Candidat direct sans preuve
- **WHEN** le modèle DeepSeek direct n'a pas de capacité Medium vérifiable
- **THEN** il est exclu avant génération et son identité n'apparaît pas dans les tableaux

### Requirement: Effort demandé exclusivement Medium

PLLM SHALL demander et publier des résultats dont l'effort effectif est
`medium` pour les politiques benchmarkées, les forçages de rang et chaque
transport. Le mode5 ne demande pas d'effort et n'exécute pas de génération.
Un refus ou une absence de prise en charge SHALL invalider les autres
candidats sans repli vers un autre effort.

#### Scenario: Demande forcée ou transport non compatible

- **WHEN** une cible forcée ou un transport ne peut pas effectuer une requête
  en Medium
- **THEN** le candidat est déclaré invalide sans génération à un autre effort

### Requirement: Historique limité aux résultats Medium

Une capacité fournisseur incluant Medium SHALL NOT valider un résultat
historique benchmarké dont l'effort demandé ou exécuté n'est pas explicitement
établi comme Medium. PLLM SHALL invalider ces résultats avant affichage et
sélection, conserver leur motif dans les exclusions et ne pas réutiliser leurs
paliers. Cette règle ne s'applique pas au mode5 non benchmarké.

#### Scenario: Historique incompatible malgré une capacité Medium

- **WHEN** le résultat ou une de ses tentatives historiques n'enregistre pas
  explicitement Medium comme effort demandé
- **THEN** PLLM l'invalide avant affichage et sélection
- **AND** conserve le motif d'exclusion sans réutiliser son palier

### Requirement: Consommation des preuves et équivalences documentées
PLLM SHALL préserver les preuves TFL par fournisseur, modèle et protocole.
Les modes benchmarkés SHALL admettre uniquement Medium après vérification et
utiliser les paramètres documentés sur leur route publiée. Le mode5 n'exige
aucun effort et n'effectue aucune génération. Un contexte encore invérifiable SHALL déclencher
le workflow d'investigation du LLM avant toute admission ; un contexte
invérifiable après investigation SHALL rester exclu.

#### Scenario: Équivalence de transport
- **WHEN** une preuve vérifiée établit une équivalence Medium vers thinking.type=enabled sur Chat Completions
- **THEN** PLLM utilise ce paramètre et trace son équivalence sans modifier la route

#### Scenario: Preuve ou contexte absent
- **WHEN** aucun résultat d'investigation ne permet l'admission
- **THEN** le modèle n'atteint pas la génération et le motif reste auditable
