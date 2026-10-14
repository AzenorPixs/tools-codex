# Design

## Context

Le périmètre initial approuvé est documentaire et spécificatif. Les scripts se trouvent
dans les skills autonomes et leurs copies embarquées ; `src/` et `tests/`
étaient vides lors de l'analyse. OpenSpec contenait une spécification principale
`release-versioning`, aucune évolution active et huit archives, dont sept
relatives à CAB. L'état Git, les données générées et les configurations locales
n'ont pas été inspectés.

## Goals / Non-Goals

**Goals:** rendre les prérequis et limites explicites, supprimer les
contradictions documentaires arbitrées et préparer des contrats traçables aux
capacités existantes. Distinguer contrats, lecture de code, validations
structurelles et preuves de fonctionnement.

**Non-Goals des lots initiaux:** corriger le code, initialiser des données, modifier les versions,
choisir une version minimale de Python, installer des outils, accéder aux
fournisseurs, créer une automatisation, synchroniser les specs ou archiver.
Les archives CAB sont préservées ; aucune provenance n'est déduite et aucune
tâche historique non cochée ne justifie leur réouverture.

## Decisions

- Préparer les cinq capacités dans les deltas de ce seul change. Leur présence
  et leur validation stricte ne signifient ni synchronisation des specs
  principales ni conformité fonctionnelle des scripts.
- Reprendre les contrats des skills et cadrages, avec les arbitrages de L2 :
  PLLM `active` reste silencieux, le type de débit reste dans le JSON, le
  protocole documentaire porte le numéro 5 et TFL `auto` ne bascule de secret
  que lors de sa récupération. Aucun repli après refus API n'est ajouté.
- Ne pas transformer une limite de code en exigence fonctionnelle souhaitée.
  Les chemins actuels et le fichier initial PLLM sont documentés comme
  dépendances observées. Une politique valide exige des mesures concluantes
  du modèle effectivement sélectionné, y compris après un repli.
- Conserver le registre ci-dessous et des tâches non cochées pour le travail
  non prouvé. Les extensions fonctionnelles autorisées ultérieurement sont
  décrites séparément ci-dessous.

## Registre de suivi CGP

Les états historiques ci-dessous sont complétés par le bilan SCM final.

| ID | Faits et sources | État après les lots documentaires | Suite et dépendances |
|---|---|---|---|
| CGP-01 | Les cinq contrats restaient dans le change actif. | Les cinq spécifications sont synchronisées ; release-versioning est complétée. Validation stricte réussie avant et après archivage. | Résolu : synchronisation, archivage et rapport d’archive vérifiés dans le périmètre validé. |
| CGP-02 | Sept archives décrivent CAB hors du catalogue actuel. | Statut historique observé explicité dans `PROJECT.md` ; provenance non vérifiée. | Aucune modification des archives ; leur provenance reste à trancher si nécessaire. |
| CGP-03 | Le catalogue voisin ne convenait pas aux plugins séparés. | Corrigé par `--tfl-catalog`, utilisé pour OpenCode Go, OpenRouter et les replis ; défaut conservé. Tests hors ligne réussis dans deux emplacements isolés et les deux distributions. | Installation réelle dans Codex non exécutée ; reste un contrôle de publication distinct. |
| CGP-04 | Le démarrage exigeait un fichier courant initial. | Corrigé : quatre politiques initialisées sans résultats inventés ; fichier valide chargé et fichier corrompu préservé avant toute publication. Tests hors ligne réussis. | Qualification fournisseur non exécutée ; initialisation seule ne prouve aucune disponibilité. |
| CGP-05 | Le dernier palier après HTTP 429 pouvait valider un remplaçant non mesuré et réutiliser les paliers du précédent. | Corrigé : candidats bornés, paliers recalculés, quotas recontrôlés, mesures propres au remplaçant et échec sans sélection lorsque les candidats sont épuisés. Tests hors ligne réussis. | Limites de performance et disponibilité réelles non mesurées pendant SCM. |
| CGP-06 | Les instructions PLLM contredisaient les règles de débit et de silence ; leur titre indiquait le protocole 4. La reprise a relevé une contradiction résiduelle entre l'affichage utilisé/restant demandé et `quota_display`, limité au restant. | L2 a harmonisé le débit, le silence et le protocole. L5 est appliqué et vérifié : les deux copies demandent d'afficher le restant et de conserver l'utilisation dans les quotas bruts du JSON, sans changer le rendu. | Contradiction documentaire résolue ; structure des deux skills validée et copies identiques. Fonctionnement réel non testé. |
| CGP-07 | La métadonnée Python 0.0.0 avait un rôle indéterminé et différait de la release. | Décision validée et appliquée : project.version = 0.2.1, aligné sur VERSION ; métadonnées/prérequis du dépôt sans packaging ni publication Python ajoutés. | Contrôle TOML et alignement réussis sur les deux interpréteurs ; aucune décision restante. |
| CGP-08 | La plage Python et sa qualification restaient indéterminées. | Décision validée : >=3.13,<3.15. Python 3.13.5 et 3.14.8 réussissent chacun les 19 tests, 7 compilations, 7 imports et le fuseau Paris. | Qualification hors ligne acquise ; installation Codex et fournisseurs restent des contrôles distincts de publication. |
| CGP-09 | TFL `select_secret` choisit un secret avant `fetch_models`, sans repli sur erreur API. | Documentation alignée sur ce comportement. | Aucune extension du repli ; une évolution exigerait une demande distincte. |
| CGP-10 | Les prix OpenRouter non finis pouvaient échapper aux filtres. | Corrigé : exclusion motivée des valeurs non finies et débordements ; sérialisation JSON stricte avant publication. Tests de filtrage et publication réussis. | Les prix fournisseurs actuels ne sont pas vérifiés par cette qualification hors ligne. |

