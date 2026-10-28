# STATISTIQUES — split-pllm-free-modes

Projet : Tools Codex. Release locale : 0.7.1. Session SCM directe.
Le développeur a validé le périmètre puis précisé les seuils stricts des
gratuits 3/4 : TTFT <30 s et débit >20 tokens/s, le 25 octobre 2026.
Rapport produit après l'archive native unique, sans télémétrie de pilotage.

## 1. Statistiques générales

Six politiques de priorités 1 à 6. Les modes 1/2 sont exclusivement payants Go :
un quota épuisé les rend rouges et invalides, y compris après une première
réussite ; aucun gratuit n'est essayé dans ces modes. Les modes 3/4 comparent
les gratuits vérifiés Go puis OpenCode général avec les comptes de 1/2
respectivement. Aucun quota ni solde n'est consulté en 3/4, même entre paliers ;
quotas=null et quota_status=not_applicable. Les contrôles effectivement
épuisés portent exhausted, les contrôles indisponibles unavailable.

Les gratuits 3/4 exigent contexte ≥1M, réponse complète, comptage fiable,
TTFT <30 s et débit >20 tokens/s. Les modes 1/2/5/6 gardent <90 s et >15.
L'ancien OpenRouter devient 5 avec son repli gratuit conditionné au crédit ;
l'ancien DeepSeek direct devient 6. Les références de trousseau restent
inchangées. Filtres TFL, Low, transports, diagnostics HTTP et paliers sont
préservés. Le classement interne garde débit maximal, TTFT minimal, ordre TFL.
active s'arrête après classement du premier mode valide et reste silencieux.

Les historiques et mémoires de schéma 1 sont adaptés en mémoire au schéma 2 :
anciens 3/4 vers 5/6, nouveaux 3/4 initialisés sans succès ni apprentissage.
L'historique n'hérite pas de sélection ou d'évaluation courante. Les fichiers
invalides restent préservés. Aucun historique réel utilisateur n'a été modifié
pendant cette livraison. L'ancien évaluateur ne lit pas le schéma 2 ; préserver
ses données avant un retour de version. Les anciens forçages OpenRouter
31–33 deviennent 51–53 ; 31–33 et 41–43 ciblent la liste gratuite admissible.

Dernières suites complètes : 191 tests sous Python 3.13.5 et 191 sous
Python 3.14.9, soit 382 exécutions finales pour 191 tests distincts. Treize
nouveaux tests des six modes, avec sous-cas pour les deux distributions.
Les 178 tests antérieurs sont conservés ; les attentes et fixtures liées
aux quatre anciens modes et aux replis de 1/2 sont adaptées au comportement
explicitement validé, sans désactivation. Les répétitions ne s'additionnent
pas au total distinct.

Syntaxe : 19 fichiers compilés par branche, soit 38 compilations finales.
Neuf scripts importés par branche, soit 18 imports, et Europe/Paris résolu.
Deux SKILL.md validés. Quatorze tâches préparatoires cochées ; les obligations
d'archive et de rapport sont distinctes et restent impératives jusqu'à leur
vérification effective.

Onze exigences modifiées et synchronisées avant archive, aucune exigence
ajoutée, supprimée ou renommée ; scénarios existants conservés et adaptés.
Global standard et strict : 9/9 avant archive, 8/8 après archive, sans
avertissement final. Archive native : specsUpdated=false, puisque les onze
blocs étaient déjà synchronisés ; aucun nouveau delta n'était à appliquer.

Durée totale, temps modèle/outils, tokens, cache, coûts, quotas consommés
et statistiques hebdomadaires : N/A, télémétrie non instrumentée.

## 2. Messages et outils

Session directe SCM, référentiel résolu depuis DEVOPS.md avec le skill prompt.
Le skill skill-creator a servi à vérifier les instructions PLLM. Aucun
sous-agent, pilotage OpenCode/CAB ou skill de statistiques pilotées.
Messages et appels exhaustifs : N/A, non agrégés.

Les tests simulent réseau, trousseau, quotas, flux et mesures. Les temporaires
de tests et compilation restent sous tests puis sont nettoyés. Les refus
400/401/403/429 sont testés sans corps privé ni secret publié ; aucune requête
fournisseur réelle ni lecture de clé par l'agent. Aucune inspection ou opération
Git, installation, mise à jour TCU, bascule de fournisseur ou modification
d'agent/service OpenCode. L'identité non secrète du projet a été extraite
localement selon l'exception du prompt, sans afficher les autres variables.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins finaux relatifs :

| Chemin | Opération |
|---|---|
| .codex/commands/pllm.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| openspec/specs/pllm-evaluation/spec.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| pyproject.toml | Modifié |
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| tests/test_extension_qualification.py | Modifié |
| tests/test_pllm_free_fallback.py | Modifié |
| tests/test_pllm_six_modes.py | Créé |
| openspec/changes/archive/2026-10-25-split-pllm-free-modes/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-split-pllm-free-modes/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-split-pllm-free-modes/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-split-pllm-free-modes/specs/pllm-evaluation/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-split-pllm-free-modes/STATISTIQUES.md | Créé après archive |

Totaux : 19 fichiers initiaux modifiés + six nouveaux chemins = 25 chemins
livrés. Aucun fichier initial supprimé ; les quatre artefacts du change
déplacés par l'archive sont comptés une seule fois à leur destination finale.

