# Tasks

## 1. Corriger et couvrir les filtres

- [x] 1.1 Ignorer les métadonnées historiques `user_override` et `performance_attempts` dans le contrôle d'effort, tout en conservant le contrôle strict des mesures courantes ; vérifier avec `python3 -m unittest discover -s tests -p 'test_reasoning_admission.py'`.
- [x] 1.2 Tolérer uniquement l'arrondi flottant documenté des prix canoniques, préserver les valeurs décimales pour le calcul et couvrir les cas équivalent/contradictoire ; vérifier avec `python3 -m unittest discover -s tests -p 'test_openrouter_eur_filter.py'`.

## 2. Aligner la release et sa documentation

- [x] 2.1 Aligner `VERSION`, `pyproject.toml`, `README.md` et les six manifestes sur 0.7.16 ; vérifier par lecture JSON des manifestes et comparaison avec la source de version.
- [x] 2.2 Décrire les deux corrections dans `CHANGELOG.md` et actualiser les attentes de version ; vérifier avec `python3 -m unittest discover -s tests -p 'test_lm_blacklist.py'` et `python3 -m unittest discover -s tests -p 'test_tcu_update.py'`.

## 3. Validation globale

- [x] 3.1 Vérifier syntaxe, parité des quatre copies, cohérence documentaire et OpenSpec ; exécuter `python3 -m py_compile` sur les sources/test concernés, `python3 -m unittest discover -s tests` et `openspec validate --all --strict`.

## Workflow follow-up

- Archiver uniquement ce change après réussite des validations et synchronisation des spécifications principales.
- Produire et vérifier `openspec/changes/archive/pllm-current-medium-and-openrouter-price-normalization/STATISTIQUES.md` conformément à `AGENTS.md`.
- Après archivage et statistiques, appliquer le commit local SCM conditionnel, puis les publications Forgejo/GitHub/GitLab uniquement si leurs variables et préconditions SCM sont présentes et satisfaites.
