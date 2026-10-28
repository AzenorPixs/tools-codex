# tfl-catalog Specification

## Purpose

Définir la collecte, le filtrage, le classement et la publication vérifiable du catalogue TFL sans données sensibles.

## Requirements

### Requirement: Collecte complète et ordre des fournisseurs
TFL SHALL collecter exclusivement OpenCode Go et OpenRouter, avec
models.dev comme complément de métadonnées OpenCode. Une erreur de collecte,
d'authentification ou de données indispensables SHALL faire échouer la
génération sans rapport partiel complet. La restitution SHALL présenter
OpenCode Go puis OpenRouter ; le JSON SHALL NOT contenir de section opencode.

#### Scenario: Collecte complète
- **WHEN** les deux collectes et leurs métadonnées indispensables réussissent
- **THEN** le rapport contient les deux tableaux Go puis OpenRouter et conserve seulement opencode_go et openrouter dans le JSON

#### Scenario: Échec d'un fournisseur
- **WHEN** une collecte indispensable échoue
- **THEN** TFL signale l'échec et ne déclare pas le catalogue actualisé

### Requirement: Seuils de sélection vérifiables
TFL SHALL vérifier contexte ≥1M, coût moyen ≤0,50 USD/M Go et ≤0,10 EUR/M
OpenRouter au taux BCE. Prix/contexte inconnus sont exclus. Les payants
OpenRouter satisfaisant contexte, coût, modalités et LM restent admissibles
sans Medium. Les gratuits vérifiés SHALL réussir réponse complète en Medium,
TTFT <30 s et débit >20 tokens/s avant inclusion ; échecs et preuves restent
dans excluded_models.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte ou le coût d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

#### Scenario: Gratuit échoué ou non mesurable
- **WHEN** le gratuit échoue sur un seuil, l'effort Medium, l'accès, HTTP ou la mesure
- **THEN** il est exclu de models avec sa cause, ses tentatives et ses mesures disponibles

#### Scenario: Payant sans Medium
- **WHEN** un payant OpenRouter vérifie contexte ≥1M, coût ≤0,10 EUR/M, modalités et liste noire, mais ne publie pas Medium
- **THEN** il reste dans models avec ses métadonnées d'effort, sans investigation Medium bloquante

#### Scenario: Seuils gratuits stricts
- **WHEN** le TTFT atteint 30 s ou le débit atteint au plus 20 tokens/s
- **THEN** le gratuit est exclu même si ses prix, contexte et effort Medium sont admissibles

### Requirement: Prix finis et JSON strict
TFL SHALL exclure avec un motif les prix OpenRouter non finis ou dont la
conversion par million ou le calcul de moyenne déborde. Le catalogue publié
SHALL être du JSON strict, sans `NaN` ni infini. Un échec de sérialisation
SHALL empêcher la publication d'un catalogue non conforme.

#### Scenario: Prix non exploitable
- **WHEN** un prix vaut `NaN`, un infini ou déborde lors du calcul
- **THEN** le modèle est exclu comme coût non vérifiable
- **AND** les prix finis admissibles restent classés selon les règles communes

### Requirement: Modalités et liste noire LM explicites
Les sorties déclarées audio, vidéo, speech ou sound SHALL être exclues. Une
entrée multimodale reste admissible ; une sortie inconnue SHALL être signalée
comme non vérifiée. TFL SHALL appliquer exclusivement la liste noire partagée
LM aux deux catalogues, sans liste propre ni exclusion permanente intégrée.
muse-spark-1.2-contributor SHALL être géré comme une entrée LM ordinaire,
avec la même identité pour Go et OpenRouter.

#### Scenario: Retrait LM respecté dans les trois catalogues
- **WHEN** muse-spark-1.2-contributor est retiré de LM
- **THEN** aucune liste interne TFL ne l'exclut dans les deux catalogues
- **AND** les autres critères de contexte, coût, modalités et effort restent obligatoires

#### Scenario: Modèle hors critères
- **WHEN** un modèle examiné ne satisfait pas un critère de sélection vérifiable
- **THEN** il ne figure pas dans le tableau retenu
- **AND** son motif d'exclusion est conservé dans le catalogue JSON

