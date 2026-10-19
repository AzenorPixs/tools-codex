## Context

Tools Codex est en 0.3.0 avec quatre plugins. DEVOPS.md désigne le dossier et
l'index des prompts de chaque projet. Dans ce projet, l'index référence GSCM
et GSCMP ; les alias GCM et GCMP ont été validés. CISMP.md supporte les RUN
numérotés et un cycle de changements ; les variantes 1CISMPn bornent ce cycle.

## Goals / Non-Goals

Offrir /prompt LIST et /prompt CODE avec arguments en majuscules, charger le
texte choisi et transmettre au skill les instructions à exécuter. Ne pas
confondre résolution et fin d'exécution. Aucun prompt n'est copié dans le
plugin ; aucune recherche dans les emplacements globaux de Codex. Les tests
ne démarrent aucun RUN réel ni processus CAB.

## Decisions

- Source : skills/prompt/SKILL.md et scripts/resolve_prompt.py ; copie identique
  sous plugins/prompt/skills/prompt/, manifeste, entrée marketplace, commande
  .codex/commands/prompt.md et lien .agents/skills/prompt.
- Le skill relève le projet courant avant d'appeler le script avec
  --project-root. Le répertoire d'installation du skill n'est jamais une
  racine de projet implicite. Le script retourne du JSON, jamais une preuve
  de travail achevé ; le skill lit et exécute ensuite le prompt complet.
- Lire exactement les deux déclarations de DEVOPS.md. Résoudre les chemins
  relatifs depuis le projet. Lire la table Sigle/Prompt/Fichier de l'index ;
  refuser doublons, absences et chemins sortant du dossier déclaré. Les liens
  déclarés peuvent être suivis en lecture si le fichier final reste dans ce
  dossier. Aucun lien n'est créé ou modifié dans le référentiel externe.
- Les noms sont une liste explicite en majuscules. GCM et GCMP sélectionnent
  les entrées GSCM et GSCMP de l'index. Les variantes CISMPn et 1CISMPn
  sélectionnent CISMP.md et transmettent le RUN exact CISMPn.
- LIST lit seulement DEVOPS et l'index, avec disponibilité des chemins. Il ne
  lit ni n'exécute les corps de prompts. Le texte de la liste vient de l'index.
- Un lancement renvoie chemin, texte, instruction équivalente et RUN. Pour
  1CISMPn, les métadonnées bornent max_changes à 1 et prescrivent ensuite
  archive, statistiques et arrêt de la session de codage selon le protocole
  du prompt. La directive explicite borne la boucle de sélection de CISMP :
  ne pas repartir sur un deuxième change et ne pas prétendre que tout le
  travail du dépôt est terminé. Les validations et barrières restent requises.
- /prompt est une commande source et un déclencheur du skill ; $prompt est
  l'invocation de skill directement prise en charge. Pas de promesse de slash
  native enregistrée par la simple présence d'un fichier.
- La release 0.4.0 concerne VERSION, TOML, README et les cinq manifestes.
  Aucun script métier CM/PLLM/TFL/TCU n'est modifié pour ajouter ce plugin.

## Risks / Trade-offs

Une source externe peut changer : la résolution est refaite à chaque invocation
et ne constitue pas un cache. Un prompt peut exiger des informations ou accords ;
le dispatcher conserve ces conditions sans inventer un résultat. Un nom
présent dans LIST peut ne pas avoir de raccourci demandé ; la liste reste
fidèle à l'index. Une résolution correcte ne prouve pas l'exécution d'un RUN.

## Migration Plan

Valider les exigences avant code et tests. Livrer le résolveur et le skill,
mettre à jour les deux catalogues CM, les cadrages et les versions. Tester avec
deux projets et référentiels temporaires, puis LIST sur le vrai DEVOPS en lecture
seule. Valider OpenSpec, synchroniser et archiver uniquement ce change, puis
produire STATISTIQUES.md à six sections. Repli : retirer le nouveau plugin,
skill, commande et lien, puis rétablir versions, catalogue et documents associés.

## Validation

Tests des trente-huit arguments d'exécution, des alias, des huit RUN normaux,
des huit limites à un change, de LIST sans lecture de corps et des projets
distincts. Erreurs : minuscule, nom inconnu, RUN hors bornes, déclaration
absente/ambiguë, index dupliqué, fichier absent, texte invalide et sortie de
dossier. Vérifier paquet isolé, parité, syntaxe, JSON/TOML, huit supports de
release, UTF-8/LF et suite complète sur Python 3.13/3.14. Exécution réelle de
processus de prompts et installation globale : non exécutées.

## Preuves de qualification du 19 octobre 2026

