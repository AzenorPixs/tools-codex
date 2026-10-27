## 1. Contrat et preuves

- [ ] 1.1 Valider le delta TFL/PLLM/release avec OpenSpec ciblé.
- [ ] 1.2 Ajouter et vérifier les preuves officielles Medium pour les modèles
      et transports OpenCode Go applicables.
- [ ] 1.3 Ajouter la preuve DeepSeek indiquant le mapping Medium vers High et
      la tracer dans le diagnostic mode7.

## 2. Alignement des distributions

- [ ] 2.1 Synchroniser les registres et moteurs TFL/PLLM autonome et embarqué.
- [ ] 2.2 Ajouter ou mettre à jour les tests de preuves, d'admission et de
      diagnostic, sans affaiblir les critères.
- [ ] 2.3 Mettre à jour TECHNICAL, BUILD, README et CHANGELOG si nécessaire.
- [ ] 2.4 Aligner VERSION, pyproject.toml et les six manifestes sur 0.7.18.

## 3. Collecte et évaluation réelles

- [ ] 3.1 Exécuter une collecte TFL fraîche et examiner les preuves requises.
- [ ] 3.2 Relancer TFL après toute complétion de preuves ; vérifier que le
      catalogue final est complet et publiable.
- [ ] 3.3 Exécuter PLLM normal avec le catalogue TFL frais et évaluer les sept
      politiques.
- [ ] 3.4 Justifier précisément chaque mode qui reste invalide ; ne reprendre
      aucun quota, solde ou benchmark historique.

## 4. Validation et clôture

- [ ] 4.1 Exécuter les tests ciblés, la suite complète, les contrôles de syntaxe,
      de parité, de version, d'encodage et de cohérence documentaire.
- [ ] 4.2 Valider OpenSpec ciblé, standard et strict.
- [ ] 4.3 Produire et examiner les rapports TFL/PLLM locaux ; contrôler
      l'absence de données personnelles dans les artefacts versionnés.
- [ ] 4.4 Archiver ce change, produire et vérifier son rapport STATISTIQUES.md.
- [ ] 4.5 Suivre les étapes SCM locales et distantes conditionnelles après
      archivage et rapport.
