# STATISTIQUES — add-tfl-live-provider-pricing

Projet : Tools Codex. Version locale : 0.5.2. Session SCM directe.
Périmètre autonome et cycle OpenSpec validés explicitement par le développeur
le 25 octobre 2026. Rapport finalisé après l'archivage natif unique.

## 1. Statistiques générales

La table tarifaire statique Go est remplacée par une collecte officielle à
chaque génération. OpenRouter conserve sa collecte API et son classement de
base ; les deux fournisseurs tracent les sources, dates et variantes.

Dernières suites complètes : 95 tests réussis sur Python 3.13.5 et 95 sur
Python 3.14.9, soit 190 exécutions réussies pour 95 tests distincts. Parmi
eux, 17 nouveaux tests tarifaires contrôlent les deux distributions avec
leurs sous-cas. La suite ciblée de 17 tests a aussi été exécutée avec succès.
Quatre fichiers Python modifiés sont compilés sur les deux branches. Deux
SKILL.md sont validés. Les deux distributions sont identiques octet pour octet.

Deux collectes réelles complètes ont réussi. La dernière, le
2026-10-25T00:25:30+02:00, retient neuf modèles Go et trois OpenRouter.
MiniMax-M3.1-Flash est retenu à 0,375 USD/M ; MiniMax-M3 est exclu à 0,75.
Les neuf tarifs Go sont collectés sans mise à jour d'une liste tarifaire dans
le code. La route de génération de cinq modèles retenus n'est pas vérifiée ;
elle reste signalée sans protocole inventé. Aucune génération de tokens n'est
testée. PREUVE-COLLECTE.json conserve les deux observations et l'empreinte du
script final pour la seconde.

Release 0.5.2 : VERSION, pyproject.toml, README et cinq manifestes alignés.
Douze tâches préparatoires terminées ; quatre exigences ajoutées au delta.
OpenSpec avant archivage : change ciblé strict valide et 9/9 éléments globaux
stricts valides. L'archivage natif a synchronisé les quatre exigences ajoutées,
sans modification, suppression ou renommage d'exigence existante. Après
archive : 8/8 spécifications valides en mode strict, aucun change actif.

Temps total de session, tokens, cache d'inférence, coûts, quotas, temps de
génération, messages et appels exhaustifs : N/A, télémétrie non instrumentée.
Aucun total n'est reconstruit à partir de mesures partielles.

## 2. Messages et outils

Session directe Codex conduite selon SCM.md résolu depuis DEVOPS.md par le
skill prompt. Le skill skill-creator sert aux seules consignes TFL. Aucun
sous-agent, pilotage OpenCode/CAB ni skill de statistiques pilotées.
Messages et appels exhaustifs : N/A, non agrégés. Les opérations utilisent
des commandes locales Python/OpenSpec et les lectures HTTPS autorisées.
Aucune inspection de l'état Git, opération Git, installation système ou de
profil, publication ou modification de service n'est exécutée.
Les valeurs de clés sont traitées localement par le générateur et ne sont
restituées ni au modèle ni dans les preuves. Aucun stockage privé OpenCode
n'est lu. Les répertoires temporaires de qualification restent sous tests
et sont nettoyés.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins relatifs finaux ci-dessous.
Le seul déplacement est l'archivage OpenSpec explicitement autorisé.

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
| openspec/specs/tfl-catalog/spec.md | Modifié par synchronisation native |
| tests/test_tfl_pricing.py | Créé |
| openspec/changes/archive/2026-10-25-add-tfl-live-provider-pricing/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-tfl-live-provider-pricing/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-tfl-live-provider-pricing/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-tfl-live-provider-pricing/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-tfl-live-provider-pricing/PREUVE-COLLECTE.json | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-tfl-live-provider-pricing/STATISTIQUES.md | Créé, finalisé après archive |

