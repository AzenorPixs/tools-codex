## ADDED Requirements

### Requirement: Effort courant exclusivement Medium

TFL SHALL n'évaluer, classer et publier que des candidats admissibles en
Medium. Chaque benchmark SHALL transmettre Medium selon le protocole déclaré
et SHALL échouer explicitement si cet effort n'est pas pris en charge.
Un refus SHALL NOT entraîner de nouvelle requête avec un effort différent.
Les métadonnées fournisseur qui déclarent plusieurs capacités restent des
preuves source ; elles SHALL NOT modifier l'effort demandé ni qualifier une
mesure réalisée avec un autre effort.

#### Scenario: Plusieurs capacités publiées

- **WHEN** les métadonnées d'un candidat déclarent Medium et d'autres capacités
- **THEN** TFL demande Medium et n'envoie aucune autre valeur d'effort
- **AND** seul un benchmark réussi avec Medium peut entrer dans le catalogue

#### Scenario: Medium indisponible ou refusé

- **WHEN** Medium n'est pas vérifiable, n'est pas pris en charge ou est refusé
  par le transport
- **THEN** le candidat est exclu du catalogue avec sa cause
- **AND** aucune requête de repli n'est effectuée
