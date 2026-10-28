# STATISTIQUES — distribute-cm-plugin

Projet : Tools Codex (`tools-codex`). Racine : `/home/devops/datas/tools-codex`.
Archive : `openspec/changes/archive/2026-10-19-distribute-cm-plugin`.
Release dans les sources : 0.2.3. Date : 19 octobre 2026.

Rapport de la reprise SCM après validation du périmètre autonome. Exécution
directe avec Codex, sans orchestrateur, sous-agent, pilotage OpenCode/CAB,
compétence de statistiques pilotées ni télémétrie associée. Les mesures non
collectées restent N/A avec leur justification.

## 1. Statistiques générales et décisions

CM est ajouté comme troisième plugin de la marketplace locale, avec son
manifeste et son skill embarqué. Le skill autonome et le lien de découverte
sont conservés. Les deux copies du skill restent identiques. La release
commune est portée de 0.2.2 à 0.2.3. Les scripts et comportements PLLM/TFL sont
préservés. Publication distante et installation dans le profil Codex sont
hors périmètre et ne sont pas annoncées réalisées.

| Mesure vérifiée | Résultat |
|---|---|
| Plugins présents dans le catalogue | 3 : PLLM, TFL et CM |
| Fichiers du paquet CM | 2 fichiers réguliers, sans lien externe |
| Copies du skill CM comparées | 2, identiques octet pour octet |
| Supports de release alignés | 6 : VERSION, TOML, README et trois manifestes |
| Tests distincts existants | 19 |
| Exécutions sur Python 3.13.5 et 3.14.8 | 38 réussies sur 38, soit 100 % |
| Tâches du change terminées | 11 sur 11 |
| OpenSpec avant archivage | 7 éléments valides sur 7 |
| OpenSpec après archivage | 6 spécifications valides sur 6 |
| Exigences synchronisées | 2 ajoutées, 2 modifiées, 0 supprimée, 0 renommée |
| Changes actifs après archivage | 0 |
| Fichiers initiaux suivis par empreintes | 103 |
| Fichiers initiaux modifiés | 12 |
| Fichiers initiaux préservés | 91, dont 67 fichiers d'archives précédentes |

Le contrôle des 103 fichiers est ciblé : cadrages, catalogue, commandes,
spécifications, archives, manifestes, skills, scripts et tests concernés. Il
ne constitue pas un inventaire récursif de tout le dépôt. Aucun quota n'est
converti en tokens ou en coût.

Modèle exact, version du modèle, raisonnement, TTMT, débit, temps de service,
tokens, cache, coût et variation de quota : N/A, télémétrie correspondante non
collectée. Durée totale de la SCM : N/A, absence de borne initiale complète.

## 2. Types de messages et d'outils

| Domaine | Observation | Compteur exhaustif |
|---|---|---|
| Messages humains | Validation du périmètre avant écriture | N/A, historique non agrégé |
| Messages de suivi | État du change, validation du paquet, tests et clôture | N/A, historique non agrégé |
| Commandes locales | Lectures, copie, contrôles, tests et cycle OpenSpec | N/A au total ; sous-ensemble borné en section 4 |
| Édition | apply_patch et copie locale par Python | Total N/A ; un patch de preuve a échoué sur son contexte puis a été corrigé |
| Horloge | Deux bornes partielles de la reprise | Intervalle en section 6 |
| Git | État non inspecté, aucune opération exécutée dans cette reprise | Non applicable |
| Pilotage, CAB, OpenCode et sous-agents | Non déclenchés | Non applicable |

L'échec du patch concernait une ligne de contexte dans design.md et n'a
modifié aucun fichier. Le correctif a été appliqué au seul document prévu.
Il est distinct des validations fonctionnelles et des commandes de cycle.

## 3. Fichiers modifiés

Les chemins sont relatifs à la racine indiquée en tête de rapport.

