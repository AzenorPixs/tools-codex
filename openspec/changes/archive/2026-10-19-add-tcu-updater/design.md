## Context

La release initiale est 0.2.3. Les plugins CM/PLLM/TFL et les skills autonomes
sont distribués séparément. Le CLI expose `plugin list --marketplace NAME
--json` et `plugin marketplace upgrade NAME --json`. Le nom final est TCU.

## Goals / Non-Goals

Mettre à jour les briques déjà installées depuis les deux canaux, exposer un
bilan réel et un contrôle préalable. Ne pas installer les briques absentes,
modifier un checkout de développement, exécuter les générateurs PLLM/TFL,
activer des services, publier ni manipuler les secrets.

## Decisions

- Créer le skill et script `skills/tcu/`, la copie complète sous
  `plugins/tcu/skills/tcu/`, le manifeste et l'entrée de marketplace.
- Utiliser `$tcu` et la reconnaissance de `/TCU` ; le fichier source ne
  promet pas une slash native. Aucun enregistrement global pendant cette SCM.
- Le script vérifie par défaut sans écriture ; `--apply` applique. Le skill
  traduit une invocation explicite sans option en `--apply`, et `--check` en
  contrôle. Une demande d'explication ne déclenche pas de mutation.
- Télécharger le dépôt public officiel via HTTPS, résoudre le HEAD en SHA,
  lire l'archive en mémoire avec limites et ne sélectionner que les sources
  des skills et commandes. Vérifier les versions, manifestes, chemins et code
  Python avant application ; aucun script téléchargé n'est exécuté.
- Les racines autonomes sont les répertoires utilisateur de skills existants
  ou des `--skills-dir` / `--commands-dir` explicites. Refuser les liens et
  checkouts de développement. Les absents sont signalés sans installation.
- Un reçu `.tools-codex-origin.json` garde dépôt, SHA, release et empreintes.
  Sans reçu, une copie déjà identique peut être reconnue ; une copie différente
  est ambiguë. `--adopt` autorise explicitement son adoption avec sauvegarde.
  Cette option ne force jamais une modification d'un fichier déjà suivi.
- Sauvegarder les fichiers remplacés et le reçu sous CODEX_HOME/tcu-backups,
  appliquer par remplacement atomique et restaurer les sources autonomes en
  cas d'échec. Conserver les anciens fichiers retirés en amont et les données.
- Sauvegarder les données générées des plugins avant le rafraîchissement CLI,
  puis les restituer dans le cache vérifié. Ne jamais les afficher. Le CLI
  possède son propre cycle : aucune atomicité globale des deux canaux n'est
  promise ; les succès partiels sont rapportés avec un code non nul.
- Vérifier les versions installées après rafraîchissement ; si le canal
  marketplace ne correspond pas à la release GitHub, bloquer l'application
  autonome. Conserver l'état activé/désactivé des plugins.
- Conserver la bibliothèque standard Python (3.13/3.14) et utiliser un verrou
  local lors de l'application. Les requêtes publiques n'emploient aucun jeton.

## Risks / Trade-offs

Les installations historiques sans reçu exigent une adoption explicite si
elles diffèrent de la source distante. Une copie modifiée reste en conflit.
Les sauvegardes sont conservées pour reprise ; aucune purge automatique.
Le rafraîchissement CLI peut avoir réussi avant un échec ultérieur : le bilan
distingue alors les canaux. Le processus en cours charge déjà son code, ce qui
permet la mise à jour de TCU sans redémarrer Codex ; les nouveaux skills sont
chargés dans une nouvelle session.

## Migration Plan

Spécifier et valider avant le code. Livrer et tester dans des répertoires sous
tests, avec réseau et CLI simulés. Mettre à jour les deux catalogues CM,
documentation et sept supports de release à 0.3.0, puis synchroniser et
archiver. Produire le rapport à six sections après archivage.

Repli du développement : retirer les nouveaux fichiers TCU, son lien et son
entrée, restaurer les documents, spécifications, catalogues et versions. Le
repli d'une exécution TCU concerne les sources autonomes sauvegardées ; une
mise à jour du cache CLI réussie reste explicitement rapportée.

## Validation

Tests hors ligne : erreurs HTTP/CLI et JSON, archive hostile, contrôle sans
écriture, absents, conflits, adoption, données conservées, remplacement,
repli, cohérence de version et mise à jour de TCU. Exécuter la suite complète
sur Python 3.13/3.14, syntaxe, validateur des skills, paquet isolé, parité,
JSON/TOML, UTF-8/LF, périmètre par empreintes et OpenSpec strict. La mise à
jour du profil réel et la publication restent non exécutées.

## Preuves de qualification

