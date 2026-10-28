# STATISTIQUES — add-tcu-updater

Projet : Tools Codex (`tools-codex`), racine `/home/devops/datas/tools-codex`.
Archive : `openspec/changes/archive/2026-10-19-add-tcu-updater`.
Release locale : 0.3.0. Date : 19 octobre 2026.

Rapport de la reprise SCM après validation du périmètre. Le nom final TCU
remplace le nom initial TFU. Exécution directe, sans orchestrateur,
sous-agent, pilotage CAB/OpenCode ni compétence de statistiques pilotées.
Les mesures non collectées restent N/A avec leur justification.

## 1. Statistiques générales et décisions

TCU est livré comme plugin, skill autonome et embarqué, script et commande
source /TCU. Le lien local expose $tcu. Le contrôle sans écriture, l'adoption
explicite, les sauvegardes, les conflits, la conservation des données et le
bilan des versions sont implémentés. Le checkout de développement et les
briques absentes restent préservés. Les deux catalogues CM sont actualisés.

| Mesure vérifiée | Résultat |
|---|---|
| Plugins dans la marketplace locale | 4 : PLLM, TFL, CM, TCU |
| Supports de release alignés à 0.3.0 | 7 : VERSION, TOML, README et quatre manifestes |
| Tests distincts finaux | 43 : 19 existants et 24 nouveaux TCU |
| Dernière suite sur Python 3.13.5 | 43 réussites sur 43 |
| Dernière suite sur Python 3.14.8 | 43 réussites sur 43 |
| Qualification finale combinée | 86 réussites sur 86, soit 100 % |
| Compilations py_compile finales | 3 réussies, fichiers temporaires nettoyés |
| Skills validés par skill-creator | 4 : deux CM et deux TCU |
| Tâches terminées | 11 sur 11 |
| OpenSpec avant archivage | 7 éléments valides sur 7 |
| OpenSpec final après archivage | 7 spécifications valides sur 7 |
| Exigences synchronisées | 7 ajoutées, 2 modifiées, 0 supprimée, 0 renommée |
| Changes actifs après archivage | 0 |
| Fichiers initiaux suivis par empreintes | 111 |
| Fichiers initiaux modifiés | 14 |
| Fichiers initiaux préservés | 97, dont 73 fichiers d'archives précédentes |

Le périmètre d'empreintes est ciblé : cadrages, catalogue, commandes,
spécifications, archives, manifestes, skills, scripts et tests concernés. Il
ne constitue pas un inventaire récursif de tout le dépôt. Les exécutions
intermédiaires sont distinguées de la qualification finale ci-dessus.

Modèle exact, version du modèle, raisonnement, TTMT, débit de génération,
temps de service, tokens, cache, coût et variations de quota : N/A, absence
de télémétrie correspondante. Durée totale SCM : N/A, borne initiale de
l'exploration complète non instrumentée. Aucun quota partagé n'est attribué
à cette session ni converti en tokens ou euros.

## 2. Types de messages et d'outils

| Domaine | Observation | Compteur exhaustif |
|---|---|---|
| Messages humains | Périmètre et règles validés ; nom final TCU fixé | N/A, historique non agrégé |
| Messages de suivi | Progression, résultats et erreurs résolues | N/A, historique non agrégé |
| Commandes locales | Lectures, écritures, tests, contrôles et archivage | N/A au total ; sous-ensemble borné en section 4 |
| Édition | apply_patch et Python locaux | Total N/A ; un patch à contexte incorrect rejeté sans écriture puis réappliqué |
| Horloge | Deux bornes partielles de la reprise | Intervalle en section 6 |
| Git | Aucune commande ni inspection de son état pendant la reprise | Non applicable |
| Pilotage, CAB, OpenCode, sous-agents et sondes | Non déclenchés | Non applicable |

La référence /cab update a été consultée comme source documentaire pour la
séparation préparation/application. Aucun service CAB n'a été piloté. Un
appel réussi n'est pas assimilé à une validation humaine individuelle.

## 3. Fichiers modifiés

Les chemins sont relatifs à la racine indiquée en tête du rapport.