### Requirement: Sélection OpenRouter explicite
La sélection OpenRouter SHALL être dynamique sur tous les modèles retournés
par l'API, sans liste prédéfinie d'identifiants admissibles. Elle SHALL retenir
les modèles payants satisfaisant les filtres communs de contexte, coût et modalités,
ainsi que la liste noire LM. L'absence d'un ancien modèle SHALL rester
sans effet sur les autres résultats admissibles.

#### Scenario: Nouveau modèle admissible
- **WHEN** un identifiant inédit respecte les filtres communs
- **THEN** il est classé sans modification de liste ou de code

#### Scenario: Identifiant fixé absent
- **WHEN** un modèle précédemment classé disparaît de la réponse API
- **THEN** les autres modèles admissibles sont publiés sans erreur liée à cet identifiant

### Requirement: Classement et colonnes communes
TFL SHALL classer les modèles de chaque catalogue par coût moyen croissant.
Les deux tableaux fournisseurs SHALL garder les colonnes rang, modèle/ID,
contexte, sortie, prix d'entrée, prix de sortie, coût moyen et code couleur.
TFL SHALL ajouter un tableau commun des essais gratuits, avec fournisseur,
modèle, TTFT, débit, raisonnement et état/cause, incluant les échecs dont
l'effort Medium est vérifiable ; les exclus faute de preuve Medium SHALL
rester seulement dans le JSON.

#### Scenario: Comparaison des tableaux fournisseurs
- **WHEN** les deux tableaux fournisseurs sont restitués
- **THEN** leurs huit colonnes ont la même structure, avec Go en USD et OpenRouter en EUR et chaque classement suit le coût moyen croissant

### Requirement: Publication des fichiers courants
TFL SHALL publier un catalogue
`tfl.json` et son rapport `tfl.md`, horodatés, dans `data/` ou dans le répertoire
demandé par `--output-dir`. Chaque fichier SHALL être remplacé atomiquement.

#### Scenario: Publication du catalogue
- **WHEN** la génération et la publication réussissent
- **THEN** les deux fichiers décrivent la même collecte et ses filtres
- **AND** la restitution indique la date et les chemins des fichiers sans exposer de secret

### Requirement: Métadonnées auditables
Le JSON TFL SHALL conserver sources, exclusions et routage sans secret.
Les essais gratuits SHALL tracer critères, niveau, tentatives, comptages,
profil, formule et durée totale non arrondie. Le débit SHALL employer le même
moteur et la même durée complète que PLLM. Une mesure historique SHALL NOT
valider une collecte actuelle. Le rapport SHALL préciser que le débit moyen
inclut l'attente et le TTFT.

#### Scenario: Consultation du routage d'un modèle OpenCode Go
- **WHEN** un consommateur examine un modèle retenu du catalogue
- **THEN** il retrouve les champs de routage et leurs sources sans déduire le protocole du seul nom commercial

#### Scenario: Qualification gratuite avec réception en rafale
- **WHEN** un gratuit fournit sa réponse par fragments groupés
- **THEN** la qualification applique les seuils au débit moyen sur la requête complète
- **AND** les mesures non fiables sont exclues avec cause, sans écrêtage artificiel

### Requirement: Accès aux secrets et repli auto limité
TFL SHALL garder les secrets en mémoire et hors du modèle et des sorties.
En auto, il SHALL essayer le secret 1 puis 2 si inaccessible ; une erreur API
après sélection SHALL NOT déclencher l'autre secret. Les gratuits SHALL
utiliser les clés existantes sans quota ni solde. OpenRouter SHALL utiliser
son environnement puis sa référence historique PLLM. Les autorisations
hors sandbox SHALL être respectées sans contournement.

#### Scenario: Secret du mode 1 inaccessible
- **WHEN** le mode `auto` ne peut pas récupérer le secret du mode 1
- **THEN** TFL tente de récupérer celui du mode 2 sans afficher aucune valeur

#### Scenario: Refus API après sélection du secret
- **WHEN** la requête API utilisant le secret sélectionné échoue
- **THEN** TFL rapporte l'erreur sans essayer l'autre secret pour cette requête