Les sources des scripts cités ont des copies embarquées identiques au début
de la session ; elles restent inchangées. Les contrats ne fournissent pas de
preuve d'exécution des scénarios ci-dessus.

Les lots L4 et L5 ont été explicitement validés par le développeur lors de la
reprise CGP du 10 octobre 2026. L4 complète ce registre, les tâches de
qualification et les limites de `TECHNICAL.md`. L5 harmonise uniquement
l'instruction d'affichage des quotas dans les deux copies de PLLM. Ces lots
ne modifient ni les scripts ni les exigences des deltas ; ils n'autorisent
aucune qualification fournisseur, synchronisation ou archive.

## Validation Strategy

- Valider les quatre skills modifiés avec le vérificateur de `skill-creator`
  et comparer les copies autonomes et embarquées.
- Vérifier UTF-8/LF, les liens internes ajoutés, les scénarios de chaque
  exigence, la correspondance entre proposition et deltas et le périmètre des
  fichiers touchés sans inspecter Git.
- Employer le chemin OpenSpec déclaré par `DEVOPS.md` pour la validation
  stricte du change, puis des specs principales et changes actifs.
- N'exécuter aucun script fournisseur ni test d'installation pendant ces lots.
  Aucun test de comportement n'est remplacé par une validation de syntaxe.

## Résultats observés le 10 octobre 2026

- L1 et L2 sont appliqués : trois cadrages et quatre fichiers de skills
  modifiés, sans modification de script. Les deux paires de skills restent
  identiques octet pour octet.
- Les quatre contrôles `quick_validate.py` ont réussi avec `/usr/bin/python3`,
  sans écriture de bytecode. Le premier essai avec le Python DevOps a échoué
  car `PyYAML` y est absent ; aucune dépendance n'a été installée. Ce repli
  concerne le vérificateur documentaire, pas une qualification Python du projet.
- Le premier contrôle OpenSpec strict a retourné 1 pour dix avertissements
  de longueur d'exigence. Après leur scission sans changement de contrat,
  les cinq deltas contiennent 38 exigences et 41 scénarios ; aucune exigence
  ne dépasse 500 caractères.
- `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate document-existing-extension-contracts --strict`
  a retourné 0, sans avertissement.
- `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict`
  a retourné 0 : le change et `release-versioning` sont validés, soit 2 éléments
  réussis et 0 échec.
- Le contrôle des sources autorisées par empreintes a constaté sept fichiers
  existants modifiés, neuf fichiers ajoutés dans ce seul change, aucune
  suppression et 78 fichiers préexistants inchangés. Les 16 fichiers touchés
  sont en UTF-8/LF ; les liens Markdown internes contrôlés sont présents.
