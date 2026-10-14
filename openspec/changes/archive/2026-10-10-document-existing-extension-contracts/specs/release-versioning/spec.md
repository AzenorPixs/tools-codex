## ADDED Requirements

### Requirement: Métadonnée Python alignée sur la release
La métadonnée `project.version` de `pyproject.toml` SHALL être égale à la
release déclarée dans `VERSION`. `VERSION` SHALL rester la source de vérité ;
une mise à jour de release SHALL préserver cet alignement et celui des
manifestes de plugins sans introduire une version Python indépendante.

#### Scenario: Vérification de la release Python
- **WHEN** les métadonnées du dépôt et les manifestes publiés sont examinés
- **THEN** `project.version`, les versions des plugins et `VERSION` déclarent la même release
