# STATISTIQUES — uppercase-tools-codex-commands

Projet : Tools Codex (`tools-codex`). Session SCM directe du 27 octobre 2026.
Release locale : 0.7.13. Rapport produit après l'archive native
`2026-10-27-uppercase-tools-codex-commands`.

## 1. Statistiques générales

Un change spécifié, réalisé et archivé. Six commandes sources canoniques :
CM, PLLM, TFL, TCU, LM et PROMPT. Quatre fichiers sources renommés ; quatre
nouveaux fichiers agents/openai.yaml pour les deux distributions CM/PROMPT.
Les identifiants et invocations techniques restent en minuscules ; les anciens
déclencheurs restent des alias. Les six manifestes, VERSION, project.version
et README déclarent 0.7.13.

TCU crée PROMPT.md pour une nouvelle copie ; les anciennes copies sont
actualisées sous leur nom existant, avec leurs reçus et sauvegardes. Les deux
graphies sont vérifiées ensemble lorsqu'elles existent. Les liens et
modifications locales restent des conflits préservés ; aucune autre commande
absente n'est créée et aucune adoption n'est forcée.

La suite globale contient 328 tests réussis sous Python 3.13.5 et 328 sous
Python 3.14.10, soit 656 exécutions globales. Les cinq nouveaux cas concernent
la compatibilité TCU. Les 52 tests TCU revalidés sous chaque branche se
recouvrent avec la suite globale et ne s'ajoutent pas au total de 656.
Durées globales observées : 15.424 s et 19.590 s, soit 35.014 s cumulées,
indépendamment du temps des contrôles ciblés.

Syntaxe : quatre fichiers Python modifiés compilés par branche, soit huit
compilations. Parité : six paires SKILL.md, six paires agents/openai.yaml et
une paire update.py, soit treize comparaisons de contenu.

OpenSpec strict : 11/11 avant archive, puis 10/10 après archive. L'archive
native a synchronisé deux specs, ajouté deux exigences et modifié quatre
exigences. Aucun second archivage. Durée exhaustive de session, temps modèle,
tokens, coût et cache : N/A, télémétrie non instrumentée dans SCM.

## 2. Messages et outils

La session est exécutée directement par Codex, sans sous-agent, pilotage CAB,
session OpenCode ou compétence de statistiques de session pilotée. Le prompt
SCM est résolu depuis le référentiel déclaré dans DEVOPS.md. Les instructions
de rédaction fournies dans AGENTS.md sont appliquées au rapport ; aucune
source de style externe disponible n'a été utilisée.

Messages et appels d'outils exhaustifs : N/A, aucun agrégat fiable instrumenté.
Les preuves sont les sorties de validation observées et VALIDATION.md.
Les diagnostics intermédiaires corrigés concernent la conservation de scénarios
OpenSpec historiques, deux paragraphes trop longs après synchronisation, deux
patches rejetés sans écriture et la revue des chemins de rapports pour garder
tfl.json/tfl.md en minuscules. Les contrôles concernés ont ensuite réussi.

## 3. Fichiers

Inventaire des écritures de ce change, distinct des nombreuses modifications
préexistantes du dépôt. Les chemins renommés ne sont comptés qu'à destination.

| Ensemble | Nombre | Opération |
|---|---:|---|
| .codex/commands/CM.md, PLLM.md, TFL.md, PROMPT.md | 4 | Renommés depuis les quatre noms en minuscules, contenu de délégation harmonisé |
| skills et plugins : six paires SKILL.md | 12 | Déclencheurs, affichage et références harmonisés |
| skills et plugins : CM/PROMPT agents/openai.yaml | 4 | Créés |
| plugins : six .codex-plugin/plugin.json | 6 | Release commune ; affichage PROMPT |
| PROJECT.md, TECHNICAL.md, BUILD.md, README.md, CHANGELOG.md | 5 | Documentation et impacts |
| VERSION, pyproject.toml | 2 | Release 0.7.13 |
| skills/tcu/scripts/update.py et copie embarquée | 2 | Compatibilité des commandes et reçus |
| tests/test_tcu_update.py, tests/test_lm_blacklist.py | 2 | Cinq nouveaux cas et attentes de release/noms adaptées |
| openspec/specs/extension-distribution/spec.md et tools-codex-update/spec.md | 2 | Synchronisés et format strict vérifié |
| Archive : proposal.md, design.md, tasks.md, deux deltas spec.md, VALIDATION.md, STATISTIQUES.md | 7 | Créés, change déplacé vers l'archive |
| Total des destinations du change | 46 | 31 fichiers préexistants modifiés, 4 renommages et 11 nouveaux fichiers |

AGENTS.md, DEVOPS.md et .gitignore ne sont pas modifiés par cette session.
Les fichiers de commande LM.md et TCU.md restent inchangés. Aucun fichier
métier, secret, donnée, rapport fournisseur ou configuration personnelle n'est
modifié. Les artefacts temporaires des tests sont nettoyés par leurs fixtures ;
les caches de compilation sont ignorés. Lignes ajoutées/supprimées : N/A,
aucune baseline textuelle exhaustive propre à ce change n'a été enregistrée.

