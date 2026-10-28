## 1. Résolution
- [x] 1.1 Implémenter les suffixes positifs sans borne et vérifier CLI/API, préservation du RUN et cycle à un change dans les deux distributions.
## 2. Présentation et release
- [x] 2.1 Uniformiser les libellés PROMPT et vérifier les trois ressources TCU sans changer les identifiants techniques.
- [x] 2.2 Synchroniser documentation, catalogue, wrappers et release 0.7.22 des six plugins.
## 3. Validation finale
- [x] 3.1 Réussir les tests ciblés puis globaux sous Python 3.13/3.14, compilation, parité, métadonnées, UTF-8/LF et résolution isolée/LIST réel.
- [x] 3.2 Revoir la matrice documentaire et réussir OpenSpec strict avant archivage.

## Preuves
- Résolveur : 20 tests ciblés réussis, CLI/API, deux distributions isolées, suffixes 9, 12345 et 5000 chiffres ; aucun RUN métier lancé.
- TCU : 53 tests ciblés réussis, dont libellés des trois ressources en check/apply et conservation du chemin historique.
- Suites finales : 347 tests sous Python 3.14.10 et 347 sous Python 3.13.5, tous réussis.
- Compilation : sept fichiers Python modifiés, deux branches. Parité PROMPT/CM/TCU, métadonnées 0.7.22, UTF-8/LF et skills PROMPT/TCU vérifiés.
- LIST réel : 24 entrées dans les deux distributions ; CISMP9, 1CISMP9 et CISMP12345 résolus sans exécution.
- OpenSpec strict global : 11/11 avant archivage.
- Matrice documentaire : PROJECT (catalogue et RUN), TECHNICAL (résolution et libellés), BUILD (utilisation et libellés), README (version et exemples), CHANGELOG (Unreleased) mis à jour. AGENTS inchangé (règles préservées), DEVOPS préexistant préservé (outils vérifiés), OpenSpec couvert par les deux deltas. Aucun cadrage additionnel nécessaire.
