## MODIFIED Requirements

### Requirement: Politiques et sélection explicites
PLLM SHALL garder six priorités : payants Go 1/2, gratuits Go 3/4,
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

### Requirement: Protocole des mesures traçable
Les mesures SHALL utiliser une horloge monotone. Le TTFT SHALL porter sur
le premier contenu visible. Le débit SHALL être le comptage de sortie divisé
par la durée totale non arrondie de la requête, TTFT inclus : global pour
Go, réponse seule pour OpenRouter/DeepSeek. Une réponse complète en
un bloc SHALL être mesurable. Durée ou comptage invalides SHALL produire
une mesure indisponible. Le JSON SHALL tracer profil, formule et durées.

#### Scenario: Deux catalogues OpenCode
- **WHEN** les candidats Go payants ou gratuits sont mesurés
- **THEN** leurs débits comptent raisonnement et réponse sur la durée complète
- **AND** aucun candidat général ne peut être mesuré depuis un ancien catalogue

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

### Requirement: Invocation forcée sans repli automatique
Un forçage SHALL limiter l'évaluation au mode et au candidat demandés.
Les commandes 1 à 6 SHALL cibler le premier candidat admissible de ce mode.
11–13 et 21–23 SHALL garder les rangs bruts Go ; 31–33 et 41–43 SHALL cibler
les rangs de la liste gratuite admissible Go ; 51–53 SHALL
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
SHALL examiner exclusivement les gratuits Go, quelle que
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

#### Scenario: Ancien catalogue général payant
- **WHEN** un ancien catalogue contient des payants généraux admissibles, avec ou sans candidat Go
- **THEN** les modes 1/2, forcés ou ordinaires, ne sélectionnent et ne testent que les payants opencode_go
- **AND** aucun résultat historique général ne remplace un candidat Go absent ou invalide

#### Scenario: Ancien catalogue général gratuit
- **WHEN** un ancien catalogue contient des gratuits généraux admissibles, avec ou sans candidat Go
- **THEN** les modes 3/4, forcés ou ordinaires, ne sélectionnent et ne testent que les gratuits opencode_go
- **AND** l'échec ou l'absence des gratuits Go ne déclenche aucun repli général

### Requirement: Classement des gratuits par performances
Les modes 3/4 SHALL parcourir les gratuits admissibles dans l'ordre TFL,
Go exclusivement, et SHALL retenir le premier succès aux tests
gratuits actuels. Ils SHALL NOT tester les candidats suivants pour chercher
un débit supérieur. Après échec d'un gratuit, le suivant SHALL conserver
ses propres mesures et les seuils stricts <30 s et >20 tokens/s.

#### Scenario: Premier gratuit valide
- **WHEN** le premier gratuit Go satisfait tous les critères
- **THEN** il est retenu et aucun autre gratuit Go n'est testé

#### Scenario: Repli vers le gratuit suivant
- **WHEN** un gratuit Go échoue sans blocage d'authentification et le gratuit Go suivant réussit
- **THEN** le premier gratuit Go conforme est retenu sans contrôle de quota ni de solde

#### Scenario: Gratuit plus performant
- **WHEN** un gratuit conforme précède un autre candidat potentiellement plus performant
- **THEN** le premier succès est retenu et le suivant n'est pas testé

### Requirement: Plafond EUR OpenRouter réappliqué
PLLM SHALL vérifier le coût moyen de base OpenRouter au plafond inclusif de
0,20 EUR/M avec le dernier taux BCE publié vérifié. Il SHALL recalculer depuis
les prix USD natifs sans faire confiance à une moyenne EUR historique et
SHALL conserver la provenance. Une conversion invérifiable SHALL empêcher
l'admission de ces candidats, y compris les rangs forcés et anciens catalogues.
Les priorités, catégories, contrôles de ressources et seuils de performance
SHALL rester inchangés.

#### Scenario: Ancien catalogue dépassant le nouveau plafond
- **WHEN** un candidat OpenRouter dépasse 0,20 EUR/M au taux courant
- **THEN** il est exclu avant génération même si son ancien catalogue le retenait

#### Scenario: Gratuit général après retrait du tableau
- **WHEN** les modes 3/4 lisent un ancien catalogue contenant opencode
- **THEN** ils ignorent cette section et ne consomment que les gratuits opencode_go admissibles
