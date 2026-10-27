# STATISTIQUES — add-user-llm-refresh-schedule

Projet : Tools Codex (tools-codex), racine /home/devops/datas/tools-codex.
Archive : 2026-10-26-add-user-llm-refresh-schedule.
Date : 26 octobre 2026. Release locale : **0.7.8**.
Session SCM directe, sans pilotage CAB/OpenCode ni sous-agent.

Le développeur a validé le périmètre autonome : installation d'un planning
utilisateur TFL puis PLLM normal à 00 h et 12 h Paris, app ou CLI Codex ouvert,
tests, release, synchronisation, archivage et présent rapport. Il a ajouté :
quota Codex restant nul, aucune exécution TFL/PLLM. Le runner bloque aussi une
valeur inconnue et relit les quotas avant chaque étape. Aucun achat, reset ou
modification d'authentification n'est autorisé ou exécuté.

## 1. Statistiques générales et décisions

| Mesure observée | Valeur |
|---|---:|
| Plugins avec hook SessionStart | 6 |
| Modules scheduler.py identiques | 12 : six autonomes et six embarqués |
| Paires de skills en parité | 6 |
| Supports de release alignés sur 0.7.8 | 9 : VERSION, TOML, README et six manifestes |
| Nouveaux tests distincts | 30 : 25 ordonnanceur et 5 TCU |
| Suite finale Python 3.13.5 | 291 réussites, 0 échec, 0 erreur |
| Suite finale Python 3.14.10 | 291 mêmes cas réussis, 0 échec, 0 erreur |
| Total des deux suites finales | 582 réussites sur 582 exécutions |
| Cas Git non exécuté dans les suites finales | 1 par branche, non compté comme réussi |
| Compilations finales py_compile | 17 par branche, soit 34 réussites |
| Skills contrôlés par quick_validate | 12 valides |
| Tâches de réalisation prouvées | 12 sur 12 |
| OpenSpec ciblé strict préalable | 1 change valide |
| OpenSpec global avant archive | 10 éléments valides sur 10 |
| Archivages exécutés | 1, réussi |
| Exigences synchronisées | 8 ajoutées, 0 modifiée, 0 supprimée, 0 renommée |
| OpenSpec global après archive | 10 spécifications valides sur 10 |
| Changes actifs après archive | 0 |
| Chemins initiaux suivis par empreinte | 72 |
| Fichiers existants modifiés | 26 |
| Fichiers initiaux préservés | 46 |
| Nouveaux fichiers finaux | 29, présent rapport inclus |
| Fichiers supprimés | 0 |
| Total des chemins finaux du dépôt concernés | 55 |

Les tests couvrent installation/réinstallation, mise à jour/retrait reconnus,
conflits, restauration, chemins avec espaces, liens, propriétaires étrangers,
sources absentes ou désactivées, isolement des paquets et hooks concurrents.
Ils couvrent Codex ouvert/fermé, autre UID, daemon/exec isolé, interface unifiée
avec backend enfant, quotas nuls/positifs/inconnus et priorité au bucket codex.
La seconde lecture de quota peut bloquer PLLM après TFL. Échec, délai ou
catalogue ancien empêchent PLLM ; une réussite transmet le nouveau catalogue
et ne passe jamais active. Les verrous empêchent doublons et mise à jour TCU
concurrente. TCU check reste sans écriture, quota ou génération.

Les deux changements d'heure de 2026 ont été vérifiés par systemd-analyze
calendar ; le parseur systemd --user verify accepte les unités en profil
temporaire. Ces commandes ne démarrent ni n'installent un timer réel.
Le contrôle en lecture seule de la présence réelle reconnaît finalement
l'application ouverte ; la lecture réelle des quotas renvoie available.

Tokens, coûts, cache, quota consommé par l'agent, modèle exact de service,
temps de génération et durée totale SCM : **N/A**, aucune télémétrie exhaustive
collectée. Les statistiques de test ne constituent pas une mesure fournisseur.

## 2. Types de messages et d'outils