Totaux finaux : 17 fichiers initiaux modifiés et 7 nouveaux chemins,
soit 24 chemins livrés. Aucun fichier initial supprimé. Les six artefacts
OpenSpec sont comptés une seule fois, à leur chemin final.
Onze fichiers hors modification contrôlés par empreinte : AGENTS, PROJECT,
DEVOPS, wrapper TFL, catalogue marketplace, config OpenSpec, trois suites de
tests préexistantes non concernées et deux métadonnées agents/openai.yaml.
La revue du diff du moteur utilise la copie installée en lecture seule,
après vérification de son égalité SHA-256 avec la source initiale du dépôt ;
aucune donnée ni aucun fichier du profil n'est actualisé.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Change avant code | Exécutée et réussie : openspec validate add-tfl-live-provider-pricing --strict. |
| Tests ciblés | Exécutée et réussie : Python 3.14, unittest discover -s tests -p test_tfl_pricing.py -v ; 17 tests. |
| Suite complète 3.13 | Exécutée et réussie : /usr/bin/python3 -B -m unittest discover -s tests -q ; 95 tests. |
| Suite complète 3.14 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 95 tests. |
| Syntaxe | Exécutée et réussie : py_compile sur les deux scripts TFL et les deux fichiers de tests modifiés, sorties temporaires sous tests. |
| Skills | Exécutée et réussie : quick_validate.py du skill-creator sur les deux distributions avec /usr/bin/python3. |
| Collecte réelle | Exécutée et réussie deux fois : script TFL autonome, --policy auto --output-dir temporaire sous tests ; code de sortie 0. |
| Release et parité | Exécutée et réussie : analyse TOML/JSON, cinq plugins et README ; comparaisons octet pour octet. |
| Périmètre et encodage | Exécutée et réussie avant archive : empreintes des onze fichiers préservés, UTF-8/LF sans BOM et contrôle ciblé de marqueurs de clé privée. |
| OpenSpec global avant archive | Exécutée et réussie : openspec validate --all --strict ; 9/9. |
| Statut ciblé | Exécutée et réussie : openspec status --change add-tfl-live-provider-pricing --json ; artefacts complets, isComplete=true. |
| Synchronisation et archive | Exécutée et réussie : openspec archive add-tfl-live-provider-pricing --json --yes ; archive 2026-10-25-add-tfl-live-provider-pricing, specsUpdated=true, quatre ajouts. |
| OpenSpec global après archive | Exécutée et réussie : openspec validate --all --strict ; 8/8. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
Premier contrôle strict : avertissement sur une exigence de plus de 500
caractères, corrigé par séparation en deux exigences avant le code.
Premier test ciblé : une égalité binaire de flottants dans la fixture a été
remplacée par une comparaison numérique approchée ; les assertions de prix
restent actives. Le validateur de skills est indisponible sous le Python
DevOps faute de PyYAML ; son exécution avec le Python système existant réussit
sans installation. Aucun de ces échecs préparatoires n'est masqué.

Non exécutées et hors périmètre : publication, installation dans le profil,
invocation dans une nouvelle session Codex et génération de tokens.
Non pertinents : build frontend et ShellCheck, aucun fichier frontend ou
shell modifié. Aucun lint ou outil de types supplémentaire n'est configuré
dans pyproject.toml pour ce périmètre.

## 5. Accès web

Lectures HTTPS réelles autorisées : documentation OpenCode Go, API modèles
OpenRouter, API modèles OpenCode Go et métadonnées models.dev. Deux lectures
ciblées initiales vérifient les tableaux Go et les champs tarifaires OpenRouter,
puis deux collectes complètes qualifient le générateur. Les redirections et
les tailles ou durées réseau exhaustives ne sont pas agrégées : N/A.
Les tests unitaires interdisent le réseau et le trousseau. Les appels de
collecte ne sont ni des complétions ni des mesures de débit ou de qualité.
Les snapshots sont datés ; ils ne constituent pas des tarifs permanents.

## 6. Synthèse et cohérence documentaire

Les prix Go sont relus dans la source officielle à chaque génération. Les
tableaux Go/Go Plus sont dédupliqués si identiques ; une contradiction est
bloquante. Les correspondances absentes et les prix OpenRouter non exploitables
sont exclus avec leur motif. Aucun repli tarifaire statique ou historique.
Les rapports précédents sont préservés si une collecte indispensable échoue.
Chaque remplacement de fichier publié reste atomique individuellement ;
aucune transaction commune aux deux fichiers n'est promise.

| Élément | État et preuve |
|---|---|
| Projet réel | Sources TFL synchronisées ; tests et deux collectes réelles réussis. |
| AGENTS.md | Inchangé, empreinte vérifiée ; règles de sources, périmètre et secrets applicables. |
| PROJECT.md | Inchangé, empreinte vérifiée ; le rôle TFL et les distributions restent identiques. |
| TECHNICAL.md | Mis à jour, section Validation : extraction, provenance, variantes et limites. |
| BUILD.md | Mis à jour, prérequis TFL : documentation HTTPS, échecs explicites et distinction installation/sources. |
| DEVOPS.md | Inchangé, empreinte vérifiée ; Python 3.13/3.14, chemin OpenSpec et référentiel SCM utilisés. |
| README.md | Mis à jour : release 0.5.2 et actualisation automatique. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased, sans date de publication inventée. |
| openspec/specs | Quatre exigences synchronisées dans tfl-catalog par l'archive ; validation globale stricte 8/8. |

La sélection OpenRouter, les filtres, blacklists, colonnes, commandes et
champs consommés par PLLM sont conservés. Le classement OpenRouter reste
fondé sur les prix API de base ; les paliers de contexte sont tracés sans
modifier cette politique. Les routes Go inconnues restent non qualifiées.
Les estimations Go non collectées sont N/A. Aucun quota n'est consulté.
ORCHESTRATED_CODING.md est non applicable à cette session directe, aucun
pilotage n'étant lancé. Les copies de profil restent à leur version installée.

Les quatre exigences archivées sont présentes à l'identique dans la
spécification principale. Les sept autres spécifications gardent leurs
empreintes initiales. Contrôle final : six sections, 24 chemins existants,
12 tâches cochées, UTF-8/LF sans BOM et totaux 17/7. Aucun réarchivage.
État : TERMINÉ pour la livraison locale SCM 0.5.2. Publication et installation
dans un profil Codex restent distinctes et n'ont pas été effectuées.
