# STATISTIQUES — add-prompt-dispatcher

Projet : Tools Codex, racine /home/devops/datas/tools-codex. Release locale :
0.4.0. Archive : openspec/changes/archive/2026-10-19-add-prompt-dispatcher.
Date : 19 octobre 2026. Rapport de SCM directe, périmètre et alias validés,
puis complétés par les huit variantes 1CISMPn explicitement demandées.
Aucun orchestrateur, sous-agent, RUN piloté ou compétence de statistiques
pilotées n'a été utilisé pour cette réalisation.

## 1. Statistiques générales et décisions

Le plugin et skill prompt, leur résolveur et la commande source sont livrés.
Le référentiel reste exclusivement celui du DEVOPS du projet courant. Les
38 actions d'exécution et LIST sont pris en charge. Les alias GCM et GCMP
sélectionnent GSCM.md et GSCMP.md. Les variantes 1CISMP1 à 1CISMP8 conservent
le RUN CISMPn et bornent son périmètre à un change complet, archivage,
statistiques puis arrêt de la session de codage selon les règles applicables.

| Mesure vérifiée | Résultat |
|---|---|
| Plugins du catalogue local | 5 : PLLM, TFL, CM, TCU et prompt |
| Supports de release 0.4.0 | 8 : VERSION, TOML, README et cinq manifestes |
| Arguments d'exécution plus LIST | 38 + 1 |
| Entrées de l'index réel observées avec LIST | 23, toutes disponibles |
| Tests nouveaux du dispatcher | 20 |
| Dernière suite Python 3.13.5 | 64 réussites sur 64 |
| Dernière suite Python 3.14.8 | 64 réussites sur 64 |
| Qualification finale combinée | 128 réussites sur 128, soit 100 % |
| Syntaxe | 3 py_compile réussis, temporaires nettoyés |
| Formats des skills CM/prompt | 4 validations réussies |
| Tâches du change terminées | 11 sur 11 |
| OpenSpec avant archivage | 8 éléments valides |
| OpenSpec après archivage | 8 spécifications valides |
| Exigences synchronisées | 8 ajoutées, 2 modifiées, 0 supprimée, 0 renommée |
| Fichiers initiaux observés par empreintes | 134 |
| Fichiers initiaux modifiés | 15 |
| Fichiers initiaux préservés | 119, dont 87 fichiers d'anciennes archives |

Le suivi des empreintes porte sur un ensemble ciblé de cadrages, catalogue,
commandes, specs, archives, manifestes, skills, scripts et tests ; il ne
constitue pas un inventaire récursif de tout le dépôt. Le lancement ciblé
initial de vingt tests réussis reste distinct du total final de 128.

Modèle exact, version du modèle, raisonnement, tokens, cache, coût, quotas,
TTMT, débit et temps de service : N/A, télémétrie correspondante non collectée.
Aucun quota partagé n'est converti en tokens ou en coût.

## 2. Messages et outils

Messages et appels d'outils exhaustifs : N/A, historique non agrégé.
Les opérations comprennent lecture ciblée, édition locale, tests et cycle
OpenSpec. Trois préparations ont été reprises : un remplacement documentaire
arrêté sur une apostrophe différente avant écriture ; un patch mal formé
rejeté avant écriture ; un appel d'audit dont la délimitation JavaScript a été
corrigée avant lancement de commande. Aucun test n'a été désactivé, aucune
validation fonctionnelle n'est restée en échec. Ces erreurs de préparation
ne sont pas assimilées à des commandes de qualification réussies.

Aucune commande Git, inspection de son état, création de branche, commit ou
push. Aucun pilotage CAB/OpenCode, agent délégué ou sonde de statistiques.
La source CISMP a été consultée pour définir les limites à un change, sans
lancer son processus. Les sources externes n'ont reçu aucune écriture.

## 3. Fichiers

Les chemins ci-dessous sont relatifs à la racine du projet.

