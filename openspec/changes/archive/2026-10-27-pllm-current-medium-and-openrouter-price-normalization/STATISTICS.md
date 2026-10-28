# STATISTIQUES — pllm-current-medium-and-openrouter-price-normalization

Projet : Tools Codex (`tools-codex`). Session SCM directe du 27 octobre 2026.
Release locale : 0.7.16. Rapport produit après l'archive native
`2026-10-27-pllm-current-medium-and-openrouter-price-normalization`.

## 1. Statistiques générales

Un change PLLM/TFL spécifié, corrigé, testé et archivé. Le contrôle Medium
ignore les anciens overrides et journaux de tentatives comme provenance, tout
en continuant à exiger Medium dans la requête courante. La vérification de prix
tolère l'arrondi flottant de sérialisation ; les calculs gardent les prix
décimaux canoniques TFL.

La suite complète a exécuté et réussi 330 tests sous Python 3.14.10, en
15,599 s. Les tests ciblés sont inclus dans ce total et ne s'y ajoutent pas.
Ils ont également été exécutés séparément : raisonnement 8/8, prix OpenRouter
6/6, liste noire et parité des distributions 26/26, TCU et versions des
manifestes 52/52.

Syntaxe : huit fichiers Python compilés avec succès : les quatre copies de
`performance.py` et quatre fichiers de tests. Les quatre moteurs partagés ont
le même SHA-256 :
`d15746670cf8e0dcb83ea0fad48888fce13bcf01f5e77d26de7e1f45f90ea34d`.
Les six manifestes, `VERSION`, `pyproject.toml` et `README.md` déclarent 0.7.16.

OpenSpec strict : 11/11 avant archivage, puis 10/10 après synchronisation.
L'archive native a ajouté deux exigences aux spécifications PLLM et TFL.
Durée de session, tokens, coût et cache : N/A, télémétrie SCM non instrumentée.

## 2. Messages et outils

Session directe Codex sans sous-agent, pilotage CAB ou session OpenCode. Le
prompt SCM a été résolu depuis le référentiel indiqué par `DEVOPS.md`. Le
périmètre validé couvre le change OpenSpec, les quatre moteurs, les tests, la
documentation et l'alignement de release. Les modifications antérieures déjà
présentes dans l'arbre de travail sont distinguées de ce change dans le
décompte ci-dessous.

Nombre exhaustif de messages et d'appels outils : N/A, aucun agrégat fiable
n'est instrumenté pour SCM. Aucun identifiant, clé ou compte fournisseur n'a
été exposé.

## 3. Fichiers

Inventaire des destinations écrites pour ce change, hors modifications
préexistantes du dépôt :

| Ensemble | Nombre | Opération |
|---|---:|---|
| Moteurs `performance.py` autonomes et embarqués TFL/PLLM | 4 | Filtre Medium courant et comparaison contrôlée des prix décimaux/flottants |
| Tests Python | 4 | Régressions effort historique, prix, attentes de release et parité TCU |
| Release et documentation | 4 | `VERSION`, `pyproject.toml`, `README.md`, `CHANGELOG.md` alignés sur 0.7.16 |
| Manifestes des six plugins | 6 | Version commune 0.7.16 |
| Spécifications principales OpenSpec | 2 | Une exigence ajoutée dans `pllm-evaluation` et une dans `tfl-catalog` |
| Artefacts de l'archive OpenSpec, hors rapport | 8 | Métadonnées, README de change, proposition, design, tâches et deux deltas |
| Rapport de statistiques | 1 | `STATISTIQUES.md` créé après archivage |
| **Total des destinations de ce change** | **29** | **Écritures attribuées à cette session** |

Lignes ajoutées/supprimées : N/A, aucune baseline textuelle exhaustive propre
au change n'a été enregistrée. Aucun secret, profil utilisateur, timer,
catalogue ou mémoire PLLM/TFL n'a été modifié. Aucun benchmark fournisseur
réel n'a été lancé.

## 4. Commandes et validations

| Contrôle | Résultat réel |
|---|---|
| Change ciblé | `openspec validate pllm-current-medium-and-openrouter-price-normalization --strict` : réussi |
| Tests effort | `python3 -m unittest discover -s tests -p 'test_reasoning_admission.py'` : 8 réussis |
| Tests prix | `python3 -m unittest discover -s tests -p 'test_openrouter_eur_filter.py'` : 6 réussis |
| Tests liste noire/parité | `python3 -m unittest discover -s tests -p 'test_lm_blacklist.py'` : 26 réussis |
| Tests TCU/version | `python3 -m unittest discover -s tests -p 'test_tcu_update.py'` : 52 réussis |
| Suite globale | `python3 -m unittest discover -s tests` : 330 réussis en 15,599 s |
| Syntaxe | `python3 -m py_compile` des huit fichiers concernés : réussie |
| Release et copies | Six manifestes et trois fichiers de version cohérents ; quatre modules partagés identiques : réussite |
| OpenSpec avant archive | `openspec validate --all --strict` : 11/11 réussis |
| Archivage | `openspec archive pllm-current-medium-and-openrouter-price-normalization --yes --json` : code 0, deux deltas synchronisés, archive créée |
| OpenSpec après archive | `openspec validate --all --strict` : 10/10 réussis |
| Rapport et encodage | Six sections présentes, UTF-8/LF et totaux vérifiés après écriture ; aucun bilan BLOCKER dans l'archive |
| Git SCM | Étape distincte après ce rapport ; résultat à consigner dans la restitution finale |

Binaire Python : `/home/devops/python/current/bin/python3`. Binaire OpenSpec :
`/home/devops/.local/npm/bin/openspec`. Aucun outil ni paquet ajouté. Lint,
types, frontend, SQL et ShellCheck : non pertinents pour ce périmètre.

## 5. Accès web

Aucune recherche web, requête fournisseur, génération, lecture de quota, crédit
ou solde n'a été effectuée pendant cette session SCM. Les tests utilisent des
données contrôlées hors ligne. Les performances fournisseur et le coût réel
des modèles restent N/A.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Comportement PLLM/TFL | Le Medium courant reste contrôlé ; la provenance historique ne l'invalide plus. Les prix canoniques restent la base des moyennes et plafonds. |
| `AGENTS.md` | Inchangé ; ordre OpenSpec, validations et rapport post-archive appliqués |
| `PROJECT.md` | Inchangé ; responsabilités et source de version demeurent exactes |
| `TECHNICAL.md` | Inchangé ; versions Python et modules partagés demeurent exacts |
| `BUILD.md` | Inchangé ; distribution autonome/embarquée et procédure de release demeurent exactes |
| `DEVOPS.md` | Inchangé ; Python 3.14.10 et chemins d'outils utilisés observés |
| `README.md` | Version de release 0.7.16 vérifiée |
| `CHANGELOG.md` | Entrée Unreleased décrivant les deux corrections et la release 0.7.16 |
| OpenSpec | Change archivé ; deux exigences synchronisées ; validation stricte après archivage 10/10 |
| Distributions | Quatre copies `performance.py` identiques ; six manifestes à 0.7.16 |

La release locale ne met pas à jour la copie installée dans le profil Codex et
ne prouve pas une nouvelle évaluation réelle des modes 1 ou 5. Cette
qualification fournisseur reste une action distincte.
