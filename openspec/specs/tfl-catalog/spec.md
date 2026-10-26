# tfl-catalog Specification

## Purpose

Définir la collecte, le filtrage, le classement et la publication vérifiable du catalogue TFL sans données sensibles.

## Requirements

### Requirement: Collecte complète et ordre des fournisseurs
TFL SHALL collecter Go, le catalogue général OpenCode et OpenRouter, avec
models.dev comme complément de métadonnées OpenCode. Une erreur de collecte,
d'authentification ou de données indispensables SHALL faire échouer la
génération sans rapport partiel complet. La restitution SHALL présenter
OpenCode Go puis OpenRouter ; OpenCode général reste dans le JSON.

#### Scenario: Collecte complète
- **WHEN** les trois collectes et leurs métadonnées indispensables réussissent
- **THEN** le rapport contient les deux tableaux Go puis OpenRouter et conserve opencode dans le JSON

#### Scenario: Échec d'un fournisseur
- **WHEN** une collecte indispensable échoue
- **THEN** TFL signale l'échec et ne déclare pas le catalogue actualisé

### Requirement: Seuils de sélection vérifiables
TFL SHALL retenir un contexte vérifiable ≥1M et un coût moyen entrée/sortie
≤0,50 USD/M pour Go et général, hors pointe pour Go ; OpenRouter SHALL appliquer ≤0,20 EUR/M au taux BCE vérifié. Prix ou contextes inconnus SHALL être exclus.
Les gratuits vérifiés SHALL réussir une réponse complète en HIGH ou son repli
XHIGH autorisé, TTFT <30 s et débit >20 tokens/s avant inclusion dans models.
Leurs échecs SHALL rester dans excluded_models avec leurs preuves.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte ou le coût d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

#### Scenario: Gratuit échoué ou non mesurable
- **WHEN** le gratuit échoue sur un seuil, le raisonnement, l'accès, HTTP ou la mesure
- **THEN** il est exclu de models avec sa cause, ses tentatives et ses mesures disponibles

#### Scenario: Seuils gratuits stricts
- **WHEN** le TTFT atteint 30 s ou le débit atteint au plus 20 tokens/s
- **THEN** le gratuit est exclu même si ses prix et contexte sont admissibles

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
LM aux trois catalogues, sans liste propre ni exclusion permanente intégrée.
muse-spark-1.2-contributor SHALL être géré comme une entrée LM ordinaire,
avec la même identité pour Go, OpenCode général et OpenRouter.

#### Scenario: Retrait LM respecté dans les trois catalogues
- **WHEN** muse-spark-1.2-contributor est retiré de LM
- **THEN** aucune liste interne TFL ne l'exclut dans les trois catalogues
- **AND** les autres critères de contexte, coût, modalités et effort restent obligatoires

#### Scenario: Modèle hors critères
- **WHEN** un modèle examiné ne satisfait pas un critère de sélection vérifiable
- **THEN** il ne figure pas dans le tableau retenu
- **AND** son motif d'exclusion est conservé dans le catalogue JSON

### Requirement: Sélection OpenRouter explicite
La sélection OpenRouter SHALL être dynamique sur tous les modèles retournés
par l'API, sans liste prédéfinie d'identifiants admissibles. Elle SHALL retenir
les modèles satisfaisant les filtres communs de contexte, coût et modalités,
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
Les deux tableaux fournisseurs SHALL garder les colonnes rang, modèle/ID, contexte,
sortie, prix d'entrée, prix de sortie, coût moyen et code couleur. TFL SHALL ajouter un tableau commun des essais gratuits, avec fournisseur, modèle, TTFT, débit, raisonnement et état/cause, incluant les échecs dont l'effort est vérifiable ; les exclus HIGH/XHIGH SHALL rester seulement dans le JSON.

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
TFL SHALL collecter à chaque génération les tarifs Go et OpenCode général
dans leurs documentations officielles respectives, et OpenRouter dans son
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
0,20 EUR/M au taux BCE vérifié. Une collecte invalide SHALL bloquer la
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

### Requirement: Catalogue général OpenCode indépendant
TFL SHALL ajouter une section opencode distincte de opencode_go et openrouter.
Disponibilité, tarifs et métadonnées opencode de models.dev SHALL être
collectés indépendamment de Go. Le contexte vérifiable SHALL être ≥ 1M et
la moyenne entrée/sortie comprise entre zéro et 0,50 USD/M inclus. Les
sections existantes SHALL rester compatibles avec leurs consommateurs.

