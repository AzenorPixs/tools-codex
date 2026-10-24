# STATISTIQUES — collect-go-modalities-and-routing-dynamically

Projet : Tools Codex. Release locale : 0.5.5. Session SCM directe.
Périmètre et cycle OpenSpec validés explicitement par le développeur le
25 octobre 2026. Rapport finalisé après l'archivage natif unique.

## 1. Statistiques générales

Modalités et transport Go sont collectés depuis les déclarations API et
models.dev, sans liste statique de modèles ni déduction par famille. Les
contrats de trois SDK/protocoles génériques restent reconnus ; un transport
inconnu reste signalé. Les modalités contradictoires et les URL non sûres
bloquent la publication sans repli sur un ancien catalogue.

Dernières suites complètes : 118 tests réussis sous Python 3.13.5 et 118 sous
Python 3.14.9, soit 236 exécutions réussies pour 118 tests distincts. Les
18 nouveaux tests de métadonnées contrôlent les deux distributions et la
lecture du catalogue par les deux consommateurs PLLM inchangés. Ils ont aussi
été exécutés séparément avec succès. Cinq fichiers Python modifiés compilés
sur les deux branches ; deux SKILL.md validés ; parité octet pour octet.

Collecte réelle réussie le 2026-10-25T00:57:53+02:00. Neuf modèles Go retenus,
neuf sorties texte et neuf routes documentées. MiniMax-M3.1-Flash déclare les
entrées image/texte/vidéo, une sortie texte et le protocole chat_completions
sur https://opencode.ai/inference/go/openai/v1/chat/completions. La source
models.dev est datée 2026-10-25T00:57:51+02:00. Le catalogue OpenRouter
conserve 46 modèles retenus lors de cette collecte. PREUVE-COLLECTE.json
consigne les modalités, routes, provenances, dates et l'empreinte du script.
Ces observations ne sont ni des générations ni des mesures de performance.

Treize tâches préparatoires terminées ; trois exigences ajoutées au delta.
OpenSpec strict avant archive : change ciblé valide puis 9/9 éléments globaux
valides. L'archivage natif synchronise trois ajouts, sans modification,
suppression ou renommage d'exigence existante. Après archive : huit
spécifications valides en mode strict, aucun change actif.
Release demandée 0.5.5, depuis l'état initial 0.5.3 ; aucune release 0.5.4
n'est inventée. VERSION, pyproject.toml, README et cinq plugins sont alignés.

Durée totale, temps modèle/outils, tokens, cache, coûts et quotas : N/A,
télémétrie non instrumentée. Les tests répétés ne sont pas additionnés comme
une couverture fonctionnelle supplémentaire.

## 2. Messages et outils

SCM est résolu par le skill prompt depuis le DEVOPS du projet. Le skill
skill-creator est appliqué aux seules consignes TFL distribuées. Aucun
sous-agent, pilotage OpenCode/CAB ou skill de statistiques pilotées.
Messages et appels exhaustifs : N/A, non agrégés. Commandes Python/OpenSpec
exécutées une par une, avec lectures HTTPS officielles autorisées.
Aucune inspection de l'état Git, opération Git, installation de profil,
publication, modification de service, consultation de quota ni génération.
Les secrets sont traités localement par le générateur, sans restitution ni
journalisation de leur valeur. Aucun stockage privé OpenCode n'est lu.
Les tests interdisent réseau et trousseau ; les temporaires de compilation,
catalogue et qualification restent sous tests et sont nettoyés.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins finaux relatifs ci-dessous.

| Chemin | Opération |
|---|---|
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
| skills/tfl/SKILL.md | Modifié |
| skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| plugins/tfl/skills/tfl/SKILL.md | Modifié |
| plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| tests/test_extension_qualification.py | Modifié |
| tests/test_tfl_pricing.py | Modifié |
| openspec/specs/tfl-catalog/spec.md | Modifié par synchronisation native |
| tests/test_tfl_go_metadata.py | Créé |
| openspec/changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/PREUVE-COLLECTE.json | Créé puis archivé |
| openspec/changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/STATISTIQUES.md | Créé, finalisé après archive |

