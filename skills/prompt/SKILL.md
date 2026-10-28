---
name: prompt
description: Lister ou lancer les prompts du projet courant via $prompt CODE ou /PROMPT CODE, avec codes en MAJUSCULE et référentiel défini exclusivement dans DEVOPS.md.
---

Ce skill lance le processus du prompt demandé ; une résolution de fichier ne
signifie pas que ce processus est terminé. Une demande de création ou de
modification de ce plugin ne lance aucun des prompts qu'il distribue.

Nom affiché du plugin, du skill et de la commande : **PROMPT**. Les chemins
et l’invocation technique `$prompt` restent compatibles.

## Résolution

Relève la racine réelle du projet courant dans le contexte de la tâche.
Utilise exclusivement son `DEVOPS.md` pour le dossier et l'index de prompts.
Ne prends pas le dossier d'installation de ce skill comme racine du projet.
N'utilise aucun chemin global de repli ni copie de prompt embarquée.

Demande l'argument s'il manque. Il est obligatoire et en MAJUSCULE :

- `LIST` ;
- `ACSP`, `ACSM`, `ACSMP`, `CGP`, `CISM`, `DOP`, `DOPP`, `EDP` ;
- `GCM`, `GCMP`, `ISM`, `ISMP`, `PPSC`, `PPSCP`, `RCAM`, `RCAMP` ;
- `SPCM`, `SPCMP`, `RSM`, `RSMP`, `SCM`, `SCMP` ;
- `CISMPx` et `1CISMPx`, où `x` est un entier décimal ASCII strictement
  positif sans zéro initial, sans borne supérieure.

Les alias validés sont `GCM → GSCM.md` et `GCMP → GSCMP.md`. Toutes les
variantes CISMP sélectionnent toutes `CISMP.md`, avec le RUN exact `CISMPn`.
Ne transforme pas silencieusement un argument invalide ou en minuscules.

Appelle réellement le script situé dans ce skill, en passant explicitement
le projet relevé et en préservant chaque chemin comme un argument distinct :

```text
python3 -B <skill>/scripts/resolve_prompt.py CODE --project-root <projet>
```

Le script est un résolveur en lecture seule. En cas d'erreur, restitue le
blocage sans chercher dans un autre dossier, créer un fichier manquant ou
modifier DEVOPS.md, l'index ou les prompts.

## LIST

Affiche les entrées JSON `entries` en tableau français : Sigle, Prompt,
Fichier, Disponibilité. Les intitulés et fichiers viennent de l'index réel.
Ne lis pas les corps et ne lance aucun prompt. Explique si nécessaire que
les entrées GSCM/GSCMP se lancent avec les alias GCM/GCMP et que CISMP utilise
les variantes numérotées prévues. N'invente pas de raccourci pour une entrée.

## Exécution

Pour le mode `execute`, lis intégralement `prompt_text` et l'instruction
équivalente retournés. Si la sortie est tronquée, lis le fichier `prompt_path`
avec un outil de lecture avant de poursuivre. Respecte les règles du projet.

Exécute réellement le processus de ce prompt dans le projet courant jusqu'à
son état terminal, ou jusqu'à une condition du prompt imposant de rendre la
main. Ne t'arrête pas à l'affichage du texte, du chemin ou d'un plan. Respecte
les validations requises, les préconditions et les informations manquantes ;
n'invente ni accord, ni RUN, ni résultat. Le statut `ready` du résolveur est
une préparation du lancement, pas une preuve d'exécution.

Pour `CISMPn`, conserve le RUN `CISMPn` et le cycle normal du prompt.
Pour `1CISMPn`, conserve ce même RUN et borne le périmètre à **un seul change** :
réaliser et valider le change complet, archiver, générer et vérifier les
statistiques, puis arrêter la session de codage suivant le protocole prévu.
Cette directive explicite remplace la poursuite de la boucle de sélection
après ce premier change ; ne démarre pas un deuxième change. Effectue les
clôtures et contrôles requis avant l'arrêt. Le bilan porte sur ce change,
sans prétendre que tout le travail du dépôt est terminé. Une condition
imposant une décision reste applicable et n'est jamais un succès inventé.
Pour cette variante, les preuves de terminaison concernent ce change et la
clôture de sa session ; la présence d'autres changes ne prolonge pas ce RUN.

Le lancement d'un prompt piloté suit son propre protocole ; un lancement SCM
reste une session de codage directe. LIST et les tests du dispatcher ne
déclenchent ni RUN ni pilotage. Aucun prompt source n'est copié dans ce plugin.

`/PROMPT` est une commande source et un déclencheur du skill, sans promesse
d'enregistrement d'une slash native. `$prompt` est l'invocation directement
prise en charge. Maintenir ce SKILL.md et le résolveur identiques dans les
distributions autonome et embarquée.

La commande canonique est `/PROMPT` ; `/prompt` reste
un alias compatible. L’identifiant technique du skill reste en minuscules.
