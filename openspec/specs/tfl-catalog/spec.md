# tfl-catalog Specification

## Purpose

Définir la collecte, le filtrage, le classement et la publication vérifiable du catalogue TFL sans données sensibles.

## Requirements

### Requirement: Collecte complète et ordre des fournisseurs
TFL SHALL collecter les modèles OpenCode Go et OpenRouter, en utilisant
models.dev comme complément de contexte pour OpenCode Go. Une erreur de
collecte, d'authentification ou de données indispensables SHALL faire échouer
la génération, sans annoncer un rapport partiel comme complet. La restitution
SHALL présenter OpenCode Go avant OpenRouter.

#### Scenario: Collecte complète
- **WHEN** les deux collectes et leurs métadonnées indispensables réussissent
- **THEN** le rapport contient les deux tableaux dans l'ordre OpenCode Go puis OpenRouter

#### Scenario: Échec d'un fournisseur
- **WHEN** une collecte indispensable échoue
- **THEN** TFL signale l'échec et ne déclare pas le catalogue actualisé

### Requirement: Seuils de sélection vérifiables
TFL SHALL retenir les modèles dont le contexte vérifiable est au moins de
1 000 000 tokens et le coût moyen entrée/sortie au plus de 0,50 USD par million
de tokens. Les coûts OpenCode Go SHALL utiliser la référence hors pointe.
Les coûts inconnus et contextes inconnus ou insuffisants SHALL être exclus.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte ou le coût d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

### Requirement: Prix finis et JSON strict
TFL SHALL exclure avec un motif les prix OpenRouter non finis ou dont la
conversion par million ou le calcul de moyenne déborde. Le catalogue publié
SHALL être du JSON strict, sans `NaN` ni infini. Un échec de sérialisation
SHALL empêcher la publication d'un catalogue non conforme.

#### Scenario: Prix non exploitable
- **WHEN** un prix vaut `NaN`, un infini ou déborde lors du calcul
- **THEN** le modèle est exclu comme coût non vérifiable
- **AND** les prix finis admissibles restent classés selon les règles communes

### Requirement: Modalités et blacklists explicites
Les sorties déclarées audio, vidéo, speech ou sound SHALL être exclues. Une
entrée multimodale reste admissible ; une sortie inconnue SHALL être signalée
comme non vérifiée.
Les blacklists permanentes SHALL exclure `muse-spark-1.2-contributor` pour
OpenCode Go et `meta/muse-spark-1.2-contributor` pour OpenRouter.

#### Scenario: Modèle hors critères
- **WHEN** un modèle examiné ne satisfait pas un critère de sélection vérifiable
- **THEN** il ne figure pas dans le tableau retenu
- **AND** son motif d'exclusion est conservé dans le catalogue JSON

### Requirement: Sélection OpenRouter explicite
La sélection OpenRouter SHALL être dynamique sur tous les modèles retournés
par l'API, sans liste prédéfinie d'identifiants admissibles. Elle SHALL retenir
les modèles satisfaisant les filtres communs de contexte, coût et modalités,
ainsi que la blacklist permanente. L'absence d'un ancien modèle SHALL rester
sans effet sur les autres résultats admissibles.

#### Scenario: Nouveau modèle admissible
- **WHEN** un identifiant inédit respecte les filtres communs
- **THEN** il est classé sans modification de liste ou de code

#### Scenario: Identifiant fixé absent
- **WHEN** un modèle précédemment classé disparaît de la réponse API
- **THEN** les autres modèles admissibles sont publiés sans erreur liée à cet identifiant

### Requirement: Classement et colonnes communes
TFL SHALL classer les modèles par coût moyen croissant. Les deux tableaux
SHALL partager les colonnes rang, modèle/ID, contexte, sortie, prix d'entrée,
prix de sortie, coût moyen et code couleur.

#### Scenario: Comparaison des tableaux fournisseurs
- **WHEN** les deux tableaux sont restitués
- **THEN** leurs colonnes sont identiques et chaque classement suit le coût moyen croissant

### Requirement: Publication des fichiers courants
TFL SHALL publier un catalogue
`tfl.json` et son rapport `tfl.md`, horodatés, dans `data/` ou dans le répertoire
demandé par `--output-dir`. Chaque fichier SHALL être remplacé atomiquement.

#### Scenario: Publication du catalogue
- **WHEN** la génération et la publication réussissent
- **THEN** les deux fichiers décrivent la même collecte et ses filtres
- **AND** la restitution indique la date et les chemins des fichiers sans exposer de secret

### Requirement: Métadonnées auditables
Le JSON SHALL conserver les sources, exclusions et champs de routage OpenCode Go
`api_endpoint`, `api_protocol` et `endpoint_source`, sans valeur secrète.

#### Scenario: Consultation du routage d'un modèle OpenCode Go
- **WHEN** un consommateur examine un modèle retenu du catalogue
- **THEN** il retrouve les champs de routage et leurs sources sans déduire le protocole du seul nom commercial

### Requirement: Accès aux secrets et repli auto limité
TFL SHALL conserver les secrets hors du contexte du modèle et des sorties.
En mode `auto`, la recherche du secret OpenCode Go SHALL essayer le mode 1,
puis le mode 2 si le premier est inaccessible. Après sélection du premier
secret accessible, une erreur API SHALL être rapportée sans repli vers
l'autre secret. Les invocations SHALL respecter les autorisations
d'exécution hors sandbox et ne pas contourner un refus de la plateforme.

#### Scenario: Secret du mode 1 inaccessible
- **WHEN** le mode `auto` ne peut pas récupérer le secret du mode 1
- **THEN** TFL tente de récupérer celui du mode 2 sans afficher aucune valeur

#### Scenario: Refus API après sélection du secret
- **WHEN** la requête API utilisant le secret sélectionné échoue
- **THEN** TFL rapporte l'erreur sans essayer l'autre secret pour cette requête

### Requirement: Actualisation tarifaire sans repli historique
TFL SHALL collecter à chaque génération les tarifs OpenCode Go dans sa
documentation officielle et les tarifs OpenRouter dans son API modèles.
TFL MUST NOT utiliser une table tarifaire statique ou un ancien catalogue
comme repli lorsque cette collecte échoue. Chaque fournisseur SHALL exposer
la source et la date de récupération tarifaire dans le JSON.

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
vérifié SHALL être admissible ; le seuil maximal SHALL rester 0,50 USD/M.
Une collecte invalide ou aucun résultat admissible SHALL bloquer la publication.

#### Scenario: Modèles gratuits et hors fenêtre
- **WHEN** le catalogue contient des modèles gratuits, trop coûteux, sans prix ou hors contexte
- **THEN** les modèles gratuits satisfaisant les autres filtres sont admissibles
- **AND** chaque modèle rejeté possède un motif d'exclusion dans le JSON

#### Scenario: Catalogue sans résultat admissible
- **WHEN** aucun modèle courant ne satisfait les filtres
- **THEN** TFL échoue explicitement et préserve les rapports précédents

#### Scenario: Variante tarifaire temporelle
- **WHEN** un modèle admissible publie des variantes conditionnées par jours ou horaires UTC
- **THEN** le JSON conserve séparément ces conditions et leurs prix
- **AND** le classement reste fondé sur les prix API de base
