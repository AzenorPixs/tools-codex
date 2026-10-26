# STATISTIQUES — remove-general-opencode-tfl

Projet : Tools Codex (`tools-codex`). Session SCM directe. Release locale :
0.7.12. Rapport produit après l'archive native, le 2026-10-26T16:44:17+01:00.
Périmètre validé par le développeur, avec ajout explicite : payants PLLM 1/2
limités à Go même pour un ancien catalogue général.

## 1. Statistiques générales

Un seul change créé, réalisé et archivé :
`2026-10-26-remove-general-opencode-tfl`. Aucun change actif après clôture.
TFL collecte, qualifie et publie exclusivement Go et OpenRouter ; aucune
section générale opencode ne participe aux ordres, investigations, essais,
JSON ou Markdown. PLLM 1/2 ne retient que les payants Go et 3/4 les gratuits
Go, y compris anciens catalogues, anciennes sélections et rangs forcés.
Le planning valide les deux listes courantes non vides, avec horaires,
activité utilisateur, quotas et autres gardes préservés.

LM utilisateur contient désormais inkling et inkling-small, avec conservation
de mimo-v2.5 et muse-spark-1.2-contributor. Les quatre routes Thinking Machines
payantes/gratuites sont bloquées par l'identité canonique existante. Huit
modules, dont les copies autonomes installées TFL/PLLM, ont relu la politique
et vérifié ces exclusions ; les sources de ces installations restent inchangées.
La répétition des deux ADD conserve contenu et mtime de la politique.
Ce sont deux familles explicites, pas une exclusion automatique de futurs
noms de modèles du fournisseur. Aucun défaut distribué n'est ajouté.

Qualification finale : 323 cas exécutés avec succès sous Python 3.14.10 et
323 sous Python 3.13.5, soit 646 exécutions globales finales. Les 158 tests
ciblés réussis se recouvrent avec cette suite et ne sont pas additionnés aux
646. Compilation finale de 24 fichiers Python modifiés par branche, soit
48 compilations. Les seuils payants/gratuits, HIGH/XHIGH et protocole 8 sont
conservés ; aucune qualification fournisseur réelle n'est déduite de ces tests.

Parités vérifiées : six paquets autonomes/embarqués et douze copies identiques
du scheduler. VERSION, pyproject.toml, README et six manifestes déclarent
0.7.12. Onze tâches de réalisation/validation sont prouvées et cochées avant
archive ; archivage et ce rapport sont des postconditions suivies séparément.
OpenSpec : baseline stricte 10/10 ; avant archive standard et strict 11/11 ;
après archive standard et strict 10/10. L'archive a synchronisé trois specs :
2 exigences ajoutées, 15 modifiées, 1 retirée et 1 renommée.

Durée exhaustive de session, temps modèle/outils, tokens, cache et coût de
conversation : N/A, télémétrie non instrumentée. Les mesures fournisseur de
latence, débit et qualité du code sont N/A : aucune génération réelle dans SCM.

## 2. Messages et outils

Session exécutée directement par Codex selon SCM, résolu depuis le DEVOPS du
projet. Aucun sous-agent, pilotage CAB, session OpenCode ou compétence de
statistiques de session pilotée n'est utilisé. Messages et appels d'outils
exhaustifs : N/A, non agrégés ; les preuves retenues sont les sorties réellement
observées et les validations conservées dans l'archive.

Échecs intermédiaires corrigés et vérifiés : la validation OpenSpec exigeait
la conservation des identifiants historiques de cinq scénarios ; une insertion
de test scheduler avait déplacé deux assertions dans la mauvaise méthode ;
un test de snapshot TCU attendait encore la release 0.7.11. Les résultats
initiaux échoués sont conservés et les suites correspondantes ont ensuite
réussi. Aucun critère de performance ni contrôle de sécurité n'a été affaibli.

## 3. Fichiers

Comparaison SHA-256 à baseline.json, sans inspection Git durant SCM.
Racine : /home/devops/datas/tools-codex. Chemins finaux :