| Domaine | Observation | Compteur exhaustif |
|---|---|---|
| Développeur | Demande, précision app/CLI ouvert, validation et condition quota nul | N/A, historique non agrégé |
| Progression | Spécification, runner, installation, vérifications et clôture | N/A, historique non agrégé |
| Lectures | Cadrages, prompt SCM, specs, sources/tests et documentation officielle | N/A, appels non totalisés |
| Éditions | apply_patch et Python locaux dans le périmètre validé | N/A, appels non totalisés |
| Validation | unittest, py_compile, quick_validate, systemd-analyze, empreintes et OpenSpec | Sous-ensemble borné section 4 |
| Git | Un test préexistant inclus par erreur dans la première suite TCU a appelé check-ignore en lecture seule ; exclu nominativement ensuite | Aucun commit, push, changement de branche ou de configuration |
| Session native | Lecture de quotas dédiée et détection de présence, sans génération ni redémarrage | Deux diagnostics de présence et une lecture de quotas |
| CAB, OpenCode et sous-agents | Non déclenchés | Non applicable |

Les skills prompt, skill-creator et OpenAI Docs ont servi respectivement à
résoudre SCM, qualifier les ressources et vérifier les interfaces natives.
La compétence coding-session-statistics n'a pas été invoquée. La lecture de
la skill CGPT a précisé le sens des fenêtres ; aucun rendu CGPT ni historique
de quotas n'a été produit.

Des essais d'édition ont été refusés pour contexte non concordant avant
écriture. Les corrections ont ensuite été appliquées aux sections réellement
observées. Ces essais ne sont pas des échecs de validation du produit.

## 3. Fichiers modifiés

Chemins relatifs à la racine indiquée en tête. Les fichiers du change sont
comptés une seule fois sous leur chemin final d'archive.

| Chemin final | Opération |
|---|---|
| `BUILD.md` | Modifié |
| `CHANGELOG.md` | Modifié |
| `PROJECT.md` | Modifié |
| `README.md` | Modifié |
| `TECHNICAL.md` | Modifié |
| `VERSION` | Modifié |
| `openspec/specs/extension-distribution/spec.md` | Modifié |
| `openspec/specs/pllm-evaluation/spec.md` | Modifié |
| `openspec/specs/tools-codex-update/spec.md` | Modifié |
| `plugins/cm/.codex-plugin/plugin.json` | Modifié |
| `plugins/lm/.codex-plugin/plugin.json` | Modifié |
| `plugins/pllm/.codex-plugin/plugin.json` | Modifié |
| `plugins/pllm/skills/pllm/SKILL.md` | Modifié |
| `plugins/prompt/.codex-plugin/plugin.json` | Modifié |
| `plugins/tcu/.codex-plugin/plugin.json` | Modifié |
| `plugins/tcu/skills/tcu/SKILL.md` | Modifié |
| `plugins/tcu/skills/tcu/scripts/update.py` | Modifié |
| `plugins/tfl/.codex-plugin/plugin.json` | Modifié |
| `plugins/tfl/skills/tfl/SKILL.md` | Modifié |
| `pyproject.toml` | Modifié |
| `skills/pllm/SKILL.md` | Modifié |
| `skills/tcu/SKILL.md` | Modifié |
| `skills/tcu/scripts/update.py` | Modifié |
| `skills/tfl/SKILL.md` | Modifié |
| `tests/test_lm_blacklist.py` | Modifié |
| `tests/test_tcu_update.py` | Modifié |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/.openspec.yaml` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/STATISTIQUES.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/design.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/proposal.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/specs/extension-distribution/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/specs/llm-refresh-scheduling/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/specs/pllm-evaluation/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/specs/tools-codex-update/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-user-llm-refresh-schedule/tasks.md` | Créé |
| `openspec/specs/llm-refresh-scheduling/spec.md` | Créé |
| `plugins/cm/hooks/hooks.json` | Créé |
| `plugins/cm/skills/cm/scripts/scheduler.py` | Créé |
| `plugins/lm/hooks/hooks.json` | Créé |
| `plugins/lm/skills/lm/scripts/scheduler.py` | Créé |
| `plugins/pllm/hooks/hooks.json` | Créé |
| `plugins/pllm/skills/pllm/scripts/scheduler.py` | Créé |
| `plugins/prompt/hooks/hooks.json` | Créé |
| `plugins/prompt/skills/prompt/scripts/scheduler.py` | Créé |
| `plugins/tcu/hooks/hooks.json` | Créé |
| `plugins/tcu/skills/tcu/scripts/scheduler.py` | Créé |
| `plugins/tfl/hooks/hooks.json` | Créé |
| `plugins/tfl/skills/tfl/scripts/scheduler.py` | Créé |
| `skills/cm/scripts/scheduler.py` | Créé |
| `skills/lm/scripts/scheduler.py` | Créé |
| `skills/pllm/scripts/scheduler.py` | Créé |
| `skills/prompt/scripts/scheduler.py` | Créé |
| `skills/tcu/scripts/scheduler.py` | Créé |
| `skills/tfl/scripts/scheduler.py` | Créé |
| `tests/test_llm_schedule.py` | Créé |

