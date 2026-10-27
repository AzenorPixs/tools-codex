## ADDED Requirements

### Requirement: Hooks et ordonnanceur embarqués
Les six plugins SHALL déclarer un hook SessionStart vers leur module local
d'ordonnancement. Les six skills autonomes et leurs plugins SHALL embarquer
un module identique, utilisable isolément. L'installation autonome SHALL
documenter le bootstrap ; la confiance native Codex SHALL rester requise.

#### Scenario: Plugin isolé et confiance
- **WHEN** un plugin est installé dans son propre cache puis son hook est approuvé
- **THEN** il peut enregistrer le même planning utilisateur sans dépendre du checkout
- **AND** l'absence de TFL ou PLLM reste signalée sans installation implicite
