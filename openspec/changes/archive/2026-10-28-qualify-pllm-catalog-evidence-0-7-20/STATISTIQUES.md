# STATISTIQUES — qualify-pllm-catalog-evidence-0-7-20

Projet : Tools Codex (`tools-codex`). Session SCM directe du 28 octobre 2026.
Release locale : 0.7.20. Rapport produit après l'archive native
`2026-10-28-qualify-pllm-catalog-evidence-0-7-20`.

## 1. Statistiques générales

Le change synchronise TFL et PLLM autour de l'acceptation du paramètre Medium,
du fingerprinting stable des sources officielles et du plafond OpenRouter payé
de 0,10 EUR/M. Les sources HTML sont empreintées sur leur texte visible en NFC
avec espaces réduits ; les autres sources utilisent les octets reçus. Le moteur
TFL/PLLM conserve le traitement `copy` du chemin de réponse complète, et une
régression couvre l'enregistrement de l'acceptation Medium et le débit.

La suite complète compte **340 tests réussis** sous Python 3.14.10. Les 19
tests ciblés de preuves/fingerprinting et les autres tests ciblés sont inclus
dans ces 340 tests et ne s'y additionnent pas. Syntaxe : 19 fichiers Python
compilés. Parité : les quatre moteurs `model_evidence.py` et les distributions
autonomes/embarquées ont été comparés. `VERSION`, `pyproject.toml` et les six
manifestes sont alignés sur 0.7.20. UTF-8/LF vérifié sur les fichiers du
périmètre contrôlé.

OpenSpec après archivage : validation standard et stricte, **10/10** chacune.
Trois exigences TFL trop longues ont été raccourcies dans la spécification et
son delta archivé ; les détails normatifs restent dans les scénarios. Durée,
tokens et coût de session : N/A, télémétrie SCM non instrumentée.

## 2. Messages et outils

Session exécutée directement par Codex via le prompt SCM, sans sous-agent,
pilotage CAB ni session OpenCode. Les collectes TFL et PLLM ont utilisé le
catalogue TFL frais. TFL a nécessité trois publications au cours de
l'investigation des preuves ; le rapport final est complet et ne contient plus
d'investigation requise. PLLM normal a évalué les sept politiques : toutes
sont valides, dont le mode5 sous le plafond 0,10 EUR/M.

Messages et appels d'outils exhaustifs : N/A, aucun agrégat fiable instrumenté.
Les rapports TFL/PLLM réels restent dans `reports/`, hors artefacts distribués.
Les détails de quotas et soldes ne sont pas reproduits dans ce rapport.

## 3. Fichiers

Le périmètre couvre les spécifications TFL/PLLM, le change archivé et son
delta, les moteurs et commandes TFL/PLLM, les références de preuves, les skills
CM/TFL/PLLM, les tests de prix, de débit et de preuve, la documentation du
projet, `VERSION`, `pyproject.toml` et les six manifestes.

| Ensemble | Total vérifié | Résultat |
|---|---:|---|
| Tests Python complets | 340 | Tous réussis |
| Tests ciblés de preuves/fingerprinting | 19 | Tous réussis, inclus dans les 340 |
| Fichiers Python compilés | 19 | Syntaxe valide |
| Paires/copies de distributions contrôlées | 11 | Identiques octet pour octet |
| Manifestes de plugins | 6 | Version 0.7.20 |
| Exigences OpenSpec validées après archive | 10 | 10 réussies en standard et strict |

Nombre exhaustif de chemins modifiés et lignes ajoutées/supprimées : N/A,
aucun instantané textuel initial n'a été enregistré ; l'étape SCM suivante
contrôle les chemins Git sans lire leur contenu.

## 4. Commandes et validations

| Contrôle | Résultat observé |
|---|---|
| Fingerprinting ciblé | `python3 -B -m unittest discover -s tests -p test_model_evidence.py -v` : 19 réussis |
| Suite complète | `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests -v` : 340 réussis |
| Syntaxe | `python3 -m py_compile` sur 19 fichiers Python : réussie |
| Parité et versions | 11 copies contrôlées identiques ; six manifestes, `VERSION` et `project.version` à 0.7.20 |
| Encodage | UTF-8/LF vérifié pour les fichiers de code, tests, documents et manifestes du périmètre |
| Seuil OpenRouter | Tests de frontière 0,10 EUR/M, ancien catalogue et rang forcé : réussis |
| TFL live | Rapport frais complet ; modèles OpenRouter retenus sous 0,10 EUR/M ; un modèle gratuit exclu par ses mesures réelles |
| PLLM live | Sept politiques évaluées avec le catalogue frais ; les sept sont valides |
| OpenSpec après archive | `/home/devops/.local/npm/bin/openspec validate --all` et `--all --strict` : 10/10 chacun |
| Rapport d'archive | Six sections présentes ; totaux, UTF-8/LF et emplacement vérifiés |

Les mesures de performance sont celles des requêtes réelles dans les rapports
locaux ; aucun débit historique n'a été réutilisé. Aucun test Shell, frontend,
SQL ou migration n'est pertinent pour le périmètre Python/Markdown/JSON.

## 5. Accès web

Les catalogues OpenCode Go, OpenRouter et BCE ont été consultés par TFL. Les
investigations de contexte ont utilisé les pages officielles des créateurs de
GLM-5.1, Kimi K2.6, MiniMax M2.5 et Qwen3.6+/Qwen3.7-Max. Les preuves Medium
DeepSeek et OpenCode Go ont été revérifiées avant PLLM. Les empreintes et
conclusions détaillées sont dans les registres TFL/PLLM et le rapport TFL local.

Les trois premiers rapports TFL étaient provisoires pendant le renouvellement
des empreintes ; le rapport final a `investigation_status=complete`. Aucun
secret fournisseur n'est inclus dans les rapports distribués. Les appels
fournisseur sont réels et datés ; leurs tarifs et performances peuvent évoluer.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Comportement TFL/PLLM | Medium est accepté selon les sources ou réponse complète ; débit et seuils restent mesurés. Mode5 applique 0,10 EUR/M sans benchmark. |
| `AGENTS.md` | Inchangé ; règles SCM, OpenSpec, sécurité, encodage et tests appliquées. |
| `PROJECT.md` | Inchangé ; la version reste déclarée dans `VERSION` et les plugins publiés restent alignés. |
| `TECHNICAL.md` | Mis à jour pour le plafond OpenRouter et les exigences de preuve/fingerprinting. |
| `BUILD.md` | Mis à jour pour le plafond mode5 et les contrats TFL/PLLM. |
| `DEVOPS.md` | Inchangé ; Python 3.14.10 et OpenSpec 1.15.0 employés. |
| `README.md` | Version 0.7.20 et plafond OpenRouter 0,10 EUR/M. |
| `CHANGELOG.md` | Entrée Unreleased pour le changement et la release 0.7.20. |
| OpenSpec | Delta TFL/PLLM archivé ; validation globale standard et stricte 10/10 après correction de longueur. |
| Distributions | Skills, moteurs de preuve, commandes et manifestes vérifiés entre sources autonomes et embarquées. |

Le rapport ne vaut ni installation de la release dans un profil Codex, ni
publication distante. Ces étapes relèvent du commit et des publications SCM
conditionnelles après vérification des destinations configurées.
