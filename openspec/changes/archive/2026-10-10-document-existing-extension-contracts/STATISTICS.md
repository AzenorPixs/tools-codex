# STATISTIQUES — document-existing-extension-contracts

Archive : /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts

Rapport de session SCM directe. Il rassemble les preuves de ce change et les
mesures disponibles de la phase de clôture Python, synchronisation et
archivage. Les opérations des phases antérieures ne sont pas reconstituées.
Les compteurs de messages, appels d'outils et tentatives d'écriture n'ont pas
été collectés exhaustivement : ils restent N/A. Les catégories de fichiers
ci-dessous décrivent des opérations logiques contrôlées, pas des appels d'outil.
Aucune compétence de statistiques pilotées ni sonde d'agent n'a été invoquée.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex ; modèle exact N/A | N/A | OpenAI | N/A | N/A | N/A | N/A |

Modèle exact, version, raisonnement et temps de génération : N/A, télémétrie
correspondante non fournie. Aucune estimation depuis la durée calendaire.

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Aucun agent orchestrateur : SCM directe | N/A | N/A | N/A | N/A | N/A | N/A |

## 1. Statistiques générales et décisions

Le développeur a validé les décisions CGP-07/08 et les trois lots de clôture :
version Python 0.2.1 alignée sur VERSION, plage >=3.13,<3.15, qualification sur
les deux branches, synchronisation, archivage et rapport. La release reste
0.2.1. Les scripts, dépendances et tests existants sont préservés.

| Contrôle mesuré de clôture | Réussites | Échecs | Total | Taux de réussite |
|---|---:|---:|---:|---:|
| Exécutions de tests : 19 tests distincts sur deux interpréteurs | 38 | 0 | 38 | 100.0 % |
| Compilations : 7 fichiers sur deux interpréteurs | 14 | 0 | 14 | 100.0 % |
| Imports : 7 fichiers sur deux interpréteurs | 14 | 0 | 14 | 100.0 % |
| Résolution Europe/Paris | 2 | 0 | 2 | 100.0 % |
| Métadonnées TOML, release et plage Python | 2 | 0 | 2 | 100.0 % |
| Total des contrôles Python comptés ci-dessus | 70 | 0 | 70 | 100.0 % |

Versions effectivement contrôlées : /usr/bin/python3 = 3.13.5 ; Python DevOps
= 3.14.8. Les 19 tests incluent les quatre tests TTFT préexistants et couvrent
les deux distributions. Les sept fichiers sont les cinq scripts distribués
et les deux modules de tests. Les services externes sont simulés dans les tests.

Tokens, cache, coûts, compactions, temps de service, quota partagé et variations
avant/après : N/A, aucune télémétrie ou paire de relevés comparable collectée.
La durée globale de la session SCM multi-tours est N/A : borne initiale
complète non instrumentée. La phase de clôture mesurée figure en section 6.

## 2. Types de messages et d'outils

| Domaine | Observation | Effectif exhaustif et pourcentage |
|---|---|---|
| Messages humains | Validation explicite du périmètre de clôture | N/A, historique non agrégé |
| Messages assistant | Explications, propositions et progression visibles | N/A, historique non agrégé |
| Commandes locales | Lectures, écritures, tests et contrôles | N/A, inventaire exhaustif non collecté |
| Édition locale | Fichiers du périmètre approuvé uniquement | Tentatives N/A ; opérations logiques en section 3 |
| Horloge | Bornes vérifiables de la phase mesurée | Bornes en section 6 ; total d'appels N/A |
| CAB/OpenCode, sous-agents, sondes | Non déclenchés par cette SCM directe | Non applicable |

Aucun appel réussi n'est assimilé à une approbation manuelle individuelle.
Les décisions humaines autorisent les lots ; les refus et erreurs restent
distincts. Les huit commandes de qualification/cycle identifiées en section 4
ont réussi sans refus observé. Aucun total d'outils exhaustif n'est inventé.

## 3. Fichiers modifiés

| Chemin final absolu | Modifié | Créé | Déplacé vers l'archive |
|---|---|---|---|
| /home/devops/datas/tools-codex/pyproject.toml | Oui | — | — |
| /home/devops/datas/tools-codex/TECHNICAL.md | Oui | — | — |
| /home/devops/datas/tools-codex/BUILD.md | Oui | — | — |
| /home/devops/datas/tools-codex/README.md | Oui | — | — |
| /home/devops/datas/tools-codex/CHANGELOG.md | Oui | — | — |
| /home/devops/datas/tools-codex/openspec/specs/release-versioning/spec.md | Oui | — | — |
| /home/devops/datas/tools-codex/openspec/specs/extension-distribution/spec.md | — | Oui | — |
| /home/devops/datas/tools-codex/openspec/specs/tfl-catalog/spec.md | — | Oui | — |
| /home/devops/datas/tools-codex/openspec/specs/pllm-evaluation/spec.md | — | Oui | — |
| /home/devops/datas/tools-codex/openspec/specs/codex-usage-reporting/spec.md | — | Oui | — |
| /home/devops/datas/tools-codex/openspec/specs/coding-session-statistics/spec.md | — | Oui | — |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/.openspec.yaml | Oui | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/proposal.md | Oui | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/design.md | Oui | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/tasks.md | Oui | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/specs/extension-distribution/spec.md | Oui | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/specs/pllm-evaluation/spec.md | — | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/specs/tfl-catalog/spec.md | — | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/specs/codex-usage-reporting/spec.md | — | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/specs/coding-session-statistics/spec.md | — | — | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/specs/release-versioning/spec.md | — | Oui | Oui |
| /home/devops/datas/tools-codex/openspec/changes/archive/2026-10-10-document-existing-extension-contracts/STATISTIQUES.md | — | Oui | — |

