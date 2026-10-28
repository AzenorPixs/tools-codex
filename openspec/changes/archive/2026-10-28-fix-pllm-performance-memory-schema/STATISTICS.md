# STATISTIQUES — fix-pllm-performance-memory-schema

Projet : Tools Codex (`tools-codex`). Session SCM directe du 28 octobre 2026.
Release : 0.7.21. Archive native : `2026-10-28-fix-pllm-performance-memory-schema`.

## 1. Statistiques générales

La mémoire installée contenait uniquement policies.mode7, avec une identité DeepSeek Medium au protocole 8, sans schema_version. Le test Medium mode7 redirigeait ROOT sans rediriger MEMORY_PATH et publiait donc sa mémoire de test dans les sources. Son isolation est corrigée et sa persistance temporaire est vérifiée. Le chargement récupère désormais ce format identifiable ou une mémoire vide, sans modifier le fichier. L'écrivain normalise et valide la mémoire avant publication atomique au schéma 3. Les données ambiguës et corrompues restent refusées et préservées. Aucun seuil, fournisseur, secret ou contrôle de ressources n'est changé.

Six nouveaux tests couvrent les deux distributions. Suite globale : 346 tests réussis sous Python 3.13.5 et 346 sous Python 3.14.10, soit 692 exécutions réussies de 346 tests distincts. Les 85 tests ciblés PLLM et les six nouveaux tests sont inclus dans ces 346, sans addition aux tests distincts. Durée totale de session, tokens et coût : N/A, télémétrie SCM non instrumentée.

## 2. Messages et outils

Session SCM exécutée directement, sans sous-agent, CAB ou OpenCode. Lectures ciblées, scripts Python de modification, unittest, py_compile et CLI OpenSpec. Messages et appels d'outils exhaustifs : N/A, aucun agrégat fiable instrumenté. La compétence de statistiques de pilotage n'a pas été utilisée.

## 3. Fichiers

Code : deux evaluate.py synchronisés. Tests : test_pllm_memory_schema.py créé, deux attentes de release actualisées dans test_lm_blacklist.py et test_tcu_update.py ; isolation de MEMORY_PATH corrigée dans test_model_evidence.py. Les deux fichiers mémoire source touchés pendant les tests ont été restaurés depuis le snapshot marketplace dont les empreintes correspondent à l'index. Documentation : README, TECHNICAL, BUILD, CHANGELOG et deux SKILL PLLM. Versions : VERSION, pyproject.toml et six manifestes. OpenSpec : quatre artefacts de change, spécification principale synchronisée et présent rapport. DEVOPS conserve sa modification préexistante.

| Ensemble | Total | Résultat |
|---|---:|---|
| Nouveaux tests distincts | 6 | Réussis sur les deux distributions |
| Tests globaux distincts | 346 | Réussis sous chaque branche Python |
| Exécutions globales finales | 692 | Toutes réussies |
| Tests ciblés PLLM | 85 | Réussis, inclus dans la suite globale |
| Fichiers Python modifiés compilés | 6 | Réussis sous Python 3.13 et 3.14 |
| Paires de distributions vérifiées | 2 | evaluate.py et SKILL.md identiques |
| Métadonnées de release | 8 | VERSION, pyproject.toml et six manifestes à 0.7.21 |

Lignes ajoutées/supprimées : N/A, aucun diff Git de contenu utilisé selon SCM.

## 4. Commandes et validations

- `python3 -B -m unittest discover -s tests -p test_pllm_memory_schema.py -v` : 6 réussites.
- `python3 -B -m unittest discover -s tests -p 'test_pllm*.py' -v` : 85 réussites.
- `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests` : 346 réussites, Python 3.14.10.
- `/usr/bin/python3.13 -B -m unittest discover -s tests` : 346 réussites, Python 3.13.5.
- Premier passage global : deux échecs d'attentes de version 0.7.20 ; attentes alignées sur la release demandée, sans affaiblissement du contrôle. Les deux passages finaux réussissent.
- `py_compile` : les six fichiers Python modifiés compilés avec succès sur les deux branches. Parité, versions et UTF-8/LF contrôlés.
- Chargement de la mémoire installée avec le correctif : schéma 3 en mémoire, fichier inchangé, aucun appel fournisseur.
- `/home/devops/.local/npm/bin/openspec validate --all --strict` : 11/11 avant archivage.
- Archivage natif : réussi, deux exigences ajoutées à pllm-evaluation, tâches complètes.
- Après correction de l'isolation du test : 19 tests de preuve réussis, puis 346/346 sous chacune des deux branches ; aucune mémoire source modifiée après exécution. Validation stricte après archive : 10/10.
- Rapport : six sections, UTF-8/LF et totaux vérifiés ; aucun bilan de blocage obsolète.

Les contrôles hors ligne ne prouvent pas les performances ou quotas actuels des fournisseurs. Installation, relance réelle et publications Git relèvent des opérations de session après ce rapport ; leur résultat sera restitué séparément. Shell, frontend et SQL : non pertinents.

## 5. Accès web

Aucun appel fournisseur ni recherche web pendant la qualification du correctif. Les tests isolent réseau et trousseau. La relance PLLM autorisée recontrôlera les fournisseurs selon le protocole existant ; aucune ancienne mesure ne constitue une preuve actuelle.

## 6. Synthèse et cohérence documentaire

| Document | État et preuve |
|---|---|
| AGENTS.md | Inchangé : règles SCM, secrets, OpenSpec et tests respectées. |
| PROJECT.md | Inchangé : architecture et version de référence dans VERSION préservées. |
| TECHNICAL.md | Mis à jour : récupération limitée et écriture rechargeable de mémoire. |
| BUILD.md | Mis à jour : formats récupérables et préservation des invalides. |
| DEVOPS.md | Modification préexistante préservée ; chemins Python et OpenSpec vérifiés. |
| README.md | Release 0.7.21 et comportement de récupération documentés. |
| CHANGELOG.md | Entrée Unreleased pour le correctif et la release 0.7.21. |
| OpenSpec | Delta validé, deux exigences synchronisées par archivage natif. |
| Distributions | Deux evaluate.py et deux SKILL.md comparés octet pour octet. |

Le rapport décrit la qualification et l'archivage. Aucune publication ni installation n'est déclarée sur cette seule base. Aucun bilan BLOCKER.md ou BLOCKERS.md n'est présent dans cette archive.
