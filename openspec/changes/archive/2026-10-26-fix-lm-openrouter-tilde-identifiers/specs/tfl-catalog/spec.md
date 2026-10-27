## ADDED Requirements

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
