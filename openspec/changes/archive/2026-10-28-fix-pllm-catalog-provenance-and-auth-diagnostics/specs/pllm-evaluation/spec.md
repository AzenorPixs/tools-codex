## ADDED Requirements

### Requirement: Provenance explicite du catalogue consommé
PLLM SHALL tracer pour chaque politique consommatrice le chemin du catalogue utilisé, le choix explicit/default, sa date validée et son âge lorsqu'il est calculable. Une date absente, invalide, sans fuseau ou future SHALL produire un avertissement structuré sans mesure inventée ni seuil arbitraire de péremption. Le chemin explicite SHALL rester prioritaire et le défaut voisin SHALL rester inchangé. PLLM SHALL NOT lancer TFL implicitement ni chercher dans les configurations privées.

#### Scenario: Copie ancienne et collecte récente
- **WHEN** un catalogue récent est explicitement fourni et une autre copie ancienne existe
- **THEN** seuls les candidats du catalogue explicite sont examinés et sa provenance est publiée
- **AND** le diagnostic vide désigne ce catalogue sans conclure à une absence universelle de gratuits

#### Scenario: Date non vérifiable
- **WHEN** le catalogue n'a pas d'horodatage exploitable
- **THEN** l'âge reste indisponible et un avertissement est conservé sans reprise d'une date historique

### Requirement: Diagnostic de sélection vide traçable
PLLM SHALL conserver les compteurs de candidats par catégorie et les motifs d'exclusion locale. L'absence de candidats gratuits SHALL être distinguée d'un benchmark échoué et SHALL identifier le catalogue et sa date dans le diagnostic, sans ajouter de colonne au tableau.

#### Scenario: Aucun gratuit retenu dans le catalogue
- **WHEN** une section ne contient que des payants admissibles
- **THEN** la politique gratuite est invalide avec test non exécuté et absence localisée au catalogue utilisé
- **AND** elle n'appelle aucun endpoint de quota ou de solde

### Requirement: Phase du contrôle des ressources observable
Les contrôles payants SHALL tracer leur phase, endpoint public, date et statut, avec diagnostic HTTP filtré en cas de refus. Un HTTP 401 au quota SHALL être distingué d'un refus de génération et d'un épuisement. Aucun secret, compte, corps brut ou identifiant de session SHALL être publié. Les nouveaux champs SHALL être réinitialisés pour chaque politique visitée.

#### Scenario: Refus du quota mode2
- **WHEN** le contrôle Go mode2 reçoit HTTP 401
- **THEN** mode2 est invalide sans génération et le diagnostic identifie le contrôle des quotas et son endpoint
- **AND** mode4 continue indépendamment sans quota avec sa propre évaluation gratuite