Contrôle ciblé de 40 empreintes initiales : 19 modifications prévues,
21 fichiers inchangés, aucun chemin initial manquant. Le nouveau test et
les cinq fichiers finaux de l'archive sont comptés séparément.
AGENTS.md, PROJECT.md, DEVOPS.md, CM et les références API conservent leurs
empreintes. Ce contrôle ne constitue pas un inventaire de l'état Git ni un
audit récursif global du dépôt. Les sources et données installées dans les
profils utilisateur n'ont pas été actualisées.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie après correction : openspec validate split-pllm-free-modes --strict. |
| Python 3.14.9 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 191 tests. |
| Python 3.13.5 | Exécutée et réussie : /usr/bin/python3.13 -B -m unittest discover -s tests -q ; 191 tests. |
| Syntaxe et imports | Exécutée et réussie : py_compile avec cfile temporaire sous tests ; 19 compilations, neuf imports de scripts et fuseau résolu par branche. |
| Skills | Exécutée et réussie : quick_validate.py sur skills/pllm et plugins/pllm/skills/pllm. |
| Release et parité | Exécutée et réussie : VERSION, pyproject.toml, README et cinq manifestes à 0.7.1 ; scripts, SKILL.md et référence API identiques. |
| Encodage avant archive | Exécutée et réussie : 24 livrables UTF-8/LF, sans BOM. |
| Périmètre | Exécutée et réussie : 40 empreintes initiales, 19 modifications prévues et 21 fichiers inchangés ; aucune suppression initiale. |
| OpenSpec avant archive | Exécutée et réussie : ciblé strict puis global standard 9/9 et strict 9/9, sans avertissement final. |
| Statut du change | Exécutée et réussie : openspec status --change split-pllm-free-modes --json ; isComplete=true pour les artefacts préparatoires. |
| Archive unique | Exécutée et réussie : openspec archive split-pllm-free-modes --json --yes ; 2026-10-25-split-pllm-free-modes, specsUpdated=false car synchronisation déjà réalisée. |
| OpenSpec après archive | Exécutée et réussie : openspec validate --all et --all --strict ; 8/8 dans les deux cas, sans avertissement. |
| Rapport final | Exécutée et réussie : six sections, 25 chemins uniques présents, totaux 19 + 6, quatorze tâches, UTF-8/LF sans BOM, onze blocs identiques et aucun change actif. |

Toutes les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
Les compilations et imports utilisent explicitement chaque interpréteur.
Le contrôle de clôture a vérifié les six sections du rapport, 25 chemins uniques
existants, 19 + 6, les quatorze tâches préparatoires, UTF-8/LF sans BOM, la
parité des onze blocs normatifs et l'absence de change actif.

Échecs intermédiaires corrigés dans le périmètre : premier delta rejeté pour
scénarios existants omis ; attente incorrecte de classement sur un mode forcé
qui ne teste que son premier candidat. Cette dernière erreur apparaissait deux
fois à cause de la découverte d'une classe importée ; l'import a été corrigé.
Deux avertissements de longueur OpenSpec ont été supprimés en déplaçant les
détails dans les scénarios. Aucun échec ni avertissement final restant.

Non exécutés : nouveaux benchmarks authentifiés, installation dans une nouvelle
session Codex, publication distante, mise à jour TCU et adoption OpenCode.
Non pertinents : frontend, ShellCheck et migration système. Aucun outil de
lint/types supplémentaire n'est configuré dans pyproject.toml.

## 5. Accès web

Aucun accès web réel pendant ce SCM. Tous les services externes sont simulés
pour les tests ; les URL documentées ne constituent pas des appels effectués.
Temps et volumes web : N/A, aucune collecte réelle instrumentée.
Les performances fournisseur actuelles ne sont pas qualifiées par cette suite.

## 6. Synthèse et cohérence documentaire

L'évolution 0.7.1 est livrée localement et archivée. La séparation payant/gratuit,
les comptes, les six priorités, les seuils 3/4, les quotas applicables, le
classement, les erreurs, les paliers, la mémoire, les forçages et la publication
restent couverts par les suites sur les deux branches Python.

| Élément | État et preuve |
|---|---|
| Projet réel | Six modes et seuils validés par 191 tests sur chacune des deux branches. |
| AGENTS.md | Inchangé, empreinte conservée ; règles de périmètre, secrets et OpenSpec appliquées. |
| PROJECT.md | Inchangé, empreinte conservée ; Organisation, Catalogue actuel et Version de release restent exacts. |
| TECHNICAL.md | Mis à jour ; six modes, ressources, seuils, schéma 2 et qualification. |
| BUILD.md | Mis à jour ; prérequis PLLM, adaptation des historiques et retour de version. |
| DEVOPS.md | Inchangé, empreinte conservée ; chemins Python/OpenSpec et référentiel de prompts utilisés. |
| README.md | Mis à jour ; tableau des six modes, version 0.7.1, migration et forçages. |
| CHANGELOG.md | Mis à jour dans Unreleased ; comportement, seuils et version locale, sans date de publication inventée. |
| openspec/specs | Onze exigences pllm-evaluation synchronisées ; standard et strict 8/8 après archive. |

ORCHESTRATED_CODING.md est non applicable à cette SCM directe.
L'absence de contrôle de quota des gratuits ne promet pas l'absence de limites
fournisseur. Livraison locale, installation, publication et disponibilité
fournisseur restent distinctes. Aucun blocage final connu.
État : TERMINÉ pour le périmètre local validé, son archive unique et son rapport.