- Aucun test fournisseur, test d'installation, accès aux secrets, contrôle Git,
  synchronisation ni archivage n'a été effectué. Les écarts CGP-03 à CGP-05
  ne sont pas corrigés et les décisions de CGP-07 et CGP-08 restent ouvertes.

## Résultats des lots L4 et L5 le 10 octobre 2026

- L4 complète CGP-05, CGP-06 et CGP-10, le suivi de qualification et les
  limites techniques. L5 applique l'arbitrage d'affichage aux deux copies de
  PLLM. Aucun script ni contrat normatif n'est modifié.
- Les deux contrôles `quick_validate.py` ont retourné 0 avec
  `/usr/bin/python3 -B`. Les copies PLLM sont identiques octet pour octet.
- Les validations OpenSpec strictes du change et de `--all` ont retourné 0,
  sans avertissement : 2 éléments réussis et 0 échec pour le contrôle global.
- Le contrôle par empreintes des 43 sources autorisées suivies constate
  exactement les cinq fichiers approuvés modifiés et 38 sources inchangées.
  Les cinq fichiers sont en UTF-8/LF. Les six tâches cochées sont préservées ;
  les huit tâches ouvertes incluent la nouvelle qualification CGP-10.
- Aucun test fonctionnel ou fournisseur, installation, accès aux secrets,
  contrôle Git, synchronisation ni archivage n'a été effectué. CGP-03 à
  CGP-05 et CGP-10 restent à qualifier dans une session SCM ; les décisions
  de CGP-07 et CGP-08 restent ouvertes. Ces résultats clôturent les seuls
  lots documentaires approuvés et ne prouvent pas la conformité fonctionnelle.

## Risks / Trade-offs

L'absence de synchronisation laisse volontairement les contrats dans ce
change actif. Le risque principal est de confondre ce dossier préparé avec une
livraison fonctionnelle : les tâches de qualification et de cycle restent
non achevées. La compatibilité Python et le rôle de la version Python ne sont
pas déduits de l'environnement inventorié.

## Migration Plan

Aucune migration runtime ni reprise de données. Appliquer les seuls lots
approuvés, contrôler leurs résultats et conserver le change préparé. Une
session SCM distincte doit traiter les écarts fonctionnels avant toute
affirmation de conformité. La synchronisation et l'archivage sont des lots
ultérieurs distincts ; aucun archivage n'est actuellement autorisé.

## Évolution ciblée du seuil et de la release — 10 octobre 2026

La demande ultérieure du développeur autorise uniquement le passage du TTFT
strict à moins de 90 secondes et la release 0.2.1 pour le projet et ses deux
plugins. Une constante commune au contrôle et à la couleur porte ce seuil
dans chaque copie du script. Les critères JSON sont actualisés pour les
politiques réellement réévaluées ; les rapports historiques ne sont pas
réécrits. Des tests hors ligne couvrent les bornes, le débit inchangé et
l’arrêt avant benchmark lorsque le quota est invalide. Cette extension ne
résout pas les autres écarts CGP et n’autorise ni publication, installation,
synchronisation ni archivage.

Validation de cette évolution : les quatre tests hors ligne réussissent pour
les deux distributions ; les trois fichiers Python compilent. Les contrôles
de structure des deux skills, UTF-8/LF, d’identité des copies et de version
0.2.1 réussissent. La validation OpenSpec stricte globale réussit avec deux
éléments et zéro échec. Aucun rapport fournisseur historique n’est régénéré.

## Correction SCM autorisée — CGP-03 à CGP-05 et CGP-10

Le développeur valide les quatre corrections et leurs contrats précis :

- Un chemin `--tfl-catalog` explicite est partagé par toutes les résolutions
  PLLM, y compris OpenRouter et les replis. Le défaut relatif est conservé ;
  aucune découverte de configuration privée n'est ajoutée.
- L'absence du fichier courant initialise les quatre politiques connues sans
  résultat historique. Un historique invalide bloque avant toute publication.
- Une boucle bornée par les candidats du catalogue recalcule les paliers à
  chaque changement de configuration. Seul un benchmark concluant autorise
  la validité ; les quotas sont recontrôlés avant chaque nouvelle requête.
