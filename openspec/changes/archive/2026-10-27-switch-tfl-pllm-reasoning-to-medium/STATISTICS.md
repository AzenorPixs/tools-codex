# STATISTIQUES — switch-tfl-pllm-reasoning-to-medium

Projet : Tools Codex (`tools-codex`). Session SCM directe du 27 octobre 2026.
Release locale : 0.7.14. Rapport produit après l'archive native
`2026-10-27-switch-tfl-pllm-reasoning-to-medium`.

## 1. Statistiques générales

Un change TFL/PLLM spécifié, implémenté, validé et archivé. Medium est exigé
dans les preuves, envoyé par les transports et utilisé pour les nouvelles
mesures. Les modèles High/XHigh seuls sont exclus. Les rapports et mémoires
existants restent des résultats historiques et ne sont pas requalifiés.

Les suites complètes totalisent 330 tests réussis sous Python 3.13.5 et 330
sous Python 3.14.10, soit 660 exécutions. Les 269 tests ciblés sont inclus dans
ces totaux et ne s'y ajoutent pas. Les durées observées des suites globales sont
8,447 s et 9,713 s, soit 18,160 s cumulées ; elles n'incluent pas les autres
contrôles ni le temps de session.

Syntaxe : 27 fichiers Python compilés par interpréteur, soit 54 compilations.
Parité : 14 comparaisons de contenu entre moteurs, skills, guides et copies
embarquées. Les six manifestes, `VERSION` et `project.version` sont alignés
sur 0.7.14. L'encodage UTF-8/LF est vérifié pour 28 fichiers.

OpenSpec strict : 11/11 avant archivage, puis 10/10 après synchronisation.
L'archive native a synchronisé sept exigences existantes : quatre TFL et trois
PLLM. Une exigence PLLM a ensuite été raccourcie, dans la source et l'archive,
pour respecter la limite de longueur ; la validation globale finale réussit.
Durée totale de session, tokens, coût et cache : N/A, télémétrie non instrumentée
dans SCM.

## 2. Messages et outils

La session a été exécutée directement par Codex, sans sous-agent, pilotage CAB,
session OpenCode ou compétence de statistiques de session pilotée. Le prompt
SCM a été résolu depuis le référentiel indiqué par `DEVOPS.md`. Le périmètre
autonome validé couvre le change OpenSpec, les sources, distributions, tests,
documentation et incrément de version.

Messages et appels d'outils exhaustifs : N/A, aucun agrégat fiable instrumenté.
Les diagnostics corrigés concernent la conservation des scénarios OpenSpec,
les intitulés requis par le validateur et la limite de longueur d'une exigence.
Les validations concernées ont ensuite réussi. Un premier test ciblé a aussi
révélé deux attentes de version 0.7.13, corrigées avant la réussite des 269
tests ciblés et des suites globales.

## 3. Fichiers

Inventaire des écritures de ce change, hors éventuelles modifications
préexistantes du dépôt :

| Ensemble | Nombre | Opération |
|---|---:|---|
| Moteurs `performance.py`, preuves `model_evidence.py`, générateurs TFL et évaluateurs PLLM, sources et copies embarquées | 12 | Admission Medium, paramètres API, diagnostics, mémoire et preuves historiques |
| Skills CM/TFL/PLLM et références de preuves, autonomes et embarqués | 10 | Contrat Medium et synchronisation des copies |
| `PROJECT.md`, `TECHNICAL.md`, `BUILD.md`, `README.md`, `CHANGELOG.md`, `VERSION`, `pyproject.toml` | 7 | Documentation et release 0.7.14 |
| Manifestes des six plugins | 6 | Version commune ; description TFL alignée sur Medium |
| Tests Python | 15 | Admission, transports, preuves, mémoire, fixtures et attentes de release |
| Spécifications OpenSpec principales | 2 | Exigences TFL et PLLM synchronisées |
| Archive OpenSpec, hors présent rapport | 5 | Proposition, conception, tâches et deux deltas de spécification |
| Présent rapport | 1 | `STATISTIQUES.md` créé après archivage |
| **Total des destinations de ce change** | **58** | **Écritures attribuées à cette session** |

