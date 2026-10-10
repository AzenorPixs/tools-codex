# Proposition

## Why

Tools Codex distribue PLLM et TFL, conserve quatre skills autonomes et trois
commandes maison, mais sa seule spécification principale porte sur la version
de release. Le diagnostic CGP du 10 octobre 2026 a également relevé des
prérequis peu explicites, des instructions contradictoires et des écarts
PLLM qui nécessitent un travail fonctionnel distinct.

## What Changes

- Clarifier les prérequis, les limites de qualification et le statut observé
  des archives CAB dans les cadrages, sans attribuer une provenance non prouvée.
- Harmoniser les instructions PLLM : protocole 5, type de débit dans le JSON
  et mode `active` silencieux. Décrire le repli TFL sur l'accès au secret.
- Préparer cinq contrats OpenSpec fondés sur les capacités documentées et
  observables, avec exigences et scénarios vérifiables.
- Conserver explicitement les écarts d'implémentation et les décisions non
  prises comme travaux non achevés ; une validation structurelle ne les résout pas.

## Capabilities

### New Capabilities

- `extension-distribution`: catalogue, organisation des ressources et limites
  entre installation des plugins, skills autonomes et commandes maison.
- `tfl-catalog`: collecte, filtrage, classement et publication du catalogue TFL.
- `pllm-evaluation`: quotas, mesures concluantes, sélection, publication et
  séparation entre évaluation et application OpenCode autorisée.
- `codex-usage-reporting`: quotas actuels, historique local et restitution CGPT.
- `coding-session-statistics`: rapport de session fondé sur des preuves,
  métriques disponibles et statistiques d'archivage.

### Modified Capabilities

Aucune. La spécification principale `release-versioning` reste inchangée.

## Impact

Les lots L1 à L3 ont été explicitement validés par le développeur le
10 octobre 2026. L1 concerne `PROJECT.md`, `TECHNICAL.md` et `BUILD.md` ;
L2 concerne les deux copies de chacun des skills PLLM et TFL ; L3 concerne
uniquement les métadonnées, cette proposition, le design, les tâches et les
cinq deltas de ce change.

Aucun script, manifeste, dépendance, configuration locale ou archive n'est
modifié. Aucun test fournisseur, installation, effet externe, commit ou push
n'est inclus. La synchronisation vers `openspec/specs/` et l'archivage exigent
des autorisations distinctes et sont exclus des lots validés.
