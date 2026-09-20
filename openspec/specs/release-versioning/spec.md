# release-versioning Specification

## Purpose
Définir une version de release commune et vérifiable pour les artefacts publiés
par Tools Codex et permettre aux utilisateurs d'identifier cette release.

## Requirements

### Requirement: Version de release unique
Tools Codex SHALL déclarer une version de release unique dans une source de
vérité versionnée. Les utilisateurs et les artefacts distribués SHALL pouvoir
identifier cette version sans recourir à une valeur implicite ou à un horodatage
de build.

#### Scenario: Consultation de la version de projet

- **WHEN** un utilisateur lit la source de vérité de version du projet
- **THEN** il obtient la version de release publiée exacte

### Requirement: Alignement des plugins publiés
Chaque plugin publié par la marketplace Tools Codex SHALL déclarer la même
version de release que la source de vérité du projet. Un suffixe de métadonnée
de build MAY être ajouté sans modifier la version de release.

#### Scenario: Vérification des manifestes de plugin

- **WHEN** les manifestes de tous les plugins de la marketplace sont contrôlés
- **THEN** leur version de release correspond à celle déclarée par Tools Codex

### Requirement: Documentation de la release
La documentation publique du projet SHALL indiquer la version de release
courante et identifier sa source de vérité.

#### Scenario: Consultation de la présentation du projet

- **WHEN** un utilisateur consulte la documentation publique de Tools Codex
- **THEN** il peut identifier la version de release courante et son fichier de référence