Les derniers appels de la suite complète sont exécutés et réussis :

- `/usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q` : 43 tests, Python 3.13.5.
- `/home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q` : 43 tests, Python 3.14.8.

Les 24 nouveaux tests TCU couvrent réseau et CLI simulés, fichiers temporaires,
contrôle sans écriture, adoption, conflits et provenance, liens et checkout,
absents, commandes présentes, auto-mise à jour, données et activation,
succès partiels, état inconnu, rollback, modification concurrente, verrou,
archive dangereuse, JSON invalide, codes de sortie et suffixes de build.
Les 19 tests existants sont préservés. Le contrôle privé des sauvegardes est
passé après correction du bit setgid hérité : chmod explicite à 0700.

Autres contrôles exécutés et réussis :

- Validateur skill-creator sur les deux skills CM et les deux skills TCU, via
  le Python système existant. Le Python DevOps ne possède pas PyYAML pour ce
  seul validateur ; aucun ajout de dépendance n'a été effectué.
- Sept supports de release 0.3.0, quatre entrées de marketplace, analyse
  JSON/TOML, liens relatifs CM/TCU et parité des ressources.
- Trois compilations py_compile finales dans un temporaire sous tests ;
  trois compilations antérieures avaient également réussi. Paquet isolé et
  son --help exécutés sur les deux Python, sans réseau.
- Instantané des vraies sources locales validé par le script avec réseau
  simulé : quatre plugins, scripts vérifiés et données générées exclues.
- Empreintes : 111 fichiers initiaux observés, 13 modifications attendues et
  98 préservés avant synchronisation, dont 73 fichiers d'archives précédentes.
  UTF-8/LF sur 26 fichiers avant synchronisation. Ce périmètre ciblé n'est pas
  un inventaire exhaustif du dépôt.
- OpenSpec strict ciblé avant code, puis global avant archivage : sept
  éléments valides, aucun échec. Mots-clés RFC 2119 et longueur vérifiés.

Échecs intermédiaires résolus : littéral bytes accentué dans un test corrigé
avant import ; validateur sans PyYAML relancé avec l'interpréteur système ;
permission héritée du parent neutralisée et test conservé. Un patch documentaire
a échoué sur son contexte sans écriture, puis a été réappliqué. Ces échecs ne
sont pas comptés comme des réussites et ne subsistent pas à la clôture.

## Matrice de cohérence documentaire

| Élément | État et preuve |
|---|---|
| Projet réel | Quatre plugins, TCU autonome/embarqué et commande source présents ; deux liens locaux et sept supports de release vérifiés. |
| AGENTS.md | Inchangé, empreinte conservée ; règles d'écriture, OpenSpec, secrets, Git et validation suffisantes. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel et description de TCU, nom final de TFU. |
| TECHNICAL.md | Mis à jour : quatre plugins, ressources TCU, prérequis, modes, provenance, sauvegardes 0700, verrou et limites du repli. |
| BUILD.md | Mis à jour : plugin TCU, commandes, racines autonomes, adoption, rafraîchissement manuel et distinction de la livraison locale. |
| DEVOPS.md | Inchangé, empreinte conservée : outils existants utilisés, pas de nouvelle dépendance ni d'inventaire à régénérer. |
| README.md | Mis à jour : release 0.3.0, quatre entrées du catalogue, usage TCU et lien vers BUILD. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased, historique préservé. |
| openspec/specs/ | Extension-distribution et tools-codex-update synchronisées ; neuf exigences identiques aux deltas archivés. Sept specs strictes valides. Release-versioning inchangée. |

L'état documentaire est cohérent dans le périmètre validé. Tests navigateur et
build frontend sont non pertinents. Publication, installation du plugin et
mise à jour du profil réel restent non exécutées. Aucune commande Git ni
inspection de son état n'a été effectuée pendant cette reprise.

## Clôture OpenSpec

L'archive `2026-10-19-add-tcu-updater` est créée par le CLI avec confirmation
dans le périmètre validé. Elle synchronise sept exigences ajoutées et deux
modifiées. Le premier contrôle post-archive a refusé le Purpose provisoire
généré automatiquement pour la nouvelle capacité. Ce texte a été remplacé
par son objet réel dans la spec principale et le delta archivé. Le contrôle
strict suivant valide les sept spécifications. Aucun réarchivage n'a été
effectué ; les onze tâches sont terminées et aucun change actif ne reste.

Le contrôle des empreintes après synchronisation identifie 14 fichiers
initiaux modifiés et 97 préservés sur les 111 observés, dont les 73 fichiers
des anciennes archives. STATISTIQUES.md est produit puis vérifié dans cette
archive. La publication et la mise à jour d'un profil réel restent exclues.