| Chemin final | Opération |
|---|---|
| VERSION | Modifié : 0.3.0 |
| pyproject.toml | Modifié : version 0.3.0 |
| plugins/pllm/.codex-plugin/plugin.json | Modifié : version 0.3.0 |
| plugins/tfl/.codex-plugin/plugin.json | Modifié : version 0.3.0 |
| plugins/cm/.codex-plugin/plugin.json | Modifié : version et description du catalogue |
| .agents/plugins/marketplace.json | Modifié : entrée TCU |
| skills/cm/SKILL.md | Modifié : catalogue à quatre invocations |
| plugins/cm/skills/cm/SKILL.md | Modifié : copie identique |
| PROJECT.md | Modifié : catalogue et rôle de TCU |
| TECHNICAL.md | Modifié : prérequis, modes, données, sauvegardes et qualification |
| BUILD.md | Modifié : installation, utilisation et limites de mise à jour |
| README.md | Modifié : release et usage TCU |
| CHANGELOG.md | Modifié : trois entrées Unreleased |
| openspec/specs/extension-distribution/spec.md | Modifié : catalogue, parité et distribution TCU |
| skills/tcu/SKILL.md | Créé : skill autonome |
| skills/tcu/scripts/update.py | Créé : moteur de mise à jour |
| plugins/tcu/.codex-plugin/plugin.json | Créé : manifeste TCU |
| plugins/tcu/skills/tcu/SKILL.md | Créé : skill embarqué identique |
| plugins/tcu/skills/tcu/scripts/update.py | Créé : script embarqué identique |
| .codex/commands/TCU.md | Créé : commande source |
| .agents/skills/tcu | Lien créé vers ../../skills/tcu |
| tests/test_tcu_update.py | Créé : 24 tests TCU hors ligne |
| openspec/specs/tools-codex-update/spec.md | Créé : six exigences de mise à jour |
| openspec/changes/archive/2026-10-19-add-tcu-updater/.openspec.yaml | Créé puis archivé |
| openspec/changes/archive/2026-10-19-add-tcu-updater/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-add-tcu-updater/design.md | Créé puis archivé ; preuves complétées |
| openspec/changes/archive/2026-10-19-add-tcu-updater/tasks.md | Créé puis archivé ; onze tâches terminées |
| openspec/changes/archive/2026-10-19-add-tcu-updater/specs/tools-codex-update/spec.md | Créé puis archivé ; Purpose précisé |
| openspec/changes/archive/2026-10-19-add-tcu-updater/specs/extension-distribution/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-add-tcu-updater/STATISTIQUES.md | Créé après archivage |

| Catégorie de chemin final | Nombre |
|---|---:|
| Fichier existant modifié | 14 |
| Nouveau fichier | 15 |
| Nouveau lien symbolique | 1 |
| Fichier supprimé | 0 |
| Total | 30 |

Les six fichiers du change sont créés à l'emplacement actif puis transférés
par OpenSpec ; ils ne comptent qu'une fois dans les chemins finaux. Le rapport
est créé après archivage. Les sources PLLM/TFL, leurs commandes et les deux
anciens modules de tests sont préservés. Le lien CM reste inchangé. Aucun
fichier TFU n'a été créé ; le nom final livré est TCU.

## 4. Commandes

Sous-ensemble borné aux seize appels de qualification et cycle ci-dessous.
Il exclut lectures, aides CLI, éditions et autres audits de clôture. Les
commandes OpenSpec utilisent `/home/devops/.local/npm/bin/openspec` avec
`OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1`.

| Commande ou contrôle | Exécutions | Réussites | Échecs |
|---|---:|---:|---:|
| openspec validate add-tcu-updater --strict | 1 | 1 | 0 |
| Python système unittest ciblé test_tcu_update.py -v | 2 | 1 | 1 |
| Suite complète unittest -v sur les deux Python | 2 | 2 | 0 |
| Qualification combinée initiale sous Python DevOps, arrêt sur absence de yaml | 1 | 0 | 1 |
| Python système : validateur skill-creator sur quatre skills | 1 | 1 | 0 |
| Python DevOps : distributions, paquet isolé, versions et instantané simulé | 1 | 1 | 0 |
| Python système : suite complète unittest -q, permission puis correction | 2 | 1 | 1 |
| Python DevOps : dernière suite complète unittest -q | 1 | 1 | 0 |
| Python DevOps : audit de périmètre, UTF-8/LF et trois py_compile finaux | 1 | 1 | 0 |
| openspec validate --all --strict avant archivage | 1 | 1 | 0 |
| openspec archive add-tcu-updater --json --yes | 1 | 1 | 0 |
| openspec validate --all --strict après archivage | 2 | 1 | 1 |
| Total borné | 16 | 12 | 4 |

Taux sur ces appels : 75 % réussis, 25 % d'échecs intermédiaires résolus. Ce
taux n'est pas celui des derniers tests : 86 réussites sur 86. Un chargement
de module échoué n'est pas compté comme un test fonctionnel réussi.

Les deux dernières commandes de tests sont :

```text
/usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q
/home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -q
```

Échecs et corrections :

- Un littéral bytes accentué dans un test empêchait son import. Il a été
  remplacé par un texte encodé explicitement ; le lancement ciblé suivant a
  réussi avec les vingt premiers tests TCU.
- Le Python DevOps ne possède pas yaml pour quick_validate.py. Le validateur
  existant a été exécuté avec le Python système qui possède sa dépendance,
  sans installation supplémentaire. Le script TCU n'utilise pas PyYAML.
- Le répertoire temporaire héritait du bit setgid du parent : le test du
  mode 0700 a échoué. Un chmod explicite est ajouté après création ; le test
  reste inchangé et réussit dans les suites finales.
