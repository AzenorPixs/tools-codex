# STATISTIQUES — manage-prompt-component

Projet : Tools Codex. Release locale : 0.4.1. Session SCM directe.

## 1. Statistiques générales

TCU gère prompt comme composant : plugin, skill embarqué et commande source.
CM, PLLM, TFL, TCU et prompt partagent la version 0.4.1.

Les dernières suites complètes comptent 77 tests chacune : 77 réussites sur
Python 3.13.5 et 77 sur Python 3.14.8, soit 154 réussites sur 154. La suite
TCU ciblée compte 38 tests réussis, dont 13 nouveaux. Les trois attentes de
blocage global adaptées à l'indépendance des canaux conservent les assertions
de conflit et de conservation. Aucun test n'est supprimé ou désactivé.

Trois fichiers compilés, quatre skills validés, un paquet isolé sur deux
Python, cinq versions alignées et 24 sources réelles validées en mémoire.
OpenSpec : neuf éléments valides avant archive, huit specs après ; quatre
exigences modifiées et trois ajoutées, aucune supprimée ou renommée.
Dix tâches sur dix terminées. Les sept exigences sont identiques aux deltas.

Relevé initial : 2026-10-19 15:26:03 UTC. Rapport préparé : 2026-10-19 15:51:25 UTC.
Intervalle : 0:25:22. Cette mesure n'inclut pas les échanges antérieurs.
Modèle exact, tokens, coûts, cache, quotas et temps de génération : N/A,
télémétrie non instrumentée. Aucune valeur n'est estimée.

## 2. Messages et outils

Messages et appels exhaustifs : N/A, non agrégés. Éditions, tests et contrôles
locaux via Python, shell et OpenSpec. Aucun sous-agent, pilotage OpenCode/CAB,
skill de statistiques pilotées ou commande Git.

Le périmètre validé inclut l'installation future ciblée de prompt par TCU,
les spécifications, documents, versions, tests et archivage. Les essais de CLI
et réseau sont simulés dans des profils temporaires sous tests. Aucun profil
réel, lien existant, service ou référentiel externe n'est modifié.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins relatifs ci-dessous.
Contrôle ciblé : 149 fichiers initiaux comparés par SHA-256, sans Git.

| Chemin | Opération |
|---|---|
| .codex/commands/TCU.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| PROJECT.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| openspec/specs/extension-distribution/spec.md | Modifié |
| openspec/specs/tools-codex-update/spec.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/cm/skills/cm/SKILL.md | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/skills/tcu/SKILL.md | Modifié |
| plugins/tcu/skills/tcu/scripts/update.py | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| pyproject.toml | Modifié |
| skills/cm/SKILL.md | Modifié |
| skills/tcu/SKILL.md | Modifié |
| skills/tcu/scripts/update.py | Modifié |
| tests/test_tcu_update.py | Modifié |
| .codex/commands/cm.md | Créé |
| openspec/changes/archive/2026-10-19-manage-prompt-component/.openspec.yaml | Créé puis archivé |
| openspec/changes/archive/2026-10-19-manage-prompt-component/STATISTIQUES.md | Créé |
| openspec/changes/archive/2026-10-19-manage-prompt-component/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-manage-prompt-component/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-manage-prompt-component/specs/extension-distribution/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-manage-prompt-component/specs/tools-codex-update/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-manage-prompt-component/tasks.md | Créé puis archivé |

Totaux : 22 fichiers initiaux modifiés, 8 nouveaux chemins finaux, aucun
fichier initial supprimé ; 30 chemins livrés. Les six artefacts créés puis
déplacés dans l'archive sont comptés une seule fois. Les temporaires sont
nettoyés. Les 94 fichiers d'archives antérieures, AGENTS.md, DEVOPS.md,
ORCHESTRATED_CODING.md et le catalogue marketplace gardent leur empreinte.
Les liens existants et le référentiel externe des prompts sont préservés.

## 4. Commandes et validations

Les validations suivantes sont exécutées et réussies :

