# STATISTIQUES — add-lm-shared-model-blacklist

Projet : Tools Codex (`tools-codex`), racine `/home/devops/datas/tools-codex`.
Archive : `2026-10-26-add-lm-shared-model-blacklist`. Release locale : **0.7.6**.
Date : 26 octobre 2026. Session SCM exécutée directement par Codex.

Le développeur a validé explicitement le périmètre autonome : /LM initialisé
avec mimo-v2.5, filtre TFL/PLLM, LM dans CM, release commune, spécification,
qualification, archivage et présent rapport. Aucun pilotage CAB/OpenCode,
sous-agent ou skill de statistiques de session pilotée n'a été utilisé.
Les preuves détaillées et la matrice documentaire figurent aussi dans
[VALIDATION.md](VALIDATION.md). Les mesures absentes restent N/A motivées.

## 1. Statistiques générales et décisions

| Mesure observée | Valeur |
|---|---:|
| Plugins locaux de marketplace | 6 : CM, LM, PLLM, TFL, TCU, prompt |
| Entrées de commandes dans chaque CM | 6, LM inclus avec /LM et LIST/ADD/REMOVE |
| Supports de release alignés à 0.7.6 | 9 : VERSION, TOML, README et 6 manifestes |
| Copies identiques du module model_blacklist.py | 6 |
| Paires autonome/embarquée en parité | 6 |
| Liens locaux conformes | 4 : CM, TCU, prompt conservés ; LM ajouté |
| Nouveaux tests distincts | 23 : 20 LM et 3 TCU |
| Suite finale Python 3.13.5 | 256 cas distincts réussis, 0 échec, 0 erreur |
| Suite finale Python 3.14.10 | 256 mêmes cas réussis, 0 échec, 0 erreur |
| Total des deux suites finales | 512 réussites sur 512 exécutions autorisées |
| Test Git préexistant non exécuté | 1 par branche ; interdit par SCM, non présenté comme réussi |
| Compilations py_compile | 35 par branche, soit 70 réussites |
| Skills contrôlés par skill-creator | 12 valides |
| Tâches de réalisation vérifiées | 11 sur 11 |
| OpenSpec global avant archivage | 9 éléments valides sur 9 |
| Archivages exécutés | 1, réussi |
| Exigences synchronisées | 8 ajoutées, 5 modifiées, 0 supprimée, 0 renommée |
| OpenSpec global final | 9 spécifications valides sur 9 |
| Changes actifs après archivage | 0 |
| Chemins initiaux suivis par empreinte | 78 |
| Chemins initiaux modifiés | 33 |
| Chemins initiaux préservés | 45 |
| Nouveaux fichiers finaux | 26 |
| Nouveau lien relatif | 1 |
| Fichiers supprimés | 0 |

Le périmètre d'empreintes est ciblé : cadrages, release, marketplace,
commandes, skills, manifestes, scripts, tests, liens et spécifications.
Il n'est pas un inventaire récursif du dépôt ni une inspection Git.
Les anciens répertoires d'archives ne sont pas inclus dans les 78 chemins.

LM LIST est sans écriture. ADD/REMOVE partagent le fichier utilisateur hors
cache ; le défaut mimo-v2.5 est appliqué même si ce fichier manque.
Les préfixes fournisseur et suffixes gratuits ne contournent pas le filtre.
Les exclusions permanentes restent en vigueur. Les tests prouvent le refus
des rangs forcés interdits sans substitution, la non-génération des modèles
interdits et la conservation des personnalisations par TCU.
Les seuils, quotas, priorités, transports et protocole 8 restent conservés.

Modèle exact de service, version, raisonnement, tokens, coûts, cache, quotas,
TTMT et débit de génération de l'agent : **N/A**, aucune télémétrie de session
collectée. Aucun quota de compte partagé n'est attribué à ce change.

## 2. Types de messages et d'outils

