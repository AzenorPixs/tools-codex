---
name: tcu
description: Mettre à jour les briques Tools Codex installées depuis marketplace et GitHub. Utiliser pour $tcu, /TCU, /tcu ou une demande explicite de mise à jour Tools Codex.
---

TCU est le nom final de l'outil initialement proposé comme TFU. Une demande
d'explication ne déclenche aucune mise à jour.

Pour une invocation explicite, exécute le script depuis ce skill installé :

- `$tcu` ou `/TCU` : `python3 -B scripts/update.py --apply` ;
- `$tcu check` ou `/tcu check` : `python3 -B scripts/update.py check` ;
- transmettre les options `--skills-dir CHEMIN` et `--commands-dir CHEMIN`
  explicitement fournies, avec chaque chemin comme argument distinct ;
- transmettre `--adopt` uniquement s'il est explicitement demandé. Ne pas
  l'ajouter pour contourner un conflit. Il adopte avec sauvegarde une copie
  historique sans reçu ; il ne force pas les fichiers suivis modifiés.

Le script utilise Python 3.13/3.14, le CLI Codex et HTTPS public GitHub. Son
invocation explicite autorise le rafraîchissement de la seule marketplace
`tools-codex`, les sauvegardes et la mise à jour des copies déjà installées
dans les racines identifiées. Seul le composant `prompt` absent est installé
automatiquement : plugin via le CLI, skill et résolveur embarqués vérifiés,
puis wrapper de commande issu de `.codex/commands/PROMPT.md`. Aucun autre
plugin absent ni doublon autonome de skill n'est créé. Le code du cache
plugin reste géré par le CLI. Ne pas lancer PLLM/TFL pendant TCU.

Le mot `check` a priorité sur le lancement par défaut : ne jamais appliquer
une demande `/tcu check`. `--check` reste un alias compatible. Le script seul
vérifie sans écriture par défaut ; appliquer exige `--apply`.
Les racines par défaut sont CODEX_HOME/skills, ~/.agents/skills,
CODEX_HOME/prompts et CODEX_HOME/commands (CODEX_HOME vaut ~/.codex par défaut).
Le wrapper PROMPT.md est créé dans CODEX_HOME/prompts par défaut, ou dans le
premier --commands-dir explicite ; les autres copies présentes sont mises à
jour. Il délègue au skill sans copier les prompts métier : DEVOPS.md reste
leur seule référence. Un lien ou checkout de développement reste inchangé.
Les anciennes copies en minuscules sont actualisées sous leur nom actuel,
avec leurs reçus et sauvegardes, sans doublon créé ni renommage. Si PROMPT.md
et prompt.md existent, ils sont vérifiés dans le même plan et reçu de
composant. Une ancienne source prompt.md reste lisible si PROMPT.md manque.
Son conflit ne bloque pas les opérations indépendantes ; il reste signalé
avec un code non nul, même après des mises à jour réussies. Aucun
git pull ni redémarrage de service. Les fichiers retirés en amont restent
conservés. Aucun secret ni configuration personnelle n'est chargé.

Les reçus `.tools-codex-origin.json` suivent les sources autonomes. Le wrapper
prompt possède son reçu `.tools-codex-prompt-origin.json` ; une preuve
existante peut être reprise sans écraser le reçu partagé. Les
sauvegardes restent sous CODEX_HOME/tcu-backups, sans purge automatique. Les
données JSON/Markdown des plugins sont sauvegardées puis restituées ; une
donnée non prise en charge bloque le rafraîchissement. Si la lecture finale
du CLI échoue, la sauvegarde reste disponible et l'état est inconnu. Aucune
annulation globale de la marketplace n'est garantie.

Restitue le bilan JSON en tableau français par brique : canal, état, version
avant/après connue et cause ; distinguer les trois ressources de prompt :
plugin, skill embarqué et commande. En contrôle seul, annoncer l'installation
prévue de prompt sans la réaliser, et distinguer version cible et
version appliquée. Indique sauvegarde, conflits, succès partiels et code de
sortie réel sans exposer les contenus sauvegardés. Une nouvelle session
Codex charge les skills actualisés.

`/TCU` est une commande source et un déclencheur reconnu par le skill ; ce
fichier ne crée pas une slash native. `$tcu` est l'invocation directement
prise en charge. Maintenir SKILL.md et scripts/update.py identiques dans les
distributions autonome et embarquée.

## Planning utilisateur TFL puis PLLM

Après vérification des sources, `--apply` enregistre aussi le planning avec
le module local `scripts/scheduler.py`, sans exécuter de code téléchargé ni
de modèle. `check` décrit seulement cette opération. Restituer la ligne
`llm-refresh` du bilan : installation, état courant, composants absents ou
échec ; aucune version de plugin n'est inventée pour ce planning.

Les deux composants TFL/PLLM doivent déjà être installés. Les six plugins
proposent le même bootstrap par hook SessionStart, soumis à la confiance
native Codex. L'installateur autonome est `python3 -B scripts/scheduler.py install`,
à utiliser seulement pour une installation demandée. Une mise à jour lancée
avec un ancien TCU n'exécute pas rétroactivement le nouveau bootstrap.

Le timer systemd utilisateur déclenche à 00 h et 12 h Europe/Paris, sans
rattrapage, si l'application ou un CLI interactif Codex est ouvert. Il lit
le quota Codex avant TFL puis avant PLLM : quota nul ou inconnu, aucun appel
de l'étape. Un échec TFL empêche PLLM. La séquence ne modifie ni LM ni les
seuils et n'exécute aucun achat, connexion ou reset de quota. TCU n'installe
pas les composants absents et ne déclenche pas la séquence pendant son apply.

La commande canonique est `/TCU` ; `/tcu` reste
un alias compatible. L’identifiant technique du skill reste en minuscules.