- Les prix non finis et les débordements de calcul TFL sont exclus avec motif.
  La sérialisation stricte est préparée avant de remplacer les fichiers.

Les tests utilisent des copies de distributions dans des emplacements isolés,
des fixtures et des services simulés. Ils ne prouvent pas une installation
réelle dans Codex ni la disponibilité des fournisseurs. Les seuils 90 s et
15 tokens/s, la limite de requête 120 s, les modes forcés, le silence `active`
et la release 0.2.1 sont préservés. Les fichiers concernés sont ceux de la
proposition SCM validée ; aucun autre change actif n'est créé.

Les décisions CGP-07/08 et la tâche 3.4 restent hors périmètre. Le change ne
sera ni synchronisé ni archivé tant que ces conditions de clôture manquent.

## Bilan terminal SCM — correctifs qualifiés, archivage bloqué

Le développeur a validé les quatre correctifs, leur périmètre précis et la
limite de terminaison liée aux décisions Python. CGP-03 à CGP-05 et CGP-10
sont corrigés et qualifiés hors ligne. La session s'arrête à l'état autorisé
`BLOQUÉ` pour le cycle d'archivage, sans déclarer le change entièrement livré.
La tâche 3.4 (CGP-07/08) et les tâches 4.1 à 4.3 restent ouvertes. Aucun autre
change, synchronisation, archive ou rapport d'archive n'est créé.

### Preuves de validation

- Les contrats complétés ont passé la validation stricte du change avant toute
  écriture de code ou de test.
- `/home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v`
  réussit : 19 tests, dont les quatre tests TTFT existants inchangés. Les deux
  distributions sont couvertes avec services simulés et réseau interdit dans
  les tests de qualification. L'avertissement initial de ressource d'une
  fixture HTTP a été corrigé ; le contrôle final ne produit pas d'avertissement.
- Les cinq fichiers Python modifiés ou créés compilent avec `py_compile` du
  Python DevOps. Les caches temporaires créés dans `tests/` sont nettoyés.
- Les deux skills PLLM passent `quick_validate.py` avec `/usr/bin/python3 -B`.
  Les deux paires de scripts et la paire de skills PLLM sont identiques.
- `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict`
  réussit : deux éléments, zéro échec, sans avertissement.
- Sur les 44 sources initialement suivies par empreintes, 18 sont modifiées et
  26 restent inchangées ; seul `tests/test_extension_qualification.py` est
  ajouté, sans suppression. Les 19 fichiers touchés sont en UTF-8/LF et leurs
  liens internes contrôlés sont présents. Aucun état Git n'est inspecté.
- Release 0.2.1, TTFT strictement inférieur à 90 secondes, débit strictement
  supérieur à 15 tokens/s, limite de requête 120 secondes, modes forcés et
  publication `active` silencieuse sont préservés.
- Aucun fournisseur, trousseau, configuration privée, installation réelle,
  migration ou service OpenCode/CAB n'est sollicité. Les tests utilisent
  uniquement des fixtures temporaires contrôlées dans le projet. Lint et
  typage : aucun mécanisme configuré identifié dans `pyproject.toml`.

### Fichiers du périmètre

- OpenSpec : `.openspec.yaml`, `proposal.md`, `design.md`, `tasks.md`,
  `specs/pllm-evaluation/spec.md` et `specs/tfl-catalog/spec.md` dans ce change.
- Scripts : `skills/pllm/scripts/evaluate.py`,
  `plugins/pllm/skills/pllm/scripts/evaluate.py`,
  `skills/tfl/scripts/test_fournisseur_llm.py` et
  `plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py`.
- Instructions : `skills/pllm/SKILL.md`, `plugins/pllm/skills/pllm/SKILL.md`,
  `.codex/commands/pllm.md` et `.codex/commands/cm.md`.
- Documentation : `TECHNICAL.md`, `BUILD.md`, `README.md` et `CHANGELOG.md`.
- Test créé : `tests/test_extension_qualification.py`.

### Matrice documentaire finale

