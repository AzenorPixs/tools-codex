# Conception

## Décisions
TCU utilise son instantané GitHub vérifié comme liste des skills et commandes et le catalogue officiel comme liste des plugins. Les plugins absents sont ajoutés exclusivement par `codex plugin add`, après sauvegarde et rafraîchissement ; versions et activation sont observées ensuite. L'activation des plugins existants reste inchangée.

Les plans locaux sélectionnent les sources même si leur destination est absente. La création utilise les mêmes contrôles de chemins, reçus et écritures atomiques que les mises à jour. Toutes les racines par défaut ou explicitement demandées sont couvertes. Pour une commande, une graphie historique existante est actualisée ; une graphie canonique est créée seulement si aucune graphie n'existe. PROMPT conserve son reçu dédié et sa vérification du skill et du résolveur embarqués.

`check` décrit les opérations et ne crée ni répertoire, ni reçu, ni sauvegarde. Le bilan expose opération, cible et version observée ; un apply distingue `installe`, `mis_a_jour` et `courant`. Une erreur CLI ou une incohérence des versions bloque les sources non sûres ; un conflit de copie locale laisse continuer les plans indépendants et retourne un code non nul.

## Repli et limites
Les fichiers remplacés sont sauvegardés ; les fichiers créés sont retirés lors du repli autonome, sans purge des données ni promesse de transaction globale du CLI. Les répertoires vides éventuellement créés peuvent rester. Ni hooks de confiance, ni quotas, ni liste noire utilisateur ne sont modifiés par le moteur d'installation. L'ordonnanceur reste un bootstrap local séparé et n'installe pas lui-même les composants.

## Validation
Tests hors ligne avec instantanés, CLI et profils temporaires : profil vide, racines multiples et explicites, noms historiques, check sans écriture, idempotence, activation préservée, échec CLI, conflit local indépendant, création suivie par reçu et repli sur création. Régression complète Python 3.13/3.14, syntaxe, distributions identiques et validations OpenSpec ciblée, globale standard et stricte. Aucun appel fournisseur ou profil réel.

## Preuves de qualification finale

- Python 3.13.5 (`/usr/bin/python3`) : 359 tests réussis, 11,837 s ; compilation de 39 fichiers réussie.
- Python 3.14.10 (`/home/devops/python/current/bin/python3`) : 359 tests réussis, 10,675 s ; compilation de 39 fichiers réussie.
- Commande de suite : `-B -m unittest discover -s tests -q` avec chacun des deux interpréteurs. Qualification réseau/CLI/profils simulés, sans appel fournisseur.
- Le premier passage global a révélé une attente LM fixée à 0.7.23 ; elle a été alignée sur la release demandée, puis les suites globales ont été rejouées avec succès. Aucun test désactivé.
- OpenSpec ciblé strict réussi ; global standard et strict : 11 éléments réussis, aucun échec avant archivage.
- Contrôle de 30 fichiers UTF-8/LF, parité des distributions TCU/CM et alignement de VERSION, métadonnée Python, README et six manifestes : réussi.
- La fixture de l’instantané réel installe six plugins, huit skills dans deux racines et six commandes dans deux racines ; l’ordonnanceur est simulé. Les autres cas prouvent idempotence, absence de mutation en check, repli, conflits et erreurs observées du CLI.

## Matrice documentaire revue avant archivage

| Document | État et preuve |
| --- | --- |
| AGENTS.md | Inchangé : règles générales respectées, aucune nouvelle autorisation permanente. |
| PROJECT.md | Mis à jour : catalogue et paragraphe TCU décrivent installation systématique et mise à jour. |
| TECHNICAL.md | Mis à jour : section Mise à jour TCU, LM et séparation moteur/bootstrap. |
| BUILD.md | Mis à jour : distribution, installation TCU, racines et conservation de la politique LM. |
| DEVOPS.md | Inchangé : chemins Python et OpenSpec utilisés ; aucun changement d’environnement requis. |
| README.md | Mis à jour : release 0.7.24 et comportement TCU, limites des distributions multiples. |
| CHANGELOG.md | Mis à jour : entrée Unreleased dédiée, sans date de publication inventée. |
| openspec/specs | Deltas tools-codex-update et lm-blacklist validés ; synchronisation effectuée par l’archivage, puis validation globale standard et stricte réussie : 10/10, sans avertissement. Le Purpose TCU décrit désormais l’installation systématique. |

Aucun écart documentaire restant identifié dans le périmètre ; ni installation dans le profil réel ni publication distante n’est déduite de ces validations. Les anciens contenus d’archives restent historiques et inchangés.

Après synchronisation, deux textes normatifs dépassaient le seuil de longueur du validateur strict. Condensation sans changement de scénario dans la spécification et son delta archivé ; validations standard et stricte rejouées, 10/10 sans avertissement. Aucun réarchivage ni changement de code supplémentaire.