| Chemin final | Opération |
|---|---|
| VERSION | Modifié : 0.2.3 |
| pyproject.toml | Modifié : version uniquement |
| plugins/pllm/.codex-plugin/plugin.json | Modifié : version uniquement |
| plugins/tfl/.codex-plugin/plugin.json | Modifié : version uniquement |
| .agents/plugins/marketplace.json | Modifié : entrée CM ajoutée |
| skills/cm/SKILL.md | Modifié : règle de synchronisation des copies |
| PROJECT.md | Modifié : organisation et catalogue |
| TECHNICAL.md | Modifié : structure, parité et qualification |
| BUILD.md | Modifié : installation, mise à jour et choix de distribution |
| README.md | Modifié : release et plugin CM |
| CHANGELOG.md | Modifié : trois entrées Unreleased |
| openspec/specs/extension-distribution/spec.md | Modifié : deux exigences ajoutées et deux modifiées |
| plugins/cm/.codex-plugin/plugin.json | Créé : manifeste CM |
| plugins/cm/skills/cm/SKILL.md | Créé : copie embarquée identique |
| openspec/changes/archive/2026-10-19-distribute-cm-plugin/.openspec.yaml | Créé puis archivé |
| openspec/changes/archive/2026-10-19-distribute-cm-plugin/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-distribute-cm-plugin/design.md | Créé puis archivé ; preuves complétées |
| openspec/changes/archive/2026-10-19-distribute-cm-plugin/tasks.md | Créé puis archivé ; onze tâches terminées |
| openspec/changes/archive/2026-10-19-distribute-cm-plugin/specs/extension-distribution/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-distribute-cm-plugin/STATISTIQUES.md | Créé après archivage |

| Catégorie de chemin final | Nombre |
|---|---:|
| Fichier existant modifié | 12 |
| Nouveau fichier | 8 |
| Fichier supprimé | 0 |
| Lien créé ou modifié | 0 |
| Total | 20 |

Les cinq fichiers du change sont créés à l'emplacement actif puis transférés
par OpenSpec ; ce mouvement ne les compte pas deux fois dans les chemins
finaux. Le lien `.agents/skills/cm -> ../../skills/cm` reste inchangé. Les
répertoires temporaires de contrôle du paquet et des tests sont nettoyés.

## 4. Commandes

Sous-ensemble borné aux huit appels de qualification et de cycle ci-dessous.
Les lectures, aides CLI, éditions et audits supplémentaires ne sont pas inclus
comme s'ils formaient un inventaire exhaustif. Toutes les commandes OpenSpec
utilisent `/home/devops/.local/npm/bin/openspec` avec
`OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1`.

| Commande ou contrôle | Exécutions | Réussites | Échecs |
|---|---:|---:|---:|
| openspec validate distribute-cm-plugin --strict | 1 | 1 | 0 |
| Python stdin : quick_validate.py de skill-creator sur les deux copies CM | 1 | 1 | 0 |
| Python DevOps stdin : catalogue, JSON/TOML, paquet isolé, parité, lien et syntaxes | 1 | 1 | 0 |
| /usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v | 1 | 1 | 0 |
| /home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v | 1 | 1 | 0 |
| openspec validate --all --strict, avant puis après archive | 2 | 2 | 0 |
| openspec archive distribute-cm-plugin --json --yes | 1 | 1 | 0 |
| Total borné | 8 | 8 | 0 |

Taux de réussite dans ce sous-ensemble : 100 %. Le validateur des skills est
chargé depuis
`/home/adema261/.codex/skills/.system/skill-creator/scripts/quick_validate.py`.
Le même appel contrôle les deux copies ; il ne représente pas deux commandes.
Les tests couvrent les deux distributions existantes PLLM/TFL avec services
simulés et ne qualifient pas les fournisseurs réels.

Audits supplémentaires exécutés et réussis :

- Vérification des empreintes initiales, des seuls changements attendus et de
  la préservation des 67 fichiers d'archives précédentes.
- Reconstruction des empreintes initiales après substitution de 0.2.3 par
  0.2.2 dans VERSION, TOML et les deux manifestes existants : seules leurs
  versions ont changé.
- UTF-8/LF et fin de ligne finale contrôlés sur 18 fichiers avant
  synchronisation ; contrôle des fichiers finaux avec le rapport après écriture.
- Quatre exigences du delta archivé égales à celles de la spec principale ;
  mots-clés RFC 2119 et longueur des exigences contrôlés.