| Chemin | Opération |
|---|---|
| .codex/commands/pllm.md | Modifié |
| .codex/commands/tfl.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| PROJECT.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| openspec/specs/llm-refresh-scheduling/spec.md | Modifié |
| openspec/specs/pllm-evaluation/spec.md | Modifié |
| openspec/specs/tfl-catalog/spec.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/cm/skills/cm/SKILL.md | Modifié |
| plugins/cm/skills/cm/scripts/scheduler.py | Modifié |
| plugins/lm/.codex-plugin/plugin.json | Modifié |
| plugins/lm/skills/lm/scripts/scheduler.py | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/references/model-evidence.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| plugins/pllm/skills/pllm/scripts/scheduler.py | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/prompt/skills/prompt/scripts/scheduler.py | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/skills/tcu/scripts/scheduler.py | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/skills/tfl/SKILL.md | Modifié |
| plugins/tfl/skills/tfl/references/model-evidence.md | Modifié |
| plugins/tfl/skills/tfl/scripts/scheduler.py | Modifié |
| plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| pyproject.toml | Modifié |
| skills/cm/SKILL.md | Modifié |
| skills/cm/scripts/scheduler.py | Modifié |
| skills/lm/scripts/scheduler.py | Modifié |
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/references/model-evidence.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| skills/pllm/scripts/scheduler.py | Modifié |
| skills/prompt/scripts/scheduler.py | Modifié |
| skills/tcu/scripts/scheduler.py | Modifié |
| skills/tfl/SKILL.md | Modifié |
| skills/tfl/references/model-evidence.md | Modifié |
| skills/tfl/scripts/scheduler.py | Modifié |
| skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| tests/test_free_performance.py | Modifié |
| tests/test_llm_schedule.py | Modifié |
| tests/test_lm_blacklist.py | Modifié |
| tests/test_pllm_free_fallback.py | Modifié |
| tests/test_pllm_six_modes.py | Modifié |
| tests/test_tcu_update.py | Modifié |
| tests/test_tfl_opencode_catalog.py | Modifié |
| tests/test_tfl_pricing.py | Modifié |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/STATISTIQUES.md | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-COHERENCE.json | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-DOCUMENTAIRE.md | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-FINALE.json | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-GLOBALE-PY313.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-GLOBALE-PY314-CORRECTION.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-GLOBALE-PY314.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-LM.json | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-OPENSPEC.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-SYNTAXE-PY313.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-SYNTAXE-U1.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-U1-CORRECTION.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/VALIDATION-U1.txt | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/baseline.json | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/design.md | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/proposal.md | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/specs/llm-refresh-scheduling/spec.md | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/specs/pllm-evaluation/spec.md | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/specs/tfl-catalog/spec.md | Créé, destination archivée |
| openspec/changes/archive/2026-10-26-remove-general-opencode-tfl/tasks.md | Créé, destination archivée |

Totaux du dépôt : **52 fichiers préexistants modifiés** et
**20 nouveaux chemins archivés**, soit **72 livrables**.
Les déplacements du change vers l'archive ne sont comptés qu'à destination.
Les trois spécifications synchronisées sont incluses dans les 52 fichiers.
Aucun fichier initial n'a été supprimé. Le relevé inclut les preuves locales
et ce rapport ; il ne compte pas les temporaires nettoyés des tests/compilations.

Hors dépôt, la mutation explicitement autorisée concerne la politique commune
`/home/ade/.codex/lm/blacklist.json`, via le verrou et le remplacement atomique
LM. Ses autres entrées sont préservées. Ce stockage utilisateur n'est pas un
livrable versionné du dépôt. AGENTS.md et DEVOPS.md conservent leurs empreintes
au début du change. Les sources installées TFL/PLLM, rapports et mémoires
utilisateur existants ne sont pas réécrits. Lignes ajoutées/supprimées : N/A,
aucun diff Git ni instantané textuel initial n'a été instrumenté.

## 4. Commandes et validations

