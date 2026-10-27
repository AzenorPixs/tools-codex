## MODIFIED Requirements

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

### Requirement: Compatibilité du rafraîchissement
Les filtres, colonnes communes, interfaces CLI et champs consommés par PLLM
SHALL rester compatibles. La sélection OpenRouter SHALL pouvoir contenir tout
identifiant admissible du catalogue courant. Une route Go inconnue SHALL
être signalée sans protocole inventé.

#### Scenario: OpenRouter actualisé
- **WHEN** le catalogue API évolue en modèles ou en prix
- **THEN** TFL recalcule sa sélection et son classement avec les données courantes
- **AND** le JSON conserve leur provenance et les prix de cache disponibles

## ADDED Requirements

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