### Requirement: Actualisation tarifaire sans repli historique
TFL SHALL collecter à chaque génération les tarifs Go
dans sa documentation officielle, et OpenRouter dans son
API modèles. TFL MUST NOT utiliser de table statique ou ancien catalogue
comme repli. Chaque catalogue SHALL exposer la source et la date de
récupération tarifaire dans le JSON.

#### Scenario: Nouveau modèle et nouveau prix
- **WHEN** un modèle disponible possède un tarif officiel exploitable ou son tarif change
- **THEN** la génération utilise ce tarif sans modification du code
- **AND** les filtres existants restent applicables

#### Scenario: Source tarifaire inexploitable
- **WHEN** une source indispensable est inaccessible, invalide ou de format non reconnu
- **THEN** TFL échoue explicitement avant publication
- **AND** les rapports précédents restent inchangés

### Requirement: Correspondances tarifaires non ambiguës
TFL SHALL associer les tarifs Go aux identifiants disponibles par une
correspondance vérifiable de nom ou d'identifiant. Une absence de tarif SHALL
produire une exclusion motivée. Une collision de correspondances ou des
tarifs contradictoires pour une même variante SHALL produire un échec explicite.
Les prix utilisés SHALL être finis, non négatifs et exprimés en USD par
million de tokens. Les montants barrés MUST NOT servir de prix courant.

#### Scenario: Tarif introuvable
- **WHEN** aucun tarif ne correspond à un modèle disponible
- **THEN** le modèle est exclu avec le motif tarifaire dans le JSON

#### Scenario: Prix contradictoires
- **WHEN** deux tableaux donnent des prix différents pour la même variante
- **THEN** la génération échoue sans choisir silencieusement l'un des tableaux

### Requirement: Variantes tarifaires auditables
TFL SHALL conserver séparément les prix d'entrée, sortie, cache et les variantes
pointe/hors pointe ou de contexte disponibles dans le JSON. Pour Go, le
classement SHALL utiliser le hors pointe et le coût moyen maximal entre
paliers de contexte lorsqu'il en existe plusieurs. Une estimation non
collectée SHALL rester non vérifiée.

#### Scenario: Pointe et paliers de contexte
- **WHEN** la source publie plusieurs variantes tarifaires pour un modèle
- **THEN** le JSON conserve les variantes et la règle ayant déterminé le prix de classement
- **AND** le cache et les prix pointe ne sont pas confondus avec l'entrée hors pointe

### Requirement: Compatibilité du rafraîchissement
Les filtres, colonnes communes, interfaces CLI et champs consommés par PLLM
SHALL rester compatibles. La sélection OpenRouter SHALL pouvoir contenir tout
identifiant admissible du catalogue courant. Une route Go inconnue SHALL
être signalée sans protocole inventé.

#### Scenario: OpenRouter actualisé
- **WHEN** le catalogue API évolue en modèles ou en prix
- **THEN** TFL recalcule sa sélection et son classement avec les données courantes
- **AND** le JSON conserve leur provenance et les prix de cache disponibles

### Requirement: Examen intégral du catalogue OpenRouter
TFL SHALL interroger le catalogue modèles OpenRouter sans filtre de catégorie,
modalité ou nombre limitant l'examen local. Chaque modèle examiné SHALL être
retenu ou exclu avec un motif selon les règles communes. Un coût moyen nul
vérifié SHALL être admissible ; le plafond OpenRouter SHALL rester
0,10 EUR/M au taux BCE vérifié. Une collecte invalide SHALL bloquer la
publication ; une sélection vide issue d'une collecte valide SHALL être
publiée sans interrompre les autres catalogues.

#### Scenario: Modèles gratuits et hors fenêtre
- **WHEN** le catalogue contient des modèles gratuits, trop coûteux, sans prix ou hors contexte
- **THEN** les modèles gratuits satisfaisant les autres filtres sont admissibles
- **AND** chaque modèle rejeté possède un motif d'exclusion dans le JSON

#### Scenario: Catalogue sans résultat admissible
- **WHEN** aucun modèle courant ne satisfait les filtres après une collecte valide
- **THEN** TFL publie models vide, ses exclusions courantes et une mention explicite dans le tableau OpenRouter
- **AND** la collecte et la publication des autres catalogues continuent