- Onze tâches terminées, une seule archive créée et aucun change actif restant.
- Paquet CM à deux fichiers réguliers sans scripts, MCP, applications ni
  dépendances externes ; copie isolée dans un chemin avec espaces résolue.
- Syntaxe d'installation confirmée par `codex plugin add --help`, sans exécuter
  d'installation dans le profil.

Compilation Python de fichiers modifiés : non pertinente, aucun fichier
Python modifié. Build web, tests navigateur et fournisseurs : non pertinents
et non exécutés. Publication, installation réelle du plugin et invocation
dans une nouvelle session : non exécutées, hors périmètre validé. Les
contrôles du paquet ne sont pas présentés comme ces opérations.

## 5. Accès web

| Périmètre | Accès | Refus | Erreurs |
|---|---:|---:|---:|
| Reprise SCM après validation couverte par ce rapport | 0 | 0 | 0 |

Aucun appel fournisseur, accès à un secret ou rafraîchissement de marketplace
distante pendant cette reprise. Les liens de documentation et de manifeste
ne constituent pas de nouvelles visites. Les sources officielles avaient
été consultées lors du diagnostic antérieur. Taux web : N/A, dénominateur nul.

## 6. Synthèse globale

| Repère temporel partiel | Heure Europe/Paris |
|---|---|
| Contrôle initial avant écriture de ce change | 2026-10-19 14:00:29 CEST |
| Après archivage, validation stricte et audit, avant le rapport | 2026-10-19 14:04:25 CEST |
| Intervalle | 00 h 03 min 56 s |
| Durée totale SCM | N/A, borne d'exploration initiale complète non instrumentée |

L'intervalle inclut les outils et les attentes. Il ne mesure pas le temps de
génération et exclut la rédaction du rapport et ses contrôles ultérieurs.

| Document de la matrice SCM | Bilan et preuve |
|---|---|
| Projet réel | Trois plugins résolus dans le catalogue ; paquet CM isolé vérifié ; deux copies identiques ; six supports de version à 0.2.3. |
| AGENTS.md | Inchangé, empreinte conservée ; sections 5–6, 8, 12 et 21 suffisantes pour ce périmètre. |
| PROJECT.md | Mis à jour : Organisation et Catalogue actuel décrivent les deux distributions CM et les trois plugins. |
| TECHNICAL.md | Mis à jour : Arborescence, Structure des plugins, Commandes et skills autonomes, Validation précisent copie autonome, paquet embarqué et parité. |
| BUILD.md | Mis à jour : catalogue, Skill catalogue cm et Mise à jour documentent installation, rafraîchissement et double entrée possible. |
| DEVOPS.md | Inchangé, empreinte conservée ; aucun nouveau runtime ou outil, chemins existants utilisés. |
| README.md | Mis à jour : release 0.2.3, plugin CM et maintien du skill autonome ; renvoi à BUILD et limite d'installation. |
| CHANGELOG.md | Mis à jour : trois nouvelles entrées Unreleased ; historique préservé. |
| openspec/specs/ | Extension-distribution synchronisée ; quatre exigences identiques au delta archivé ; six specs strictes valides. Release-versioning reste inchangée, ses invariants sont respectés. |

Le comportement de `$cm` reste un catalogue français des trois invocations,
sans lancement de PLLM/TFL. Le paquet embarqué ajoute un second mode de
distribution. Le risque de double entrée est documenté ; aucune copie
installée n'est retirée ou désactivée. Le repli local est décrit dans design.md.
Aucun écart documentaire restant identifié dans le périmètre.

Contrôle final exécuté et réussi : six sections, vingt chemins existants,
douze modifications et huit créations, totaux de commandes 8/8/0, UTF-8/LF sur
les vingt fichiers finaux. Le lien autonome, la parité des copies, les trois
manifestes à 0.2.3, les onze tâches terminées et l'absence de change actif ou
d'artefact temporaire dans les répertoires contrôlés sont vérifiés.

État : TERMINÉ pour le périmètre local SCM, rapport vérifié et archivage
unique prouvé. Publication, installation réelle et invocation dans une nouvelle
session restent non exécutées conformément au périmètre validé.
