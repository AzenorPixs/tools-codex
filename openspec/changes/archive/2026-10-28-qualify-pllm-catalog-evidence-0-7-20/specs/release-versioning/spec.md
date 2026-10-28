## MODIFIED Requirements

### Requirement: Alignement des plugins publiés
Chaque plugin publié par la marketplace Tools Codex SHALL déclarer la même
version de release que la source de vérité du projet. Un suffixe de métadonnée
de build MAY être ajouté sans modifier la version de release. Une release
validée SHALL aligner les six manifestes plugins actuellement déclarés dans
le catalogue Tools Codex.

#### Scenario: Vérification des manifestes de plugin
- **WHEN** les manifestes de tous les plugins de la marketplace sont contrôlés
- **THEN** leur version de release correspond à celle déclarée par Tools Codex
- **AND** chacun des six plugins actuellement déclarés porte la même version