#### Scenario: Variante tarifaire temporelle
- **WHEN** un modèle admissible publie des variantes conditionnées par jours ou horaires UTC
- **THEN** le JSON conserve séparément ces conditions et leurs prix
- **AND** le classement reste fondé sur les prix API de base

### Requirement: Modalités Go collectées sans liste de modèles
TFL SHALL résoudre les modalités Go depuis les déclarations courantes de
l'API et de models.dev, sans liste statique de modèles ni inférence par nom.
Les modalités connues SHALL conserver leur source ; une modalité absente
SHALL rester non vérifiée. Des déclarations contradictoires SHALL produire
une erreur explicite avant publication.

#### Scenario: Modèle inédit documenté
- **WHEN** un modèle inédit possède des modalités publiées dans models.dev
- **THEN** TFL les restitue avec leur provenance sans ajout de son identifiant au code

#### Scenario: Modalité absente ou contradictoire
- **WHEN** les sources n'indiquent aucune sortie ou indiquent des sorties contradictoires
- **THEN** une absence reste non vérifiée et une contradiction bloque explicitement la publication

### Requirement: Transport Go résolu sans liste de modèles
TFL SHALL résoudre le transport Go depuis des métadonnées explicites de
protocole/SDK et de base API, sans liste statique de modèles. Les champs
api_endpoint, api_protocol et endpoint_source SHALL conserver un contrat
compatible avec les consommateurs. Un protocole non reconnu ou une base
manquante SHALL rester non vérifié avec un motif, sans repli implicite.

#### Scenario: Nouvelle route publiée
- **WHEN** la source publie une nouvelle base API et un transport reconnu pour un modèle
- **THEN** TFL actualise ses champs de routage et leur provenance sans modifier de liste de modèles

#### Scenario: Protocole inconnu
- **WHEN** le transport publié n'est pas reconnu ou manque
- **THEN** TFL signale une route non vérifiée sans en inventer une autre

### Requirement: Origine sûre des endpoints Go
TFL SHALL valider HTTPS et l'origine OpenCode des endpoints publiés. Une URL
avec identifiants utilisateur, query, fragment ou origine étrangère SHALL
être rejetée explicitement avant publication. La résolution documentaire
SHALL être distinguée d'une qualification réelle de génération.

#### Scenario: Source de routage non sûre
- **WHEN** une métadonnée désigne une URL non sûre ou extérieure à l'origine OpenCode
- **THEN** la génération échoue avant publication sans restituer de secret

#### Scenario: Route documentée
- **WHEN** une route est résolue depuis les sources publiées
- **THEN** le catalogue indique ses sources et sa date sans prétendre à un test de génération

### Requirement: Exclusion LM avant sélection et test
TFL SHALL charger la liste commune LM avant tout appel fournisseur et
l'appliquer à Go et OpenRouter avant tout classement et
test gratuit. Les modèles interdits SHALL être absents de models et
free_performance_results ; excluded_models SHALL conserver leur motif.
Le JSON SHALL tracer la liste appliquée sans données personnelles.
Les seuils, prix, transports et ordre SHALL rester inchangés. Les exclusions
par identifiant SHALL dépendre exclusivement de LM.

#### Scenario: Modèle interdit pourtant admissible
- **WHEN** mimo-v2.5 satisfait prix, contexte et modalités dans un catalogue
- **THEN** il est exclu avant tout test gratuit et absent des tableaux retenus
- **AND** son exclusion est auditée sans requête de génération

#### Scenario: Liste utilisateur modifiée
- **WHEN** LM ajoute un modèle avant la nouvelle invocation TFL
- **THEN** les deux catalogues appliquent la liste courante sans mise à jour du code

### Requirement: Catalogue OpenRouter avec préfixes marqués
TFL SHALL examiner les identifiants OpenRouter à préfixe `~` valide sans
échec de grammaire LM. Les exclusions LM SHALL précéder métadonnées, tri
et génération. Les autres filtres, seuils, identifiants publiés et règles
de publication atomique SHALL rester inchangés.

#### Scenario: Catalogue mélangeant identifiants ordinaires et marqués
- **WHEN** le catalogue contient un modèle marqué autorisé et un modèle marqué exclu
- **THEN** le premier est évalué selon les filtres habituels en conservant son identifiant fournisseur
- **AND** le second figure dans les exclusions sans génération ni examen de ses prix

