# STATISTIQUES — fix-lm-openrouter-tilde-identifiers

Projet : Tools Codex (`tools-codex`), racine `/home/devops/datas/tools-codex`.
Archive : `2026-10-26-fix-lm-openrouter-tilde-identifiers`.
Date : 26 octobre 2026. Release locale : **0.7.7**.
Session SCM directe, périmètre autonome explicitement validé : correction
sans affaiblir LM, tests, incrément, archivage et statistiques, puis TFL réel.
Aucun pilotage CAB/OpenCode, sous-agent ou télémétrie de session pilotée.

## 1. Statistiques générales et décisions

| Mesure observée | Valeur |
|---|---:|
| Modules identiques LM/TFL/PLLM | 6 |
| Supports de release alignés sur 0.7.7 | 9 : VERSION, TOML, README et 6 manifestes |
| Nouveaux tests distincts | 5 |
| Suite LM ciblée | 25 cas, deux exécutions réussies |
| Suite finale Python 3.13.5 | 261 réussites, 0 échec, 0 erreur |
| Suite finale Python 3.14.10 | 261 mêmes cas réussis, 0 échec, 0 erreur |
| Total des deux suites finales | 522 réussites sur 522 exécutions |
| Test Git non exécuté | 1 par branche, non compté comme réussi |
| Compilations py_compile | 8 par branche, soit 16 réussites |
| Tâches de réalisation vérifiées | 8 sur 8 |
| OpenSpec ciblé strict préalable | 1 change valide |
| OpenSpec global avant archive | 10 éléments valides sur 10 |
| Archivages exécutés | 1, réussi |
| Exigences synchronisées | 2 ajoutées, 0 modifiée, 0 supprimée, 0 renommée |
| OpenSpec global après archive | 9 spécifications valides sur 9 |
| Chemins initiaux suivis par empreinte | 72 |
| Fichiers existants modifiés | 21, dont 2 spécifications synchronisées |
| Fichiers initiaux préservés | 51 |
| Nouveaux fichiers finaux | 7, présent rapport inclus |
| Fichiers supprimés | 0 |
| Total des chemins finaux du dépôt concernés | 28 |

Les empreintes couvrent les cadrages, versions, marketplace, spécifications,
tests et sources ciblées des six distributions. Ce périmètre n'est pas un
inventaire récursif du dépôt ni une inspection Git. Le déplacement du change
vers son archive est l'archivage demandé, compté une seule fois au chemin final.

Le seul `~` nouvellement admis précède un segment fournisseur suivi de `/`.
Il disparaît avec ce préfixe et ne contourne ni mimo-v2.5, ni les exclusions
personnalisées, ni muse-spark permanent. Les tests couvrent casse, suffixes,
idempotence, noms voisins, limite complète 256/257, emplacements invalides,
ASCII, corruption, doublons canoniques et persistance. TFL et PLLM préservent
les identifiants fournisseur autorisés et bloquent les interdits avant génération.

Modèle exact de service, tokens, coûts, cache, quotas et temps de génération
de l'agent : **N/A**, aucune télémétrie disponible. Le nombre de tests n'est
pas une mesure de qualité fonctionnelle d'un modèle fournisseur.

## 2. Types de messages et d'outils

| Domaine | Observation | Compteur exhaustif |
|---|---|---|
| Développeur | Demande de correction et validation explicite du périmètre SCM | N/A, historique non agrégé |
| Progression | Spécification, résultats ciblés, régression de version puis correction, archivage | N/A, historique non agrégé |
| Lectures | Sources, spécifications, cadrages, archives et tests ciblés | N/A, appels non totalisés |
| Éditions | apply_patch et Python locaux dans le périmètre validé | N/A, appels non totalisés |
| Vérifications | unittest, py_compile, audits de parité/version/encodage et OpenSpec | Sous-ensemble borné en section 4 |
| Git | Aucun appel après validation ; un git status de l'exploration précédente a été refusé pour propriété non reconnue | Aucune configuration modifiée |
| CAB, OpenCode et sous-agents | Non déclenchés | Non applicable |

