# Validation SCM — restore-mode5-paid-benchmark

Projet : Tools Codex (`tools-codex`). Session directe SCM, périmètre validé le 28 octobre 2026. Release source : 0.7.25.

## Résultats observés

- Python 3.14.10 (`/home/devops/python/current/bin/python3`) : `-B -m unittest discover -s tests`, 366 tests réussis (11,143 s).
- Python 3.13.5 (`/usr/bin/python3`) : même suite, 366 tests réussis (12,141 s).
- Compilation explicite des 59 scripts/tests dans un dossier temporaire de tests, sous chaque interpréteur : réussie ; aucun cache conservé. ZoneInfo Europe/Paris disponible sous les deux interpréteurs.
- Tests ciblés PLLM : réussis ; les échecs initiaux reflétaient les anciennes attentes sans benchmark, corrigées pour la nouvelle spécification avant les deux suites finales.
- OpenSpec cible strict : exécuté et réussi après découpage d'une exigence initialement trop longue.
- OpenSpec global strict avant archivage : 11/11, zéro échec. Standard global avant archivage : 11/11, zéro échec. Contrôle après archivage : voir complément ci-dessous.
- Parité PLLM autonome/embarquée : 10 fichiers de distribution identiques, données et caches exclus.
- VERSION, pyproject, README et six manifestes : 0.7.25.
- UTF-8/LF des 24 fichiers source et conservation des scénarios MODIFIED : réussis.

## Critères couverts

La suite vérifie les seuils stricts payants 90 s/15 tokens/s, le comptage réponse seule OpenRouter, Medium demandé, les paliers, la reprise d'une mémoire de même identité, l'absence de substitution forcée, le tri tarifaire et l'arrêt au premier succès, les replis après HTTP 400/429, l'arrêt sur HTTP 401 ou solde épuisé entre paliers, les ressources avant chaque requête, les anciens résultats non benchmarkés invalidés, les catégories et la publication. Les fixtures isolent réseau et trousseau ; les transports et le calcul du débit sont couverts par le moteur commun existant et sa suite.

## Matrice documentaire

| Document | État et preuve |
|---|---|
| Projet réel | Moteur mode5 raccordé à evaluate_candidate ; tests mode5 et deux distributions qualifiés hors ligne. |
| AGENTS.md | Inchangé : règles générales et sécurité applicables, aucun changement requis. |
| PROJECT.md | Inchangé : sections Version de release, Catalogue actuel et Principes restent exactes ; aucune nouvelle ressource ni architecture. |
| TECHNICAL.md | Mis à jour : politique PLLM, Medium, prix et section Benchmark payant OpenRouter du mode5. |
| BUILD.md | Mis à jour : règles d'évaluation et Livraison du benchmark mode5 0.7.25 ; installation distincte explicitée. |
| DEVOPS.md | Inchangé par cette réalisation : inventaire observé, chemins Python/OpenSpec utilisés ; pas de modification d'environnement. |
| README.md | Mis à jour : release, tableau des modes, critères, catalogue TFL distinct et anciens historiques mode5. |
| CHANGELOG.md | Entrée Unreleased 0.7.25 avec comportement, limites et compatibilité. |
| OpenSpec | Delta pllm-evaluation et clarification tfl-catalog, scénarios antérieurs conservés ; validation stricte. |

## Limites

Aucun benchmark fournisseur réel ni installation TCU/profil utilisateur, activation timer ou configuration OpenCode effectué. Les mesures réelles précédentes ne prouvent pas le nouveau code. TFL conserve son catalogue tarifaire payant sans benchmark. Le stockage LM utilisateur est inchangé. Aucun ajout de dépendance. Le retour à une ancienne release réintroduit l'ancien mode5 ; préserver les données avant retour. Les contrôles Git et publications conditionnelles sont une étape de clôture séparée du code, tracée dans la restitution.

## Fichiers source concernés

- `VERSION`
- `pyproject.toml`
- `README.md`
- `TECHNICAL.md`
- `BUILD.md`
- `CHANGELOG.md`
- `.codex/commands/PLLM.md`
- `skills/pllm/SKILL.md`
- `skills/pllm/scripts/evaluate.py`
- `plugins/pllm/skills/pllm/SKILL.md`
- `plugins/pllm/skills/pllm/scripts/evaluate.py`
- `plugins/cm/.codex-plugin/plugin.json`
- `plugins/lm/.codex-plugin/plugin.json`
- `plugins/pllm/.codex-plugin/plugin.json`
- `plugins/prompt/.codex-plugin/plugin.json`
- `plugins/tcu/.codex-plugin/plugin.json`
- `plugins/tfl/.codex-plugin/plugin.json`
- `tests/test_pllm_six_modes.py`
- `tests/test_pllm_price_priority.py`
- `tests/test_pllm_free_fallback.py`
- `tests/test_free_performance.py`
- `tests/test_extension_qualification.py`
- `tests/test_lm_blacklist.py`
- `tests/test_pllm_mode5_benchmark.py`

## Clôture OpenSpec observée

`openspec archive restore-mode5-paid-benchmark --yes` a réussi : archive 2026-10-28-restore-mode5-paid-benchmark, trois exigences ajoutées et neuf modifiées ; aucune suppression d'exigence. Le CLI a signalé un avertissement non bloquant de titres proposal (Pourquoi/Changement au lieu de Why/What Changes) ; les deltas ont été validés et synchronisés avec succès. Après archivage, validations globale standard et stricte : 10/10 chacune, zéro échec. Aucun BLOCKER.md/BLOCKERS.md ni lien caduc : nettoyage non applicable. STATISTICS.md est produit dans cette même archive.

## Préparation Git locale

La branche main correspond à LOCAL_DEFAULT_BRANCH. Aucun chemin ignoré n'est déjà indexé. Le contrôle initial a rencontré la propriété différente du dépôt ; les commandes Git utilisent une exception safe.directory limitée à ce seul processus, sans configuration globale ou système. Git relève aussi DEVOPS.md modifié, sans écriture de cette réalisation sur ce fichier. La clôture SCM porte sur le projet complet et préserve cet état existant ; ce fichier supplémentaire peut donc figurer dans le commit, sans attribution de sa modification à ce change. Les 33 fichiers du périmètre ci-dessus restent distincts de cet inventaire Git.