| Chemin final | Opération |
|---|---|
| .agents/plugins/marketplace.json | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| PROJECT.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| openspec/specs/extension-distribution/spec.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/cm/skills/cm/SKILL.md | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| pyproject.toml | Modifié |
| skills/cm/SKILL.md | Modifié |
| .codex/commands/prompt.md | Créé |
| openspec/changes/archive/2026-10-19-add-prompt-dispatcher/.openspec.yaml | Créé |
| openspec/changes/archive/2026-10-19-add-prompt-dispatcher/STATISTIQUES.md | Créé |
| openspec/changes/archive/2026-10-19-add-prompt-dispatcher/design.md | Créé |
| openspec/changes/archive/2026-10-19-add-prompt-dispatcher/proposal.md | Créé |
| openspec/changes/archive/2026-10-19-add-prompt-dispatcher/specs/extension-distribution/spec.md | Créé |
| openspec/changes/archive/2026-10-19-add-prompt-dispatcher/specs/prompt-dispatch/spec.md | Créé |
| openspec/changes/archive/2026-10-19-add-prompt-dispatcher/tasks.md | Créé |
| openspec/specs/prompt-dispatch/spec.md | Créé |
| plugins/prompt/.codex-plugin/plugin.json | Créé |
| plugins/prompt/skills/prompt/SKILL.md | Créé |
| plugins/prompt/skills/prompt/scripts/resolve_prompt.py | Créé |
| skills/prompt/SKILL.md | Créé |
| skills/prompt/scripts/resolve_prompt.py | Créé |
| tests/test_prompt_dispatch.py | Créé |
| .agents/skills/prompt | Lien créé |

| Catégorie | Nombre |
|---|---:|
| Fichier existant modifié | 15 |
| Nouveau fichier | 15 |
| Nouveau lien | 1 |
| Fichier supprimé | 0 |
| Total de chemins finaux | 31 |

Les six fichiers du change sont créés à l'emplacement actif puis archivés
sans double comptage. Le rapport est créé après archivage. Les liens locaux
CM et TCU restent inchangés. Le moteur de mise à jour TCU, les scripts
PLLM/TFL et les trois modules de tests préexistants sont préservés. DEVOPS.md
et le référentiel externe restent les sources de résolution, sans duplication
ni régénération dans le plugin.

## 4. Commandes et validations

Sous-ensemble borné de onze commandes de qualification/cycle, hors lectures,
éditions et audits de clôture supplémentaires :

| Commande ou contrôle | Exécutions | Réussites | Échecs |
|---|---:|---:|---:|
| openspec validate add-prompt-dispatcher --strict | 1 | 1 | 0 |
| Python système unittest ciblé test_prompt_dispatch.py -v | 1 | 1 | 0 |
| Suite complète unittest -q sur les deux Python | 2 | 2 | 0 |
| Résolveur LIST sur le vrai projet | 1 | 1 | 0 |
| Python système : validateur skill-creator sur quatre skills | 1 | 1 | 0 |
| Python DevOps : versions, parité, py_compile et paquet isolé | 1 | 1 | 0 |
| Python : périmètre, encodage et catalogue CM | 1 | 1 | 0 |
| openspec validate --all --strict avant puis après archive | 2 | 2 | 0 |
| openspec archive add-prompt-dispatcher --json --yes | 1 | 1 | 0 |
| Total borné | 11 | 11 | 0 |

Taux dans ce sous-ensemble : 100 %. Les commandes OpenSpec utilisent le chemin
/home/devops/.local/npm/bin/openspec déclaré dans DEVOPS avec
OPENSPEC_TELEMETRY=0 et DO_NOT_TRACK=1. Les suites complètes utilisent :

/usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q
/home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q

Les quatre formats de skills sont validés avec le helper existant
/home/adema261/.codex/skills/.system/skill-creator/scripts/quick_validate.py,
sans ajout de dépendance. Les trois compilations portent sur les résolveurs
autonome/embarqué et tests/test_prompt_dispatch.py, avec cfile temporaire.