| Domaine | Observation | Compteur exhaustif |
|---|---|---|
| Messages humains | Demande initiale puis validation explicite ; rappel LM dans CM | N/A, historique non agrégé |
| Messages de progression | Exploration, réalisation, résultats et clôture | N/A, historique non agrégé |
| Lectures et diagnostics | Sources ciblées, prompt SCM, cadrages, tests et spécifications | N/A, tous les appels ne sont pas totalisés |
| Éditions | apply_patch et Python locaux, dans le projet | N/A, pas d'agrégation exhaustive des appels |
| Vérifications | unittest, py_compile, quick_validate, audits locaux et OpenSpec | Sous-ensemble borné en section 4 |
| Git | Aucune commande ou inspection exécutée ; cas de test appelant Git exclu | Non applicable |
| Réseau fournisseur, publication, installation | Non exécutés | Non applicable |
| CAB, OpenCode et sous-agents | Non déclenchés | Non applicable |

Les skills prompt et skill-creator servent à résoudre SCM et construire les
ressources LM. Ils n'autorisent pas de modification du profil installé.
Un appel outil réussi n'est pas une validation humaine supplémentaire.

## 3. Fichiers modifiés

Chemins relatifs à la racine indiquée en tête du rapport. Les neuf fichiers
du change avant ce rapport ont été créés dans le change actif puis archivés ;
ils sont comptés une seule fois sous leur chemin final.

