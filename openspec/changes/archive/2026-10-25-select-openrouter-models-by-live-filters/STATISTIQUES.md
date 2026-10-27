# STATISTIQUES — select-openrouter-models-by-live-filters

Projet : Tools Codex. Release locale : 0.5.3. Session SCM directe.
Complément fonctionnel et cycle OpenSpec validés explicitement par le développeur
le 25 octobre 2026. Rapport finalisé après l'archivage natif unique.

## 1. Statistiques générales

OpenRouter est interrogé sans filtre de catégorie, modalité, prix ou nombre
dans la requête. La sélection locale n'utilise aucune liste d'identifiants
admissibles : contexte ≥ 1M, moyenne API de base entre zéro et 0,50 USD/M
inclus, modalités de sortie et blacklist. Les exclusions restent motivées.
Les variantes tarifaires de contexte et les conditions de jours/horaires UTC
sont conservées séparément, sans remplacer les prix de classement de base.

Dernières suites complètes : 100 tests réussis sur Python 3.13.5 et 100 sur
Python 3.14.9, soit 200 exécutions réussies pour 100 tests distincts. La suite
tarifaire comporte désormais 22 tests, dont cinq nouveaux dans ce complément,
et contrôle les deux distributions. Elle a également été exécutée séparément.
Quatre fichiers Python compilés sur les deux branches, deux skills validés,
scripts et SKILL.md autonomes/embarqués identiques octet pour octet.

Collecte réelle complète réussie le 2026-10-25T00:34:01+02:00 : 467 modèles
OpenRouter examinés, 46 retenus et 421 exclus, soit 467 au total. Cinq modèles
gratuits sont retenus. MiniMax-M3.1-Flash apparaît à 0,375 USD/M. Le résultat
Go conserve neuf modèles admissibles. PREUVE-COLLECTE.json conserve les IDs,
coûts, variantes temporelles observées, source, date et SHA-256 du script.
Il s'agit d'une collecte de catalogue, sans génération de tokens.

Onze tâches préparatoires terminées. Delta : deux exigences modifiées, une
ajoutée, aucune supprimée ou renommée. OpenSpec strict : change validé avant
code et 9/9 éléments globaux valides avant archive. L'archivage natif a
synchronisé les deux modifications et l'ajout ; après archive, les huit
spécifications sont valides en mode strict et aucun change actif ne reste.

Durée totale, temps modèle/outils, tokens, cache, coûts et quotas : N/A,
télémétrie non instrumentée. Aucun cumul de tests répétés n'est présenté
comme une couverture distincte.

## 2. Messages et outils

SCM directe via le référentiel résolu depuis DEVOPS.md et le skill prompt.
Le skill skill-creator reste appliqué aux consignes distribuées TFL.
Aucun sous-agent, pilotage OpenCode/CAB ou skill de statistiques pilotées.
Messages et appels exhaustifs : N/A, non agrégés. Commandes exécutées une
par une via Python, shell et OpenSpec, avec examen des résultats.
Aucune consultation de quota, inspection de l'état Git, opération Git,
installation, publication ou modification de service. Les clés sont traitées
localement par le générateur sans restitution ni journalisation de leur valeur.
Les tests utilisent des fixtures hors réseau et des temporaires sous tests,
nettoyés après exécution. Aucun stockage privé OpenCode n'est consulté.

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
| openspec/changes/archive/2026-10-25-select-openrouter-models-by-live-filters/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-select-openrouter-models-by-live-filters/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-select-openrouter-models-by-live-filters/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-select-openrouter-models-by-live-filters/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-select-openrouter-models-by-live-filters/PREUVE-COLLECTE.json | Créé puis archivé |
| openspec/changes/archive/2026-10-25-select-openrouter-models-by-live-filters/STATISTIQUES.md | Créé, finalisé après archive |

