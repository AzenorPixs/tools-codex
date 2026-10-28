# STATISTIQUES — add-openrouter-catalog-and-free-policy

Projet : Tools Codex (`tools-codex`). Racine : `/home/devops/datas/tools-codex`.
Archive : `openspec/changes/archive/2026-10-27-add-openrouter-catalog-and-free-policy`.
Release source : 0.7.17. Date : 27 octobre 2026.

Rapport SCM direct dans Codex, sans orchestrateur, sous-agent, pilotage OpenCode/CAB
ou télémétrie associée. Les statistiques non collectées sont indiquées N/A ;
aucune mesure de fournisseur n'est reprise comme preuve de cette livraison.

## 1. Statistiques générales et décisions

PLLM passe à sept politiques : Go payant 1/2, Go gratuit 3/4, OpenRouter payé
5 sans génération/Medium/performance, OpenRouter gratuit 6 benchmarké en Medium,
et DeepSeek 7. TFL conserve les payants OpenRouter admissibles même sans preuve
Medium, tout en gardant Medium et le benchmark gratuit. Le schéma PLLM passe à 3,
les spécifications, distributions et documentation sont alignées sur 0.7.17.

| Mesure vérifiée | Résultat |
|---|---:|
| Priorités PLLM publiées | 7 |
| Modes OpenRouter | 2 : payé metadata-only, gratuit benchmarké |
| Plugins avec manifeste versionné | 6 sur 6 à 0.7.17 |
| Distributions PLLM/TFL comparées | 8 paires identiques |
| Fichiers modifiés par ce change | 43 |
| Fichiers créés dans l'archive, rapport compris | 6 |
| Tests Python | 330 réussis sur 330 |
| Fichiers compilés syntaxiquement | 4 scripts Python |
| Validations OpenSpec strictes avant archivage | 11 éléments sur 11 |
| Validations OpenSpec après archivage | 10 spécifications sur 10 |
| Tâches SCM terminées | 8 sur 8 |
| Changes OpenSpec actifs après archivage | 0 |

Le catalogue TFL généré n'a pas été rafraîchi par des appels fournisseur : les
changements mettent à jour les collecteurs et leur contrat, pas un résultat live.
Les profils/installations locales, la publication distante et le planning réel
restent hors de cette livraison.

Un changement de date dans `DEVOPS.md` était déjà présent avant cette SCM ; il
est préservé et exclu des 43 fichiers modifiés par ce change.

## 2. Types de messages et d'outils

| Domaine | Observation | Compteur exhaustif |
|---|---|---:|
| Messages humains | Périmètre SCM et règle des sept modes fournis par le développeur | N/A, historique non agrégé |
| Suivis de travail | Cadrage, mise à jour, tests et clôture | N/A, historique non agrégé |
| Commandes | Lecture ciblée, syntaxe, suite hors ligne, OpenSpec, comparaison des copies | N/A au total ; vérifications pertinentes en section 4 |
| Édition | Sources, tests, contrats OpenSpec, docs et version locale | 43 fichiers modifiés |
| Archivage | Une archive OpenSpec, cinq artefacts de change et ce rapport | 6 fichiers créés |
| Git | État consulté en lecture seule ; aucun commit, branche, push ou configuration modifiée | Non applicable |
| Web et fournisseurs | Aucun appel externe dans cette SCM | 0 |
| OpenCode, CAB et sous-agents | Non utilisés | Non applicable |

La durée totale SCM est N/A : aucune borne de début complète n'a été instrumentée.

## 3. Fichiers modifiés et archivés

Les 43 fichiers modifiés se répartissent ainsi :

| Groupe | Nombre | Contenu |
|---|---:|---|
| PLLM autonome et embarqué | 10 | Skills, évaluateurs, JSON/Markdown d'initialisation et mémoire de performance, parité des deux distributions |
| TFL autonome et embarqué | 4 | Skills et collecteurs OpenRouter, parité des deux distributions |
| Catalogue CM | 2 | Description TFL mise à jour dans les deux copies CM |
| Tests | 11 | Migrations, catégories, sélection, prix, Medium, blacklist, performances et versions |
| Commandes et documentation | 10 | Wrappers PLLM/TFL, BUILD, README, TECHNICAL, CHANGELOG, VERSION, pyproject et deux spécifications actives |
| Manifestes plugins | 6 | CM, LM, PLLM, PROMPT, TCU et TFL, version 0.7.17 |

L'archive contient `proposal.md`, `design.md`, `tasks.md`, deux spécifications
delta, et `STATISTIQUES.md`. `DEVOPS.md` n'est pas inclus dans les modifications
SCM de cette archive.

## 4. Vérifications et résultats

- `/home/devops/python/current/bin/python3 -m unittest discover -s tests` :
  330 tests réussis, aucun échec.
- `python3 -m py_compile` : les évaluateurs PLLM autonome/embarqué et les
  générateurs TFL autonome/embarqué compilent.
- `openspec validate --all --strict` avant archivage : 11/11 éléments valides.
- `openspec validate --all --strict` après archivage : 10/10 spécifications
  valides ; `openspec status --all` confirme zéro change actif.
- Comparaison octet par octet : PLLM skill, script et trois fichiers de données ;
  TFL skill et script ; CM skill : 8 paires identiques.
- Contrôle de version : `VERSION`, `pyproject.toml` et les six manifestes
  déclarent 0.7.17 ; l'état de départ PLLM contient sept modes au schéma 3.
- UTF-8/LF et fin LF vérifiés sur les 50 chemins texte modifiés, créés ou
  préexistants du statut de travail ; `DEVOPS.md` est contrôlé mais reste hors
  des modifications de cette SCM.

Les tests sont hors ligne : ils ne prouvent ni l'accès aux fournisseurs, ni la
performance réelle d'un modèle, ni une installation dans un profil Codex.
Mode5 ne déclenche volontairement aucun benchmark. Le catalogue `tfl.json` n'a
pas été régénéré ; un prochain TFL le reconstruira depuis OpenRouter avec les
nouveaux filtres payant/gratuit.

## 5. Accès web et fournisseurs

| Périmètre SCM | Appels | Refus | Erreurs |
|---|---:|---:|---:|
| Accès web | 0 | 0 | 0 |
| APIs OpenCode Go, OpenRouter ou DeepSeek | 0 | 0 | 0 |
| Trousseau fournisseur | 0 | 0 | 0 |

Les clés, soldes et données de compte n'ont pas été consultés dans cette SCM.
Les résultats de l'évaluation PLLM précédente ne sont pas repris comme mesures.

## 6. Synthèse et statut SCM

| Document ou contrôle | Résultat |
|---|---|
| `VERSION`, `pyproject.toml`, README et manifests | 0.7.17 aligné |
| `openspec/specs/pllm-evaluation/spec.md` | Sept politiques, migration schéma 3, mode5 sans benchmark, modes 6/7 distincts |
| `openspec/specs/tfl-catalog/spec.md` | Payants OpenRouter admis sans Medium ; gratuits encore benchmarkés en Medium |
| Skills et scripts PLLM/TFL | Copies autonomes/embarquées synchronisées |
| Tâches du change | 8/8 terminées |
| Archivage | `2026-10-27-add-openrouter-catalog-and-free-policy` réussi |
| Vérification finale | Six sections présentes ; totaux concordants ; UTF-8/LF contrôlés |

État : TERMINÉ pour le périmètre SCM local. Aucune installation utilisateur,
publication distante, actualisation live TFL ou sélection de modèle mesurée
n'est annoncée.
