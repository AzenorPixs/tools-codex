# STATISTIQUES — prioritize-paid-model-price

Projet : Tools Codex. Session SCM directe. Release locale : 0.7.4.
Archive native unique du 26 octobre 2026. Aucun pilotage OpenCode/CAB ni
compétence de statistiques de session pilotée n'a été utilisé.

## 1. Statistiques générales

Le développeur a demandé le prix prioritaire après qualification des payants,
puis précisé que les gratuits restent classés par performances. Après la
proposition SCM, il a demandé immédiatement une nouvelle évaluation réelle
avec cette règle, puis l'incrément des briques Tools Codex.

Payants des modes 1/2 et de la catégorie payante de 5 : coût moyen TFL
croissant, puis débit décroissant, TTFT croissant et ordre TFL stable à prix
égal. Gratuits 3/4 et repli gratuit de 5 : débit décroissant, TTFT croissant
puis ordre TFL stable. Mode6 garde son candidat direct unique. Les tests,
contrôles de ressources, seuils, HIGH/XHIGH, forçages, protocole 8 et priorités
entre les six politiques restent préservés.

Qualification finale : 230 tests sous Python 3.14.10 et 230 sous Python
3.13.5, soit 460 exécutions finales pour 230 tests distincts. Huit tests sont
ajoutés, avec sous-cas sur les deux distributions. Une fixture de seuils
existante reçoit les nouveaux champs de candidat, sans modification des
assertions de seuils. Quatre fichiers Python sont compilés par branche,
soit huit compilations ciblées. Deux paires PLLM (script et SKILL.md) sont
identiques octet pour octet.

L'évaluation réelle a terminé avec le code 0 et publié à
2026-10-26T00:44:49+01:00. Elle a examiné 52 candidats : 27 valides et
25 invalides. Les preuves tracent 79 tentatives de benchmark, dont 27
complètes et 52 en échec. Ces totaux excluent les requêtes de métadonnées
et contrôles de ressources, non instrumentées exhaustivement.

Mode1 : quota hebdomadaire épuisé, sans génération. Mode2 sélectionne
muse-spark-1.3-contributor à 0,15 USD/M, TTFT 5,533 s et 140,540 tokens/s.
MiMo-v2.6-flash est également valide, plus rapide (191,437 tokens/s) mais plus
cher (0,21 USD/M) : il ne passe pas devant Muse. Modes 3/4 : beam-free valide,
sans contrôle de quota. Mode5 : ~z-ai/glm-flash-latest, le moins cher de ses
16 payants qualifiés. Mode6 : deepseek-v4-flash valide.

Une ancienne règle OpenSpec est retirée et quatre exigences la remplacent.
Quinze tâches sont clôturées. OpenSpec avant archive : ciblé strict valide,
global standard et strict 9/9. Après archive : global standard et strict 8/8.

Durée totale de session, temps modèle/outils, tokens de conversation, cache,
coûts exacts et consommation différentielle des comptes : N/A, télémétrie
non instrumentée. Les crédits et quotas courants du rapport ne constituent
pas un calcul du coût total de la session.

## 2. Messages et outils

Session directe résolue via le skill prompt depuis le DEVOPS du projet.
Aucun sous-agent, orchestration CAB, changement d'agent OpenCode ou collecte
de télémétrie pilotée. Messages et appels d'outils exhaustifs : N/A, non agrégés.

Les tests hors ligne isolent le réseau et le trousseau. Leurs temporaires et
ceux de compilation sont créés sous tests puis nettoyés. Les contrôles de
classement réel lisent seulement les preuves publiées et ne relancent aucun
benchmark. Les secrets de génération restent confinés au processus existant,
hors arguments, contexte du modèle et rapports.

L'évaluation a été lancée avec le script corrigé du dépôt, en Python 3.14.10,
et le catalogue TFL existant /home/ade/.codex/skills/tfl/data/tfl.json, daté du
26 octobre 2026 à 00:06:29+01:00. Aucun nouveau TFL ou TCU n'est déclenché.
Le profil installé de Codex reste distinct des sources et n'est pas actualisé.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins relatifs finaux :

| Chemin | Opération |
|---|---|
| .codex/commands/pllm.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| pyproject.toml | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| tests/test_pllm_ttft.py | Fixture adaptée |
| openspec/specs/pllm-evaluation/spec.md | Synchronisé par l'archive |
| tests/test_pllm_price_priority.py | Créé |
| openspec/changes/archive/2026-10-26-prioritize-paid-model-price/.openspec.yaml | Créé puis archivé |
| openspec/changes/archive/2026-10-26-prioritize-paid-model-price/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-prioritize-paid-model-price/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-prioritize-paid-model-price/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-prioritize-paid-model-price/specs/pllm-evaluation/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-26-prioritize-paid-model-price/STATISTIQUES.md | Créé après archive |

Totaux des livrables source/documentation : 18 chemins préexistants modifiés
et sept nouveaux chemins, soit 25. Les cinq fichiers déplacés par l'archive
ne sont comptés qu'à leur destination finale. Aucune suppression de fichier
initial n'est réalisée.

Trois fichiers générés sont actualisés séparément :
skills/pllm/data/pllm-current.json, skills/pllm/data/pllm-current.md et
skills/pllm/data/pllm-performance-memory.json. Ils ne sont pas des sources
à publier ni à ajouter à Git. Aucun fichier de données du plugin ou du profil
Codex installé n'est remplacé.

