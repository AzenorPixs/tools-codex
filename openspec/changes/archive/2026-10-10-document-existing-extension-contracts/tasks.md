# Tasks

## 1. Cadrages et instructions approuvés

- [x] 1.1 Clarifier les prérequis, limites de qualification et archives CAB dans les trois cadrages du lot L1.
- [x] 1.2 Harmoniser les quatre fichiers de skills du lot L2 et vérifier leur structure ainsi que l'égalité des copies.

## 2. Préparation spécificative approuvée

- [x] 2.1 Rédiger les métadonnées, la proposition et le design avec le registre CGP et les limites d'autorisation.
- [x] 2.2 Préparer les cinq deltas avec des exigences et scénarios traçables aux capacités existantes.
- [x] 2.3 Réussir la validation OpenSpec stricte du change et le contrôle des specs principales et changes actifs.
- [x] 2.4 Examiner les fichiers touchés, UTF-8/LF, les liens ajoutés et l'absence de modification hors lots dans les sources autorisées.

## 3. Qualification distincte non exécutée par CGP

Les tâches 3.1, 3.2, 3.3 et 3.5 sont reprises dans le périmètre SCM
explicitement validé. La tâche 3.4 est ensuite autorisée avec les deux
décisions Python et leur qualification sur les branches 3.13 et 3.14. La qualification
SCM porte sur des emplacements isolés et des services simulés ; elle ne
constitue pas une installation réelle dans Codex.

- [x] 3.1 Qualifier CGP-03 dans des emplacements de plugins séparés et isolés avec un catalogue explicite ; installation réelle dans Codex non exécutée, conformément au périmètre SCM validé.
- [x] 3.2 Qualifier le démarrage PLLM avec et sans données initiales et traiter CGP-04 dans une session SCM.
- [x] 3.3 Reproduire et traiter CGP-05 par des tests isolés du repli HTTP 429 au dernier palier et des paliers après changement de configuration, sans déclarer valide un modèle non mesuré ni réutiliser un palier appris pour un autre modèle.
- [x] 3.4 Décider de la plage Python supportée et du rôle de la version Python, puis qualifier les comportements applicables sans inventer de preuve.
- [x] 3.5 Qualifier et traiter CGP-10 dans une session SCM par des tests isolés des prix OpenRouter non finis, sans les considérer comme des coûts vérifiés ni produire un catalogue JSON non conforme.

## 4. Cycle OpenSpec distinct désormais autorisé

- [x] 4.1 Synchroniser les six contrats vers les specs principales après contrôle des écarts, selon l’autorisation distincte du développeur.

Les deux jalons suivants sont obligatoires après les tâches préparatoires.
Ils sont suivis par preuves d'exécution et non cochés avant leur réalisation ;
la session ne peut être déclarée terminée tant qu'ils restent en attente.

| Jalon | Critère et preuve | État |
|---|---|---|
| 4.2 | Archiver ce seul change après preuve de tous les critères et validations applicables. | Réalisé : archive 2026-10-10-document-existing-extension-contracts ; transfert des 10 fichiers contrôlé par empreintes. |
| 4.3 | Produire et vérifier le STATISTIQUES.md de l'archive, sans réarchiver. | Réalisé : STATISTIQUES.md vérifié, six sections, UTF-8/LF, chemins, libellés et totaux conformes. |

## 5. Seuil PLLM et release demandés ultérieurement

- [x] 5.1 Porter le seuil strict de TTFT à 90 secondes dans les deux scripts, les instructions, les critères publiés et le delta PLLM, puis aligner VERSION, README et les deux manifestes sur 0.2.1.
- [x] 5.2 Vérifier hors ligne les bornes de TTFT, les couleurs, le seuil de débit inchangé et le blocage du benchmark par un quota invalide dans les deux distributions.
- [x] 5.3 Compiler les fichiers Python modifiés, contrôler UTF-8/LF, l’égalité des copies, l’alignement des versions et réussir les validations OpenSpec strictes.

## 6. Correctifs SCM ciblés validés

- [x] 6.1 Compléter et valider les contrats avant toute écriture de code ou de test.
- [x] 6.2 Implémenter et tester le catalogue explicite et le démarrage sans historique dans les deux distributions.
- [x] 6.3 Implémenter et tester les replis bornés, leurs paliers et leur validité après HTTP 429.
- [x] 6.4 Implémenter et tester les prix non finis et la publication JSON stricte TFL.
- [x] 6.5 Actualiser les instructions, commandes, cadrages, README et CHANGELOG dans le périmètre validé.
- [x] 6.6 Vérifier syntaxe, tests hors ligne, copies, UTF-8/LF, périmètre et OpenSpec ; consigner les preuves et le blocage d'archivage.
