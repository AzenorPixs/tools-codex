# Statistiques — support-acl-prompt

Session SCM directe du 28 octobre 2026 (Europe/Paris), plan SCM-ACL-R1 validé par le développeur. Release source : 0.7.26. Change archivé par OpenSpec dans 2026-10-28-support-acl-prompt, avec synchronisation d’une exigence modifiée. Aucun code de lot attribué.

## 1. Statistiques générales et décisions

Objectif : accepter ACL en majuscules dans PROMPT CLI/API depuis le seul référentiel DEVOPS/index, sans RUN ni effet du texte résolu. Spécification validée avant code et tests ; 5/5 tâches validées puis cochées avant archivage. Incrément 0.7.25 vers 0.7.26 demandé et validé. Aucun sous-agent, CAB, OpenCode, PLLM ou installation utilisateur.

22 tests ciblés PROMPT réussis. Les deux nouveaux tests reproduisaient initialement le refus : première passe à 5 échecs et 2 erreurs de sous-cas, corrigés par l’ajout ACL. La suite complète finale compte 368 tests distincts, exécutés avec succès sur Python 3.13 et 3.14 : 736 exécutions finales. Les 22 tests ciblés sont inclus dans ces 368 et ne sont pas additionnés aux tests distincts. Durée globale, tokens et coût : N/A, absence de télémétrie exhaustive.

## 2. Types de messages et d’outils

Agent de codage direct Codex ; modèle exact de runtime et métriques de messages : N/A, non mesurés. Décisions observées : mandat SCM avec incrément, puis validation explicite de SCM-ACL-R1, spécification, implémentation, 0.7.26, tests et archivage avec ce rapport. Skills prompt et skill-creator utilisées. Aucun appel de statistiques de pilotage. Outils : lectures ciblées, édition Python, unittest, py_compile, validation des skills et OpenSpec. Comptage exhaustif des appels : N/A, pas d’agrégat instrumenté.

## 3. Fichiers modifiés

- Deux resolve_prompt.py et deux SKILL.md PROMPT, distributions autonome et embarquée : ajout ACL uniquement.
- tests/test_prompt_dispatch.py : API/CLI dans les deux distributions, source absente, lecture seule, absence de RUN, refus de acl ; couverture existante alias et CISMP préservée. tests/test_lm_blacklist.py : attente littérale de release alignée sur 0.7.26.
- VERSION, pyproject.toml et les six plugins/.codex-plugin/plugin.json : release commune 0.7.26.
- README.md, BUILD.md, TECHNICAL.md et CHANGELOG.md : comportement ACL et version documentés.
- DEVELOPMENT_MAP.md et openspec/BATCH_CODES.md : seul change ajouté puis archivé, entrée provisoire sans code et liens vérifiés. 44 codes historiques conservés ; 45 archives au total, aucune active. L’attribution future relève d’ACL.
- openspec/specs/prompt-dispatch/spec.md synchronisé par l’archivage ; proposition, conception, tâches, delta et présent rapport dans cette archive.

21 fichiers existants modifiés et 5 nouveaux fichiers d’archive, soit 26 fichiers dans le périmètre avant clôture Git. Lignes ajoutées/supprimées : N/A, inspection de diff Git non utilisée pendant le développement. Les autres archives sont inchangées.

## 4. Commandes et validations

- `openspec validate support-acl-prompt --strict` : succès avant implémentation.
- Python DevOps `-B -m unittest discover -s tests -p test_prompt_dispatch.py` : 22/22 après correction.
- `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests` : 368/368, durée rapportée 12,292 s.
- `/usr/bin/python3.13 -B -m unittest discover -s tests` : 368/368, durée rapportée 12,954 s.
- py_compile : quatre fichiers Python modifiés compilés ; artefacts temporaires supprimés. Parité octet pour octet : SKILL.md, resolve_prompt.py et agents/openai.yaml, trois paires. JSON/TOML : huit sources alignées (VERSION, pyproject et six manifestes), plus version README contrôlée séparément.
- quick_validate.py : premier appel sous Python DevOps échoué car PyYAML absent ; aucune installation. Reprise sous `/usr/bin/python3` : les deux skills valides.
- CLI réelle LIST puis ACL des deux distributions : 25 entrées, ACL disponible, texte exact du référentiel déclaré retourné en état ready sans exécution, RUN ni action de clôture.
- OpenSpec global avant archive : standard 11/11 et strict 11/11. `openspec archive support-acl-prompt --yes` : succès, une exigence modifiée synchronisée. Strict global après archive : 10/10.
- Liens locaux des deux registres, UTF-8/LF, empreintes du périmètre et préservation des cadrages non concernés vérifiés. Structure Mermaid simple revue manuellement ; rendu non exécuté, mmdc indisponible. Aucun BLOCKER.md/BLOCKERS.md à nettoyer dans cette archive.

Tests Shell, frontend, SQL et benchmarks fournisseurs : non pertinents. Ces validations hors ligne ne prouvent ni installation du profil ni chargement dans une nouvelle session. Les opérations Git conditionnelles de clôture sont traitées séparément ; leurs résultats sont restitués dans la conversation. Elles couvrent l’état complet non ignoré du projet, y compris les modifications antérieures observées par leurs seuls chemins (.gitignore, AGENTS.md et titres des 44 archives), sans attribuer ces modifications à ce correctif.

## 5. Accès web

Aucun accès web ni appel fournisseur pendant la réalisation ou les tests. Référentiel de prompts lu localement. Publications Git éventuelles distinctes des validations hors ligne.

## 6. Synthèse globale et cohérence documentaire

| Document | État et preuve |
|---|---|
| AGENTS.md | Inchangé : règles d’écriture, OpenSpec, tests et archivage respectées dans le mandat SCM. |
| PROJECT.md | Inchangé : organisation des deux distributions et version de release commune déjà exactes ; les codes directs couvrent ACL. |
| TECHNICAL.md | Mis à jour : section Résolution et lancement de prompts, ACL sans RUN ni action de clôture. |
| BUILD.md | Mis à jour : section Utilisation de PROMPT, exemple et liste des arguments avec ACL. |
| DEVOPS.md | Inchangé : chemins Python/OpenSpec et référentiel déclarés utilisés, inventaire non régénéré. |
| DEVELOPMENT_MAP.md | Amendement ciblé : nouveau change sans code, 5/5 tâches, tests et archivage ; aucune attribution ni activation inférée. |
| README.md | Mis à jour : release 0.7.26, exemple ACL et rappel des validations du prompt. |
| CHANGELOG.md | Mis à jour : entrée Unreleased décrivant correction, compatibilité et release. |
| openspec/specs/ | Une exigence prompt-dispatch modifiée, scénarios existants préservés et deux scénarios ACL ajoutés ; strict final 10/10. |
| openspec/BATCH_CODES.md | Amendement ciblé : archive support-acl-prompt en entrée provisoire sans code, 44 codes conservés. |

Résolveur prêt à reconnaître ACL dans les sources 0.7.26, sans déploiement utilisateur. Alias GCM/GCMP, variantes CISMP et protections du référentiel couverts par les tests. Aucune dépendance nouvelle, aucune archive antérieure rouverte ni statistique historique régénérée.