| Élément | État et preuve dans le périmètre SCM |
|---|---|
| Projet réel | Correctifs locaux qualifiés par les 19 tests ; installation et fournisseurs réels non vérifiés. |
| `AGENTS.md` | Inchangé par empreinte : règles de sécurité et de validation conservées. |
| `PROJECT.md` | Inchangé par empreinte : catalogue, responsabilités et architecture restent applicables. |
| `TECHNICAL.md` | Mis à jour : prérequis, catalogue explicite, initialisation et suite de validation hors ligne. |
| `BUILD.md` | Mis à jour : commande avec catalogue explicite, premier démarrage et limite du test d'installation. |
| `DEVOPS.md` | Inchangé par empreinte : aucun outil ou environnement installé ; Python et OpenSpec déclarés utilisés. |
| `README.md` | Mis à jour : option, initialisation, préservation et filtrage ; release 0.2.1 conservée. |
| `CHANGELOG.md` | Mis à jour : entrée Unreleased pour les quatre correctifs, sans nouvelle release. |
| `openspec/specs/` | Inchangé par empreinte : release-versioning préservé, aucune synchronisation. |
| Change actif | Contrats PLLM/TFL complétés, tâches du périmètre cochées et preuves consignées ; décisions Python et archivage restent ouverts. |

## Décisions de clôture CGP-07/08 validées

Le développeur valide `project.version = "0.2.1"` et
`requires-python = ">=3.13,<3.15"`. `VERSION` reste la source de vérité ;
`pyproject.toml` décrit les métadonnées et prérequis du dépôt sans introduire
de packaging ou publication Python. Cette plage exclut explicitement Python
antérieur à 3.13 et à partir de 3.15. Aucun script ni dépendance n'est modifié.

Les trois lots autorisés couvrent les contrats, métadonnées et documents,
puis la qualification des branches 3.13/3.14 et enfin la synchronisation,
l'archivage de ce seul change et son rapport. Cette autorisation remplace le
blocage historique décrit plus haut ; elle ne transforme pas les tests hors
ligne en qualification d'une installation Codex ou des fournisseurs.

Avant synchronisation : valider les contrats, appliquer les métadonnées,
réussir les 19 tests sur chaque interpréteur, compiler tous les scripts et
tests, vérifier les imports et `ZoneInfo("Europe/Paris")`, les copies, les
versions, UTF-8/LF et OpenSpec strict. Les jalons d'archivage et de rapport
restent obligatoires et ne sont déclarés réalisés qu'après leurs preuves.

## Qualification Python de clôture — preuves du 10 octobre 2026

| Contrôle | Python 3.13.5 (`/usr/bin/python3`) | Python 3.14.8 (Python DevOps) |
|---|---|---|
| Tests unittest, avertissements ResourceWarning traités en erreurs | 19 réussis, 0 échec | 19 réussis, 0 échec |
| Compilation avec py_compile | 7 fichiers réussis | 7 fichiers réussis |
| Imports sans exécution des générateurs | 7 fichiers réussis | 7 fichiers réussis |
| `ZoneInfo("Europe/Paris")` | Réussi | Réussi |
| TOML, version 0.2.1 et plage >=3.13,<3.15 | Conformes | Conformes |

Les sept fichiers sont les cinq scripts distribués et les deux modules de
 tests existants. Aucun script ni test n'a changé durant ce lot. Les caches
 temporaires sous `tests/` ont été nettoyés. Les deux commandes de test sont :

- `/usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v`
- `/home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v`

Le contrat OpenSpec complété a été validé strictement avant l'application des
métadonnées. CGP-07/08 sont résolus et la tâche 3.4 est prouvée. Le blocage
historique d'archivage est levé par ces preuves et l'autorisation du développeur.
Les jalons 4.2 et 4.3 restent en attente de leurs opérations effectives.

### Matrice documentaire avant synchronisation

| Document | État et justification |
|---|---|
| `AGENTS.md` | Inchangé : règles applicables respectées, aucune modification nécessaire. |
| `PROJECT.md` | Inchangé : responsabilités, architecture et source de release restent applicables. |
| `TECHNICAL.md` | Mis à jour : rôle de pyproject, plage Python et protocole de qualification. |
| `BUILD.md` | Mis à jour : prérequis Python 3.13/3.14 ; aucun packaging ou installation ajouté. |
| `DEVOPS.md` | Inchangé : inventaire généré conservé, aucun environnement installé ou modifié. |
| `README.md` | Mis à jour : branches Python supportées et métadonnée alignée. |
| `CHANGELOG.md` | Entrée Unreleased complétée, sans nouvelle release. |
| `pyproject.toml` | Version 0.2.1, plage >=3.13,<3.15, dépendances inchangées. |
| OpenSpec | Contrats complétés et qualification prouvée ; synchronisation puis archivage autorisés. |

