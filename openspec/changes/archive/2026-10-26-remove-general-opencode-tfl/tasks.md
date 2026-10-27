## 1. Spécifications
- [x] 1.1 Valider les deltas OpenSpec du périmètre approuvé et leurs scénarios.

## 2. Contrat TFL/PLLM/planning
- [x] 2.1 Retirer la collecte, les qualifications et les publications générales TFL dans les deux distributions.
- [x] 2.2 Borner PLLM 1/2 aux payants Go et 3/4 aux gratuits Go, anciens catalogues et rangs forcés compris.
- [x] 2.3 Adapter les copies du scheduler à Go/OpenRouter sans changer les horaires ni les autres gardes.
- [x] 2.4 Réussir les tests ciblés producteur/consommateurs, exclusions et planning.

## 3. LM utilisateur
- [x] 3.1 Ajouter inkling et inkling-small via LM ADD en préservant les exclusions existantes.
- [x] 3.2 Vérifier la persistance, l'idempotence et le blocage des variantes payantes/gratuites.

## 4. Release et cohérence
- [x] 4.1 Aligner VERSION, pyproject.toml, six manifestes et présentation sur 0.7.12.
- [x] 4.2 Synchroniser les documentations, commandes et distributions concernées.
- [x] 4.3 Réussir la suite globale hors ligne sous Python 3.13 et 3.14, la syntaxe, les parités et UTF-8/LF.
- [x] 4.4 Vérifier la matrice documentaire, les changements autorisés et OpenSpec global strict.

## 5. Postconditions de clôture
Ces opérations suivent la validation complète des tâches de réalisation :
- Synchroniser puis archiver le seul change finalisé et vérifier les spécifications résultantes.
- Produire et vérifier STATISTIQUES.md dans l'archive avec six sections et N/A motivés.
Leurs preuves sont ajoutées après exécution ; elles ne constituent pas des tâches de code à cocher avant leur propre archivage.


Preuve de la première postcondition : archive native réalisée le 26 octobre
2026 sous 2026-10-26-remove-general-opencode-tfl ; specsUpdated=true,
standard et strict globaux 10/10 après archive, aucun change actif.
La seconde postcondition est suivie par STATISTIQUES.md et VALIDATION-FINALE.json.

Seconde postcondition réalisée : STATISTIQUES.md produit après archive, relu
et vérifié (six sections, UTF-8/LF, totaux 52 + 20 = 72, 646 exécutions
globales finales). Voir VALIDATION-FINALE.json pour son empreinte.
