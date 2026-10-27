# Statistiques — optimize-pllm-first-valid-selection

## 1. Statistiques générales

- Projet : Tools Codex (`tools-codex`). Session : SCM directe, périmètre validé
  explicitement par le développeur dans cette conversation.
- Rapport établi le 2026-10-26T01:35:48+01:00, heure de Paris.
- Objectif : premier succès des payants 1/2/5 par coût moyen croissant et ordre
  TFL à prix égal ; premier succès des gratuits 3/4 dans l'ordre Go puis général.
- Mode5 exclusivement payant ; crédit épuisé, invalide sans gratuit. Mode6
  conserve son candidat direct. Seuils, paliers et HIGH/XHIGH conservés.
- Release incrémentée après qualification : 0.7.4 → 0.7.5, sept fichiers de
  métadonnées alignés (VERSION, pyproject.toml, cinq manifestes).
- Archivage réussi : `2026-10-26-optimize-pllm-first-valid-selection` ;
  synchronisation de 12 exigences, 0 ajout, 0 suppression, 0 renommage.
- Durée totale et temps actif : N/A — début et temps actif non instrumentés.
- Tokens de l'agent et coût de session : N/A — collecte exhaustive absente.
- Quotas, soldes et performances fournisseur actuels : N/A — aucun benchmark
  réel lancé par ce correctif hors ligne, résultats antérieurs non réutilisés.

## 2. Messages et outils

Messages développeur/agent, nombre total d'appels et répartition exhaustive :
N/A — aucun comptage exhaustif instrumenté. Les outils locaux d'exécution,
d'édition et le résolveur prompt ont servi à charger SCM et réaliser ce change.
Aucune télémétrie de session pilotée ni compétence coding-session-statistics
n'a été déclenchée. Le travail est une session de codage directe.

Les validations humaines sont le périmètre SCM, les règles reformulées des
modes 1 à 5 et l'incrément des briques à l'issue du correctif. Aucun mandat CAB
n'est applicable. Aucun commit, préparation de commit, branche, push,
installation de profil ou bascule OpenCode n'a été réalisé sous SCM.

## 3. Fichiers

Inventaire local du périmètre final, sans utilisation de Git sous SCM :
**28 fichiers** = 23 fichiers préexistants modifiés + 5 artefacts créés dans
l'archive. Les quatre artefacts initiaux du change ont été déplacés par
l'archivage OpenSpec ; STATISTIQUES.md a été créé après cet archivage.

| Groupe | Nombre |
|---|---:|
| Scripts PLLM | 2 |
| Instructions PLLM | 2 |
| Tests | 6 |
| README, TECHNICAL, BUILD, CHANGELOG | 4 |
| Commande source PLLM | 1 |
| VERSION, pyproject.toml et cinq manifestes | 7 |
| Spécification courante | 1 |
| Artefacts d'archive, rapport inclus | 5 |
| Total | 28 |

- `skills/pllm/scripts/evaluate.py`
- `plugins/pllm/skills/pllm/scripts/evaluate.py`
- `skills/pllm/SKILL.md`
- `plugins/pllm/skills/pllm/SKILL.md`
- `tests/test_pllm_price_priority.py`
- `tests/test_pllm_free_fallback.py`
- `tests/test_pllm_six_modes.py`
- `tests/test_free_performance.py`
- `tests/test_extension_qualification.py`
- `tests/test_throughput_measurement.py`
- `README.md`
- `TECHNICAL.md`
- `BUILD.md`
- `CHANGELOG.md`
- `.codex/commands/pllm.md`
- `VERSION`
- `pyproject.toml`
- `plugins/cm/.codex-plugin/plugin.json`
- `plugins/pllm/.codex-plugin/plugin.json`
- `plugins/prompt/.codex-plugin/plugin.json`
- `plugins/tcu/.codex-plugin/plugin.json`
- `plugins/tfl/.codex-plugin/plugin.json`
- `openspec/specs/pllm-evaluation/spec.md`
- `openspec/changes/archive/2026-10-26-optimize-pllm-first-valid-selection/proposal.md`
- `openspec/changes/archive/2026-10-26-optimize-pllm-first-valid-selection/design.md`
- `openspec/changes/archive/2026-10-26-optimize-pllm-first-valid-selection/tasks.md`
- `openspec/changes/archive/2026-10-26-optimize-pllm-first-valid-selection/specs/pllm-evaluation/spec.md`
- `openspec/changes/archive/2026-10-26-optimize-pllm-first-valid-selection/STATISTIQUES.md`

Lignes ajoutées/supprimées : N/A — aucun diff Git demandé et aucune mesure
initiale de lignes enregistrée. Les fichiers de données fournisseur,
rapports de politique et configurations privées n'ont pas été régénérés.

## 4. Commandes et validations

