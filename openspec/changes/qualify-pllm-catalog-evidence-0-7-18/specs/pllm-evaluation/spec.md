## MODIFIED Requirements

### Requirement: Effort vérifiable indépendant du catalogue et de l'historique
PLLM SHALL exiger une capacité Medium vérifiable pour tout candidat
benchmarké, y compris DeepSeek direct au mode7. Le mode5 est exempté de cette
exigence et de toute génération. Seul Medium SHALL être demandé et admis pour
les autres modes. Un mapping documenté de la valeur demandée `medium` vers un
effort effectif différent SHALL NOT être traité comme une capacité Medium.
Un exclu SHALL NOT être généré, sélectionné ou affiché dans les tableaux ;
son motif précis SHALL rester dans le JSON. Les sept politiques SHALL rester
présentes dans l'état interne.

#### Scenario: Mapping Medium vers High
- **WHEN** la documentation officielle indique que Medium est accepté comme alias de High
- **THEN** le candidat reste invalide pour les modes benchmarkés exigeant Medium effectif
- **AND** le diagnostic précise le mapping observé et aucune génération n'est envoyée

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie une liste contenant medium, ou null explicite signifiant tous les efforts
- **THEN** le candidat satisfait le filtre d'effort sous réserve des autres critères
- **AND** une clé absente, une valeur invalide, un booléen reasoning ou supports_max_tokens seul reste exclu

#### Scenario: Ancien catalogue ou résultat historique
- **WHEN** un candidat benchmarké précédemment retenu n'a pas de preuve d'effort admissible
- **THEN** il ne peut être sélectionné, généré ou affiché malgré son historique
- **AND** cette exigence ne s'applique pas au mode5, qui ne benchmarke pas

#### Scenario: Cible forcée sans effort vérifiable
- **WHEN** un rang forcé désigne un modèle sans preuve Medium
- **THEN** il est refusé dans les modes benchmarkés sans génération ni substitution
- **AND** un rang du mode5 reste soumis seulement au plafond de coût et au contexte

#### Scenario: Candidat direct sans preuve
- **WHEN** le modèle DeepSeek direct n'a pas de capacité Medium vérifiable
- **THEN** il est exclu avant génération et son identité n'apparaît pas dans les tableaux

#### Scenario: Preuve d'effort liée au transport
- **WHEN** un candidat TFL publie une preuve Medium vérifiée pour son identifiant et son protocole courants
- **THEN** PLLM recontrôle cette source avant génération et conserve le résultat dans l'audit
- **AND** toute source modifiée ou inaccessible empêche la génération
