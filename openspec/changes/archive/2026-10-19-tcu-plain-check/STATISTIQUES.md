# STATISTIQUES — tcu-plain-check

Projet : Tools Codex. Release locale conservée : 0.3.0. Date : 19 octobre 2026.
Rapport de correction dans le périmètre TCU validé, exécutée directement sans
pilotage, sous-agent ou compétence de statistiques pilotées.

## 1. Statistiques générales

La syntaxe check sans tirets est acceptée par le script, les skills et la
commande. --check reste compatible ; check --apply est refusé avant le moteur.
Les dernières suites comptent 44 tests sur chacun des Python 3.13.5 et 3.14.8,
soit 88 réussites sur 88. Trois py_compile réussissent, les copies CM/TCU sont
identiques et la release reste 0.3.0. OpenSpec : huit éléments valides avant
archive puis sept specs valides après. Deux exigences modifiées synchronisées.

Modèle exact, tokens, coûts, cache, quotas, temps de génération et durée globale :
N/A, télémétrie correspondante non instrumentée. Aucun quota n'est estimé.

## 2. Messages et outils

Messages et appels exhaustifs : N/A, non agrégés. Édition locale, tests et
contrôles via Python et OpenSpec ; aucune commande Git. Les contrôles réels
utilisent la lecture GitHub et le CLI de liste sans rafraîchissement ni
remplacement dans le profil. Aucun forçage du lien de prompts n'est tenté.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins relatifs ci-dessous.

| Chemin | Opération |
|---|---|
| .codex/commands/TCU.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| PROJECT.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| openspec/specs/extension-distribution/spec.md | Modifié |
| openspec/specs/tools-codex-update/spec.md | Modifié |
| plugins/cm/skills/cm/SKILL.md | Modifié |
| plugins/tcu/skills/tcu/SKILL.md | Modifié |
| plugins/tcu/skills/tcu/scripts/update.py | Modifié |
| skills/cm/SKILL.md | Modifié |
| skills/tcu/SKILL.md | Modifié |
| skills/tcu/scripts/update.py | Modifié |
| tests/test_tcu_update.py | Modifié |
| openspec/changes/archive/2026-10-19-tcu-plain-check/.openspec.yaml | Créé |
| openspec/changes/archive/2026-10-19-tcu-plain-check/design.md | Créé |
| openspec/changes/archive/2026-10-19-tcu-plain-check/proposal.md | Créé |
| openspec/changes/archive/2026-10-19-tcu-plain-check/specs/extension-distribution/spec.md | Créé |
| openspec/changes/archive/2026-10-19-tcu-plain-check/specs/tools-codex-update/spec.md | Créé |
| openspec/changes/archive/2026-10-19-tcu-plain-check/tasks.md | Créé |
| openspec/changes/archive/2026-10-19-tcu-plain-check/STATISTIQUES.md | Créé |

Totaux : 15 fichiers modifiés, 7 créés, 0 supprimé ; 22 chemins finaux. Les six
fichiers du change sont créés puis archivés sans double comptage. Les cinq
fichiers protégés du contrôle initial (VERSION, TOML, AGENTS, DEVOPS et
catalogue marketplace) sont inchangés.

## 4. Commandes

Sous-ensemble de neuf commandes de qualification/cycle, hors éditions, lectures
et contrôle final du rapport : deux contrôles réels (codes 1 attendus pour le
conflit), une validation ciblée, deux suites de tests, un contrôle
py_compile/parité, une validation globale avant archive, l'archivage et une
validation globale après archive. Totaux : 9 appels, 7 codes 0, 2 codes 1,
0 échec inattendu. Le code non nul du contrôle n'est pas présenté comme une
mise à jour réussie.

Dernières suites : /usr/bin/python3 et Python DevOps, avec -B -W
error::ResourceWarning -m unittest discover -s tests -q. Les trois sources
compilées sont les deux scripts TCU et tests/test_tcu_update.py ; leurs
artefacts temporaires sont nettoyés. OpenSpec utilise le chemin déclaré
/home/devops/.local/npm/bin/openspec, OPENSPEC_TELEMETRY=0 et DO_NOT_TRACK=1.
Archive unique : 2026-10-19-tcu-plain-check, six tâches terminées.

Contrôle réel avant puis après correction : scripts/update.py --check puis
scripts/update.py check, depuis le skill local. Les deux observent GitHub
0.2.2 au SHA ef51e8f07279e99dfeebe6be5b53e0fc23f26af0, PLLM et TFL installés
0.2.2, le skill global coding-session-statistics courant, les autres copies
globales recherchées absentes et le lien /home/adema261/.codex/prompts en
conflit. Sauvegarde : aucune (null), aucun remplacement. Les versions restent
observées telles quelles ; la release locale 0.3.0 est distincte.

## 5. Accès web

Deux exécutions réelles réussissent leur lecture GitHub : quatre requêtes
initiales API au total (HEAD et archive par exécution). Nombre de redirections
et volume transféré : N/A, non instrumentés. Aucun accès fournisseur, secret,
publication ou application de mise à jour. Aucune recherche web documentaire
supplémentaire n'a été effectuée. Le conflit est local et préservé.

## 6. Synthèse et cohérence documentaire

PROJECT (catalogue), TECHNICAL (contrôle), BUILD et README (exemples), CHANGELOG
(Unreleased) sont mis à jour avec check sans tirets. AGENTS et DEVOPS sont
inchangés : aucune nouvelle règle, dépendance ou installation. Les deux specs
sont synchronisées et passent strict ; les copies TCU et CM sont identiques.
La version reste 0.3.0. Aucun change actif ne reste après archivage.

La correction de syntaxe est livrée ; le contrôle réel n'a appliqué aucune
mise à jour. Le conflit du lien de prompts et la source distante 0.2.2 sont
rapportés, sans élargir la correction ni publier la release locale.

Le premier contrôle final du rapport a été arrêté par un motif de vérification
mal échappé ; le contrôle corrigé réussit sans réarchivage. Six sections,
22 chemins, totaux 15/7 et 9/7/2, UTF-8/LF et six tâches sont vérifiés.
État : TERMINÉ pour la correction locale.