| Validation | Commande ou preuve |
|---|---|
| TCU ciblé | /usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -p test_tcu_update.py -v : 38 tests OK. |
| Suite Python 3.13 | /usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q : 77 tests OK. |
| Suite Python 3.14 | /home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q : 77 tests OK. |
| Syntaxe | py_compile sur les deux moteurs TCU et tests/test_tcu_update.py ; sorties temporaires nettoyées. |
| Format des skills | quick_validate.py du skill-creator : quatre copies CM/TCU valides. |
| Paquet isolé | scripts/update.py --help depuis une copie du plugin, sur les deux Python. |
| Sources et release | ZIP de 24 sources réelles validé en mémoire ; cinq plugins, wrappers CM/prompt, versions 0.4.1 et parité. |
| Catalogue | Une seule entrée prompt dans chaque copie CM ; wrapper cm.md déléguant au skill. |
| Normatif | Sept exigences avec mots-clés RFC 2119 en MAJUSCULE et corps de 500 caractères au plus. |
| OpenSpec avant code | openspec validate manage-prompt-component --strict : valide. |
| OpenSpec complet | openspec validate --all --strict : 9/9 avant archivage puis 8/8 après. |
| Statut ciblé | openspec status --change manage-prompt-component --json : isComplete=true. |
| Archive | openspec archive manage-prompt-component --json --yes : archive unique, trois ajouts et quatre modifications synchronisés. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec,
OPENSPEC_TELEMETRY=0 et DO_NOT_TRACK=1. Le Purpose de tools-codex-update est
aligné après synchronisation sur la gestion et l'installation ciblée.

Le premier contrôle de comparaison des exigences a échoué : son expression
régulière capturait les titres sur plusieurs lignes. Le contrôle corrigé
confirme les sept exigences identiques, sans modifier les specs ni réarchiver.
UTF-8/LF et un contrôle ciblé de marqueur de clé privée sont vérifiés sur les
fichiers concernés ; cela ne constitue pas une analyse des secrets exclus.

Non exécutées : publication, mise à jour d'un profil réel et invocation dans
une nouvelle session Codex. Ces opérations sont distinctes de la livraison.
Non pertinents : build frontend et shellcheck, aucun code frontend ou shell
modifié. Aucun lint supplémentaire n'est configuré pour ce périmètre.
Aucun échec non résolu ou blocage connu dans le périmètre livré.

## 5. Accès web

Aucun accès web ou réseau réel pendant cette implémentation et qualification.
Les requêtes GitHub et opérations CLI sont simulées ; le SHA de fixture n'est
pas un SHA publié. Aucun téléchargement, publication ou rafraîchissement de
marketplace réelle n'est déduit des tests. Volumes et temps réseau : N/A,
aucun transfert réalisé.

## 6. Synthèse et cohérence documentaire

Seul prompt absent est installé automatiquement par TCU. Son plugin reste
géré par le CLI ; son skill et son résolveur sont vérifiés, puis le wrapper
est déployé avec provenance dédiée. Les copies autonomes présentes restent
mises à jour ; aucun doublon autonome absent n'est créé. Les autres briques
absentes restent absentes. Un conflit local préserve sa cible et ne bloque
pas les opérations indépendantes, avec bilan partiel et code non nul.
Une erreur de source, sauvegarde ou cohérence CLI bloque les opérations non
sûres. Aucune atomicité globale de la marketplace n'est promise.

| Élément | État et preuve |
|---|---|
| Projet réel | Moteurs et skills CM/TCU synchronisés ; fixtures des trois ressources et des conflits indépendants réussies. |
| AGENTS.md | Inchangé, empreinte vérifiée ; règles SCM, liens, secrets et périmètre applicables respectées. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel et rôle TCU décrivent /cm, prompt et les opérations indépendantes. |
| TECHNICAL.md | Mis à jour : Arborescence, catalogue CM et Mise à jour TCU précisent cibles, reçus et vérifications. |
| BUILD.md | Mis à jour : Skill catalogue cm et Mise à jour décrivent usages, déploiement ciblé et limites. |
| DEVOPS.md | Inchangé, empreinte vérifiée ; environnement et référentiel exclusif de prompts restent applicables. |
| README.md | Mis à jour : version 0.4.1 et comportement CM/TCU/prompt livré. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased pour cette évolution, aucune date de publication inventée. |
| openspec/specs | Deux specs synchronisées ; sept exigences identiques, Purpose TCU aligné, validation stricte 8/8. |

Les deux catalogues CM contiennent une seule entrée prompt. /cm délègue au
skill ; les wrappers ne créent pas automatiquement une slash native. Le
référentiel métier reste exclusivement celui de DEVOPS.md. Le protocole
ORCHESTRATED_CODING.md est inchangé car cette SCM est directe.

Aucun change actif ne reste. Contrôle final du rapport : six sections,
30 chemins, totaux 22/8, dix tâches terminées et UTF-8/LF, sans réarchivage.
État : TERMINÉ pour la livraison locale SCM 0.4.1. Publication et installation
réelles n'ont pas été exécutées dans cette session.
