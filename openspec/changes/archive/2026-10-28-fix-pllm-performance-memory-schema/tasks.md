## 1. Correctif
- [x] 1.1 Valider le delta OpenSpec avant code et tests.
- [x] 1.2 Corriger et synchroniser les deux évaluateurs ; couvrir récupération, écriture/relecture, rejets et migrations.
- [x] 1.3 Exécuter les tests ciblés et la syntaxe.
## 2. Release et qualification
- [x] 2.1 Aligner 0.7.21 et mettre à jour les documents concernés.
- [x] 2.2 Exécuter suite globale, parité, encodage, versions et validation stricte OpenSpec.
- [x] 2.3 Revoir la cohérence documentaire et consigner les preuves avant archivage.

Preuves : 6 nouveaux tests, 85 tests ciblés PLLM ; suite globale 346/346 sous Python 3.13.5 et 3.14.10. Deux attentes de version de tests ont été alignées sur 0.7.21 après un premier échec global (344 réussites, 2 attentes obsolètes). Syntaxe des 6 fichiers Python modifiés réussie sous les deux branches. Deux paires de distributions identiques ; VERSION, pyproject et six manifestes alignés. Mémoire réellement installée chargée au schéma 3 sans modification ni appel fournisseur. OpenSpec strict : 11/11 avant archivage.

Cohérence : AGENTS et PROJECT inchangés (règles et architecture préservées) ; TECHNICAL et BUILD documentent la récupération limitée ; README porte 0.7.21 et le comportement ; CHANGELOG contient l'entrée Unreleased ; DEVOPS préservé dans son état préexistant (interpréteurs et CLI effectivement vérifiés). Spécifications : delta validé et migrations préservées. Aucun secret ni changement de configuration OpenCode.

La clôture de session comprend ensuite l'archivage, STATISTIQUES.md et les opérations Git SCM conditionnelles.

La mise à jour installée et PLLM réel sont des opérations de session après clôture Git, distinctes des critères de qualification du correctif.

Cause confirmée après archive : le test Medium mode7 écrivait dans les données source. MEMORY_PATH est maintenant isolé avec ROOT ; les données source ont été restaurées depuis le snapshot marketplace après vérification de leur empreinte contre l'index. Nouvelle qualification complète avant commit, sans nouvel archivage.
