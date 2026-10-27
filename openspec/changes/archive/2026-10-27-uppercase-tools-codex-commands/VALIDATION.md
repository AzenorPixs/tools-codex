# Validation — commandes en majuscules

Release locale : 0.7.13. Session SCM directe, projet Tools Codex (tools-codex).

## Résultats

| Contrôle | État et preuve observée |
|---|---|
| Spécification avant code | Exécutée et réussie : openspec validate uppercase-tools-codex-commands --strict --no-interactive, code 0 avant les écritures de code et de tests. Les scénarios historiques requis ont été conservés après le premier diagnostic. |
| Syntaxe | Exécutée et réussie : py_compile des deux scripts update.py et des deux tests modifiés sous Python 3.13.5 et 3.14.10. |
| Tests TCU | Exécutée et réussie : 52 tests, dont cinq nouveaux tests de compatibilité ; dernière revalidation sous les deux branches après revue des textes distribués. |
| Suite globale Python 3.13.5 | Exécutée et réussie : /usr/bin/python3.13 -B -m unittest discover -s tests ; 328 tests, 15.424 s. |
| Suite globale Python 3.14.10 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests ; 328 tests, 19.590 s. |
| Déclarations et release | Exécutée et réussie : ensemble exact des six noms de fichiers en majuscules ; déclencheurs canoniques et alias ; identifiants techniques inchangés ; VERSION, project.version, README et six manifestes à 0.7.13. |
| Parité | Exécutée et réussie : six paires SKILL.md, six paires agents/openai.yaml et les deux scripts update.py identiques octet pour octet. |
| Encodage | Exécutée et réussie : 52 fichiers du périmètre contrôlés en UTF-8/LF, puis revue des chemins techniques pour conserver tfl.json et tfl.md en minuscules. |
| OpenSpec avant archive | Exécutée et réussie : validate --all --strict --no-interactive, 11 éléments valides, 0 échec. |
| Archivage natif | Exécuté et réussi : archive uppercase-tools-codex-commands --json --yes, code 0 ; deux specs synchronisées, deux exigences ajoutées et quatre modifiées. |
| OpenSpec après archive | Exécutée et réussie : 10 éléments valides, 0 échec. Deux paragraphes trop longs détectés par ce contrôle ont été raccourcis avec déplacement des détails vers les scénarios, dans les specs et deltas archivés, sans réarchivage. |
| Revue Git globale SCM | 260 fichiers dans l'index, dont les travaux antérieurs. diff --cached --check retourne 2 pour six lignes vides finales dans des archives préexistantes des 19, 25 et 26 octobre. Ces fichiers hors périmètre sont conservés ; le diff non indexé du change courant passait avant indexation. Aucun autre diagnostic de ce contrôle. |
| Fournisseurs, installation et interface réelle | Non exécutées : aucune génération TFL/PLLM, migration de profil ni invocation dans une nouvelle session Codex dans cette livraison de sources. |
| Frontend, SQL, ShellCheck, lint et types supplémentaires | Non pertinents : aucun fichier frontend, SQL ou shell modifié ; aucun outil additionnel configuré dans pyproject.toml. |

## Matrice documentaire

| Élément | État, section et contrôle |
|---|---|
| Projet réel | Six commandes sources canoniques ; 328 tests globaux réussis par branche et 52 tests TCU revalidés après revue documentaire. |
| AGENTS.md | Inchangé par cette session : règles de périmètre, OpenSpec, validation et statistiques appliquées ; aucun changement de règles demandé. |
| PROJECT.md | Mis à jour : Organisation et Catalogue actuel, commandes canoniques et identifiants techniques distincts. |
| TECHNICAL.md | Mis à jour : Arborescence, Commandes et skills autonomes, Mise à jour TCU ; noms, affichage, reçus historiques et chemins métier conservés. |
| BUILD.md | Mis à jour : Distribution, catalogue CM, Utilisation de prompt et Mise à jour ; migration des liens explicitement distincte de la livraison des sources. |
| DEVOPS.md | Inchangé par cette session : ses rubriques OpenSpec, Python et Prompts fournissent les binaires et le référentiel ; aucune modification d'environnement. |
| README.md | Mis à jour : release 0.7.13, six noms canoniques, alias et compatibilité des anciennes installations. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased sur les déclarations, TCU, compatibilité et release ; historique antérieur préservé. |
| OpenSpec | Deux deltas validés : extension-distribution et tools-codex-update ; synchronisation par l'archive native du seul change, puis contrôle strict 10/10 réussi. |

## Impacts et limites

Les identifiants et invocations $… restent en minuscules. Les arguments,
scripts métier, données, seuils, blacklist et planning ne changent pas. TCU
préserve les anciens noms installés, les reçus, sauvegardes, liens et
modifications locales ; check reste sans écriture. Les anciens liens de
profil qui visent directement cm.md, pllm.md ou tfl.md dans les sources
doivent être réorientés vers les nouveaux fichiers lors d'une migration
explicite du profil. Cette livraison ne migre ni ne réinstalle ce profil.

Les contraintes historiques sans rapport avec ce change ne sont pas
réécrites : extension-distribution contient encore des formulations de
livraisons antérieures (trois plugins et release LM 0.7.6). La présente
validation ne prétend pas résoudre ces écarts préexistants. Aucun écart
induit par l'harmonisation des commandes n'est laissé sans documentation.