| Contrôle | État et résultat |
|---|---|
| OpenSpec ciblé avant code | Exécuté et réussi : validate add-prompt-dispatcher --strict. |
| Tests ciblés | Exécutés et réussis : 20 tests du dispatcher sur Python système. |
| Suite complète système | Exécutée et réussie : 64 tests, Python 3.13.5. |
| Suite complète DevOps | Exécutée et réussie : 64 tests, Python 3.14.8. |
| LIST réel | Exécuté et réussi : 23 entrées disponibles, dossier /home/devops/datas/prompts et index INDEX.md déclarés par DEVOPS ; aucun corps de prompt lu par cette opération. |
| Formats des skills | Exécutés et réussis : quatre validations CM/prompt par quick_validate.py du skill-creator avec le Python système existant. |
| Syntaxe Python | Exécutée et réussie : trois py_compile, artefacts temporaires sous tests puis nettoyés. |
| Paquet isolé | Exécuté et réussi : exactement manifeste, SKILL.md et résolveur ; LIST et 1CISMP3 sur les deux Python avec un projet de fixture explicite ; aucun RUN réel. |
| Versions et ressources | Exécuté et réussi : huit supports de release 0.4.0, cinq plugins, parité CM/prompt et trois liens locaux vérifiés. |
| Périmètre et encodage | Exécuté et réussi : 134 fichiers initiaux observés, 14 modifications attendues et 120 fichiers préservés avant synchronisation, dont 87 fichiers d'archives ; UTF-8/LF sur 27 fichiers courants. |
| OpenSpec global avant archive | Exécuté et réussi : huit éléments valides. |
| Exécution réelle de prompts, RUN, CAB, publication et installation globale | Non exécutées conformément au périmètre validé ; aucune commande Git ni inspection de son état. |

Les tests utilisent -B -W error::ResourceWarning -m unittest discover -s tests,
avec -q pour les suites complètes et -v pour la cible. OpenSpec utilise le
chemin /home/devops/.local/npm/bin/openspec déclaré dans DEVOPS, avec
OPENSPEC_TELEMETRY=0 et DO_NOT_TRACK=1. Le validateur de skill est chargé depuis
/home/adema261/.codex/skills/.system/skill-creator/scripts/quick_validate.py.
Les contrôles sont proportionnés : aucune nouvelle dépendance ni build web.

Les validations fonctionnelles n'ont pas échoué. Trois opérations de préparation
ont été reprises : remplacement documentaire arrêté sur une apostrophe de
contexte différente avant écriture ; patch mal formé rejeté avant écriture ;
appel d'audit arrêté par une erreur de délimitation JavaScript avant lancement
de commande. Leurs relances ont réussi, sans désactiver de test ni élargir le
périmètre. Elles sont distinguées des résultats des commandes de qualification.

## Matrice de cohérence documentaire

| Élément | État et preuve |
|---|---|
| Projet réel | Cinq plugins et trois liens locaux résolus ; commande prompt et deux distributions identiques ; huit supports 0.4.0 vérifiés. |
| AGENTS.md | Inchangé, empreinte conservée : règles générales et autorité DEVOPS pour les prompts suffisantes. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel et Lancement de prompts décrivent les arguments, alias et limites à un change. |
| TECHNICAL.md | Mis à jour : cinquième plugin, ressources, prérequis et Résolution et lancement de prompts décrivent les limites et la qualification. |
| BUILD.md | Mis à jour : catalogue, installation, Utilisation de prompt, modes et vérification avant publication. |
| DEVOPS.md | Inchangé, empreinte conservée : ses déclarations réelles de dossier/index ont été utilisées, aucun nouveau prérequis à inventorier. |
| README.md | Mis à jour : release 0.4.0 et exemples LIST, CISMP3 et 1CISMP3 ; renvoi aux arguments détaillés. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased ; historique conservé. |
| openspec/specs/ | Prompt-dispatch et extension-distribution synchronisées ; dix exigences identiques aux deltas archivés et huit specs strictes valides. Release-versioning inchangée. |

Le mode à un change borne la boucle et les preuves de terminaison à ce change,
avec les clôtures requises de sa session, sans prétendre vider le dépôt. La
qualification vérifie les métadonnées et directives de ce contrat ; elle ne
prouve pas l'exécution opérationnelle d'un RUN piloté, volontairement exclue.

## Clôture OpenSpec

L'archive 2026-10-19-add-prompt-dispatcher est créée et vérifiée. Elle a
synchronisé huit exigences ajoutées et deux modifiées. Le Purpose de la
nouvelle capacité est rédigé et conservé. Le contrôle strict après archive
réussit sur huit spécifications ; les onze tâches sont terminées et aucun
change actif ne reste. Les empreintes identifient 15 fichiers initiaux
modifiés et 119 préservés sur 134, dont les 87 fichiers des archives précédentes.
Le rapport STATISTIQUES.md est produit après archivage puis vérifié.
