# Validation locale SCM — 26 octobre 2026

Le développeur a validé le périmètre autonome LM, TFL/PLLM, CM et 0.7.6,
y compris OpenSpec, archivage et rapport. Exécution directe, sans sous-agent,
CAB, installation, réseau fournisseur ou commande Git.

## Résultats exécutés et réussis
- Python 3.13.5 : 256 cas autorisés distincts, 0 échec, 0 erreur, suite finale après isolation des profils.
- Python 3.14.10 : 256 mêmes cas, 0 échec, 0 erreur.
- 20 tests LM et 3 nouveaux tests TCU ; génération, réseau et profils réels isolés.
- 35 py_compile sur chaque branche, soit 70 compilations ; imports des modules et Europe/Paris.
- Validateur skill-creator : 12 skills valides.
- Six paires de paquets identiques, six copies identiques de model_blacklist.py.
- Quatre liens locaux : CM, TCU, prompt préservés ; LM ajouté. Les liens PLLM/TFL ne faisaient pas partie de l'état initial et ne sont pas ajoutés.
- Neuf supports 0.7.6 : VERSION, pyproject.toml, README et six manifestes.
- LM LIST exécuté sous profil de test absent : mimo-v2.5 affiché et aucun profil créé.
- Catalogue CM : six entrées, dont LM et ses syntaxes dans les deux copies.
- TCU simulé : vraie source locale à six plugins acceptée ; LM présent actualisé, LM absent conservé et politique utilisateur intacte.
- OpenSpec ciblé strict valide ; global avant archivage 9/9.
- Archivage unique réussi : 8 exigences ajoutées, 5 modifiées, 0 supprimée ou renommée ; quatre capacités synchronisées.
- Inventaire d'empreintes ciblé avant écriture : 78 chemins ; avant synchronisation, 30 modifiés et 16 ajoutés, dont un lien ; aucune suppression.
- Aucun répertoire temporaire restant sous tests/ ; AGENTS et DEVOPS préservés.

## Commandes de référence

Les suites sont chargées avec `unittest.defaultTestLoader.discover('tests')`
puis exécutées après exclusion du seul cas Git ci-dessous, avec -B et
-W error::ResourceWarning, CODEX_HOME sous tests/.
Interpréteurs : /usr/bin/python3.13 et /home/devops/python/current/bin/python3.
La compilation utilise py_compile.compile avec cfile dans un temporaire
sous tests/ puis nettoyé. Les validateurs utilisent le Python système et
/home/ade/.codex/skills/.system/skill-creator/scripts/quick_validate.py.
OpenSpec utilise /home/devops/.local/npm/bin/openspec et
OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1.

## Non exécuté
`test_command_sources_are_publishable_without_local_codex_files` appelle Git.
SCM interdit cette inspection sans demande explicite ; le test n'est pas
modifié et n'est pas présenté comme réussi. Contrôle documentaire de .gitignore
effectué sans Git : exclusions .codex et réinclusions des commandes présentes.
Installation/chargement réel dans une nouvelle session, publication distante,
benchmarks et accès fournisseur : non exécutés, hors périmètre.
Build web/navigateur : non pertinents.

## Échecs intermédiaires résolus
- Premier OpenSpec ciblé : un texte d'exigence PLLM dépassait 500 caractères ; séparation en deux exigences, puis strict valide avant écriture du code.
- Première suite LM : 3 erreurs de fixtures (classe d'exception d'un autre paquet, candidate_exclusions absent de l'état simulé, catalogue OpenRouter vide devant rester bloquant). Fixtures corrigées sans affaiblir les invariants ; 19/19 puis 20/20.
- Première suite globale : 1 erreur dans la nouvelle fixture TFL, provenance tarifaire source absente ; fixture complétée, suite suivante 256/256.
- Audit de distribution : une assertion supposait six liens locaux préexistants ; diagnostic a confirmé quatre liens pertinents après ajout LM. Contrôle corrigé sans création de liens hors périmètre.

- Premier contrôle après archive : le Purpose provisoire généré par OpenSpec pour lm-blacklist restait un marqueur ; remplacé par son objet réel dans la spec principale et le delta archivé, sans réarchivage.

## Matrice documentaire finale
| Élément | État et preuve |
|---|---|
| Projet réel | LM, six plugins, filtrage et release vérifiés par tests/contrôles ci-dessus. |
| AGENTS.md | Inchangé, empreinte conservée ; règles d'écriture, secrets et validation suffisantes. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel et Liste noire des modèles. |
| TECHNICAL.md | Mis à jour : six plugins, table des invocations, section Liste noire LM. |
| BUILD.md | Mis à jour : catalogue, release protocole et Distribution et utilisation de LM. |
| DEVOPS.md | Inchangé, empreinte conservée ; mêmes outils, pas de dépendance ni inventaire modifié. |
| README.md | Mis à jour : 0.7.6, LM dans CM et section LM avec limites d'installation. |
| CHANGELOG.md | Trois entrées ajoutées dans Unreleased ; historique conservé. |
| openspec/specs/ | Deltas validés lm-blacklist, extension-distribution, tfl-catalog et pllm-evaluation, synchronisés par archivage unique ; contrôle strict final consigné dans STATISTIQUES.md. |

La checklist porte sur les réalisations et preuves préalables ; l'archivage
et le rapport sont constatés après leur effet, sans case cochée par anticipation.
Le passage à une ancienne release ignore LM : il ne conserve pas sa garantie
d'exclusion. Aucun historique utilisateur n'est réécrit par LM.

## Contrôle final du rapport
STATISTIQUES.md vérifié : six sections, 60 chemins existants (33 modifiés,
26 fichiers créés et un lien), totaux 32/27/5 bornés et 512 tests finaux,
UTF-8/LF, treize exigences identiques entre deltas et specs principales,
onze tâches prouvées, zéro change actif et aucun temporaire restant.
Les expressions régulières du vérificateur et une syntaxe d'orchestration
ont été corrigées avant ce contrôle réussi ; aucune source produit n'a
été modifiée à cette occasion.
