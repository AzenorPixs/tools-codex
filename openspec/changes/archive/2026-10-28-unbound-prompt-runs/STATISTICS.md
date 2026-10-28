# STATISTIQUES — unbound-prompt-runs

Projet : Tools Codex. Session SCM directe du 28 octobre 2026. Release : 0.7.22.

## 1. Statistiques générales

Les familles CISMPx et 1CISMPx acceptent désormais tout suffixe décimal ASCII strictement positif sans zéro initial, sans borne supérieure applicative. Le suffixe reste une chaîne, y compris au-delà des limites de conversion numérique Python. 1CISMPx conserve son cycle à un change. Les présentations plugin, skill, commande et bilan TCU utilisent PROMPT ; les identifiants techniques, chemins, anciens alias et reçus restent compatibles.

347 tests distincts réussis sous Python 3.13.5 et 347 sous Python 3.14.10, soit 694 exécutions globales finales réussies. Un nouveau test TCU porte le total de 346 à 347 ; les tests de résolution existants couvrent désormais davantage de suffixes et de rejets CLI/API. Les 20 tests PROMPT et 53 tests TCU ciblés sont inclus dans les 347, sans addition aux tests distincts. Durée complète, tokens et coût : N/A, aucune télémétrie exhaustive instrumentée.

## 2. Messages et outils

Session exécutée directement, sans sous-agent, pilotage CAB ou OpenCode. Compétences prompt et skill-creator utilisées. Statistiques de pilotage non invoquées conformément à SCM. Appels et messages exhaustifs : N/A, aucun agrégat fiable. Outils : lectures ciblées, édition Python, unittest, py_compile, validation de skills et CLI OpenSpec.

## 3. Fichiers

- Résolution : skills/prompt/scripts/resolve_prompt.py et sa copie embarquée ; les deux SKILL PROMPT.
- Présentation : deux SKILL CM, deux SKILL TCU, deux update.py TCU et .codex/commands/PROMPT.md. Les métadonnées plugin et agents/openai.yaml affichaient déjà PROMPT et ont été vérifiées.
- Tests : test_prompt_dispatch.py, test_tcu_update.py et attente de release dans test_lm_blacklist.py.
- Documentation : PROJECT.md, TECHNICAL.md, BUILD.md, README.md, CHANGELOG.md.
- Release : VERSION, pyproject.toml et six manifestes.
- OpenSpec : proposal, design, tasks, deux deltas, deux spécifications synchronisées et présent rapport. DEVOPS.md préexistant préservé.

| Mesure | Total vérifié |
|---|---:|
| Tests distincts de la suite finale | 347 |
| Exécutions globales finales, deux branches | 694 |
| Tests ciblés PROMPT / TCU | 20 / 53 |
| Fichiers Python modifiés compilés, chaque branche | 7 |
| Paires de ressources de distribution vérifiées | 6 |
| Métadonnées de release alignées | 8 |
| Entrées LIST du référentiel réel, chaque distribution | 24 |

Les six paires sont PROMPT SKILL/résolveur/agents, CM SKILL et TCU SKILL/update.py. Lignes ajoutées ou supprimées : N/A, pas de diff Git de contenu selon SCM.

## 4. Commandes et validations

- Tests ciblés : `python3 -B -m unittest discover -s tests -p test_prompt_dispatch.py` : 20 réussites ; `-p test_tcu_update.py` : 53 réussites.
- `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests` : 347 réussites, Python 3.14.10.
- `/usr/bin/python3.13 -B -m unittest discover -s tests` : 347 réussites, Python 3.13.5.
- Premier contrôle TCU : erreurs dans le nouveau test (état de fixture réinitialisé deux fois et ligne autonome sans ressource). Fixture corrigée et sélection des trois ressources précisée ; contrôles ciblés et globaux finaux tous réussis.
- Sept fichiers Python modifiés compilés par `-m py_compile` sur chacune des deux branches ; ressources de distribution comparées octet pour octet, métadonnées JSON/TOML et UTF-8/LF vérifiés.
- quick_validate.py : skills PROMPT et TCU valides.
- CLI isolée des deux distributions : CISMP9, CISMP12345 et suffixes de 5000 chiffres, avec ou sans préfixe 1 ; RUN et limite préservés. Rejets invalides vérifiés avant configuration par API et CLI.
- LIST réel : 24 entrées pour chaque distribution ; CISMP9, 1CISMP9 et CISMP12345 résolus depuis le DEVOPS réel. Aucun processus du prompt retourné n'est exécuté.
- OpenSpec : change strict valide, puis validation globale 11/11 avant archive ; archivage natif réussi avec une exigence ajoutée et trois modifiées.
- Premier strict après synchronisation : exigence trop longue ; texte raccourci et cas de rejet placés dans le scénario sans changement du contrat, delta archivé et spécification principale alignés, sans réarchivage. Contrôle final `openspec validate --all --strict` : 10/10.
- Rapport : six sections, UTF-8/LF et totaux vérifiés après écriture. Aucun BLOCKER.md ou BLOCKERS.md dans cette archive.

Shell, frontend et SQL : non pertinents. Aucun profil installé modifié, aucun RUN métier ni benchmark fournisseur lancé. Les tests hors ligne ne prouvent pas le chargement dans une nouvelle session Codex. La publication Git conditionnelle relève de la clôture SCM après ce rapport et sera restituée séparément.

## 5. Accès web

Aucune recherche web ni appel fournisseur pour la qualification. Le référentiel de prompts déclaré a été lu localement. Les éventuels accès Git de clôture sont distincts des preuves de tests.

## 6. Synthèse et cohérence documentaire

| Document | État et preuve |
|---|---|
| AGENTS.md | Inchangé : règles de sécurité, tests, SCM et statistiques d'archive appliquées. |
| PROJECT.md | Mis à jour : catalogue PROMPT et section des familles de RUN sans borne. |
| TECHNICAL.md | Mis à jour : résolution, couverture et section des libellés PROMPT du bilan. |
| BUILD.md | Mis à jour : catalogue, utilisation CISMPx/1CISMPx et libellés TCU. |
| DEVOPS.md | Modification préexistante préservée ; chemins de prompts, Python et OpenSpec utilisés. |
| README.md | Mis à jour : release 0.7.22, présentation PROMPT et exemples sans borne. |
| CHANGELOG.md | Mis à jour : entrée Unreleased décrivant les deux comportements et la release. |
| OpenSpec | Deux deltas synchronisés ; validation stricte finale 10/10. |
| Distributions | Six paires vérifiées, versions communes 0.7.22. |

Les changements concernent uniquement Tools Codex. Aucun dépôt CAB ni installation utilisateur modifié. Le cycle à un seul change de 1CISMPx et les barrières du prompt choisi restent applicables. Aucune limite du nombre de RUN n'est ajoutée par le résolveur ; les limites matérielles usuelles du système restent celles de l'environnement d'exécution.