La skill prompt a servi à résoudre SCM. La skill TFL régit la relance réelle
autorisée après archivage ; ses secrets restent dans les processus locaux.
Un premier essai de capture des sources en mémoire a dépassé la limite de
sortie de l'outil ; la capture par 72 empreintes a ensuite réussi, sans écriture.

## 3. Fichiers modifiés

Chemins relatifs à la racine indiquée en tête. Tous les fichiers existants
modifiés sont listés ci-dessous ; le test TCU ne change que son attente de
release de 0.7.6 à 0.7.7, démontrée incorrecte par la première suite globale.

| Chemin final | Opération |
|---|---|
| `CHANGELOG.md` | Modifié |
| `README.md` | Modifié |
| `TECHNICAL.md` | Modifié |
| `VERSION` | Modifié |
| `pyproject.toml` | Modifié |
| `plugins/cm/.codex-plugin/plugin.json` | Modifié |
| `plugins/lm/.codex-plugin/plugin.json` | Modifié |
| `plugins/pllm/.codex-plugin/plugin.json` | Modifié |
| `plugins/prompt/.codex-plugin/plugin.json` | Modifié |
| `plugins/tcu/.codex-plugin/plugin.json` | Modifié |
| `plugins/tfl/.codex-plugin/plugin.json` | Modifié |
| `skills/lm/scripts/model_blacklist.py` | Modifié |
| `plugins/lm/skills/lm/scripts/model_blacklist.py` | Modifié |
| `skills/tfl/scripts/model_blacklist.py` | Modifié |
| `plugins/tfl/skills/tfl/scripts/model_blacklist.py` | Modifié |
| `skills/pllm/scripts/model_blacklist.py` | Modifié |
| `plugins/pllm/skills/pllm/scripts/model_blacklist.py` | Modifié |
| `tests/test_lm_blacklist.py` | Modifié |
| `tests/test_tcu_update.py` | Modifié |
| `openspec/specs/lm-blacklist/spec.md` | Modifié |
| `openspec/specs/tfl-catalog/spec.md` | Modifié |
| `openspec/changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/.openspec.yaml` | Créé |
| `openspec/changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/proposal.md` | Créé |
| `openspec/changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/design.md` | Créé |
| `openspec/changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/tasks.md` | Créé |
| `openspec/changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/specs/lm-blacklist/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/specs/tfl-catalog/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/STATISTIQUES.md` | Créé |

Total dépôt : **21 fichiers modifiés + 7 créés = 28 chemins** ; aucun fichier
supprimé. Les deux rapports TFL usuels hors dépôt sont traités séparément
en section 5. Aucune source installée dans le profil n'est mise à jour.

## 4. Commandes

Sous-ensemble borné aux validations de code, audits initiaux et archivage,
hors lectures, éditions, diagnostics, vérifications du présent rapport et
relance TFL traitée séparément en section 5. Une suite ou un groupe de
compilations compte comme une exécution.

| Famille de commande | Exécutions | Réussies | Échouées |
|---|---:|---:|---:|
| OpenSpec ciblé strict préalable | 1 | 1 | 0 |
| Suites LM ciblées | 2 | 2 | 0 |
| Suites globales Python 3.13/3.14 | 3 | 2 | 1 |
| Groupes py_compile | 2 | 2 | 0 |
| Audit empreintes/parité/versions/UTF-8/LF avant archive | 1 | 1 | 0 |
| OpenSpec global strict avant/après archive | 2 | 2 | 0 |
| Archivage ciblé | 1 | 1 | 0 |
| Total borné | 12 | 11 | 1 |

Commandes et mécanismes réellement exécutés :

- `/usr/bin/python3.13 -B -W error::ResourceWarning -m unittest discover -s tests -p test_lm_blacklist.py` : deux succès de 25 cas.
- `/usr/bin/python3.13 -B -W error::ResourceWarning` et
  `/home/devops/python/current/bin/python3 -B -W error::ResourceWarning` :
  découverte unittest et sélection de tous les tests sauf le seul cas Git
  nommé ci-dessous, puis TextTestRunner. Succès finaux de 261 cas par branche.
- `py_compile.compile(..., cfile=..., doraise=True)` : les six modules et
  les deux fichiers de tests, sous les deux branches. Sorties temporaires
  sous tests/ nettoyées à la fin des gestionnaires de contexte.
