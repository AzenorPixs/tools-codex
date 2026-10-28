# Statistiques — install-missing-tools-codex-components

## 1. Statistiques générales et décisions

- Projet : Tools Codex (`tools-codex`). Session directe SCM, périmètre présenté puis validé explicitement par le développeur (« Je valide »).
- Constat UTC : 2026-10-28T17:36:45.451799+00:00.
- Release source : 0.7.23 → 0.7.24. Change achevé et archivé dans `2026-10-28-install-missing-tools-codex-components`.
- Agent réellement intervenu : un agent Codex direct ; aucun sous-agent ni pilotage OpenCode/CAB.
- Durée complète, tokens et quotas : N/A, absence de mesure fiable pour ce périmètre. Aucune sonde de session pilotée lancée.
- Installation réelle de la nouvelle version : non exécutée pendant ce mandat. Publications et Git : étapes postérieures à ce rapport, dont le résultat est restitué à l’écran, sans les déduire des tests.

## 2. Types de messages et d’outils

- Échanges observés : demande d’évolution, proposition de périmètre, validation explicite et suivis de réalisation/qualification.
- Outils : lectures ciblées et commandes locales via exec_command ; aucune délégation.
- Nombre exhaustif de messages et appels outils : N/A, aucun export de télémétrie fiable utilisé. Les mesures TCU/installations effectuées avant ce mandat sont exclues de ces statistiques.

## 3. Fichiers modifiés

- Moteur et instructions TCU : `skills/tcu/scripts/update.py`, `SKILL.md`, `agents/openai.yaml` et les trois copies embarquées ; commande `.codex/commands/TCU.md`.
- Catalogue CM : deux copies `skills/cm/SKILL.md` et `plugins/cm/skills/cm/SKILL.md`.
- Tests : `tests/test_tcu_update.py` et attente de release dans `tests/test_lm_blacklist.py`.
- Release et documentation : `VERSION`, `pyproject.toml`, six manifestes plugins, `README.md`, `PROJECT.md`, `TECHNICAL.md`, `BUILD.md`, `CHANGELOG.md`.
- OpenSpec : deux spécifications courantes synchronisées ; proposition, conception, tâches et deux deltas conservés dans cette archive ; présent rapport ajouté après archivage.
- Ensemble contrôlé : 32 fichiers ; aucune suppression de source, renommage métier, changement d’AGENTS/DEVOPS ou modification d’ancienne archive. Le déplacement du change est celui de la commande officielle d’archivage.

## 4. Commandes et validations

| Validation | Résultat réellement observé |
| --- | --- |
| Suite ciblée TCU, Python 3.14 | 59 tests réussis avant l’ajout du dernier contrôle négatif ; ce contrôle est ensuite inclus dans les suites globales finales. |
| `/usr/bin/python3 -B -m unittest discover -s tests -q` | 359 tests réussis, Python 3.13.5, 11,837 s. |
| `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q` | 359 tests réussis, Python 3.14.10, 10,675 s. |
| Compilation py_compile isolée | 39 fichiers compilés avec succès sur chacune des deux versions ; artefacts temporaires nettoyés. |
| Intégrité et distribution | UTF-8/LF ; copies TCU/CM identiques ; VERSION, métadonnée Python, README et six manifestes alignés sur 0.7.24. |
| `openspec validate install-missing-tools-codex-components --strict` | Exécutée et réussie. |
| `openspec validate --all` | 11 éléments réussis, aucun échec avant archivage. |
| `openspec validate --all --strict` | 11 éléments réussis, aucun échec avant archivage. |
| OpenSpec global standard et strict après synchronisation | 10 spécifications réussies, aucun échec ni avertissement après condensation de deux textes normatifs. |
| `openspec archive install-missing-tools-codex-components --yes` | Exécutée et réussie ; 7 exigences modifiées dans 2 spécifications ; archive vérifiée. |

Les commandes OpenSpec utilisent `/home/devops/.local/npm/bin/openspec`. Les suites finales représentent **359 tests distincts, exécutés sur deux interpréteurs**, soit 718 exécutions finales réussies ; il ne s’agit pas de 718 tests distincts. Les passages intermédiaires ne sont pas ajoutés à ce total. Le premier passage global a échoué sur une attente LM figée à 0.7.23 ; correction limitée à 0.7.24, puis nouvelles suites réussies. Aucun test désactivé ni critère affaibli. La première validation stricte après synchronisation a signalé deux exigences trop longues ; leurs textes ont été condensés sans modifier les scénarios, dans la spécification et le delta de cette archive, puis les validations standard et stricte ont réussi sans avertissement. Aucun second archivage.

Réseau, CLI, profils et ordonnanceur sont isolés dans les tests. Le profil vide issu des sources réelles couvre six plugins, huit skills dans deux racines et six commandes dans deux racines. Les autres tests couvrent check sans mutation, racines explicites avec espaces, idempotence, provenance, conflits, activation, erreurs de version et repli.

## 5. Accès web

Aucun accès web ni appel fournisseur pendant l’implémentation et les tests de ce mandat ; aucun téléchargement n’est exécuté. La résolution du prompt SCM s’est faite dans le référentiel local déclaré par DEVOPS. Les accès distants éventuels de publication Git sont des étapes ultérieures, distinctes des preuves de qualification ; ils ne sont pas comptabilisés comme des visites web.

## 6. Synthèse globale

Le comportement source demandé est réalisé, qualifié hors ligne sur Python 3.13 et 3.14, documenté et archivé. Check reste sans écriture ; l’apply installe les briques absentes et met à jour les présentes, avec gardes, reçus et sauvegardes. Le planning n’exécute ni TFL ni PLLM pendant l’apply.

La matrice documentaire complète figure dans `design.md`, section « Matrice documentaire revue avant archivage ». AGENTS et DEVOPS restent inchangés avec justification ; PROJECT, TECHNICAL, BUILD, README, CHANGELOG et les deux spécifications concernées sont cohérents avec le change. Aucun BLOCKER.md/BLOCKERS.md n’était présent dans le change ; aucun nettoyage requis.

Ce rapport prouve l’archivage et les contrôles décrits ; il ne prouve ni le chargement dans une nouvelle session, ni une activation réelle, ni une publication distante. La clôture SCM dépend encore du bilan des étapes Git conditionnelles à effectuer après sa vérification.
