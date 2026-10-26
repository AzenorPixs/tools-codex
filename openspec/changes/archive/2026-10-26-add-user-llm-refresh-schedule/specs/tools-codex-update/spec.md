## ADDED Requirements

### Requirement: Bootstrap du planning sans génération
Après vérification des sources installées, TCU --apply SHALL installer ou
actualiser le planning avec son module local. Check SHALL seulement décrire
l'état et l'opération prévue. TCU SHALL NOT exécuter TFL, PLLM ou du code
téléchargé pour ce bootstrap, ni installer leurs paquets absents.

#### Scenario: Application avec TFL et PLLM présents
- **WHEN** TCU applique une mise à jour avec les deux composants utilisables
- **THEN** le planning est vérifié ou actualisé et son résultat figure dans le bilan
- **AND** aucune évaluation LLM n'est déclenchée par TCU

#### Scenario: Contrôle ou composants manquants
- **WHEN** TCU vérifie seulement ou qu'un composant nécessaire manque
- **THEN** aucune planification n'est activée implicitement et l'état explique le résultat