| Opération logique | Nombre | Part des 28 opérations |
|---|---:|---:|
| Modifications | 11 | 39.3 % |
| Créations | 7 | 25.0 % |
| Déplacements | 10 | 35.7 % |
| Total | 28 | 100.0 % |

Ces 28 opérations concernent 22 chemins finaux distincts. Un fichier modifié
puis déplacé compte dans les deux opérations ; le nouveau delta de release
est créé puis déplacé. Les dix fichiers du change ont été transférés avec
leurs empreintes inchangées ; seules les preuves de clôture de design/tasks
sont ensuite complétées et le présent rapport ajouté. Aucune suppression
fonctionnelle : la disparition du chemin actif résulte du déplacement autorisé.

Contrôle de périmètre : 45 sources initiales suivies ; 11 modifiées avant
archivage et 34 inchangées, dont quatre déplacées sans changement. Les cinq
specs principales créées, le delta de release et le rapport constituent les
sept créations. Les huit archives antérieures sont préservées. Les tentatives
d'écriture approuvées, refusées ou en erreur restent N/A, non collectées.

## 4. Commandes

Tableau borné aux huit commandes de qualification/cycle identifiables, et non
au total des commandes de la session. Chaque libellé est limité à 100 caractères.
Les validations OpenSpec utilisent /home/devops/.local/npm/bin/openspec,
avec OPENSPEC_TELEMETRY=0 et DO_NOT_TRACK=1. Les scripts par stdin compilent
et importent les sept fichiers, contrôlent le TOML et le fuseau, puis nettoient
leurs artefacts temporaires sous tests/.

| Commande ou script identifié | Exécutions | Part des 8 | Résultat observé |
|---|---:|---:|---|
| /usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v | 1 | 12.5 % | 19 tests réussis |
| /home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests … | 1 | 12.5 % | 19 tests réussis |
| /usr/bin/python3 -B - (qualification par stdin) | 1 | 12.5 % | 7 compilations, 7 imports, TOML et fuseau réussis |
| /home/devops/python/current/bin/python3 -B - (qualification par stdin) | 1 | 12.5 % | 7 compilations, 7 imports, TOML et fuseau réussis |
| openspec validate document-existing-extension-contracts --strict | 1 | 12.5 % | Change valide avant métadonnées |
| openspec validate --all --strict | 2 | 25.0 % | 7 éléments avant archive ; 6 après archive |
| openspec archive document-existing-extension-contracts --json --skip-specs | 1 | 12.5 % | Archive créée ; validation conservée |
| Total du périmètre identifié | 8 | 100.0 % | 8 réussies, 0 refus, 0 erreur |

Les lectures, aides CLI, écritures et audits par empreintes ne sont pas inclus
comme s'ils formaient un inventaire exhaustif. Aucun test fournisseur, build,
installation système, migration, commit, push, branche ou commande Git exécuté.
Aucune commande refusée observée dans le périmètre identifié.

## 5. Accès web

| Domaine | Exécutés | Refus | Erreurs | Total | Taux |
|---|---:|---:|---:|---:|---|
| Accès web de cette phase de clôture | 0 | 0 | 0 | 0 | N/A, dénominateur nul |

Aucune URL effectivement visitée ou refusée à restituer. Les URL de fixtures
et les références documentaires ne constituent pas des accès réalisés. Aucun
fournisseur ni secret sollicité ; aucune télémétrie OpenSpec autorisée.

## 6. Synthèse globale

| Mesure temporelle | Valeur |
|---|---|
| Repère initial de collecte de la clôture | 2026-10-10T17:51:27+02:00 |
| Après archivage et validation, avant rédaction du rapport | 2026-10-10T17:56:03+02:00 |
| Durée calendaire entre ces bornes | 00 h 04 min 36 s |
| Durée totale de la SCM multi-tours | N/A, borne initiale complète non instrumentée |

La durée mesurée couvre les attentes et outils de cet intervalle. Elle ne
mesure pas la génération de l'agent et exclut la rédaction du rapport et les
contrôles finaux ultérieurs. Aucun pourcentage de quota n'est converti en
tokens ou euros ; aucun quota partagé n'est attribué à cette conversation.

Bilan : 19 tests distincts exécutés sur deux branches (38 réussites), 14
compilations, 14 imports et quatre contrôles de fuseau/métadonnées réussis.
OpenSpec strict réussit sur 7 éléments avant archivage puis 6 specs après.
Les six specs principales totalisent 47 exigences et 55 scénarios, contrôlés
sans mots-clés normatifs employés en minuscules. Les 21 tâches préparatoires
sont terminées ; l'archivage est prouvé et le rapport est produit.

État : TERMINÉ — rapport vérifié, six sections, UTF-8/LF, chemins, libellés et totaux conformes. Aucun autre change
n'est sélectionné. Installation réelle Codex et qualification fournisseur
restent des contrôles distincts avant publication, sans être annoncées réussies.
