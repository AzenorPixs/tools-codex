# STATISTIQUES — modify-tfl-pllm-reasoning-and-openrouter-eur-filter

Projet : Tools Codex. Session SCM directe. Release locale : 0.7.9.
Archive native unique : 2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter.
Autorisation : périmètre SCM validé par le développeur, y compris exclusion
stricte des capacités HIGH/XHIGH inconnues, version et archivage complet.

## 1. Statistiques générales

Le change exige une preuve HIGH/XHIGH pour chaque gratuit et payant de TFL
et PLLM, avant génération, sélection et affichage. Les exclus d'effort sont
conservés dans les audits JSON et absents de tous les tableaux. HIGH est
préféré, XHIGH est le seul repli. Un budget seul ou un historique ne suffit
plus. Le candidat DeepSeek direct sans preuve est aussi exclu.

TFL affiche Go puis OpenRouter, huit colonnes chacun, puis les essais gratuits
admissibles à l'effort. La collecte générale et opencode restent dans le JSON
pour les modes gratuits PLLM 3/4. OpenRouter est plafonné à 0,20 EUR/M après
conversion au dernier taux BCE USD par EUR publié, avec source et dates.
Prix natifs USD, décimales exactes et prix EUR restent auditables. Le plafond
inclusif est comparé avant arrondi. PLLM refait le contrôle indépendamment
des moyennes historiques. Une conversion non vérifiable ou une section vide
bloque le nouveau TFL et préserve les anciens rapports.

Qualification finale : 303 tests distincts sous Python 3.14.10 et 303 sous
Python 3.13.5, soit 606 exécutions finales, sans échec ni erreur. Onze tests
nouveaux dans deux modules : cinq d'admission et six de conversion/rapport.
Les 205 tests du lot effort et les 113 du lot EUR/présentation se recouvrent
avec la suite globale ; ils ne sont pas additionnés aux 606 exécutions finales.
Un module de fixtures de taux est ajouté ; son taux simulé ne vaut pas cours réel.

Compilation des 24 fichiers Python touchés sur chaque branche : 48 compilations.
Quatre moteurs performance.py identiques ; deux paires de scripts et deux
paires de skills TFL/PLLM, ainsi que les skills CM, identiques octet pour octet.
VERSION, pyproject.toml, README et six manifestes déclarent 0.7.9.

OpenSpec : sept tâches de réalisation/validation satisfaites avant archive ;
deux postconditions distinctes exécutées ensuite (archive et ce rapport).
Archive native : cinq exigences ajoutées, quatre modifiées, aucune supprimée
ou renommée. Avant archive : ciblé strict valide, global standard et strict
11/11. Après archive : standard et strict 10/10 ; aucun change actif.

Durée de session, temps modèle/outils, tokens, cache et coûts de conversation :
N/A, télémétrie non instrumentée. Aucune mesure ou réussite fournisseur réelle
n'est déduite des tests hors ligne.

## 2. Messages et outils

SCM est exécuté directement par Codex, via le référentiel prompt déclaré dans
DEVOPS.md et le résolveur de la skill prompt. Aucun sous-agent, pilotage CAB,
session OpenCode ou compétence de statistiques des sessions pilotées utilisé.

Messages et appels d'outils exhaustifs : N/A, non agrégés. Les preuves retenues
sont les résultats de commandes et les fichiers réellement observés. Les
écritures sont limitées au projet. Les temporaires de tests/compilation sont
créés sous tests puis nettoyés ; aucune installation de dépendance ajoutée.

Échecs intermédiaires corrigés : exigences OpenSpec trop longues, fixtures
positives sans déclaration d'effort, anciennes attentes DeepSeek et budget
seul devenues incompatibles, import de classe collectant des tests en double.
Les assertions de performance sont conservées. Les nouvelles attentes
d'exclusion suivent la décision validée ; aucun seuil n'est affaibli pour
faire passer une vérification.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Comparaison ciblée SHA-256 à l'état
initial, sans inspection Git. Chemins finaux :

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
| openspec/specs/pllm-evaluation/spec.md | Modifié |
| openspec/specs/tfl-catalog/spec.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/cm/skills/cm/SKILL.md | Modifié |
| plugins/lm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| plugins/pllm/skills/pllm/scripts/performance.py | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/skills/tfl/SKILL.md | Modifié |
| plugins/tfl/skills/tfl/scripts/performance.py | Modifié |
| plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| pyproject.toml | Modifié |
| skills/cm/SKILL.md | Modifié |
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| skills/pllm/scripts/performance.py | Modifié |
| skills/tfl/SKILL.md | Modifié |
| skills/tfl/scripts/performance.py | Modifié |
| skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| tests/test_extension_qualification.py | Modifié |
| tests/test_free_performance.py | Modifié |
| tests/test_lm_blacklist.py | Modifié |
| tests/test_pllm_free_fallback.py | Modifié |
| tests/test_pllm_http_diagnostics.py | Modifié |
| tests/test_pllm_price_priority.py | Modifié |
| tests/test_pllm_six_modes.py | Modifié |
| tests/test_pllm_ttft.py | Modifié |
| tests/test_tcu_update.py | Modifié |
| tests/test_tfl_go_metadata.py | Modifié |
| tests/test_tfl_opencode_catalog.py | Modifié |
| tests/test_tfl_pricing.py | Modifié |
| tests/test_throughput_measurement.py | Modifié |
| tests/test_reasoning_admission.py | Créé |
| tests/test_openrouter_eur_filter.py | Créé |
| tests/eur_fixtures.py | Créé |
| openspec/changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/specs/pllm-evaluation/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/STATISTIQUES.md | Créé |