| Chemin final | Opération |
|---|---|
| `.agents/plugins/marketplace.json` | Modifié |
| `BUILD.md` | Modifié |
| `CHANGELOG.md` | Modifié |
| `PROJECT.md` | Modifié |
| `README.md` | Modifié |
| `TECHNICAL.md` | Modifié |
| `VERSION` | Modifié |
| `openspec/specs/extension-distribution/spec.md` | Modifié |
| `openspec/specs/pllm-evaluation/spec.md` | Modifié |
| `openspec/specs/tfl-catalog/spec.md` | Modifié |
| `plugins/cm/.codex-plugin/plugin.json` | Modifié |
| `plugins/cm/skills/cm/SKILL.md` | Modifié |
| `plugins/pllm/.codex-plugin/plugin.json` | Modifié |
| `plugins/pllm/skills/pllm/SKILL.md` | Modifié |
| `plugins/pllm/skills/pllm/scripts/evaluate.py` | Modifié |
| `plugins/prompt/.codex-plugin/plugin.json` | Modifié |
| `plugins/tcu/.codex-plugin/plugin.json` | Modifié |
| `plugins/tfl/.codex-plugin/plugin.json` | Modifié |
| `plugins/tfl/skills/tfl/SKILL.md` | Modifié |
| `plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py` | Modifié |
| `pyproject.toml` | Modifié |
| `skills/cm/SKILL.md` | Modifié |
| `skills/pllm/SKILL.md` | Modifié |
| `skills/pllm/scripts/evaluate.py` | Modifié |
| `skills/tfl/SKILL.md` | Modifié |
| `skills/tfl/scripts/test_fournisseur_llm.py` | Modifié |
| `tests/test_extension_qualification.py` | Modifié |
| `tests/test_free_performance.py` | Modifié |
| `tests/test_pllm_free_fallback.py` | Modifié |
| `tests/test_tcu_update.py` | Modifié |
| `tests/test_tfl_go_metadata.py` | Modifié |
| `tests/test_tfl_opencode_catalog.py` | Modifié |
| `tests/test_tfl_pricing.py` | Modifié |
| `.codex/commands/LM.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/.openspec.yaml` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/STATISTIQUES.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/VALIDATION.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/design.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/proposal.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/specs/extension-distribution/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/specs/lm-blacklist/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/specs/pllm-evaluation/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/specs/tfl-catalog/spec.md` | Créé |
| `openspec/changes/archive/2026-10-26-add-lm-shared-model-blacklist/tasks.md` | Créé |
| `openspec/specs/lm-blacklist/spec.md` | Créé |
| `plugins/lm/.codex-plugin/plugin.json` | Créé |
| `plugins/lm/skills/lm/SKILL.md` | Créé |
| `plugins/lm/skills/lm/agents/openai.yaml` | Créé |
| `plugins/lm/skills/lm/scripts/lm.py` | Créé |
| `plugins/lm/skills/lm/scripts/model_blacklist.py` | Créé |
| `plugins/pllm/skills/pllm/scripts/model_blacklist.py` | Créé |
| `plugins/tfl/skills/tfl/scripts/model_blacklist.py` | Créé |
| `skills/lm/SKILL.md` | Créé |
| `skills/lm/agents/openai.yaml` | Créé |
| `skills/lm/scripts/lm.py` | Créé |
| `skills/lm/scripts/model_blacklist.py` | Créé |
| `skills/pllm/scripts/model_blacklist.py` | Créé |
| `skills/tfl/scripts/model_blacklist.py` | Créé |
| `tests/test_lm_blacklist.py` | Créé |
| `.agents/skills/lm` | Lien relatif créé vers ../../skills/lm |

| Catégorie finale | Nombre |
|---|---:|
| Fichier existant modifié | 33 |
| Nouveau fichier | 26 |
| Nouveau lien symbolique relatif | 1 |
| Fichier supprimé | 0 |
| Total des chemins finaux concernés | 60 |

Les modifications des tests existants servent à embarquer le nouveau module
dans les paquets isolés et à isoler CODEX_HOME, y compris lorsqu'une fixture
vide l'environnement. Les trois nouveaux cas TCU qualifient LM absent,
LM présent et le véritable instantané local à six plugins.
Les sources TCU et prompt ne sont pas modifiées ; seuls leurs manifestes
portent la nouvelle release. AGENTS.md et DEVOPS.md ont conservé leur empreinte.
Aucun ancien rapport utilisateur n'a été migré ou réécrit par LM.

## 4. Commandes

Sous-ensemble borné aux validations et à l'archivage ci-dessous, excluant
lectures, aides, diagnostics de localisation, éditions et contrôle du présent
rapport. Chaque invocation enfant de quick_validate compte séparément ;
une suite ou un groupe de compilations compte pour une exécution.

| Famille de commande | Exécutions | Réussies | Échouées |
|---|---:|---:|---:|
| OpenSpec ciblé strict | 2 | 1 | 1 |
| Suites LM ciblées | 3 | 2 | 1 |
| Suites globales autorisées Python 3.13/3.14 | 4 | 3 | 1 |
| Groupes py_compile, imports et fuseau | 2 | 2 | 0 |
| quick_validate des skills | 12 | 12 | 0 |
| Audit versions/parité/liens/catalogue | 2 | 1 | 1 |
| Audit UTF-8/LF préalable | 1 | 1 | 0 |
| Exécution LM LIST sans profil | 1 | 1 | 0 |
| OpenSpec global strict avant/après archive | 4 | 3 | 1 |
| Archive ciblée | 1 | 1 | 0 |
| Total borné | 32 | 27 | 5 |

Les cinq exécutions en échec sont intermédiaires et résolues ; ce décompte
n'est pas le taux des suites finales, qui est de 512/512 exécutions autorisées.

Commandes et mécanismes effectivement utilisés :

- `/usr/bin/python3.13 -B -W error::ResourceWarning` et
  `/home/devops/python/current/bin/python3 -B -W error::ResourceWarning`,
  avec `unittest.defaultTestLoader.discover('tests')` et
  `unittest.TextTestRunner`, après exclusion nominative du seul cas Git.
- Ciblage LM : `-m unittest discover -s tests -p test_lm_blacklist.py`.
- `py_compile.compile(..., cfile=..., doraise=True)` sur les 35 scripts/tests,
  sorties temporaires sous tests/ puis nettoyées.
- `/usr/bin/python3.13 -B /home/ade/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill>`
  pour les douze distributions.
- `skills/lm/scripts/lm.py LIST` sous CODEX_HOME de test absent ; affichage
  de mimo-v2.5, aucun fichier ou dossier de profil créé.
- `/home/devops/.local/npm/bin/openspec validate add-lm-shared-model-blacklist --strict`,
  `validate --all --strict` et
  `archive add-lm-shared-model-blacklist --json --yes`, avec
  `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1`.

Erreurs résolues :

1. Exigence PLLM trop longue au premier strict : séparée en deux exigences
   avant toute implémentation.
2. Trois erreurs dans la première suite LM : classe d'exception d'un autre
   paquet, état simulé incomplet et attente incorrecte d'un catalogue TFL vide.
   Les fixtures ont été corrigées ; le blocage sur catalogue vide est préservé.
3. Première suite globale : la nouvelle fixture TFL omettait la provenance
   tarifaire ; elle a été complétée sans modifier le collecteur.
4. Premier audit de distribution : il supposait six liens de découverte
   préexistants ; le diagnostic a établi les quatre liens réellement concernés.
   Aucun lien PLLM/TFL supplémentaire n'a été ajouté.
5. Premier strict après archive : OpenSpec avait généré un Purpose provisoire
   pour la nouvelle capacité. Son objet réel a été renseigné dans la spec
   principale et le delta archivé, sans second archivage ; strict final 9/9.

Le vérificateur final du rapport a nécessité deux corrections d'expressions
régulières (détection des sections puis séparation des titres d'exigence) et
une correction de syntaxe du script d'orchestration, avant contrôle réussi.
Ces essais sont exclus du sous-ensemble borné ci-dessus ; ils n'ont pas
révélé d'anomalie des sources ni des totaux du rapport.

Le test préexistant
`test_command_sources_are_publishable_without_local_codex_files` est
**non exécuté**, car il lance Git, interdit par SCM sans demande explicite.
Un contrôle documentaire séparé a vérifié les exclusions .codex et les
réinclusions des commandes dans .gitignore, sans se substituer à ce test
comme preuve d'une exécution Git.

Aucun échec restant connu dans les validations exécutées. Installation et
chargement réel d'une nouvelle session, publication distante, tests de
performance fournisseur : **non exécutés**, hors périmètre.
Build web et tests navigateur : **non pertinents**.

## 5. Accès web

| Domaine | Accès réels exécutés | Observation |
|---|---:|---|
| Fournisseurs LLM | 0 | Requêtes, générations et trousseau simulés dans les tests |
| GitHub/marketplace | 0 | Instantanés et CLI TCU simulés |
| Documentation distante | 0 | Sources locales et conventions existantes suffisantes |
| Total réseau métier/documentaire | 0 | Aucune visite web n'est déduite d'une URL de code |

La télémétrie OpenSpec est désactivée pour les validations et l'archivage.
Les URL présentes dans les fixtures ou les sources ne comptent pas comme
visites. Aucun secret fournisseur n'est sollicité ou affiché.

## 6. Synthèse globale

| Repère temporel partiel | Europe/Paris |
|---|---|
| Empreintes initiales avant écriture du change | 26/10/2026 2:47:05 UTC+1 |
| Audit après archivage et strict réussi, avant rapport | 26/10/2026 3:05:05 UTC+1 |
| Intervalle mesuré | 18 min 0 s |
| Durée totale SCM | N/A : exploration antérieure, attente de validation et rédaction finale non instrumentées |

L'intervalle comprend outils et attentes ; il n'est pas une mesure du temps
de génération ni du temps de calcul du modèle.

| Document ou périmètre | Bilan final et preuve |
|---|---|
| Projet réel | LM, six plugins, stockage commun, filtrage et release validés par tests et audits. |
| AGENTS.md | Inchangé, empreinte conservée ; règles suffisantes pour ce périmètre. |
| PROJECT.md | Mis à jour : Organisation, Catalogue actuel, Liste noire des modèles. |
| TECHNICAL.md | Mis à jour : six plugins, invocations et section Liste noire LM. |
| BUILD.md | Mis à jour : catalogue et Distribution et utilisation de LM, limites du retour de version. |
| DEVOPS.md | Inchangé, empreinte conservée ; outils existants et aucune nouvelle dépendance. |
| README.md | Mis à jour : 0.7.6, LM dans CM, syntaxes et limites d'installation. |
| CHANGELOG.md | Trois entrées Unreleased ; historique conservé. |
| openspec/specs/ | Quatre capacités synchronisées ; neuf spécifications strictes valides. |
| Archive et rapport | Archivage unique prouvé, zéro change actif ; présent rapport à six sections et chemins vérifiables. |

La livraison locale satisfait le périmètre validé. Les copies installées
dans le profil réel ne sont pas actualisées par ce travail. Une publication
puis une installation/mise à jour distinctes seront nécessaires pour les
charger dans une nouvelle session. Une ancienne release ignore LM et ne
conserve donc pas sa garantie d'exclusion. Les rapports précédents restent
historiques jusqu'à leur prochaine invocation.

État : **TERMINÉ pour le périmètre local SCM**. Rapport contrôlé : six
sections, 60 chemins existants (33 modifiés, 26 fichiers créés et un lien),
totaux cohérents, UTF-8/LF, treize exigences synchronisées identiques et
aucun change actif ni temporaire de test restant.