| Contrôle | État et résultat observé |
|---|---|
| Spécifications avant code | openspec validate remove-general-opencode-tfl --strict : exécutée et réussie avant les écritures de code. |
| Contrat producteur/consommateurs | VALIDATION-U1-CORRECTION.txt : 158 tests ciblés exécutés et réussis. |
| Python 3.14.10 | /home/devops/python/current/bin/python3 -B, unittest.defaultTestLoader.discover('tests') : 323 tests exécutés et réussis. |
| Python 3.13.5 | python3 -B, même découverte unittest : 323 tests exécutés et réussis. |
| Syntaxe | py_compile.compile(..., doraise=True) : 24 fichiers compilés sur chacune des deux branches, cibles temporaires sous tests et nettoyées. |
| LM | Deux commandes ADD explicites exécutées ; persistance, huit consommateurs, variantes, préservation et idempotence vérifiées dans VALIDATION-LM.json. |
| Release et parités | Six manifestes à 0.7.12 ; six paires de paquets et douze schedulers conformes dans VALIDATION-COHERENCE.json. |
| Périmètre/encodage | Empreintes, UTF-8/LF et recherche des signatures usuelles de jetons/clés privées : exécutées et réussies. |
| OpenSpec avant archive | --all puis --all --strict : 11/11 exécutés et réussis. |
| Préparation archive | status --change remove-general-opencode-tfl --json : isPlanningComplete=true, isComplete=true. |
| Archivage natif | archive remove-general-opencode-tfl --json --yes : code 0, specsUpdated=true, destination unique vérifiée. |
| OpenSpec après archive | --all puis --all --strict : 10/10 exécutés et réussis ; aucune évolution active. |
| Rapport | Présence, six sections, UTF-8/LF, totaux, tâches et empreinte vérifiés après écriture dans VALIDATION-FINALE.json. |

Binaire OpenSpec : /home/devops/.local/npm/bin/openspec. Aucun nouvel outil ou
paquet n'est installé. Aucun lint/type additionnel n'est déclaré dans le
pyproject.toml lu ; frontend, ShellCheck et migrations sont non pertinents.
Tests fournisseur réels, installation TFL/PLLM, activation du planning,
publication distante et opérations Git : non exécutés dans cette livraison.

## 5. Accès web

Aucune recherche web, requête fournisseur, génération, lecture de quota,
crédit ou solde n'est explicitement lancée dans ce change SCM. Les tests
emploient données, trousseaux, métadonnées et transports contrôlés hors ligne.
Les recherches et essais Inkling antérieurs de la conversation ne sont pas
des validations de cette release ; ils restent hors de cette session SCM.
Les métriques commerciales, les prix et performances fournisseur courants
sont N/A dans ce rapport. Aucune clé fournisseur n'est lue pour les tests,
transmise au modèle, passée en argument ou conservée dans les livrables.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Projet réel | Deux catalogues, Go exclusif en 1 à 4, LM Inkling ; 323 tests globaux réussis par branche. |
| AGENTS.md | Inchangé, empreinte de début de change conservée. |
| PROJECT.md | Mis à jour : catalogue TFL et investigation limités à Go/OpenRouter. |
| TECHNICAL.md | Mis à jour : contrat 0.7.12, producteurs/consommateurs, général retiré, planning adapté et limites des helpers historiques. |
| BUILD.md | Mis à jour : distribution à deux catalogues, sélection Go exclusive et distinction installation/activation. |
| DEVOPS.md | Inchangé par cette session ; binaires Python DevOps/OpenSpec déclarés utilisés. |
| README.md | Mis à jour : release 0.7.12 et comportements Go/OpenRouter courants. |
| CHANGELOG.md | Entrées Unreleased ajoutées ; anciennes livraisons préservées comme historique. |
| OpenSpec | Trois specs synchronisées par archive native ; standard et strict globaux 10/10 après archivage. |
| Commandes, skills et guides | TFL/PLLM/CM cohérents ; six distributions et schedulers synchronisés. |
| Métadonnées | VERSION, project.version, README et six manifestes à 0.7.12. |

Les sources locales sont livrées ; les profils installés et le timer réel ne
sont pas actualisés. La liste LM utilisateur est, elle, réellement mise à jour
et consommable dès la prochaine invocation. Les anciens rapports restent
historiques. Le défaut de rendu de certains prix OpenRouter constaté avant
SCM reste signalé et hors périmètre validé. Aucun blocage de réalisation
connu ne subsiste sur ce change ; les qualifications externes non exécutées
restent des limites explicites. Aucun second change n'a été ouvert.
