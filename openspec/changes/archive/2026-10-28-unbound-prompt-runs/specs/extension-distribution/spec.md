## ADDED Requirements

### Requirement: Présentation uniforme de PROMPT
Les libellés affichés du plugin, du skill et de la commande PROMPT SHALL être en majuscules. Le bilan TCU SHALL fournir libelle: PROMPT pour chacune de ces trois ressources et ses instructions SHALL utiliser ce libellé dans la restitution. Les identifiants techniques prompt, invocations $prompt, chemins, alias historiques et clés de suivi SHALL rester compatibles.

#### Scenario: Trois ressources du bilan TCU
- **WHEN** TCU contrôle ou actualise le composant PROMPT
- **THEN** les lignes plugin, skill et commande portent libelle: PROMPT
- **AND** les clés brique et composant conservent leurs valeurs techniques, même pour un chemin de commande historique prompt.md
