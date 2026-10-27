## ADDED Requirements

### Requirement: Effort demandé exclusivement Medium

PLLM SHALL demander et publier des résultats dont l'effort effectif est
`medium`, pour les six politiques, les forçages de rang et chaque transport.
Un refus ou une absence de prise en charge SHALL invalider le candidat sans
repli vers un autre effort.

#### Scenario: Demande forcée ou transport non compatible

- **WHEN** une cible forcée ou un transport ne peut pas effectuer une requête
  en Medium
- **THEN** le candidat est déclaré invalide sans génération à un autre effort

### Requirement: Historique limité aux résultats Medium

Une capacité fournisseur incluant Medium SHALL NOT valider un résultat
historique dont l'effort demandé ou exécuté n'est pas explicitement établi
comme Medium. PLLM SHALL invalider ces résultats avant affichage et sélection,
conserver leur motif dans les exclusions et ne pas réutiliser leurs paliers.

#### Scenario: Historique incompatible malgré une capacité Medium

- **WHEN** le résultat ou une de ses tentatives historiques n'enregistre pas
  explicitement Medium comme effort demandé
- **THEN** PLLM l'invalide avant affichage et sélection
- **AND** conserve le motif d'exclusion sans réutiliser son palier
