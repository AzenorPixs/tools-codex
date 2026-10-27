# Spec Delta

## ADDED Requirements

### Requirement: Prix décimaux canoniques malgré l'arrondi flottant
TFL SHALL utiliser les prix décimaux natifs comme référence du classement et des plafonds. Une projection numérique flottante SHALL être acceptée seulement si elle est finie, non négative et équivalente à la valeur décimale avec une tolérance relative de 1e-12 et sans tolérance absolue.

#### Scenario: Arrondi binaire de la projection tarifaire
- **WHEN** le prix numérique vaut `0.049999999999999996` et son prix décimal canonique vaut `0.05000000`
- **THEN** la projection est cohérente et le classement et les plafonds utilisent `0.05000000`

#### Scenario: Écart tarifaire réel
- **WHEN** le prix numérique vaut `0.051` et son prix décimal canonique vaut `0.05000000`
- **THEN** TFL exclut le candidat comme prix contradictoire avant classement ou génération