**26 fichiers modifiés + 29 créés = 55 chemins**, aucune suppression.
Les fichiers de configuration personnelle, rapports fournisseur et unités
du profil réel ne sont pas modifiés. Les artefacts temporaires de tests et
de compilation ont été nettoyés et ne sont pas des livrables.

## 4. Commandes

Sous-ensemble borné aux familles ci-dessous, hors lectures, éditions,
diagnostics natifs, vérification du présent rapport et invocations enfant
systemd déjà incluses dans les suites. Une suite ou un groupe de compilations
compte pour une exécution ; chaque quick_validate enfant compte séparément.

| Famille | Exécutions | Réussies | Échouées |
|---|---:|---:|---:|
| Suites ordonnanceur ciblées | 5 | 4 | 1 |
| Suites TCU ciblées | 3 | 1 | 2 |
| Suites globales Python 3.13/3.14 | 4 | 4 | 0 |
| Groupes py_compile | 3 | 3 | 0 |
| quick_validate de skills | 12 | 12 | 0 |
| OpenSpec ciblé strict | 1 | 1 | 0 |
| OpenSpec global strict | 3 | 3 | 0 |
| Archivage ciblé | 1 | 1 | 0 |
| Audits empreintes/distribution/synchronisation | 2 | 2 | 0 |
| Total borné | 34 | 31 | 3 |

Commandes et mécanismes réellement exécutés :

- /usr/bin/python3.13 -B -W error::ResourceWarning avec unittest ; ciblage
  test_llm_schedule.py, test_tcu_update.py, puis découverte globale.
- /home/devops/python/current/bin/python3 -B -W error::ResourceWarning avec
  la même découverte globale. Les suites finales comportent 291 cas par
  branche ; les deux suites globales antérieures comportaient 289 cas,
  avant les deux derniers cas de présence et de conflit.
- Le lanceur global filtre uniquement
  test_tcu_update.TcuUpdateTests.test_command_sources_are_publishable_without_local_codex_files,
  car ce cas inspecte Git. Aucun code de ce test n'est supprimé ou désactivé.
  Son passage dans la toute première suite TCU n'est pas une preuve de
  réexécution finale, et ne justifie pas de nouvelle inspection Git.
- py_compile.compile avec cfile temporaire et doraise=True : les douze
  ordonnanceurs, les deux updaters et les trois fichiers de tests, sous
  Python 3.13 et 3.14. Un premier groupe 3.13 précédait la dernière correction ;
  les deux groupes finaux qualifient les 17 fichiers courants.
- /home/ade/.codex/skills/.system/skill-creator/scripts/quick_validate.py
  sur les douze distributions de skills ; douze retours zéro.
- systemd-analyze calendar avec base-time aux changements d'heure de mars
  et octobre, et systemd-analyze --user verify sur les unités temporaires.
- /home/devops/.local/npm/bin/openspec validate add-user-llm-refresh-schedule --strict,
  validate --all --strict (trois fois), puis
  archive add-user-llm-refresh-schedule --json --yes entre les deux derniers
  contrôles globaux. OPENSPEC_TELEMETRY=0 et DO_NOT_TRACK=1 à chaque invocation.
- Audits Python par empreintes, sans Git : périmètre attendu, versions,
  douze modules identiques, six paires de skills, UTF-8/LF, huit exigences
  synchronisées et aucun change actif.

Les trois commandes de test en échec étaient intermédiaires et résolues :

1. La première fixture du cas composants absents renvoyait un stdout vide
   pour plugin list ; elle publie désormais la liste JSON vide attendue.
