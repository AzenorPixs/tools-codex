## MODIFIED Requirements

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

## ADDED Requirements

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