- `/home/devops/.local/npm/bin/openspec validate fix-lm-openrouter-tilde-identifiers --strict`,
  `validate --all --strict` avant et après l'archive, puis
  `archive fix-lm-openrouter-tilde-identifiers --json --yes` entre ces deux
  contrôles globaux ; `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1` à chaque fois.
- Audit Python sans Git : neuf supports de release 0.7.7, six modules
  identiques, UTF-8/LF et comparaison des empreintes avec la liste autorisée.

Échec intermédiaire résolu : le test d'instantané réel TCU attendait encore
0.7.6. La première suite globale comptait 260 réussites et un échec ; son
attente a été alignée sur la nouvelle release demandée. Aucun test n'a été
supprimé, désactivé ou affaibli pour masquer une anomalie.

Le contrôle indépendant du débit publié a d'abord comparé avec une tolérance
plus fine que l'arrondi JSON à trois décimales. La vérification a été corrigée
pour comparer le calcul exact arrondi à cette précision ; aucune source de
mesure ni donnée fournisseur n'a été modifiée.

**Non exécuté** :
`test_tcu_update.TcuUpdateTests.test_command_sources_are_publishable_without_local_codex_files`,
car il inspecte Git, interdit par SCM sans demande explicite. Il est exclu
nominativement du lanceur, sans modification de son code ni faux succès.
**Non pertinents** : build web, tests navigateur et skill-creator, les
interfaces, paquets de skills et métadonnées de skill restant inchangés.

## 5. Accès web

Avant la relance TFL : aucun accès fournisseur réel pendant les tests,
qui utilisent des profils et des réponses contrôlés. Télémétrie OpenSpec
désactivée. Aucune publication GitHub, installation ou modification de secret.

Relance réelle TFL : **exécutée et réussie**, code de sortie **0**, après
archivage et contrôle du présent rapport. Commande depuis `skills/tfl` :
`/usr/bin/python3.13 -B scripts/test_fournisseur_llm.py --policy auto --output-dir /home/ade/.codex/skills/tfl/data`.
Rapports actualisés le **2026-10-26T03:37:52+01:00**, Europe/Paris.

| Catalogue | Modèles examinés | Retenus | Exclus |
|---|---:|---:|---:|
| OpenCode Go | 38 | 8 | 30 |
| OpenCode général | 85 | 3 | 82 |
| OpenRouter | 467 | 38 | 429 |
| Total | 590 | 49 | 541 |

Les 467 modèles OpenRouter ont été examinés sans liste fixe. Quatre
identifiants marqués sont retenus : `~deepseek/deepseek-v4-flash-latest`,
`~z-ai/glm-flash-latest`, `~anthropic/claude-haiku-latest` et
`~openai/gpt-luna-latest`. Les autres sont soumis aux mêmes filtres.
Le catalogue publié déclare mimo-v2.5 et l'exclusion permanente muse-spark ;
l'audit local confirme qu'aucun modèle retenu n'est interdit par cette politique.

| Source réelle | Usage |
|---|---|
| opencode.ai/zen/go/v1/models | Disponibilité Go |
| opencode.ai/docs/go/ | Tarifs Go courants, référence hors pointe |
| opencode.ai/zen/v1/models | Disponibilité du catalogue général |
| opencode.ai/v2/docs/console/models/ | Tarifs courants du catalogue général |
| models.dev/api.json | Métadonnées indépendantes opencode-go et opencode |
| openrouter.ai/api/v1/models | Catalogue complet, prix et capacités OpenRouter |
| Endpoints de génération OpenCode et OpenRouter | Qualification des gratuits autorisés uniquement |

Huit candidats gratuits audités ; six requêtes de génération tracées, deux
réussites complètes, deux refus HTTP 429 et deux refus HTTP 403. Deux autres
candidats sont exclus sur métadonnées HIGH/XHIGH avant requête. Aucun quota,
crédit ou solde n'a été consulté. Les payants n'ont pas été benchmarkés.