#### Scenario: Modèle gratuit trop court
- **WHEN** une variante gratuite possède seulement 200 000 tokens de contexte
- **THEN** elle est exclue avec le motif de contexte sans abaisser le seuil 1M

#### Scenario: Même identifiant dans deux catalogues
- **WHEN** Go et le catalogue général publient le même identifiant avec des tarifs ou métadonnées distincts
- **THEN** chaque section conserve ses propres données et sources sans emprunt à l'autre

#### Scenario: Compatibilité des consommateurs existants
- **WHEN** un consommateur lit opencode_go ou openrouter dans le catalogue enrichi
- **THEN** il retrouve leurs champs et classements sans dépendre de la nouvelle section opencode

#### Scenario: Plusieurs variantes publiées
- **WHEN** le catalogue général publie plusieurs variantes de contexte ou de période
- **THEN** son prix de classement est la moyenne maximale des variantes publiées
- **AND** la référence hors pointe de Go reste inchangée

### Requirement: Exclusion LM avant sélection et test
TFL SHALL charger la liste commune LM avant tout appel fournisseur et
l'appliquer à Go, OpenCode général et OpenRouter avant tout classement et
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
- **THEN** les trois catalogues appliquent la liste courante sans mise à jour du code

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
- **WHEN** les trois catalogues valides sont collectés avec ces identifiants OpenRouter
- **THEN** TFL peut publier les trois sections avec leurs filtres et exclusions inchangés
- **AND** les modèles interdits restent absents des listes retenues et des tests gratuits

### Requirement: Effort vérifiable avant admission
TFL SHALL exiger une capacité HIGH ou XHIGH vérifiable pour chaque gratuit
ou payant, avant génération et classement. HIGH SHALL être préféré et XHIGH
SHALL être le seul repli. Les modèles exclus SHALL rester auditables dans
le JSON et SHALL NOT apparaître dans les tableaux, essais gratuits compris.

#### Scenario: Modèle payant ou gratuit sans preuve
- **WHEN** HIGH et XHIGH ne sont pas vérifiables dans les sources publiées
- **THEN** le modèle est exclu avant toute génération, absent des tableaux et motivé dans le JSON

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie une liste contenant high ou xhigh, ou null explicite signifiant tous les efforts
- **THEN** le candidat satisfait le filtre d'effort sous réserve des autres critères
- **AND** une clé absente, une valeur invalide, un booléen reasoning ou supports_max_tokens seul reste exclu

#### Scenario: XHIGH seul ou tous les efforts
- **WHEN** seuls XHIGH ou tous les efforts via null explicite sont publiés
- **THEN** le modèle est admissible respectivement en XHIGH ou HIGH sous réserve des autres critères

#### Scenario: Budget seul
- **WHEN** le modèle ne publie qu'un budget de raisonnement sans preuve d'effort HIGH/XHIGH
- **THEN** il est exclu sans équivalence de niveau inventée

### Requirement: Plafond OpenRouter en EUR
TFL SHALL appliquer une moyenne de base OpenRouter <= 0,20 EUR/M après
conversion au dernier taux BCE USD par EUR, positif et fini. Comparaison
non arrondie, prix natifs USD, prix EUR, source et dates de publication et de
récupération SHALL être tracés. Une conversion invérifiable SHALL bloquer
la publication et préserver les rapports précédents.

#### Scenario: Limite inclusive et montant supérieur
- **WHEN** la moyenne convertie atteint exactement 0,20 EUR/M ou dépasse ce seuil avant arrondi
- **THEN** seul le premier montant est admissible sous réserve des autres filtres

#### Scenario: Conversion non vérifiable
- **WHEN** le cours BCE est absent, invalide ou inaccessible
- **THEN** aucun nouveau rapport n'est publié et les fichiers précédents restent préservés

### Requirement: Deux tableaux fournisseurs et catalogue général préservé
TFL SHALL afficher Go puis OpenRouter, puis les essais gratuits admissibles
à l'effort. Les tableaux SHALL garder huit colonnes, Go en USD/M et OpenRouter
en EUR/M avec taux daté, même vides. La collecte et le JSON opencode SHALL
rester disponibles à PLLM 3/4. Go et général SHALL garder le plafond 0,50 USD/M.
Une sélection vide après filtrage ou qualification SHALL NOT bloquer les
autres sections. Les filtres et validations indispensables SHALL rester inchangés.

