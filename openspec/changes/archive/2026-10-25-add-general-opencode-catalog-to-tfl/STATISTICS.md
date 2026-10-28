# STATISTIQUES — add-general-opencode-catalog-to-tfl

Projet : Tools Codex. Release locale : 0.5.6. Session SCM directe.
Demande explicite du développeur : catalogue général OpenCode, contexte ≥ 1M,
moyenne maximale 0,50 USD/M, cycle OpenSpec et incrément 0.0.1 depuis 0.5.5.
Rapport finalisé après l'archivage natif unique.

## 1. Statistiques générales

TFL collecte désormais trois catalogues indépendants et restitue Go, OpenCode
général puis OpenRouter avec les mêmes huit colonnes. La section opencode
s'ajoute aux sections existantes sans changer les politiques PLLM. Une clé
Go n'est jamais empruntée pour la requête publique du catalogue général.

Dernières suites complètes : 132 tests réussis sous Python 3.13.5 et 132 sous
Python 3.14.9, soit 264 exécutions réussies pour 132 tests distincts. Les
14 nouveaux tests couvrent les deux distributions, le catalogue indépendant,
les bornes, variantes gratuites 200K, prix/route/source d'un même ID, accès
public, ordre/colonnes, erreurs, blacklist et compatibilité PLLM. Un premier
passage ciblé de 12 tests a réussi ; les deux scénarios supplémentaires sont
inclus dans les suites complètes finales. Cinq fichiers Python compilés sur
les deux branches ; quatre SKILL.md CM/TFL validés. Parité de leurs copies.

Collecte réelle réussie le 2026-10-25T01:30:15+02:00 : neuf modèles Go,
cinq modèles généraux et 46 OpenRouter retenus. Le catalogue général contient
85 modèles examinés : cinq retenus et 80 exclus. Les modèles généraux retenus
sont beam-free, nemotron-3.5-super-vl-free, qwen3.8-flash, glm-5.3-flash et
gpt-6-luna. GLM-5.3-Flash Free et DeepSeek V4.1 Flash Free sont examinés et
exclus avec leur contexte 200 000, sans abaisser le seuil 1M. La preuve JSON
consigne sources, modèles, coûts, routes, exclusions et empreinte du script.
Il s'agit de collecte et résolution documentaire, sans génération ni quotas.

Treize tâches préparatoires terminées. Delta : quatre exigences modifiées,
une ajoutée, aucune supprimée ou renommée. OpenSpec strict avant archive :
change ciblé validé avant code, puis 9/9 éléments globaux valides.
L'archivage natif synchronise un ajout et quatre modifications ; après archive,
huit spécifications sont valides en mode strict et aucun change actif ne reste.
VERSION, pyproject.toml, README et cinq plugins partagent 0.5.6.

Durée totale, temps modèle/outils, tokens, cache, coûts et quotas : N/A,
télémétrie non instrumentée. Les répétitions de suites ne constituent pas une
couverture distincte supplémentaire.

## 2. Messages et outils

SCM résolu depuis DEVOPS.md avec le skill prompt ; skill-creator appliqué
aux consignes distribuées. Aucun sous-agent, pilotage OpenCode/CAB ou skill
de statistiques pilotées. Messages et appels exhaustifs : N/A, non agrégés.
Commandes Python/OpenSpec exécutées une par une, avec lectures publiques
HTTPS autorisées. Aucune inspection de l'état Git, opération Git, installation
de profil, publication ou modification de service.
Le générateur traite localement le secret Go sans le transmettre au modèle,
aux rapports ou à la requête publique du catalogue général. Aucun stockage
privé OpenCode n'est lu. Tests hors réseau/trousseau ; temporaires sous tests
nettoyés. Aucun appel de génération, consultation de quota ou benchmark PLLM.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins finaux relatifs ci-dessous.

| Chemin | Opération |
|---|---|
| PROJECT.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| pyproject.toml | Modifié |
| .codex/commands/tfl.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| skills/cm/SKILL.md | Modifié |
| plugins/cm/skills/cm/SKILL.md | Modifié |
| skills/tfl/SKILL.md | Modifié |
| skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| plugins/tfl/skills/tfl/SKILL.md | Modifié |
| plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| tests/test_extension_qualification.py | Modifié |
| tests/test_tfl_pricing.py | Modifié |
| openspec/specs/tfl-catalog/spec.md | Modifié par synchronisation native |
| tests/test_tfl_opencode_catalog.py | Créé |
| openspec/changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/PREUVE-COLLECTE.json | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/STATISTIQUES.md | Créé, finalisé après archive |