Totaux finaux : 18 fichiers initiaux modifiés et sept nouveaux chemins,
soit 25 chemins livrés. Aucun fichier initial supprimé ; les six artefacts
OpenSpec sont comptés une seule fois à leur chemin d'archive.
Contrôle ciblé initial : 50 empreintes, incluant les deux moteurs PLLM et les
12 fichiers des deux archives précédentes de cette conversation. Avant
synchronisation : 17 fichiers modifiés, 33 inchangés, un nouveau test et aucun
écart hors périmètre. Moteurs PLLM et archives précédentes restent inchangés.
Les copies installées dans le profil Codex ne sont pas actualisées.
Après synchronisation, les 50 empreintes initiales comptent 18 modifications
attendues et 32 fichiers inchangés ; le nouveau test reste compté séparément.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate collect-go-modalities-and-routing-dynamically --strict. |
| Métadonnées ciblées | Exécutée et réussie : Python 3.14, unittest discover -s tests -p test_tfl_go_metadata.py -v ; 18 tests. |
| Suite Python 3.13 | Exécutée et réussie : /usr/bin/python3 -B -m unittest discover -s tests -q ; 118 tests. |
| Suite Python 3.14 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 118 tests. |
| Syntaxe | Exécutée et réussie : py_compile des deux scripts TFL et trois tests modifiés/créés sur les deux branches, artefacts temporaires nettoyés. |
| Format des skills | Exécutée et réussie : quick_validate.py du skill-creator sur les deux distributions avec /usr/bin/python3. |
| Compatibilité PLLM | Exécutée et réussie dans la suite : les deux consommateurs inchangés lisent les routes générées, sans benchmark ni quota. |
| Collecte réelle | Exécutée et réussie : script TFL autonome --policy auto --output-dir temporaire sous tests ; sortie 0, neuf sorties texte et neuf routes Go documentées. |
| Release, parité et encodage | Exécutée et réussie : version 0.5.5, deux scripts et deux SKILL.md identiques, UTF-8/LF sans BOM et contrôle ciblé de marqueurs privés. |
| Périmètre | Exécutée et réussie avant archive : 50 empreintes comparées, aucun changement inattendu, ancienne documentation archivée préservée. |
| OpenSpec global avant archive | Exécutée et réussie : openspec validate --all --strict ; 9/9. |
| Statut ciblé | Exécutée et réussie : openspec status --change collect-go-modalities-and-routing-dynamically --json ; isComplete=true. |
| Synchronisation et archivage | Exécutée et réussie : openspec archive collect-go-modalities-and-routing-dynamically --json --yes ; specsUpdated=true, trois ajouts. |
| OpenSpec global après archive | Exécutée et réussie : openspec validate --all --strict ; 8/8. |
| Rapport final | Six sections, 25 chemins existants, treize tâches cochées, trois exigences identiques au delta archivé, UTF-8/LF sans BOM. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
La première lecture web de la page OpenAI AI SDK dépasse la limite de l'outil ;
un ancien chemin de source openai-compatible répond 404. Les chemins actuels
sont ensuite identifiés dans le dépôt officiel et les trois contrats sont
vérifiés sur leurs sources. Aucun contrat n'est déduit d'un nom de modèle.
Les tests, la collecte réelle et les validations OpenSpec n'ont aucun échec
non résolu. Aucun test n'est supprimé ni désactivé.

Non exécutées et hors périmètre : publication, installation réelle, invocation
dans une nouvelle session Codex, complétion et mesure de débit. Les routes
publiées indiquent generation_tested=false. Non pertinents : build frontend
et ShellCheck. Aucun lint ou outil de types supplémentaire n'est configuré
dans pyproject.toml pour ce périmètre.

## 5. Accès web

Lectures publiques models.dev pour le fournisseur opencode-go, documentation
et sources officielles Vercel AI SDK pour les trois transports. Les URL et
contrats sont consignés dans design.md et dans les références du catalogue.
Une collecte réelle complète lit les modèles Go, models.dev, les tarifs Go
et les modèles OpenRouter. PREUVE-COLLECTE.json décrit l'observation datée.
Temps, volumes et appels réseau exhaustifs : N/A, non agrégés. Les tests
unitaires sont isolés du réseau et des secrets. Aucun appel de génération,
quota, installation de SDK ou coût d'inférence n'est déduit de ces lectures.

## 6. Synthèse et cohérence documentaire

Les informations Go connues proviennent des déclarations courantes. Les
modalités concordantes utilisent la provenance API si disponible ; sinon
models.dev complète la déclaration. Les contradictions bloquent la génération.
Le transport vient de l'API explicite ou des métadonnées npm/api, avec
surcharge du modèle. Trois contrats SDK génériques sont supportés, sans
table d'identifiants ni familles. Une information inconnue reste signalée.
Les URL sont validées avant publication ; une route documentée n'est pas une
qualification de génération. Tarifs, filtres, blacklists, CLI, colonnes et
sélection OpenRouter sont préservés. Les rapports précédents restent intacts
si la collecte indispensable échoue ; les remplacements sont atomiques par
fichier, sans promesse de transaction commune.

| Élément | État et preuve |
|---|---|
| Projet réel | Deux distributions synchronisées, tests et collecte réelle réussis. |
| AGENTS.md | Inchangé, empreinte conservée ; périmètre, sources et règles de secrets appliqués. |
| PROJECT.md | Inchangé, empreinte conservée ; rôle de TFL et distributions toujours exacts. |
| TECHNICAL.md | Mis à jour, Validation : modalités, transports, provenance, URL et compatibilité des consommateurs. |
| BUILD.md | Mis à jour, prérequis TFL : métadonnées models.dev, informations inconnues et distinction génération/documentation. |
| DEVOPS.md | Inchangé, empreinte conservée ; runtimes, OpenSpec et référentiel SCM utilisés. |
| README.md | Mis à jour : version 0.5.5 et métadonnées Go dynamiques. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased, sans date de publication inventée. |
| openspec/specs | Trois ajouts synchronisés par l'archive, identiques au delta ; validation globale stricte 8/8. |

Les champs api_endpoint, api_protocol et endpoint_source restent lisibles
par PLLM. Les métadonnées supplémentaires tracent les sources et dates ;
generation_tested=false reste explicite. ORCHESTRATED_CODING.md est non
applicable à cette session directe sans pilotage. Aucun quota n'est consulté.
État : TERMINÉ pour la livraison locale SCM 0.5.5. Aucun réarchivage ni échec
non résolu. Publication et installation de profil n'ont pas été effectuées.
