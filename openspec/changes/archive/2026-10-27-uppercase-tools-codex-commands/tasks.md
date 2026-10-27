## 1. Spécification
- [x] 1.1 Valider le change et ses scénarios avant toute écriture de code ou de test.

## 2. Commandes et compatibilité
- [x] 2.1 Harmoniser les six déclarations, noms de fichiers, déclencheurs, libellés et deux distributions ; adapter TCU et ses tests aux installations historiques.
- [x] 2.2 Vérifier syntaxe, tests ciblés, profils isolés, gardes de provenance et parité.

## 3. Release et documentation
- [x] 3.1 Aligner la release commune sur 0.7.13 et actualiser les cadrages, README et CHANGELOG concernés.
- [x] 3.2 Valider l'ensemble hors ligne sous Python 3.13 et 3.14, la conformité OpenSpec et la matrice documentaire.

## 4. Postconditions de clôture
Ces opérations sont suivies après les validations ci-dessus ; elles ne sont
pas annoncées accomplies avant leurs preuves effectives.
- Archiver le seul change validé et vérifier les spécifications synchronisées.
- Produire et vérifier STATISTIQUES.md dans l'archive ; appliquer le nettoyage conditionnel SCM.
- Appliquer et vérifier les étapes Git conditionnelles de SCM ou justifier leur non-application.

Preuves : [VALIDATION.md](VALIDATION.md), puis STATISTIQUES.md après archivage.