Le contrôle est ciblé sur les chemins touchés par cette session, sans
inspection Git ni inventaire récursif global. La liste n'est pas une preuve
d'absence de modifications antérieures ou concurrentes ailleurs dans le dépôt.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate prioritize-paid-model-price --strict. |
| Python 3.14.10 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests ; 230 tests. |
| Python 3.13.5 | Exécutée et réussie : python3 -B -m unittest discover -s tests ; 230 tests. |
| Syntaxe | Exécutée et réussie : py_compile des deux scripts PLLM et deux fichiers de tests modifiés, sur chaque branche. |
| Parité | Exécutée et réussie : script et SKILL.md PLLM identiques dans les deux distributions. |
| Release | Exécutée et réussie : VERSION, pyproject.toml, README, BUILD et cinq manifestes à 0.7.4 ; JSON marketplace valide. |
| OpenSpec avant archive | Exécutée et réussie : ciblé strict et global standard/strict 9/9. |
| Évaluation réelle | Exécutée et réussie : /home/devops/python/current/bin/python3 -B scripts/evaluate.py --tfl-catalog /home/ade/.codex/skills/tfl/data/tfl.json, depuis skills/pllm ; code 0. |
| Preuves publiées | Exécutée et réussie : gagnants recalculés indépendamment par catégorie, six priorités, quotas non applicables 3/4, huit colonnes, six politiques actuelles, champs privés interdits absents. |
| Préparation | Exécutée et réussie : openspec status --change prioritize-paid-model-price --json ; artefacts complets. |
| Archive native unique | Exécutée et réussie : openspec archive prioritize-paid-model-price --json --yes ; specsUpdated=true, quatre exigences ajoutées et une retirée. |
| OpenSpec après archive | Exécutée et réussie : openspec validate --all et --all --strict ; 8/8 chacun. |

OpenSpec utilise /home/devops/.local/npm/bin/openspec. L'archive est unique :
2026-10-26-prioritize-paid-model-price. Aucun Git, commit, push, tag ou release
distante n'est exécuté ni préparé. Aucun nouveau langage, dépendance ou outil
de lint/types n'est ajouté ; pyproject.toml n'en configure aucun.

Échecs intermédiaires corrigés : avertissement d'exigence normative trop
longue, scindée avant le code ; dix sous-cas de seuils échoués parce que leur
fixture simulée ne contenait pas encore les champs prix/catégorie du candidat.
Les assertions de ces seuils sont préservées et passent après adaptation.
L'import initial d'une classe de tests a aussi été remplacé par un import de
module afin d'éviter une collecte en double. Les 460 exécutions finales ne
comptent pas ces essais intermédiaires.

Installation et chargement de 0.7.4 dans une nouvelle session Codex : non
exécutés. Publication distante et adoption OpenCode : non exécutées.
Frontend, ShellCheck et migrations système : non pertinents pour ce périmètre.

## 5. Accès web

L'évaluateur utilise les endpoints HTTPS existants des fournisseurs, avec
authentification injectée en mémoire : OpenCode pour quotas et générations,
OpenRouter pour crédits, métadonnées et générations, DeepSeek pour solde et
génération, service de taux de change pour les couleurs des soldes.

Les routes proviennent du catalogue TFL daté et du contrat direct DeepSeek
existant. Les 79 tentatives de benchmark sont comptées depuis les preuves
JSON, sans inclure les appels de contrôle ni les métadonnées. Total exhaustif
des requêtes HTTP, volumes et temps web : N/A, non instrumentés. Aucun outil
de recherche web ni lecture de configuration privée n'a été nécessaire.
Le catalogue tarifaire TFL n'est pas rafraîchi pendant cette invocation.

Les erreurs d'accès et limites sont des constats datés du compte utilisé,
pas une indisponibilité permanente des modèles. Aucune clé, donnée de compte,
session, réponse de code généré ou corps d'erreur brut n'est reproduit ici.

## 6. Synthèse et cohérence documentaire

La règle livrée donne la priorité au prix des payants qualifiés et conserve
les performances pour les gratuits. L'évaluation réelle confirme le changement
attendu : Muse Spark est retenu malgré un débit inférieur à MiMo, grâce à son
prix de référence inférieur. Les seuils d'admissibilité ne sont pas assouplis.

| Élément | État et preuve |
|---|---|
| Projet réel | 230 tests réussis sur chaque branche ; évaluation complète publiée avec classement corrigé. |
| AGENTS.md | Inchangé par cette session ; sécurité, périmètre et archivage respectés. |
| PROJECT.md | Inchangé par cette session ; catalogue, organisation et responsabilités restent exacts. |
| TECHNICAL.md | Mis à jour ; classement par catégorie, prix tracés et tests correspondants. |
| BUILD.md | Mis à jour ; sélection par prix et cohérence de la release 0.7.4. |
| DEVOPS.md | Inchangé par cette session ; chemins Python, OpenSpec et prompts utilisés. |
| README.md | Mis à jour ; release 0.7.4 et règle prix/performance. |
| CHANGELOG.md | Mis à jour dans Unreleased ; comportement, limites d'installation et incrément demandés. |
| openspec/specs | pllm-evaluation synchronisée ; validation globale standard/stricte 8/8 après archive. |

ORCHESTRATED_CODING.md et CAB sont non applicables à cette session SCM directe.
La qualification de vitesse ne mesure pas la qualité fonctionnelle du code.
Le classement utilise les prix du catalogue TFL daté ; les mesures réelles
restent un instantané, sans garantie de disponibilité future.

Les sources locales 0.7.4, l'évaluation demandée et l'archive sont finalisées.
Les fichiers du profil Codex installé restent à livrer séparément ; une future
invocation de cette ancienne copie ne bénéficie pas automatiquement du correctif.
Le contrôle de clôture vérifie les six sections, UTF-8/LF sans BOM, 25 chemins
source uniques présents, quinze tâches cochées et absence du change actif ciblé.