#### Scenario: Collecte complète sans génération interdite
- **WHEN** les deux catalogues valides sont collectés avec ces identifiants OpenRouter
- **THEN** TFL peut publier les deux sections avec leurs filtres et exclusions inchangés
- **AND** les modèles interdits restent absents des listes retenues et des tests gratuits

### Requirement: Effort vérifiable avant admission
TFL SHALL tester Medium sur le transport publié pour les gratuits admissibles,
même si leurs métadonnées sont absentes ou ne déclarent pas cet effort. Une
réponse complète SHALL prouver l'acceptation du paramètre sans établir l'effort
interne. Contexte, gratuité, réponse complète, TTFT et débit restent requis.
TFL SHALL conserver les payants OpenRouter comme catalogue tarifaire sans benchmark ; PLLM mode5 SHALL vérifier Medium et ses performances lors de sa propre évaluation.

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

### Requirement: Plafond OpenRouter en EUR
TFL SHALL appliquer une moyenne de base OpenRouter <= 0,10 EUR/M après
conversion au dernier taux BCE USD par EUR, positif et fini. Comparaison
non arrondie, prix natifs USD, prix EUR, source et dates de publication et de
récupération SHALL être tracés. Une conversion invérifiable SHALL bloquer
la publication et préserver les rapports précédents.

#### Scenario: Limite inclusive et montant supérieur
- **WHEN** la moyenne convertie atteint exactement 0,10 EUR/M ou dépasse ce seuil avant arrondi
- **THEN** seul le premier montant est admissible sous réserve des autres filtres

#### Scenario: Conversion non vérifiable
- **WHEN** le cours BCE est absent, invalide ou inaccessible
- **THEN** aucun nouveau rapport n'est publié et les fichiers précédents restent préservés

### Requirement: Deux tableaux fournisseurs sans catalogue général
TFL SHALL afficher Go puis OpenRouter, puis les essais gratuits admissibles
à l'effort. Les tableaux SHALL garder huit colonnes, Go en USD/M et OpenRouter
en EUR/M avec taux daté, même vides. La collecte, les essais et le JSON SHALL exclure OpenCode général. Go SHALL garder le plafond 0,50 USD/M.
Une sélection vide après filtrage ou qualification SHALL NOT bloquer les
autres sections. Les filtres et validations indispensables SHALL rester inchangés.

#### Scenario: Publication à deux tableaux
- **WHEN** les deux collectes satisfont les critères de validité
- **THEN** le rapport affiche Go puis OpenRouter, aucun tableau général, et le JSON conserve les deux sections

#### Scenario: Aucune preuve d'effort dans une section benchmarkée
- **WHEN** tous ses candidats gratuits sont exclus faute de preuve Medium
- **THEN** TFL publie la sélection vide et ses motifs sans réutiliser d'anciennes qualifications
- **AND** les exclus restent absents des tableaux et des essais gratuits

### Requirement: Publication explicite des sélections vides
Chaque catalogue valide SHALL publier models éventuellement vide,
selection_status (available ou empty), exclusion_summary (motif vers nombre),
compteurs et exclusions détaillées. Un tableau vide SHALL afficher
« Aucun modèle admissible » et la synthèse, sans fausse ligne de modèle.
Deux sélections vides valides SHALL produire les fichiers frais et un code
zéro. Les erreurs réelles SHALL rester bloquantes ; le planning contrôle les deux sections courantes.

#### Scenario: Go vide et OpenRouter admissible
- **WHEN** les collectes sont valides, Go ne retient aucun modèle et OpenRouter en retient
- **THEN** les deux tableaux sont publiés dans l'ordre Go puis OpenRouter et le second contient ses modèles admissibles
- **AND** Go expose son état vide, sa synthèse et ses exclusions courantes

#### Scenario: Catalogue général vide
- **WHEN** TFL publie une nouvelle collecte
- **THEN** aucune section opencode ni donnée générale ne figure dans le JSON ou les essais
- **AND** Go et OpenRouter sont les deux seuls catalogues courants