Totaux : 44 fichiers préexistants modifiés et 9 nouveaux chemins, soit
53 livrables. Les cinq artefacts du change sont comptés à leur destination
archivée, sans double compte de leur déplacement. Aucun fichier initial
supprimé. Les deux spécifications de référence sont synchronisées nativement.

La revue porte sur les chemins concernés, sans inventaire récursif global ;
elle ne qualifie pas les modifications antérieures ou concurrentes ailleurs.
AGENTS.md, DEVOPS.md et openspec/config.yaml conservent leurs empreintes initiales.
Les rapports TFL/PLLM et mémoires utilisateur existants ne sont pas réécrits.
Nombre de lignes ajoutées/supprimées : N/A, aucun diff Git ni instantané
textuel initial exhaustif instrumenté pour ce calcul.

## 4. Commandes et validations

| Validation | Résultat observé |
|---|---|
| Spécification avant code | openspec validate modify-tfl-pllm-reasoning-and-openrouter-eur-filter --strict : exécutée et réussie. |
| Lot effort | 205 tests ciblés hors ligne et compilation : exécutés et réussis. |
| Lot EUR/présentation | 113 tests ciblés puis six tests EUR de l'état final : exécutés et réussis. |
| Suite Python 3.14.10 | /home/devops/python/current/bin/python3 -B, unittest.defaultTestLoader.discover('tests') : 303 tests exécutés et réussis. |
| Suite Python 3.13.5 | /usr/bin/python3 -B, même découverte unittest : 303 tests exécutés et réussis. |
| Syntaxe | py_compile.compile(..., doraise=True) des 24 fichiers touchés sur chaque branche, cibles temporaires sous tests : réussie. |
| Distributions | Quatre moteurs identiques ; scripts/skills TFL/PLLM et skills CM synchronisés : exécutée et réussie. |
| Version | VERSION, project.version, README et six plugins à 0.7.9 : exécutée et réussie. |
| Encodage et secrets | UTF-8/LF et signatures de secrets sur les fichiers touchés : exécutés et réussis. |
| OpenSpec avant archive | Ciblé strict valide ; openspec validate --all puis --all --strict, 11/11 : exécutés et réussis. |
| Préparation archive | openspec status --change modify-tfl-pllm-reasoning-and-openrouter-eur-filter --json : artefacts complets. |
| Archive native | openspec archive modify-tfl-pllm-reasoning-and-openrouter-eur-filter --json --yes : code 0, specsUpdated=true, 5 ajouts/4 modifications. |
| OpenSpec après archive | openspec validate --all puis --all --strict : 10/10, exécutés et réussis. |
| Rapport d'archive | Présence, six sections, UTF-8/LF, totaux croisés et empreinte contrôlés après écriture. |

Binaire OpenSpec : /home/devops/.local/npm/bin/openspec. Tests lancés par un
runner unittest capturant les sorties attendues des scénarios d'échec ; seuls
leurs bilans et erreurs éventuelles sont restitués. Temporaires contrôlés et
nettoyés. Aucun outil de lint/types configuré pour ce périmètre ; contrôles
frontend, ShellCheck et migrations : non pertinents.

Qualification fournisseur réelle, installation dans un nouveau profil Codex,
TCU, activation de hook ou planning, publication distante : non exécutées.
Git, commit, push et tags : non exécutés.

## 5. Accès web

Aucun appel fournisseur, recherche web, benchmark réel, contrôle de quota,
crédit ou solde effectué dans ce change SCM. Les tests injectent réseau,
métadonnées, taux et trousseau fictifs. Les sources réseau utilisées lors des
futures invocations restent les catalogues officiels existants et, pour les
coûts EUR, https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml.

Les prix et disponibilités de l'ancien rapport de la conversation ne valident
pas cette release. Aucun secret n'est ajouté ou créé. Les identifiants et
clés de fournisseur ne sont ni passés en arguments, ni publiés dans ce rapport.
Mesures de latence, débit et coût web réel de cette livraison : N/A, tests
hors ligne sans invocation fournisseur.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Projet réel | Admission commune, plafond EUR et deux tableaux ; 303 tests distincts réussis par branche. |
| AGENTS.md | Inchangé, empreinte initiale conservée ; règles de sécurité et de travail toujours applicables. |
| PROJECT.md | Mis à jour, présentation TFL Go/OpenRouter et général JSON préservé. |
| TECHNICAL.md | Mis à jour, preuve HIGH/XHIGH, conversion BCE, prix natifs et limites de qualification. |
| BUILD.md | Mis à jour, contrat 0.7.9, distribution et distinction installation/activation réelles. |
| DEVOPS.md | Inchangé, empreinte initiale conservée ; binaires Python et OpenSpec déclarés utilisés. |
| README.md | Mis à jour, release 0.7.9, deux tableaux, plafond EUR et effort vérifiable. |
| CHANGELOG.md | Entrée Unreleased ajoutée ; historique des anciennes releases préservé. |
| OpenSpec | tfl-catalog et pllm-evaluation synchronisés par l'archive ; strict global 10/10. |
| Commandes/skills/CM | Instructions et descriptions cohérentes, distributions identiques vérifiées. |

Les catégories et six priorités PLLM, seuils de performance, paliers et
protocole 8, contrôles de ressources et exclusions LM sont préservés.
Les filtres tarifaire/effort s'appliquent désormais avant admission. Un modèle
dont la capacité n'est pas vérifiable reste exclu, y compris DeepSeek direct ;
le dernier catalogue Go peut perdre toutes ses entrées. Ce risque a été
explicitement accepté par le développeur.

La livraison concerne les sources locales 0.7.9. Les installations utilisateur,
rapports réels et activations restent distincts. Aucun blocage de réalisation
connu ne subsiste dans le périmètre approuvé ; les qualifications externes
non exécutées ci-dessus restent des limites explicites.