Totaux finaux : 22 fichiers initiaux modifiés et sept nouveaux chemins,
soit 29 chemins livrés. Aucun fichier initial supprimé ; les six artefacts
OpenSpec sont comptés une seule fois à leur chemin final d'archive.
Contrôle ciblé initial : 59 empreintes, incluant les deux moteurs PLLM et les
18 fichiers des trois archives précédentes de cette conversation. Avant
synchronisation : 21 modifications attendues, 38 inchangés, un nouveau test,
aucun écart hors périmètre. Moteurs PLLM et archives précédentes préservés.
Aucune copie installée dans le profil Codex n'est actualisée.
Après synchronisation : 22 modifications attendues et 37 fichiers inchangés
sur les 59 empreintes initiales ; le nouveau test est compté séparément.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate add-general-opencode-catalog-to-tfl --strict. |
| Catalogue ciblé | Exécutée et réussie : Python 3.14, unittest discover -s tests -p test_tfl_opencode_catalog.py -v ; premier passage de 12 tests. |
| Suite Python 3.13 | Exécutée et réussie : /usr/bin/python3 -B -m unittest discover -s tests -q ; 132 tests, dont les 14 nouveaux. |
| Suite Python 3.14 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 132 tests, dont les 14 nouveaux. |
| Syntaxe | Exécutée et réussie : py_compile des deux scripts TFL et trois tests modifiés/créés sur les deux branches, temporaires nettoyés. |
| Format des skills | Exécutée et réussie : quick_validate.py du skill-creator sur quatre copies CM/TFL avec /usr/bin/python3. |
| Compatibilité PLLM | Exécutée et réussie dans la suite : consommateurs inchangés lisant leurs sections dans un catalogue enrichi. |
| Collecte réelle | Exécutée et réussie : script TFL --policy auto --output-dir temporaire sous tests ; sortie 0, catalogues 9/5/46, général 85 = 5 + 80. |
| Release, parité et encodage | Exécutée et réussie : 0.5.6, copies CM/TFL identiques, wrapper/manifestes cohérents, UTF-8/LF sans BOM et contrôle ciblé de marqueurs privés. |
| Périmètre | Exécutée et réussie avant archive : 59 empreintes comparées, aucune modification inattendue, trois archives préservées. |
| OpenSpec global avant archive | Exécutée et réussie : openspec validate --all --strict ; 9/9. |
| Statut ciblé | Exécutée et réussie : openspec status --change add-general-opencode-catalog-to-tfl --json ; isComplete=true. |
| Synchronisation et archivage | Exécutée et réussie : openspec archive add-general-opencode-catalog-to-tfl --json --yes ; specsUpdated=true, un ajout et quatre modifications. |
| OpenSpec global après archive | Exécutée et réussie : openspec validate --all --strict ; 8/8. |
| Rapport final | Six sections, 29 chemins existants, treize tâches cochées, cinq blocs identiques au delta archivé, UTF-8/LF sans BOM. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
Les validations exécutées, tests et collecte n'ont aucun échec non résolu.
Les fixtures de publication existantes sont adaptées à la troisième collecte,
sans désactivation de test ni accès réseau pendant les suites.
Non exécutées et hors périmètre : publication, installation de profil,
invocation dans une nouvelle session Codex, génération et mesures de débit.
Non pertinents : build frontend et ShellCheck. Aucun lint ou outil de types
supplémentaire n'est configuré dans pyproject.toml pour ce périmètre.

## 5. Accès web

Vérification publique initiale de l'API https://opencode.ai/zen/v1/models :
85 modèles sans Authorization. Vérification de la page de tarifs Console :
84 références lisibles par l'extracteur. Une collecte complète des trois
catalogues utilise les sources de disponibilité et prix respectives et les
métadonnées models.dev de opencode-go/opencode. La preuve JSON est datée et
liée au script final. Temps, volumes et requêtes réseau exhaustifs : N/A,
non agrégés. Aucun appel de génération, solde ou quota ; aucun SDK installé.

## 6. Synthèse et cohérence documentaire

Le catalogue général est indépendant et public, avec mêmes bornes 1M/0,50
USD/M. Les variantes gratuites 200K sont exclues et auditées. Le prix général
de référence est la moyenne maximale des variantes publiées ; Go garde le
hors pointe. Prix de cache, contextes, routes et sources ne sont pas empruntés
entre sections. Les modèles sont triés séparément ; les trois tableaux ont
les huit mêmes colonnes. Une collecte indispensable en échec empêche toute
publication partielle. Les remplacements restent atomiques par fichier,
sans promesse de transaction commune aux deux fichiers.

| Élément | État et preuve |
|---|---|
| Projet réel | Trois collectes et trois tableaux ; sources synchronisées, tests et collecte réelle réussis. |
| AGENTS.md | Inchangé, empreinte conservée ; règles de sources, périmètre et secrets appliquées. |
| PROJECT.md | Mis à jour, Catalogue actuel : rôle TFL étendu aux trois catalogues. |
| TECHNICAL.md | Mis à jour, Prérequis et Validation : source publique, séparation, règles tarifaires et compatibilité. |
| BUILD.md | Mis à jour, tableau des plugins et prérequis TFL : troisième source sans nouvelle dépendance. |
| DEVOPS.md | Inchangé, empreinte conservée ; runtimes, OpenSpec et référentiel SCM utilisés. |
| README.md | Mis à jour : release 0.5.6, trois tableaux et seuils inchangés. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased, sans date de publication inventée. |
| openspec/specs | Quatre modifications et un ajout synchronisés par l'archive, cinq blocs identiques au delta ; validation stricte globale 8/8. |

Consignes TFL/CM et wrapper décrivent le même ordre et la même portée. Le
manifeste TFL actualise ses descriptions et son prompt de lancement ; les
cinq plugins partagent la release. Les politiques et moteurs PLLM restent
inchangés. ORCHESTRATED_CODING.md est non applicable à cette session directe
sans pilotage. Aucune consultation de quota ni génération n'est effectuée.
État : TERMINÉ pour la livraison locale SCM 0.5.6. Aucun réarchivage ni échec
non résolu. Publication et installation de profil n'ont pas été effectuées.