### Synchronisation prouvée et éligibilité à l'archivage

Les cinq spécifications préparées ont été créées dans `openspec/specs/` et
`release-versioning` a reçu l'exigence de métadonnée Python. La validation
stricte globale réussit après synchronisation : 7 éléments, 0 échec et aucun
avertissement. La tâche 4.1 est prouvée ; les 21 tâches préparatoires sont
cochées. Les jalons obligatoires 4.2 et 4.3 restent en attente de leur preuve.

L'archivage CLI conserve la validation et utilise `--skip-specs` uniquement
parce que la synchronisation complète est déjà réalisée et contrôlée. Le
mode JSON non interactif correspond à l'autorisation explicite de ce cycle.
Aucun skip de validation, publication, Git, fournisseur ou service n'est
inclus. L'état est prêt pour l'archivage de ce seul change.

### Archivage réussi — jalon 4.2 prouvé

La commande `openspec archive document-existing-extension-contracts --json --skip-specs`
a retourné 0 et désigné `2026-10-10-document-existing-extension-contracts`.
Le dossier actif a disparu ; les dix fichiers ont été transférés avec les
mêmes empreintes, et les six specs synchronisées sont restées inchangées.
La validation stricte globale après archivage retourne 0 : six specs validées,
zéro échec et aucun avertissement. Aucune autre archive n'est reprise.
Le seul jalon restant est 4.3 : produire et vérifier `STATISTIQUES.md`.

## Clôture finale conforme — TERMINÉ

Ce bilan remplace les états historiques de blocage précédents. Les décisions
CGP-07/08 sont appliquées et qualifiées ; les six contrats sont synchronisés,
ce seul change est archivé et son STATISTIQUES.md est produit et vérifié.
Les 21 tâches préparatoires et les deux jalons de clôture sont prouvés.

Le rapport comporte exactement six sections de niveau 2, les deux tables
 d'agents, des chemins absolus présents, des libellés de commandes bornés à
100 caractères et des totaux cohérents : 22 chemins finaux, 11 modifications,
7 créations et 10 déplacements logiques. Les mesures absentes restent N/A
avec cause ; la durée instrumentée porte seulement sur la phase de clôture.
La qualification compte 19 tests sur chaque interpréteur (38 exécutions),
14 compilations et 14 imports. Aucune mesure fournisseur n'est déduite.

La matrice finale est conforme dans le périmètre autorisé :

| Élément | État final et preuve |
|---|---|
| Projet réel | Corrections précédentes préservées ; qualification Python 3.13.5/3.14.8 réussie. |
| AGENTS.md | Inchangé par empreinte, règles respectées. |
| PROJECT.md | Inchangé par empreinte, catalogue et source de release applicables. |
| TECHNICAL.md | Mis à jour : rôle des métadonnées, plage Python et validation. |
| BUILD.md | Mis à jour : prérequis Python et portée de qualification. |
| DEVOPS.md | Inchangé par empreinte : inventaire conservé, aucun outil installé. |
| README.md | Mis à jour : plage supportée, release 0.2.1 préservée. |
| CHANGELOG.md | Unreleased complété sans nouvelle release. |
| pyproject.toml | Version alignée 0.2.1, requires-python >=3.13,<3.15, dépendances préservées. |
| openspec/specs/ | Six specs, 47 exigences et 55 scénarios ; validation stricte après archive réussie, 6 éléments et 0 échec. |
| Archive ciblée | Dix fichiers transférés, preuves de clôture complétées et rapport obligatoire vérifié. |

Les huit archives antérieures et les scripts/tests sont préservés. Aucun
fournisseur, secret, installation réelle Codex, Git, infrastructure ou service
OpenCode/CAB n'est sollicité. L'installation réelle et la disponibilité des
fournisseurs restent des contrôles distincts avant publication ; elles ne
sont pas annoncées réussies ni requises par le périmètre de clôture validé.
Aucun nouveau change n'est sélectionné.