2. L'instantané réel simulé de TCU omettait les nouveaux hooks ; sa collecte
   de fixture a été complétée. L'ancienne assertion « toutes les briques
   absentes » distingue désormais la ligne de planification différée.
3. Cette assertion a ensuite dû utiliser get pour les anciennes lignes
   autonomes qui n'ont pas de champ ressource. Aucun contrôle de produit
   n'a été affaibli pour masquer un échec.

Un diagnostic réel de présence a aussi détecté l'interface unifiée chatgpt :
le détecteur initial renvoyait False. La relation frontend/backend vivant
a été ajoutée et testée, sans assimiler un serveur indépendant à Codex ouvert.
La seconde observation réelle renvoie True.

**Non exécutés** : installation/approbation du hook dans le profil réel,
activation du timer réel, exécution automatique observée à 00 h ou 12 h,
publication Git/marketplace et benchmarks fournisseurs réels.
**Non pertinents** : build web et tests navigateur.
Les erreurs rencontrées sont résolues dans les contrôles exécutés ; le test
Git reste explicitement non exécuté dans les suites finales.

## 5. Accès web

| Source ou domaine | Accès réel | Usage |
|---|---|---|
| developers.openai.com/plugins/build/plugins | Recherche puis ouverture | Manifestes, hooks et confiance native |
| learn.chatgpt.com/docs/hooks | Recherche puis ouverture | SessionStart, commande, variables et async |
| learn.chatgpt.com/docs/app-server | Recherche puis ouverture | initialize et account/rateLimits/read |
| Service Codex via son client natif | Une lecture en direct | available ; aucune donnée de compte ou secret publiée |
| Fournisseurs TFL/PLLM | 0 appel réel | Réseau, quotas et réponses simulés dans les tests |
| GitHub/marketplace pour distribution | 0 publication ou installation | Instantanés et CLI simulés |

Les résultats de recherche non officiels ne servent pas de référence.
Le client de quota est propre au runner et ne se fait pas passer pour un
client natif privilégié. Son unique requête métier est account/rateLimits/read.
Le stockage d'identifiants du client n'est pas lu par l'agent ni copié ; les
sorties du sous-processus restent en mémoire et ne sont pas journalisées.
Les réponses d'authentification ne figurent pas dans les états ou rapports.
Aucune réinitialisation de quota, achat, connexion ou génération Codex.

## 6. Synthèse globale

| Document ou périmètre | Bilan final et preuve |
|---|---|
| Projet réel | Planning, quota avant chaque étape, sources et hooks qualifiés par tests isolés et audits. |
| AGENTS.md | Inchangé, empreinte conservée ; règles existantes suffisantes. |
| PROJECT.md | Mis à jour, Rafraîchissement utilisateur planifié : responsabilité et conditions. |
| TECHNICAL.md | Mis à jour, composition CM, prérequis et Planning utilisateur : interfaces, verrous, stockage, quotas et limites. |
| BUILD.md | Mis à jour, Planning utilisateur : confiance native, bootstrap, contrôle, retrait et distinction d'activation réelle. |
| DEVOPS.md | Inchangé, empreinte conservée ; outils existants, aucun SDK ou paquet système installé. |
| README.md | Mis à jour : 0.7.8 et comportement utilisateur aux deux horaires. |
| CHANGELOG.md | Deux nouvelles entrées Unreleased ; historique antérieur conservé. |
| openspec/specs/ | Une nouvelle capacité et trois capacités complétées ; dix spécifications strictes valides. |
| Archive et statistiques | Archivage unique réussi, douze tâches prouvées, huit exigences synchronisées et présent rapport à six sections. |

Début de l'intervalle d'empreintes : 2026-10-26T10:46:21+01:00.
Durée totale SCM et temps actif du modèle : **N/A**, non instrumentés.
L'exploration et l'attente de validation précèdent cet intervalle.

Le profil réel ne contient toujours ni CODEX_HOME/llm-refresh ni les deux
unités tools-codex-llm-refresh : absence vérifiée après qualification.
La release **locale** 0.7.8 est livrée et archivée. Aucun planning réel n'est
annoncé actif : publication, installation dans le profil et confiance des
hooks restent des étapes distinctes. Un ancien TCU ne peut pas exécuter le
nouveau bootstrap avant son propre chargement actualisé.

État : **TERMINÉ pour le périmètre local SCM validé**.