#### Scenario: Publication à deux tableaux
- **WHEN** les trois collectes satisfont les critères de validité
- **THEN** le rapport affiche Go puis OpenRouter, aucun tableau général, et le JSON conserve les trois sections

#### Scenario: Aucune preuve d'effort dans une section
- **WHEN** tous ses candidats sont exclus faute de preuve HIGH/XHIGH
- **THEN** TFL publie la sélection vide et ses motifs sans réutiliser d'anciennes qualifications
- **AND** les exclus restent absents des tableaux et des essais gratuits

### Requirement: Publication explicite des sélections vides
Chaque catalogue valide SHALL publier models éventuellement vide,
selection_status (available ou empty), exclusion_summary (motif vers nombre),
compteurs et exclusions détaillées. Un tableau vide SHALL afficher
« Aucun modèle admissible » et la synthèse, sans fausse ligne de modèle.
Trois sélections vides valides SHALL produire les fichiers frais et un code
zéro. Les erreurs réelles SHALL rester bloquantes ; le planning reste inchangé.

#### Scenario: Go vide et OpenRouter admissible
- **WHEN** les collectes sont valides, Go ne retient aucun modèle et OpenRouter en retient
- **THEN** les deux tableaux sont publiés dans l'ordre Go puis OpenRouter et le second contient ses modèles admissibles
- **AND** Go expose son état vide, sa synthèse et ses exclusions courantes

#### Scenario: Catalogue général vide
- **WHEN** seule la sélection générale est vide
- **THEN** son état et ses exclusions sont publiés dans le JSON sans ajouter de tableau général ni bloquer Go et OpenRouter

#### Scenario: Section vidée par la qualification gratuite
- **WHEN** tous les modèles d'une section sont des gratuits échoués ou non mesurables
- **THEN** models est vide et les essais, leurs causes filtrées et les exclusions sont publiés
- **AND** les autres sections et leurs qualifications continuent

#### Scenario: Trois sélections vides
- **WHEN** les trois collectes sont valides mais aucun modèle ne reste après filtrage ou qualification
- **THEN** TFL publie les sections vides, les deux tableaux explicites, les exclusions et les essais effectués avec un code de sortie zéro

#### Scenario: Erreur réelle
- **WHEN** une source indispensable, une authentification, une conversion BCE ou une donnée de sécurité est invalide
- **THEN** TFL signale l'erreur, retourne un code non nul et préserve les rapports précédents

### Requirement: Investigation des preuves manquantes
Pour Go, OpenCode général et OpenRouter, un contexte ou un effort invérifiable
SHALL déclencher une analyse et une recherche du LLM dans les sources
officielles. Le catalogue SHALL tracer fournisseur, ID exact, champ, sources,
dates, empreintes et conclusion. Une absence de preuve SHALL NOT être présentée
comme une incapacité démontrée. L'agent SHALL terminer l'investigation avant
la restitution finale, ou déclarer explicitement son blocage.

#### Scenario: Contexte encore invérifiable
- **WHEN** l'investigation ne permet pas de vérifier le contexte
- **THEN** le modèle reste exclu avec les sources examinées et la conclusion
- **AND** aucun contexte ni seuil plus faible n'est inventé

#### Scenario: Source devenue différente ou inaccessible
- **WHEN** une preuve supplémentaire ne correspond plus à sa source courante
- **THEN** elle ne permet aucune admission et une nouvelle investigation est requise

### Requirement: Efforts publiés et équivalences documentées
Les niveaux de reasoning_options type=effort/values SHALL être normalisés.
HIGH/XHIGH officiellement acceptés SHALL être admissibles même si plusieurs
niveaux produisent le même comportement. Une équivalence documentée vers un
interrupteur SHALL être tracée avec son protocole, ses paramètres et ses
sources, sans inventer un endpoint ni une intensité distincte.

#### Scenario: HIGH équivaut au raisonnement activé
- **WHEN** les sources officielles du modèle établissent cette équivalence sur le protocole utilisé
- **THEN** HIGH est admissible et le paramètre équivalent documenté est envoyé
- **AND** les autres critères et contrôles restent obligatoires

### Requirement: Source unique LM
TFL SHALL appliquer uniquement la liste LM, sans liste permanente intégrée.

#### Scenario: Retrait d'une ancienne exclusion permanente
- **WHEN** LM retire muse-spark-1.2-contributor
- **THEN** aucune liste TFL résiduelle ne l'exclut, y compris avec préfixe fournisseur