- OpenSpec a généré un Purpose provisoire à l'archivage de la nouvelle
  capacité. Le texte a été remplacé par son objet réel dans la spec et son
  delta archivé ; les sept specs passent ensuite en strict, sans réarchivage.

Un patch documentaire rejeté sur son contexte est signalé en section 2 et
n'est pas inclus comme une commande de test. Aucun échec restant connu.

Autres contrôles exécutés et réussis : parité des deux fichiers TCU et du
skill CM ; liens relatifs ; JSON/TOML et sept supports de release ; trois
py_compile intermédiaires puis trois finaux dans des temporaires ; --help du
paquet isolé sur les deux Python ; instantané des vraies sources locales
contrôlé par TCU avec réseau simulé ; RFC 2119 et longueurs ; égalité des neuf
exigences entre deltas et specs principales ; empreintes, tâches et absence
de change actif. Les profils temporaires sont sous tests et nettoyés.

Le test des profils temporaires désactive uniquement la détection de leur
parent dépôt pour simuler une installation ; un test distinct vérifie la
protection du vrai checkout. Aucun cache de profil réel n'est modifié.

Build web et tests navigateur : non pertinents. Publication, installation du
plugin, invocation réelle contre GitHub et mise à jour d'un profil utilisateur :
non exécutées conformément au périmètre validé. Les succès locaux ne sont pas
présentés comme ces opérations.

## 5. Accès web

| Domaine | Pages lues | Refus | Erreurs |
|---|---:|---:|---:|
| docs.github.com | 2 | 0 | 0 |
| Total documentaire | 2 | 0 | 0 |

Deux pages officielles ont été ouvertes dans un appel de documentation :
[contenus et archives GitHub](https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28)
et [commits GitHub](https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28).
Ce sont des lectures documentaires, sans appel réel aux fournisseurs ou au
moteur de mise à jour GitHub. Les URL du code et des fixtures ne sont pas des
visites. Les requêtes des tests sont simulées. La télémétrie OpenSpec est
désactivée ; aucun secret n'est sollicité. Taux documentaire observé : 100 %.

## 6. Synthèse globale

| Repère temporel partiel | Heure Europe/Paris |
|---|---|
| Empreintes avant écriture du change | 2026-10-19 14:31:29 CEST |
| Après archive, validation et audit, avant rapport | 2026-10-19 14:50:12 CEST |
| Intervalle mesuré | 00 h 18 min 43 s |
| Durée totale SCM | N/A, borne initiale complète non instrumentée |

L'intervalle inclut outils et attentes. Il ne mesure pas le temps de génération
et exclut l'exploration antérieure, la rédaction du rapport et les derniers
contrôles ultérieurs.

| Document de la matrice SCM | Bilan et preuve |
|---|---|
| Projet réel | Quatre plugins, commande TCU, deux distributions identiques et liens locaux vérifiés ; sept supports à 0.3.0. |
| AGENTS.md | Inchangé, empreinte conservée ; règles suffisantes pour les écritures, OpenSpec, secrets et tests. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel et rôle de TCU, nom final de TFU. |
| TECHNICAL.md | Mis à jour : quatre plugins, prérequis TCU, provenance, modes, permissions privées et limites du repli. |
| BUILD.md | Mis à jour : plugin et commandes TCU, racines, adoption, sauvegardes et distinction de la livraison locale. |
| DEVOPS.md | Inchangé, empreinte conservée : outils existants utilisés, aucun ajout de dépendance ou inventaire à régénérer. |
| README.md | Mis à jour : 0.3.0, catalogue et usage TCU, liens vers sources et BUILD. |
| CHANGELOG.md | Mis à jour : trois entrées Unreleased ; historique conservé. |
| openspec/specs/ | Extension-distribution et nouvelle capacité tools-codex-update synchronisées ; neuf exigences comparées ; sept specs strictes valides. Release-versioning inchangée. |

Le rôle de TCU est réalisé dans le périmètre local validé. La préparation et
l'application sont distinctes, comme dans la référence documentaire CAB,
sans utiliser ses services. Une invocation explicite autorisera l'application
aux distributions identifiées ; les absents et checkouts resteront préservés.
Les sauvegardes concernent les sources autonomes et données prises en charge ;
une mutation CLI déjà réussie ne bénéficie pas d'une annulation globale.
Les limites, conflits et succès partiels sont explicitement restitués.

Contrôle final exécuté et réussi : six sections, trente chemins existants,
catégories 14 modifications / 15 créations / 1 lien, totaux de commandes
16/12/4 et UTF-8/LF sur les 29 fichiers finaux. Les onze tâches sont terminées,
aucun change actif ni temporaire dans tests ne reste. La parité des ressources
TCU et CM et le nom final TCU sont vérifiés.

État : TERMINÉ pour le périmètre local SCM, rapport vérifié et archivage unique
prouvé. La publication, l'installation et la mise à jour du profil réel
restent non exécutées conformément au périmètre validé.