#### Scenario: Section vidée par la qualification gratuite
- **WHEN** tous les modèles d'une section sont des gratuits échoués ou non mesurables
- **THEN** models est vide et les essais, leurs causes filtrées et les exclusions sont publiés
- **AND** les autres sections et leurs qualifications continuent

#### Scenario: Trois sélections vides
- **WHEN** les deux collectes sont valides mais aucun modèle ne reste après filtrage ou qualification
- **THEN** TFL publie les sections vides, les deux tableaux explicites, les exclusions et les essais effectués avec un code de sortie zéro

#### Scenario: Erreur réelle
- **WHEN** une source indispensable, une authentification, une conversion BCE ou une donnée de sécurité est invalide
- **THEN** TFL signale l'erreur, retourne un code non nul et préserve les rapports précédents

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

#### Scenario: Effort inconnu éprouvé par appel réel
- **WHEN** Medium n'est pas publié dans les métadonnées mais une réponse complète suit la requête avec ce paramètre
- **THEN** TFL enregistre l'acceptation API et continue d'appliquer les seuils de performance
- **AND** le rapport ne prétend pas que le fournisseur a utilisé un niveau interne Medium

### Requirement: Empreintes de preuves documentaires reproductibles
TFL SHALL calculer SHA-256 du texte visible HTML normalisé en UTF-8 NFC et
espaces réduits, ou des octets reçus pour les sources non HTML. Chaque entrée
SHALL tracer `fingerprint_method`. Les scripts et balises sans changement de
texte visible SHALL NOT invalider une preuve.

#### Scenario: Balisage HTML volatil
- **WHEN** les scripts ou balises changent sans différence du texte visible
- **THEN** l'empreinte reste stable ; un changement visible déclenche une nouvelle recherche

### Requirement: Efforts publiés et équivalences documentées
TFL SHALL normaliser reasoning_options et conserver la preuve Medium par
fournisseur, modèle et protocole. Un alias ou une réponse complète acceptant
`medium` satisfait le critère de paramètre, sans prouver l'effort interne. Seul
le paramètre Medium du transport publié SHALL être envoyé.

#### Scenario: Medium équivaut au raisonnement activé
- **WHEN** les sources officielles ou une réponse API complète établissent l'acceptation de Medium sur le protocole utilisé
- **THEN** Medium est admissible et le paramètre documenté du protocole est envoyé
- **AND** les autres critères, contrôles et seuils restent obligatoires

### Requirement: Source unique LM
TFL SHALL appliquer uniquement la liste LM, sans liste permanente intégrée.

#### Scenario: Retrait d'une ancienne exclusion permanente
- **WHEN** LM retire muse-spark-1.2-contributor
- **THEN** aucune liste TFL résiduelle ne l'exclut, y compris avec préfixe fournisseur

### Requirement: Retrait intégral du catalogue général
TFL SHALL NOT appeler les collecteurs de disponibilité, prix ou métadonnées
du catalogue général OpenCode, ni qualifier ou lister ses modèles. Seules les
métadonnées opencode-go de models.dev SHALL servir à Go. Les sections, ordres,
investigations et essais publiés SHALL concerner exclusivement Go/OpenRouter.

#### Scenario: Collecteurs généraux interdits
- **WHEN** les trois collecteurs généraux sont configurés pour échouer s'ils sont appelés
- **THEN** une collecte Go/OpenRouter valide réussit sans aucun appel général
- **AND** le JSON, le Markdown et stdout ne contiennent aucun modèle général

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

### Requirement: Prix décimaux canoniques malgré l'arrondi flottant
TFL SHALL utiliser les prix décimaux natifs comme référence du classement et des plafonds. Une projection numérique flottante SHALL être acceptée seulement si elle est finie, non négative et équivalente à la valeur décimale avec une tolérance relative de 1e-12 et sans tolérance absolue.

#### Scenario: Arrondi binaire de la projection tarifaire
- **WHEN** le prix numérique vaut `0.049999999999999996` et son prix décimal canonique vaut `0.05000000`
- **THEN** la projection est cohérente et le classement et les plafonds utilisent `0.05000000`

#### Scenario: Écart tarifaire réel
- **WHEN** le prix numérique vaut `0.051` et son prix décimal canonique vaut `0.05000000`
- **THEN** TFL exclut le candidat comme prix contradictoire avant classement ou génération