Totaux finaux : 18 fichiers initiaux modifiés et six nouveaux chemins,
soit 24 chemins livrés. Aucun fichier initial supprimé ; les six artefacts
OpenSpec sont comptés une seule fois à leur chemin d'archive.
Contrôle initial : 42 empreintes ciblées, incluant les six fichiers de
l'archive précédente add-tfl-live-provider-pricing. Avant synchronisation,
17 fichiers modifiés et 25 inchangés ; aucun écart hors périmètre.
L'archive précédente est préservée. Aucun fichier de profil n'est actualisé.
Après synchronisation : 18 fichiers initiaux modifiés et 24 empreintes
inchangées sur les 42 ; seuls les chemins attendus ont changé.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate select-openrouter-models-by-live-filters --strict. |
| Tests tarifaires | Exécutée et réussie : Python 3.14, unittest discover -s tests -p test_tfl_pricing.py -v ; 22 tests. |
| Suite Python 3.13 | Exécutée et réussie : /usr/bin/python3 -B -m unittest discover -s tests -q ; 100 tests. |
| Suite Python 3.14 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 100 tests. |
| Syntaxe | Exécutée et réussie : py_compile des deux scripts TFL et deux tests modifiés, sous Python 3.13/3.14, artefacts temporaires nettoyés. |
| Format des skills | Exécutée et réussie : quick_validate.py du skill-creator avec /usr/bin/python3, deux distributions. |
| Collecte réelle | Exécutée et réussie après correction des variantes UTC : script TFL autonome --policy auto --output-dir temporaire, sortie 0 ; total 467 = 46 + 421. |
| Release et parité | Exécutée et réussie : VERSION, pyproject.toml, README et cinq plugins 0.5.3 ; deux scripts et deux SKILL.md identiques. |
| Périmètre | Exécutée et réussie avant archive : comparaison de 42 empreintes, aucune modification inattendue, ancienne archive inchangée. |
| OpenSpec global avant archive | Exécutée et réussie : openspec validate --all --strict ; 9/9. |
| Statut ciblé | Exécutée et réussie : openspec status --change select-openrouter-models-by-live-filters --json ; isComplete=true. |
| Synchronisation et archivage | Exécutée et réussie : openspec archive select-openrouter-models-by-live-filters --json --yes ; specsUpdated=true, un ajout et deux modifications. |
| OpenSpec global après archive | Exécutée et réussie : openspec validate --all --strict ; 8/8. |
| Rapport et encodage | Contrôle final : six sections, 24 chemins existants, onze tâches cochées, UTF-8/LF sans BOM ; les trois blocs d'exigences sont identiques au delta archivé. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
Premier contrôle du delta en échec : nom du scénario historique absent dans
le bloc MODIFIED. Son nom est conservé avec le nouveau résultat fonctionnel
validé (absence sans échec), puis le delta est validé avant code.
Première collecte réelle en échec : le lecteur de variantes supposait un
min_prompt_tokens obligatoire. Le catalogue intégral révèle des variantes
UTC légitimes ; elles sont désormais préservées et leurs types vérifiés,
avec scénario OpenSpec et tests déterministes. Aucun tarif ni ancien résultat
n'est utilisé comme repli. Aucun échec non résolu dans la qualification.

Non exécutées et hors périmètre : installation de profil, publication,
invocation dans une nouvelle session Codex, génération et mesure de débit.
Non pertinents : build frontend et ShellCheck. Aucun lint ou outil de types
supplémentaire n'est configuré dans pyproject.toml pour ce périmètre.

## 5. Accès web

Une première collecte complète échoue avant publication, une lecture publique
ciblée de l'API modèles identifie les overrides temporels, puis une collecte
complète corrigée réussit. Les collectes lisent OpenCode Go, models.dev,
la documentation tarifaire Go et l'API OpenRouter. Des recherches web ciblées
sur le domaine officiel OpenRouter vérifient la documentation des variantes ;
aucune source secondaire n'est utilisée pour choisir les prix.
Les preuves tarifaires proviennent directement des réponses officielles API.
Temps, volumes et requêtes réseau exhaustifs : N/A, non agrégés. Les tests
unitaires n'effectuent aucun appel réseau ou au trousseau. Les snapshots
restent datés et ne constituent pas une disponibilité permanente.

## 6. Synthèse et cohérence documentaire

La sélection OpenRouter est dynamique et auditable, modèles gratuits inclus,
sans liste fixe ni catégorie programmation imposée. Le classement conserve
les prix API de base et le tri existant. Les paliers de contexte et les
conditions temporelles UTC sont des métadonnées séparées ; aucune sélection
tarifaire selon l'heure locale n'est inventée. Les filtres, la blacklist,
colonnes, CLI et champs consommés par PLLM restent compatibles. L'absence
de résultat admissible préserve les rapports. Chaque fichier publié reste
remplacé atomiquement individuellement, sans promesse de transaction commune.

| Élément | État et preuve |
|---|---|
| Projet réel | Sources TFL synchronisées ; tests et collecte réelle réussis. |
| AGENTS.md | Inchangé, empreinte initiale conservée ; périmètre et exclusions respectés. |
| PROJECT.md | Inchangé, empreinte conservée ; rôle TFL et distributions toujours exacts. |
| TECHNICAL.md | Mis à jour, Validation : catalogue intégral, sélection dynamique, variantes UTC et limites. |
| BUILD.md | Mis à jour, prérequis TFL : filtrage local du catalogue entier et évolution sans release. |
| DEVOPS.md | Inchangé, empreinte conservée ; Python, chemin OpenSpec et référentiel SCM appliqués. |
| README.md | Mis à jour : release 0.5.3 et filtres de sélection dynamique. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased pour ce complément, sans date de publication inventée. |
| openspec/specs | Deux modifications et un ajout synchronisés par l'archive ; trois blocs identiques au delta et validation stricte 8/8. |

Le moteur Go conserve sa collecte et sa sélection dynamique ; aucun protocole
de génération Go n'est ajouté. ORCHESTRATED_CODING.md est non applicable à
cette session directe sans pilotage. Les profils installés et la précédente
archive restent inchangés.
État : TERMINÉ pour la livraison locale SCM 0.5.3. Aucun réarchivage ni échec
non résolu. Publication et installation de profil n'ont pas été effectuées.
