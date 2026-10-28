## 1. Contrat et preuves

- [x] 1.1 Valider le delta TFL/PLLM/release avec OpenSpec ciblé.
- [x] 1.2 Ajouter et vérifier les preuves officielles Medium pour les modèles
      et transports OpenCode Go applicables.
- [x] 1.3 Tracer l'acceptation DeepSeek de Medium comme alias High et mesurer
      réellement le mode7 sans prétendre que l'effort interne est Medium.

## 2. Alignement des distributions

- [x] 2.1 Synchroniser les registres et moteurs TFL/PLLM autonome et embarqué,
      avec une méthode d'empreinte source stable et explicitement tracée.
- [x] 2.2 Ajouter ou mettre à jour les tests de preuves, d'admission et de
      diagnostic, dont la réussite du chemin de réponse complète et
      l'enregistrement de l'acceptation Medium et du débit dans les quatre
      moteurs distribués, ainsi que l'invariance des empreintes aux scripts et
      balisages HTML volatils, sans affaiblir les critères ; vérifier qu'aucun
      `NameError` ne survient dans le benchmark complet et la publication TFL.
- [x] 2.3 Vérifier la frontière inclusive 0,10 EUR/M et le rejet au-dessus,
      dans TFL et PLLM mode5, y compris sur les anciens catalogues et les
      candidats forcés.
- [x] 2.4 Mettre à jour TECHNICAL, BUILD, README, CHANGELOG et les catalogues
      de commande CM/PLLM/TFL si nécessaire.
- [x] 2.5 Aligner VERSION, pyproject.toml et les six manifestes sur 0.7.20.

## 3. Collecte et évaluation réelles

- [x] 3.1 Exécuter une collecte TFL fraîche et examiner les preuves requises.
- [x] 3.2 Relancer TFL après toute complétion de preuves ; vérifier que le
      catalogue final est complet et publiable.
- [x] 3.3 Exécuter PLLM normal avec le catalogue TFL frais et évaluer les sept
      politiques.
- [x] 3.4 Justifier précisément chaque mode qui reste invalide ; ne reprendre
      aucun quota, solde ou benchmark historique.

## 4. Validation et clôture

- [x] 4.1 Exécuter les tests ciblés, la suite complète, les contrôles de syntaxe,
      de parité, de version, d'encodage et de cohérence documentaire.
- [x] 4.2 Valider OpenSpec ciblé, standard et strict.
- [x] 4.3 Produire et examiner les rapports TFL/PLLM locaux ; contrôler
      l'absence de données personnelles dans les artefacts versionnés.

Après validation des tâches du change, le processus SCM exécute l'archivage,
produit et vérifie `STATISTIQUES.md`, puis applique les étapes locales et
distantes conditionnelles de commit et de publication. Ces opérations relèvent
de la clôture SCM, pas des critères d'acceptation du change.
