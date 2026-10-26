# STATISTIQUES — allow-empty-tfl-provider-selections

Projet : Tools Codex. Session SCM directe. Release locale : 0.7.10.
Archive native unique : 2026-10-26-allow-empty-tfl-provider-selections.
Autorisation : périmètre SCM explicitement validé par le développeur, incluant
la spécification, l'implémentation, les tests, la version et l'archivage.

## 1. Statistiques générales

Une sélection vide issue d'une collecte valide ne bloque plus les autres
catalogues TFL. Cette règle vaut avant et après qualification gratuite,
y compris si les trois sélections sont vides. Les deux tableaux Go puis
OpenRouter restent présents ; un tableau vide affiche « Aucun modèle
admissible » avec une synthèse des exclusions. Le général reste dans le JSON.
Chaque section ajoute selection_status et exclusion_summary, sans modifier
models, les sources, compteurs, exclusions détaillées ou essais courants.
Les filtres et les vraies erreurs bloquantes restent conservés. Une publication
valide retourne zéro, sans qualification historique reprise.

Qualification finale : 305 tests distincts réussis sous Python 3.14.10,
puis 305 sous Python 3.13.5, soit 610 exécutions finales sans échec ni erreur.
Durées observées : respectivement 10,798 s et 9,590 s. Les contrôles ciblés
réussis comprennent 56 tests TFL et 17 tests du moteur gratuit ; ils recouvrent
la suite globale et ne sont pas ajoutés aux 610 exécutions finales.
Deux méthodes de test sont ajoutées, et les attentes existantes de sélection
vide sont adaptées à la décision validée. Les assertions de seuils et les
tests d'erreurs réelles restent conservés.

Syntaxe finale : sept fichiers Python compilés sur chaque branche, soit
14 compilations finales réussies. Les compilations intermédiaires ne sont
pas ajoutées à ce total. Deux générateurs et deux SKILL.md TFL identiques
octet pour octet. VERSION, pyproject.toml, README et six manifestes déclarent
0.7.10. Six tâches de réalisation et validation sont satisfaites ; les
postconditions archive native et présent rapport ont été réalisées ensuite.

OpenSpec avant archive : ciblé strict valide, global standard 11/11 et strict
11/11. Archive native : une exigence ajoutée, deux modifiées, aucune supprimée
ou renommée, specsUpdated=true. Après correction rédactionnelle d'une exigence
trop longue : global standard et strict 10/10, aucun change actif ciblé.

Durée globale de session, tokens, temps modèle/outils, cache et coûts de
conversation : N/A, télémétrie exhaustive non instrumentée. Aucune mesure
fournisseur réelle n'est déduite des tests hors ligne.

## 2. Messages et outils

Le prompt SCM est résolu par la skill prompt depuis le référentiel indiqué
dans DEVOPS.md. SCM est exécuté directement par Codex, sans sous-agent,
OpenCode, CAB ni compétence de statistiques des sessions pilotées.
Le développeur a validé la proposition avant les écritures OpenSpec et code.

Messages et appels d'outils exhaustifs : N/A, non agrégés. Les preuves sont
les résultats de commandes et les fichiers effectivement observés. Les
écritures de cette réalisation sont limitées au projet ; les tests utilisent
des temporaires contrôlés. Aucune dépendance n'est ajoutée.

Échecs intermédiaires corrigés : une exigence ajoutée trop longue avant code,
deux attentes de version LM/TCU encore à 0.7.9, puis une exigence modifiée trop
longue détectée dans la spécification synchronisée après archive. Cette
dernière a été condensée à sens constant dans le canon et le delta archivé,
puis revalidée ; aucun second archivage n'a été exécuté.

Le nouveau test de lecture PLLM a aussi isolé une limite préexistante des
prix flottants ; les détails et les prix de fixture exacts figurent en
section 6. Le moteur tarifaire n'a pas été modifié pour ce change.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Inventaire limité aux chemins écrits,
sans inspection de l'état Git sous SCM ni parcours récursif global du dépôt.

| Chemin | Opération |
|---|---|
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| pyproject.toml | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/lm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| skills/tfl/SKILL.md | Modifié |
| skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| plugins/tfl/skills/tfl/SKILL.md | Modifié |
| plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| tests/test_tfl_opencode_catalog.py | Modifié |
| tests/test_tfl_pricing.py | Modifié |
| tests/test_free_performance.py | Modifié |
| tests/test_lm_blacklist.py | Modifié, attente de version uniquement |
| tests/test_tcu_update.py | Modifié, attente de version uniquement |
| openspec/specs/tfl-catalog/spec.md | Synchronisé, puis rédaction condensée |
| openspec/changes/archive/2026-10-26-allow-empty-tfl-provider-selections/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-allow-empty-tfl-provider-selections/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-allow-empty-tfl-provider-selections/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-allow-empty-tfl-provider-selections/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-allow-empty-tfl-provider-selections/STATISTIQUES.md | Créé |

Totaux : 22 fichiers préexistants modifiés et 5 nouveaux chemins, soit
27 livrables. Les quatre artefacts du change sont comptés à leur destination
archivée, sans compter deux fois leur déplacement. Aucun fichier initial
supprimé. Les caches de compilation et temporaires de tests ne sont pas des
livrables et sont exclus de ce total.

Les empreintes des fichiers de réalisation sont contrôlées entre validation
finale et clôture ; les rapports data/tfl.json et data/tfl.md des deux
distributions n'ont pas été régénérés. Aucun état de profil utilisateur n'est
modifié. Cette revue ne qualifie pas les modifications antérieures ou
concurrentes ailleurs. Lignes ajoutées/supprimées globales : N/A, aucun diff
Git ni instantané textuel initial exhaustif utilisé pour cette mesure.