| Fournisseur | Modèle | TTFT (s) | Tokens/s | Raisonnement | Résultat |
|---|---|---:|---:|---|---|
| Go | beam-free | 2.1103 | 275.2910 | HIGH | Valide |
| OpenCode général | beam-free | N/A | N/A | HIGH | HTTP 429, réessai publié le 27/10/2026 à 01:00 Paris |
| OpenCode général | nemotron-3.5-super-vl-free | N/A | N/A | HIGH | HTTP 429, même échéance |
| OpenRouter | nvidia/nemotron-3-ultra-550b-a55b:free | 2.0471 | 83.8940 | HIGH | Valide |
| OpenRouter | nvidia/nemotron-3.5-lightning:free | N/A | N/A | HIGH demandé | HIGH/XHIGH non publiés ; aucune requête |
| OpenRouter | nvidia/nemotron-3.5-super-vl:free | N/A | N/A | HIGH demandé | HIGH/XHIGH non publiés ; aucune requête |
| OpenRouter | thinkingmachines/inkling-small:free | N/A | N/A | HIGH | HTTP 403 |
| OpenRouter | thinkingmachines/inkling:free | N/A | N/A | HIGH | HTTP 403 |

Les deux réussites respectent TTFT <30 s, débit >20 tokens/s, réponse complète,
contexte et gratuité vérifiés. Le protocole 8 applique request_average_v1 sur
request_total : 668 tokens Go / 2.426519859000109 s ; 365 tokens de réponse
OpenRouter / 4.350743718096055 s. Les mesures des refus restent indisponibles,
sans débit inventé, baisse de raisonnement ou qualification historique.
Ces résultats sont datés et liés aux accès utilisés, pas une indisponibilité
permanente des fournisseurs ni une qualification de qualité du code généré.

Les deux fichiers hors dépôt réellement actualisés sont
`/home/ade/.codex/skills/tfl/data/tfl.json` et
`/home/ade/.codex/skills/tfl/data/tfl.md` ; ils portent la même date de collecte.
Leurs empreintes ont changé. Les modules installés TFL et PLLM conservent
leurs empreintes 0.7.6 ; aucune source de profil ni secret n'a été modifié.
Total des chemins de livraison : 28 dans le dépôt et 2 rapports hors dépôt,
soit 30, sans compter les fichiers temporaires de test nettoyés.

## 6. Synthèse globale

| Document ou périmètre | Bilan et preuve |
|---|---|
| Projet réel | Grammaire minimale, six copies, intégrations et 0.7.7 validés par les tests et l'audit. |
| AGENTS.md | Inchangé, empreinte conservée ; règles applicables suffisantes. |
| PROJECT.md | Inchangé, empreinte conservée ; version issue de VERSION et catalogue de six plugins inchangés. |
| TECHNICAL.md | Mis à jour, section Liste noire LM : grammaire marquée, limite et identité canonique. |
| BUILD.md | Inchangé, empreinte conservée ; distribution, installation et stockage compatibles, aucune migration. |
| DEVOPS.md | Inchangé, empreinte conservée ; interpréteurs et OpenSpec existants utilisés, aucune dépendance ajoutée. |
| README.md | Mis à jour : release 0.7.7 et exemple d'exclusion avec préfixe marqué. |
| CHANGELOG.md | Deux nouvelles entrées Unreleased : correction, garanties et release locale ; historique conservé. |
| openspec/specs/ | Deux exigences ajoutées par l'archivage, neuf spécifications strictes valides. |
| Archive | Un archivage réussi, huit tâches prouvées ; rapport à six sections. |

Début de l'intervalle d'empreintes : 26/10/2026 03:30:09 Europe/Paris.
Durée totale SCM, temps actif de l'agent et temps d'attente : **N/A**, non
instrumentés. L'exploration et la validation humaine précèdent cet intervalle.

La correction locale, l'archivage et la relance TFL sont qualifiés sur leurs
preuves propres. Les installations utilisateur restent en 0.7.6 ;
une publication et une mise à jour distinctes seront nécessaires pour charger
les sources 0.7.7 lors d'invocations ultérieures du skill installé.

État : **TERMINÉ pour le périmètre SCM validé et la relance TFL**.
Les six échecs de qualification gratuite sont des exclusions attendues et
auditées ; ils n'ont pas empêché la publication du catalogue complet filtré.
Le seul contrôle de dépôt non exécuté reste le test Git nommé en section 4.
