## Context

La release initiale est 0.4.0. Le catalogue CM contient déjà prompt, mais TCU
n'installe aucune brique absente. Le profil de commandes peut contenir des
liens vers les sources de développement, que cette évolution conserve.

## Decisions

- Seul prompt devient installable automatiquement s'il figure dans le
  catalogue officiel validé. Le CLI reste propriétaire du code des plugins.
- Vérifier manifeste, SKILL.md et résolveur du cache prompt après opération,
  en comparant les sources à l'instantané GitHub. Ne pas créer une seconde
  copie autonome absente ; actualiser celles qui existent selon leur provenance.
- Le wrapper source .codex/commands/prompt.md se déploie dans le premier
  --commands-dir explicite, ou CODEX_HOME/prompts par défaut. Les autres
  copies présentes dans les racines indiquées sont actualisées. Son reçu
  dédié .tools-codex-prompt-origin.json n'écrase pas un reçu global existant.
- La création du seul wrapper prompt est autorisée dans une racine absente ;
  une copie différente sans provenance exige toujours --adopt. Les liens,
  modifications suivies et checkouts restent en conflit sans écriture.
- Les plans génériques de commandes excluent prompt pour éviter deux propriétaires.
  Les conflits locaux ne bloquent plus la marketplace ni les plans locaux valides.
  Un échec de sauvegarde, une source invalide ou un état CLI incohérent reste bloquant.
- Installer prompt après un rafraîchissement et une vérification réussis. Relire
  l'état même après un échec d'installation pour rapporter l'effet réel.
  Vérifier activation et versions, puis appliquer les plans locaux valides.
- Préserver les sauvegardes privées et le rollback des fichiers locaux. Le
  cycle CLI ne bénéficie pas d'une atomicité globale ; les succès partiels
  restent visibles et un conflit ou échec conserve un code non nul.
- Ajouter cm.md comme wrapper du skill CM et le déclencheur /cm ; conserver
  une seule entrée prompt dans les deux catalogues. Les fichiers de commande
  ne promettent pas une slash native sans namespace enregistrée par Codex.
- La commande installée délègue au skill. Les prompts métier restent dans le
  seul référentiel DEVOPS ; aucun contenu de ce référentiel n'est copié.

## Migration Plan

Valider les deltas avant code. Mettre à jour les deux moteurs et skills TCU,
les wrappers, les catalogues et documents. Aligner VERSION, TOML, README et les
cinq manifestes sur 0.4.1. Tester sous tests sans CLI ni réseau réel. Valider,
synchroniser, archiver et produire STATISTIQUES.md. Le Purpose de la spec de
mise à jour sera aligné sur la gestion et l'installation ciblée après synchronisation.

Repli local du développement : restaurer sources, documents et versions puis
retirer le nouveau wrapper CM. En exécution TCU, restaurer les sources locales
sauvegardées ; rapporter une installation CLI réussie sans prétendre l'annuler.

## Validation

Couvrir prompt absent, déjà installé, réinstallation et ressource manquante,
contrôle sans écriture, refus d'installer un autre plugin absent, version ou
activation divergente, erreur CLI partielle, reçus, adoption et rollback,
liens et données préservés, conflits locaux indépendants, wrapper seul créé
et catalogue sans doublon. Suite complète Python 3.13/3.14, py_compile,
parité, formats, paquet isolé, versions, UTF-8/LF et OpenSpec strict.

## Preuves de qualification

- Exécutées et réussies : 38 tests TCU ciblés, puis 77 tests complets sur
  /usr/bin/python3 (3.13.5) et /home/devops/python/current/bin/python3 (3.14.8),
  avec -B et ResourceWarning traité en erreur.
- Exécutées et réussies : py_compile des deux moteurs et du fichier de tests,
  --help du paquet TCU isolé sur les deux Python, quick_validate.py des quatre
  copies de skills CM/TCU, parité octet pour octet et cinq versions 0.4.1.
- Trois attentes historiques qui bloquaient toute opération en cas de conflit
  local sont remplacées par des assertions de succès marketplace indépendant.
  Les assertions de conflit, d'échec global et de conservation restent actives.
- Les treize nouveaux tests utilisent réseau et CLI simulés et des profils
  temporaires sous tests. Ils couvrent les ressources prompt, les reçus,
  l'adoption, les caches incomplets, les liens et les erreurs partielles.
- Non exécutées : publication et installation dans le profil réel, hors de
  cette livraison SCM. Non pertinente : invocation du skill de statistiques
  de pilotage, exclue par SCM. Aucun blocage connu dans le périmètre livré.

## Matrice documentaire finale

| Élément | État et preuve |
|---|---|
| Projet réel | Moteurs TCU synchronisés ; fixtures de test des trois ressources et des conflits indépendants. |
| AGENTS.md | Inchangé : règles SCM, OpenSpec, liens et périmètre respectées ; empreinte comparée à l'état initial. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel et rôle TCU décrivent /cm et l'installation ciblée. |
| TECHNICAL.md | Mis à jour : Arborescence, catalogue CM et Mise à jour TCU décrivent canaux, reçus et vérifications. |
| BUILD.md | Mis à jour : Skill catalogue cm et Mise à jour décrivent les déclencheurs, cibles et limites réelles. |
| DEVOPS.md | Inchangé : environnement Python et emplacement exclusif des prompts restent applicables ; empreinte vérifiée. |
| README.md | Mis à jour : release 0.4.1, wrapper CM et synthèse TCU avec prompt et conflits partiels. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased sur prompt géré, indépendance des canaux et release 0.4.1. |
| openspec/specs | Deux deltas ciblés : gestion TCU et distribution ; la distribution TCU précise désormais cinq manifestes. Synchronisation avant clôture. |

Le nombre de manifestes TCU passe de quatre à cinq dans le delta pour rester
cohérent avec le composant prompt et la release commune validée. Aucun autre
cadrage n'est absent ou bloqué ; ORCHESTRATED_CODING.md reste inchangé car
cette session SCM est directe.

Contrôles complémentaires exécutés et réussis : instantané en mémoire de 24
sources réelles de release, cinq plugins et wrappers CM/prompt reconnus ; sept
exigences des deltas avec mot-clé RFC 2119 en MAJUSCULE et corps inférieur ou
égal à 500 caractères. Le contrôle ciblé des 149 empreintes initiales trouve
20 fichiers modifiés attendus, sept nouveaux fichiers avant archivage et les
94 fichiers d'archives antérieures inchangés. UTF-8/LF et absence de marqueur
de clé privée vérifiés sur les fichiers concernés. Ces contrôles n'utilisent
pas Git et ne constituent pas une analyse des secrets exclus du dépôt.