## 4. Commandes et validations

| Validation | État et résultat observé |
|---|---|
| Spécification préalable | openspec validate allow-empty-tfl-provider-selections --strict --no-interactive : exécutée et réussie avant code. |
| TFL ciblé | /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -p 'test_tfl*.py' -v : 56 tests exécutés et réussis. |
| Moteur gratuit ciblé | Même interpréteur, découverte test_free_performance.py : 17 tests exécutés et réussis. |
| Régression Python 3.14.10 | /home/devops/python/current/bin/python3 -B -m unittest discover -s tests : 305 tests exécutés et réussis. |
| Régression Python 3.13.5 | python3 -B -m unittest discover -s tests : 305 tests exécutés et réussis. |
| Syntaxe finale | python3 -m py_compile des sept fichiers modifiés sur chaque branche : exécutée et réussie, 14 compilations. |
| Parité et release | Comparaison octet pour octet TFL, lecture JSON/TOML et README : exécutées et réussies, 0.7.10 partout. |
| Encodage et secrets | UTF-8/LF, fins de fichiers et recherche de signatures reconnues de secrets sur les fichiers concernés : exécutés et réussis. |
| OpenSpec avant archive | Ciblé strict valide ; global standard et strict 11/11 : exécutés et réussis. |
| Éligibilité | openspec status --change allow-empty-tfl-provider-selections --json : artefacts complets ; six tâches satisfaites. |
| Archive native | openspec archive allow-empty-tfl-provider-selections --json --yes : code zéro, specsUpdated=true, un ajout et deux modifications. |
| OpenSpec après archive | Global standard et strict : exécutés et réussis, 10/10 après condensation rédactionnelle. |
| Rapport d'archive | Présence, six sections, UTF-8/LF, fichiers listés, totaux et concordance canon/delta contrôlés après écriture. |

Binaire OpenSpec : /home/devops/.local/npm/bin/openspec. Les tests couvrent
chaque catalogue vide et les trois vides, avant qualification (réponse vide
ou effort absent) et après qualification gratuite, les exclusions et le taux
BCE même sans ligne OpenRouter, ainsi que la lecture par les modes PLLM 1–5.
Les vraies erreurs restent couvertes par les régressions de sources, prix,
modalités, routage et taux. Aucun seuil n'est affaibli.

Lint et types : non disponibles, aucun outil configuré dans pyproject.toml.
Construction frontend, ShellCheck, migrations : non pertinents pour ce change.
Qualification fournisseur réelle, installation dans un nouveau profil,
TCU, hook, activation du planning et publication distante : non exécutées.
Commit, préparation de commit, push, tag et création de branche : non exécutés.

## 5. Accès web

Aucun appel fournisseur, recherche web, benchmark réel, contrôle de quota,
crédit ou solde exécuté pendant cette réalisation SCM. Le diagnostic TFL
antérieur à SCM ne qualifie pas les sources 0.7.10. Les tests injectent des
catalogues, métadonnées, taux, réponses et accès trousseau fictifs.

Aucun secret n'est ajouté, créé ou transmis dans les rapports. Les futurs
appels TFL conservent les sources officielles et les accès existants.
Latence, débit, disponibilité et coût fournisseur de cette livraison : N/A,
qualification hors ligne sans appel de génération réel.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Projet réel | Sélections vides explicites, autres catalogues publiés ; 305 tests réussis sur chaque branche. |
| AGENTS.md | Inchangé ; règles de sécurité, autorisations et archivage toujours applicables. |
| PROJECT.md | Inchangé ; catalogue TFL Go/OpenRouter et général JSON toujours exact, sans règle imposant une sélection non vide. |
| TECHNICAL.md | Mis à jour, sections qualification, validation et contrat 0.7.10 : états, synthèses, erreurs réelles et limite du planning. |
| BUILD.md | Mis à jour, qualification et contrat 0.7.10 ; distribution locale distincte de l'installation et du planning réels. |
| DEVOPS.md | Inchangé ; binaires Python/OpenSpec et référentiel de prompts applicables. Python 3.13.5 utilisé en complément pour la compatibilité. |
| README.md | Mis à jour, release 0.7.10 et comportement vide explicite, y compris la limite du planning. |
| CHANGELOG.md | Deux entrées Unreleased ajoutées pour le comportement et la release ; historique antérieur préservé. |
| OpenSpec | tfl-catalog synchronisé ; delta archivé cohérent avec le canon ; validation stricte globale 10/10. |
| Skills et code TFL | Les deux copies restent identiques ; états JSON et synthèses sans réintégration de modèles exclus. |

Les filtres HIGH/XHIGH, contexte, prix, modalités et LM, les huit colonnes,
les devises, les routes, les seuils gratuits, le protocole 8 et les interfaces
CLI restent conservés. Aucun changement des sélections PLLM ni du planning.

Limites explicites : le planning continue d'exiger trois listes models non
vides avant PLLM. Une publication manuelle valide avec une section vide
n'autorise donc pas cette étape planifiée. Les installations utilisateur
restent à leur version antérieure jusqu'à une mise à jour distincte autorisée.

Une incohérence numérique préexistante reste hors périmètre : les prix de
fixture 0,0000001 et 0,0000002 USD/token peuvent devenir des flottants
USD/M légèrement différents des valeurs natives exactes, que PLLM rejette
comme contradictoires. Le test des sections vides utilise 0,000000125 et
0,00000025, exactement représentables après conversion, pour isoler son
critère. Aucun assouplissement du contrôle ni correctif tarifaire n'est inclus.

La réalisation locale est validée dans le périmètre SCM approuvé. Elle ne
prouve ni installation, ni publication distante, ni résultat fournisseur réel.
