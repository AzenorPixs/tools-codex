## Context

Les skills autonomes sont conservés sous `skills/`. Codex découvre les skills
du dépôt sous `.agents/skills/` et suit les liens symboliques de répertoires.
Référence consultée lors du diagnostic :
https://learn.chatgpt.com/docs/build-skills.

## Goals / Non-Goals

Fournir `$cm` comme catalogue français des trois invocations maison existantes,
sans exécution de générateur ni ajout de dépendance. Préserver PLLM/TFL et les
autres skills. Ne pas installer de fichier hors du projet ni publier de release.

## Decisions

- Source canonique : `skills/cm/SKILL.md`, sans script ni métadonnée facultative.
- Découverte locale : `.agents/skills/cm -> ../../skills/cm`. Ce lien relatif
  conserve la portabilité et évite deux copies à maintenir.
- Catalogue : `$cm`, `$pllm [active|MODE] [--tfl-catalog CHEMIN]`,
  `$tfl [auto|mode1|mode2]`, avec les colonnes Commande, Utilisation, Description.
- Les fichiers `.codex/commands/pllm.md` et `tfl.md` restent des sources
  historiques ; leur présence ne promet pas un enregistrement natif de slash.
- Release : 0.2.2 dans VERSION, pyproject.toml, README et les deux manifestes.
- Les exigences de `release-versioning` restent inchangées : aucune version
  indépendante n'est ajoutée aux skills.

## Risks / Trade-offs

Le remplacement de `/cm` par `$cm` est une rupture explicite. La découverte
dépend du chargement effectif des skills par Codex. Le contrôle du lien et du
format ne prouve pas une invocation dans une nouvelle session ; cette limite
est conservée dans les preuves et dans la documentation. Hors du dépôt, le
skill doit être installé dans un emplacement de skills reconnu.

## Migration Plan

Créer et valider le change avant le skill. Transférer le catalogue, créer le
lien, supprimer l'ancienne commande et actualiser les documents et versions.
Valider le skill, la structure, la release, les tests existants et OpenSpec.
Synchroniser et archiver uniquement ce change lorsqu'il est éligible, puis
produire et vérifier STATISTIQUES.md avec les six sections requises.

Repli local : restaurer le contenu initial de `.codex/commands/cm.md`, retirer
le skill et son lien, puis rétablir les documents, versions et spécifications
associés. Aucun stockage de données ni migration irréversible n'est impliqué.

## Validation

- Format : validateur `quick_validate.py` du skill-creator.
- Découverte : lien relatif existant, résolu vers la source unique dans le projet.
- Catalogue : revue des trois syntaxes contre les skills et commandes préservés.
- Release : analyse TOML/JSON et égalité à 0.2.2 des artefacts publiés.
- Régression : suite unittest existante sur Python 3.13 et 3.14 si disponibles.
- Cohérence : UTF-8/LF, empreintes des sources préservées, revue documentaire,
  OpenSpec strict avant et après archivage.
- Invocation effective dans une nouvelle session : contrôle distinct, sans
  affirmation de réussite tant qu'il n'a pas été réalisé.

## Preuves de validation du 19 octobre 2026

- `python3 -B /home/adema261/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/cm` : exécutée et réussie.
- `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate migrate-cm-to-skill --strict` : exécutée et réussie avant implémentation.
- `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict` : exécutée et réussie avant archivage, sept éléments, aucun échec.
- `/usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` : exécutée et réussie, 19 tests, Python 3.13.5.
- `/home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v` : exécutée et réussie, 19 tests, Python 3.14.8.
- Contrôle Python par stdin : exécuté et réussi pour le lien relatif, sa
  résolution vers le fichier canonique, une copie déplacée dans un chemin avec
  espaces, la suppression de l'ancienne commande, les trois syntaxes et les
  métadonnées JSON/TOML de release. Les fichiers temporaires sont nettoyés.
- Contrôle des 15 fichiers créés ou modifiés avant synchronisation : UTF-8/LF
  et fin de ligne finale exécutés et réussis.
- Comparaison SHA-256 sur 97 fichiers observés avant écriture : 10 chemins
  initiaux changés dans le périmètre prévu, dont une suppression ; 87
  préservés avant synchronisation. La spec principale changera lors de la
  synchronisation autorisée. Cette observation ciblée ne prétend pas être un
  inventaire de l'ensemble du dépôt.
- Compilation de fichiers Python modifiés : non pertinente, aucun fichier
  Python modifié. Tests navigateur et appels fournisseurs : non pertinents.
- Invocation effective de `$cm` dans une nouvelle session : non exécutée,
  aucune nouvelle session n'a été lancée. Le contrôle local de découverte est
  distinct et réussi ; cette limite ne constitue pas une preuve d'exécution.

## Matrice de cohérence documentaire

| Élément | État et preuve observée |
|---|---|
| Projet réel | Source `skills/cm/SKILL.md` et lien `.agents/skills/cm` résolus ; commande cm supprimée ; release 0.2.2 contrôlée. |
| AGENTS.md | Inchangé : sections 5–6, 8, 12 et 21 couvrent les éditions autorisées, OpenSpec, Git et les validations ; empreinte conservée. |
| PROJECT.md | Mis à jour : Organisation et Catalogue actuel décrivent le skill et distinguent les commandes sources conservées. |
| TECHNICAL.md | Mis à jour : Arborescence, Commandes et skills autonomes, Prérequis et Validation décrivent le lien, l'invocation et la qualification locale. |
| BUILD.md | Mis à jour : Skill catalogue cm décrit découverte locale, copie autonome dans un autre projet ou emplacement personnel, et contrôle effectif distinct. |
| DEVOPS.md | Inchangé : rubriques Python, OpenSpec et Prompts utilisées ; aucun nouveau runtime ni outil requis ; empreinte conservée. |
| README.md | Mis à jour : release 0.2.2, `$cm`, source et renvoi à BUILD. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased pour le remplacement, la découverte et la release ; historique 0.2.1 conservé. |
| openspec/specs/ | Delta extension-distribution validé avant implémentation puis synchronisé par l'archivage. Égalité des trois exigences entre delta archivé et spec principale contrôlée. Release-versioning reste inchangé : ses invariants sont respectés. |

Aucun écart documentaire restant identifié dans ce périmètre. La qualification
locale et le test effectif de nouvelle session restent explicitement distincts.

## Clôture OpenSpec

L'archivage a créé `2026-10-19-migrate-cm-to-skill` le 19 octobre 2026 et
synchronisé une exigence ajoutée et deux modifiées, sans suppression ni
renommage d'exigence. Le premier appel JSON sans confirmation a retourné
`archive_confirmation_required` sans créer d'archive. L'appel avec `--yes`,
dans le périmètre d'archivage déjà validé, a réussi.

Le premier contrôle strict post-archive a échoué sur la longueur de
l'exigence de catalogue. Ses syntaxes ont été déplacées dans le scénario,
dans la spec principale et son delta archivé. L'exigence conserve le même
comportement et compte désormais 438 caractères. Le contrôle strict suivant
a réussi : six spécifications, aucun échec. Aucun second archivage n'a été
effectué. Les onze tâches sont terminées ; aucun change actif ne reste.

Le rapport `STATISTIQUES.md` de cette archive consigne le bilan, les commandes,
les fichiers, les contrôles et leurs limites sans télémétrie de pilotage.