Lignes ajoutées/supprimées : N/A, aucune baseline textuelle exhaustive propre
au change n'a été enregistrée. Aucun secret, rapport fournisseur courant,
mémoire de performance, profil utilisateur, timer ou configuration personnelle
n'a été modifié. Aucun benchmark fournisseur réel n'a été lancé.

## 4. Commandes et validations

| Contrôle | Résultat réel |
|---|---|
| Spécification avant code | `openspec validate 2026-10-27-switch-tfl-pllm-reasoning-to-medium --strict` : réussie |
| Tests ciblés | 269 tests exécutés et réussis sous Python 3.14.10 |
| Tests globaux | `unittest discover -s tests` : 330 tests exécutés et réussis sous Python 3.13.5 et 3.14.10 |
| Syntaxe | `py_compile` de 27 fichiers Python sous chaque version supportée : 54 compilations réussies |
| Parité, release, encodage | 14 comparaisons de parité, six manifestes alignés, versions cohérentes et 28 fichiers UTF-8/LF : réussis |
| OpenSpec avant archive | `openspec validate --all --strict` : 11/11 réussis |
| Préparation | `openspec status --change 2026-10-27-switch-tfl-pllm-reasoning-to-medium --json` : artefacts complets |
| Archivage | `openspec archive 2026-10-27-switch-tfl-pllm-reasoning-to-medium --yes` : code 0, deux spécifications synchronisées, archive unique créée |
| OpenSpec après archive | `openspec validate --all --strict` : 10/10 réussis après correction de longueur |
| Rapport et nettoyage | Six sections présentes ; UTF-8/LF et totaux vérifiés après écriture. Aucun `BLOCKER.md` ou `BLOCKERS.md` n'est présent dans l'archive |
| Git SCM | Étape séparée de ce rapport, exécutée après sa production conformément au prompt SCM ; résultat indiqué dans la restitution de session |

Binaire OpenSpec : `/home/devops/.local/npm/bin/openspec`. Aucun outil ni
paquet ajouté. Contrôles frontend, SQL, ShellCheck et lint/types : non
pertinents pour le périmètre Python/Markdown/JSON modifié.

## 5. Accès web

Aucune recherche web, requête fournisseur, génération, lecture de quota,
crédit ou solde n'a été lancée. Les transports, catalogues et profils des tests
sont contrôlés hors ligne. Performances fournisseur et coût réel des modèles :
N/A, aucun appel fournisseur.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Comportement TFL/PLLM | Medium est l'effort demandé et prouvé ; aucun repli vers High/XHigh. Les anciennes preuves High/XHigh déclenchent une nouvelle investigation et ne valident pas Medium |
| `AGENTS.md` | Inchangé ; règles OpenSpec, tests, versions et encodage appliquées |
| `PROJECT.md` | Actualisé : Medium requis ; preuves et mesures antérieures restent historiques |
| `TECHNICAL.md` | Actualisé : admission, paramètres de transport et mémoire Medium |
| `BUILD.md` | Actualisé : qualification Medium et contrats d'installation |
| `DEVOPS.md` | Inchangé ; Python 3.13/3.14 et binaire OpenSpec utilisés |
| `README.md` | Version 0.7.14, filtres et benchmark Medium actualisés |
| `CHANGELOG.md` | Deux entrées Unreleased décrivent le changement et l'incrément de version |
| OpenSpec | Deltas TFL/PLLM synchronisés ; validation stricte après archivage 10/10 |
| Distributions | Moteurs, skills et références synchronisés dans les sources autonomes et embarquées |

Les profils installés et les catalogues déjà produits restent distincts de la
release locale 0.7.14. Une nouvelle invocation TFL/PLLM produira ses propres
mesures Medium ; les anciennes mesures High/XHigh ne sont pas converties.