Le paquet isolé contient exactement le manifeste, SKILL.md et le résolveur.
LIST et 1CISMP3 ont été résolus sur les deux Python contre un projet de
fixture explicite : statut listed pour LIST, ready avec RUN CISMP3 et limite
1 pour la variante. Aucun RUN n'a été exécuté. Le LIST réel retourne le dossier
/home/devops/datas/prompts et son INDEX.md, tels que déclarés par DEVOPS.
Les corps ne sont pas lus par LIST ; les tests vérifient aussi cette propriété.

Autres contrôles réussis : huit supports de release et cinq entrées de
marketplace ; copies CM/prompt identiques ; trois liens locaux ; RFC 2119 et
longueur des exigences ; égalité de dix exigences entre les deltas et specs
principales ; empreintes ; tâches terminées et absence de change actif.

Build web et navigateurs : non pertinents. Exécution réelle d'un processus
sélectionné, pilotage d'un RUN, publication et installation dans le profil
Codex : non exécutées conformément au périmètre. Le statut ready ne démontre
pas une fin de travail. La capacité de conduite par le skill est revue dans
ses directives ; elle n'est pas présentée comme un RUN opérationnel qualifié.

## 5. Accès web

| Périmètre | Accès | Refus | Erreurs |
|---|---:|---:|---:|
| Réseau de cette réalisation | 0 | 0 | 0 |

Aucun fournisseur, marketplace distante, service CAB ou secret sollicité.
Les liens présents dans les documents ne constituent pas de nouvelles visites.
La lecture réelle du référentiel est locale, via DEVOPS et son index déclaré.
Taux de réussite web : N/A, dénominateur nul. La télémétrie OpenSpec est désactivée.

## 6. Synthèse et cohérence documentaire

| Repère temporel partiel | Heure Europe/Paris |
|---|---|
| Empreintes avant les écritures | 2026-10-19 16:10:07 CEST |
| Après archive, validation et audit, avant rapport | 2026-10-19 16:27:15 CEST |
| Intervalle mesuré | 00 h 17 min 08 s |
| Durée totale SCM | N/A, exploration initiale complète non instrumentée |

Cet intervalle inclut outils et attentes. Il ne mesure pas la génération du
modèle et exclut la rédaction du rapport et ses contrôles finaux ultérieurs.

| Document | État et preuve |
|---|---|
| Projet réel | Cinq plugins, huit supports 0.4.0, paquet et ressources résolus, deux distributions identiques. |
| AGENTS.md | Inchangé, empreinte conservée ; règles générales et autorité DEVOPS suffisantes. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel et Lancement de prompts. |
| TECHNICAL.md | Mis à jour : ressources, prérequis, Résolution et lancement de prompts, qualification et limites. |
| BUILD.md | Mis à jour : catalogue, installation, Utilisation de prompt et vérification avant publication. |
| DEVOPS.md | Inchangé, empreinte conservée ; ses déclarations de dossier et d'index sont utilisées sans repli. |
| README.md | Mis à jour : 0.4.0 et exemples LIST, CISMP3, 1CISMP3 avec renvoi à BUILD. |
| CHANGELOG.md | Mis à jour : trois nouvelles entrées Unreleased ; historique préservé. |
| openspec/specs/ | Prompt-dispatch et extension-distribution synchronisées ; dix exigences comparées, huit specs strictes valides. Release-versioning inchangée. |

Les preuves de terminaison des variantes 1CISMPn portent sur le seul change
et la clôture de sa session, sans sélectionner un deuxième change ni prétendre
avoir terminé tout le dépôt. Les conditions de validation et de décision
restent applicables. Le repli local est décrit dans design.md ; aucune donnée
n'a été migrée. Aucun écart documentaire restant identifié dans le périmètre.

La livraison est locale. La publication et l'installation globale restent des
étapes distinctes ; les liens existants et les sources externes sont préservés.

Contrôles finaux exécutés et réussis : six sections, 31 chemins existants,
catégories 15/15/1, totaux de qualification 11/11/0, UTF-8/LF sur trente
fichiers, versions et parité, onze tâches terminées et aucun change actif.
État : TERMINÉ pour le périmètre local SCM, rapport vérifié, archive unique.