## 4. Commandes et validations

| Contrôle | Résultat réel |
|---|---|
| Spécification avant code | openspec validate uppercase-tools-codex-commands --strict --no-interactive : exécutée et réussie |
| Syntaxe | python3 -m py_compile des deux update.py et deux tests modifiés : exécutée et réussie sur 3.13.5 et 3.14.10 |
| Tests globaux | unittest discover -s tests : 328 tests exécutés et réussis par branche |
| Tests TCU finaux | unittest discover -s tests -p test_tcu_update.py : 52 tests exécutés et réussis par branche |
| Déclarations et release | Six noms sources exacts, six libellés, alias, identifiants techniques, versions et treize parités : exécutées et réussies |
| OpenSpec avant archive | validate --all --strict --no-interactive : 11/11 exécutés et réussis |
| Préparation | status --change uppercase-tools-codex-commands --json : planning et artefacts complets |
| Archivage | archive uppercase-tools-codex-commands --json --yes : code 0, specsUpdated=true, destination unique vérifiée |
| OpenSpec après archive | validate --all --strict --no-interactive : 10/10 exécutés et réussis après correction documentaire de longueur |
| Rapport et nettoyage | Six sections, UTF-8/LF et totaux vérifiés après écriture ; aucun BLOCKER.md ni BLOCKERS.md présent dans l'archive |
| Git conditionnel SCM | Variables locales, Forgejo et GitHub présentes ; branche main vérifiée, aucun fichier ignoré déjà suivi, diff --check réussi et 383 chemins candidats examinés sans signature sensible détectée. Commit global puis publications exactes applicables ; résultats et SHA finaux consignés dans la restitution. GitLab non applicable : ses cinq variables sont absentes. |
| Index global SCM | 260 fichiers, 42 682 insertions et 2 102 suppressions avant ajout de ces précisions documentaires ; ces totaux incluent les travaux antérieurs et ne représentent pas les seules modifications de ce change. diff --cached --check : exécuté avec code 2 pour six lignes vides finales dans des archives préexistantes hors périmètre ; fichiers conservés. |

Binaire OpenSpec : /home/devops/.local/npm/bin/openspec. Aucun outil ou paquet
ajouté. Frontend, SQL, ShellCheck et lint/types supplémentaires : non pertinents
pour les fichiers modifiés et la configuration disponible.

## 5. Accès web

Aucune recherche web, requête fournisseur, génération, lecture de quota,
crédit ou solde n'est lancée par cette correction SCM. Les tests utilisent
des transports, catalogues et profils contrôlés hors ligne. Les recherches
documentaires et installations réalisées plus tôt dans le chat sont distinctes
de cette correction et ne sont pas des validations de la release 0.7.13.
Performances fournisseur et coût commercial des modèles : N/A, aucun appel
réel. Les publications Git conditionnelles sont applicables vers
forgejo.pixs.fr/rootforgejo/tools-codex et github.com/AzenorPixs/tools-codex,
branche main, après les contrôles de ce rapport. Le plugin GitHub disponible
ne propose pas de transfert brut du commit local avec ses métadonnées exactes ;
Git conserve le SHA local sans recréation de commit par API.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Projet réel | Six commandes et libellés en majuscules ; 328 tests globaux réussis par branche ; compatibilité TCU revalidée |
| AGENTS.md | Inchangé par cette session ; règles de périmètre, spécification et validation appliquées |
| PROJECT.md | Mis à jour : Organisation et Catalogue actuel |
| TECHNICAL.md | Mis à jour : Arborescence, Commandes et skills autonomes, Mise à jour TCU |
| BUILD.md | Mis à jour : Distribution, catalogue CM, Utilisation de prompt, Mise à jour et migration explicite des liens |
| DEVOPS.md | Inchangé par cette session ; ses rubriques Prompts, Python et OpenSpec sont utilisées |
| README.md | Mis à jour : release 0.7.13, déclarations canoniques, alias et limites de migration |
| CHANGELOG.md | Trois entrées Unreleased, historique antérieur conservé |
| OpenSpec | Deux specs synchronisées, contrôle strict final 10/10 ; détails dans VALIDATION.md |

Les profils installés restent distincts de la livraison des sources. Les liens
personnels dirigés vers les anciens fichiers sources cm.md, pllm.md ou tfl.md
nécessitent une réorientation lors d'une migration explicite. Aucun benchmark,
timer ou profil n'est actualisé par ce change. Les formulations historiques
hors périmètre encore présentes dans extension-distribution (anciens nombres
de plugins et ancienne release LM) sont signalées dans VALIDATION.md sans
être corrigées silencieusement. Aucun nouveau comportement métier n'est ajouté.