- Référence avant modification et avant SCM : 71 tests PLLM réussis.
- Suite finale Python DevOps 3.14.10 : **234 tests réussis en 6,635 s**.
- Suite finale Python système 3.13.5 : **234 tests réussis en 5,127 s**.
- Total des deux suites finales : **468 exécutions de tests**, correspondant
  à **234 tests distincts**. Ce total n'inclut pas les passes intermédiaires.
- Les suites utilisent réellement `unittest.defaultTestLoader.discover("tests")`
  avec le lanceur suivant, exécuté sous chaque interpréteur avec `-B -c` :

```python
import pathlib, tempfile, unittest
root = pathlib.Path.cwd()
holder = tempfile.TemporaryDirectory(prefix=".pllm-validation-", dir=root)
tempfile.tempdir = holder.name
suite = unittest.defaultTestLoader.discover("tests")
result = unittest.TextTestRunner(verbosity=1).run(suite)
holder.cleanup()
raise SystemExit(not result.wasSuccessful())
```

- Syntaxe des huit fichiers Python modifiés : `py_compile` réussi sous
  3.14.10, cache temporaire dans le dépôt puis nettoyé.
- Parité exacte des deux scripts PLLM et des deux SKILL.md ; UTF-8/LF
  contrôlés. Moteur de mesure partagé conservé.
- `quick_validate.py skills/pllm` et
  `quick_validate.py plugins/pllm/skills/pllm` : réussis sous Python 3.13.5.
  La tentative initiale sous le Python DevOps n'avait pas PyYAML ; le Python
  système déjà équipé a permis le contrôle, sans installer de dépendance.
- `openspec validate optimize-pllm-first-valid-selection --strict` : réussi
  avant code/tests, après correction des scénarios initialement omis du delta.
- Avant archivage : `openspec validate --all` et `--all --strict`, **9/9**.
- `openspec archive optimize-pllm-first-valid-selection --json --yes` :
  réussi, 12 exigences synchronisées. L'appel JSON initial sans `--yes`
  demandait la confirmation déjà couverte par le périmètre d'archivage validé.
- Après archivage : un nouvel avertissement de longueur a d'abord fait échouer
  le strict ; le texte a été resserré sans changement de règle dans le delta
  archivé et la spécification courante. Aucun réarchivage.
- Résultats finaux : `openspec validate --all` et `--all --strict`, **8/8**,
  zéro échec et zéro avertissement.

Les échecs intermédiaires des anciennes attentes exhaustives et de fixtures
ont été corrigés dans le périmètre. Les tests finaux vérifient l'ordre des
prix, leur égalité décimale, l'arrêt au premier succès, le candidat suivant
après échec, contexte ≥1M, HIGH/XHIGH, les seuils payants/gratuits distincts,
les erreurs HTTP, ressources avant requête, mémoire, forçages et publication.
Les benchmarks fournisseurs et l'installation réelle sont **non exécutés**.
Les tests navigateur sont **non pertinents** : aucune interface modifiée.

## 5. Accès web

Aucun benchmark réel ni collecte TFL lancé pendant SCM. Réseau et trousseau
fournisseur sont isolés dans les fixtures de test. Les mesures réelles de la
précédente invocation PLLM ne sont pas des résultats de ce correctif.
Nombre de requêtes réseau de tous les processus auxiliaires : N/A — absence
de télémétrie exhaustive ; aucun contenu secret ou corps privé n'est publié.

## 6. Synthèse et cohérence documentaire

| Élément | Bilan et preuve |
|---|---|
| Projet réel | Premier succès vérifié dans les deux distributions par les 234 tests sur chaque runtime ; mode6 préservé. |
| AGENTS.md | Inchangé : règles générales, secrets, Git et rapport d'archive toujours applicables. |
| PROJECT.md | Inchangé : catalogue d'extensions, distribution et source VERSION toujours exacts. |
| TECHNICAL.md | Mis à jour : Prérequis d'exécution, catégories fixes, sélection ordonnée, contexte d'entrée et active. |
| BUILD.md | Mis à jour : utilisation PLLM et référence à la release 0.7.5 ; installation distincte conservée. |
| DEVOPS.md | Inchangé : inventaire et chemins des outils conservés, aucune dépendance ajoutée. |
| README.md | Mis à jour : modes, premier succès, contexte et version 0.7.5. |
| CHANGELOG.md | Mis à jour : entrées Unreleased sur le correctif, le mode5 exclusivement payant et l'incrément, sans publication distante inventée. |
| openspec/specs/ | pllm-evaluation synchronisé ; release-versioning respecté ; contrôle final standard et strict 8/8. |

Le choix n'est plus le meilleur débit parmi toutes les réussites : à prix
égal ou pour les gratuits, le premier candidat conforme est retenu. C'est le
compromis de durée explicitement demandé. Le mode5 n'offre plus de repli
gratuit. Les tests actuels, leurs contrôles et leurs mesures ne sont pas
assouplis. La release locale ne prouve ni publication distante ni activation
dans les profils déjà installés. Aucun blocage connu ne subsiste dans le
périmètre livré. Ce rapport, ses six sections et ses totaux sont contrôlés
avant la restitution finale.
