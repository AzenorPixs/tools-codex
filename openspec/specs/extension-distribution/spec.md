# extension-distribution Specification

## Purpose

Définir les ressources distribuées, leurs modes d’installation, leur cohérence et les prérequis Python qualifiés de Tools Codex.

## Requirements

### Requirement: Contrat Python déclaré et qualifié
Tools Codex SHALL déclarer `requires-python = ">=3.13,<3.15"` dans
`pyproject.toml`. Le support des branches 3.13 et 3.14 SHALL être étayé par
les tests hors ligne, la compilation et les imports des scripts distribués
sur chacune. La version observée d'un interpréteur seule SHALL NOT constituer
une preuve de qualification.

#### Scenario: Qualification des deux branches
- **WHEN** les validations de compatibilité sont réalisées
- **THEN** leurs résultats et versions exactes sont consignés séparément pour 3.13 et 3.14
- **AND** un échec empêche de déclarer la qualification complète

#### Scenario: Interpréteur hors plage
- **WHEN** les prérequis Python du projet sont consultés
- **THEN** les versions antérieures à 3.13 et à partir de 3.15 sont exclues de la plage déclarée

### Requirement: Portée des métadonnées Python
`pyproject.toml` SHALL décrire les métadonnées et prérequis Python du dépôt,
sans constituer une annonce de publication d'un paquet Python. La
qualification locale SHALL rester distincte des installations réelles et
des accès fournisseurs, qui exigent leurs preuves propres.

#### Scenario: Consultation des métadonnées
- **WHEN** les métadonnées Python sont documentées
- **THEN** leur rôle et la portée de qualification sont explicites sans annoncer une publication Python

### Requirement: Catalogue et ressources explicites
Tools Codex SHALL décrire les plugins publiés dans
`.agents/plugins/marketplace.json`, avec des chemins locaux relatifs à la
racine commençant par `./`. Les plugins SHALL utiliser leur manifeste sous
`plugins/<nom>/.codex-plugin/plugin.json` et déclarer leurs skills embarqués.
L'alignement des releases reste défini par `release-versioning`.

#### Scenario: Résolution des plugins du catalogue
- **WHEN** les entrées publiées du catalogue sont examinées
- **THEN** chacune désigne un répertoire de plugin et son manifeste présents
- **AND** les chemins et skills déclarés correspondent à l'organisation documentée

### Requirement: Modes de distribution distincts
Tools Codex SHALL distinguer les plugins sous `plugins/`, les skills autonomes
sous `skills/` et les commandes sources conservées sous `.codex/commands/`.
L'installation d'un plugin SHALL NOT être présentée comme installant à elle
seule les commandes sources ou les skills autonomes du dépôt. La documentation
SHALL expliquer la découverte locale de cm et son installation autonome hors
du projet, sans prétendre qu'un fichier de commande enregistre une slash native.

#### Scenario: Installation d'un plugin seul
- **WHEN** un utilisateur suit la procédure d'installation d'un plugin
- **THEN** la documentation distingue ses ressources embarquées des ressources autonomes
- **AND** elle ne prétend pas que les commandes sources du dépôt sont automatiquement disponibles

#### Scenario: Installation autonome du catalogue
- **WHEN** un utilisateur souhaite utiliser cm hors de Tools Codex
- **THEN** la documentation décrit l'installation de `skills/cm/` dans un emplacement de skills reconnu par Codex
- **AND** cette installation est distincte de celle des plugins PLLM et TFL

### Requirement: Catalogue des commandes cohérent
Le skill `cm` dans `skills/cm/SKILL.md` SHALL remplacer la commande source
`.codex/commands/cm.md`, qui SHALL être supprimée. `$cm` SHALL afficher un
tableau français concis : `Commande`, `Utilisation`, `Description`. Il SHALL
conserver les syntaxes et responsabilités de `$cm`, `$pllm` et `$tfl`. Il
SHALL NOT lancer leurs générateurs ni inventer de commande. Toute évolution
autorisée des entrées publiées SHALL actualiser ce catalogue.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** `$cm` est invoqué
- **THEN** le tableau décrit `$cm`, `$pllm` et `$tfl` conformément aux sources présentes
- **AND** les utilisations sont `$cm`, `$pllm [active|MODE] [--tfl-catalog CHEMIN]` et `$tfl [auto|mode1|mode2]`
- **AND** il conserve leurs responsabilités sans lancer une évaluation ou un rapport
- **AND** il ne présente plus `/cm` comme une invocation disponible

### Requirement: Préservation des copies et qualification de distribution
Les ressources communes volontairement distribuées sous forme autonome et
embarquée SHALL rester cohérentes. La qualification d'une distribution SHALL
distinguer l'examen de ses sources d'un test réel d'installation dans une
nouvelle session Codex et SHALL préserver les secrets et données personnelles
hors des artefacts publiés.

#### Scenario: Mise à jour d'instructions communes
- **WHEN** les instructions communes PLLM ou TFL sont modifiées
- **THEN** leurs copies autonomes et embarquées sont mises à jour et comparées
- **AND** cette comparaison n'est pas présentée comme un test d'installation réussi

### Requirement: Découverte locale du skill cm
Le projet SHALL exposer `.agents/skills/cm` comme lien symbolique relatif vers
`../../skills/cm`. Le lien SHALL résoudre le même `SKILL.md` canonique sans
copie divergente ni installation globale. La qualification locale SHALL
distinguer le contrôle du format et du lien d'une invocation effective dans
une nouvelle session Codex.

#### Scenario: Résolution dans le projet
- **WHEN** le répertoire de découverte des skills du projet est examiné
- **THEN** `.agents/skills/cm/SKILL.md` résout `skills/cm/SKILL.md` dans ce projet
- **AND** aucune seconde copie du catalogue n'est nécessaire

#### Scenario: Limite de qualification
- **WHEN** seuls le format et le lien ont été vérifiés
- **THEN** les preuves ne déclarent pas qu'une nouvelle session Codex a exécuté `$cm`
