## 1. Spécification

- [x] 1.1 Explorer les sources et faire valider le périmètre autonome.
- [x] 1.2 Définir la proposition, la conception et le delta extension-distribution.
- [x] 1.3 Valider le change strict avant l'implémentation.

## 2. Distribution et release

- [x] 2.1 Créer le manifeste CM et ajouter son entrée dans la marketplace.
- [x] 2.2 Conserver le skill autonome et le lien, synchroniser le skill embarqué.
- [x] 2.3 Aligner VERSION, TOML, README et les trois manifestes sur 0.2.3.
- [x] 2.4 Actualiser PROJECT, TECHNICAL, BUILD, README et CHANGELOG.

## 3. Contrôles

- [x] 3.1 Valider JSON/TOML, chemins, skills, parité et paquet CM isolé.
- [x] 3.2 Exécuter les tests existants sur les deux branches Python.
- [x] 3.3 Vérifier les empreintes, UTF-8/LF et la matrice documentaire.
- [x] 3.4 Valider OpenSpec strict et établir l'éligibilité à la clôture.

## Opérations de clôture après éligibilité

Synchroniser et archiver uniquement `distribute-cm-plugin`. Produire ensuite
STATISTIQUES.md avec six sections et vérifier ses chemins, totaux et encodage.
Consigner les résultats réellement obtenus après ces opérations, sans les
cocher par anticipation et sans réarchiver le change pour compléter le rapport.
