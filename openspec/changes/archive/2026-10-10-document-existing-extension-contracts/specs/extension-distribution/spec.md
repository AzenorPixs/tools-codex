## ADDED Requirements

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
sous `skills/` et les commandes maison sous `.codex/commands/`. L'installation
d'un plugin SHALL NOT être présentée comme installant à elle seule les
commandes maison ou les skills autonomes du dépôt.

#### Scenario: Installation d'un plugin seul
- **WHEN** un utilisateur suit la procédure d'installation d'un plugin
- **THEN** la documentation distingue ses ressources embarquées des ressources autonomes
- **AND** elle ne prétend pas que les commandes maison du dépôt sont automatiquement disponibles

### Requirement: Catalogue des commandes cohérent
La commande `/cm` SHALL décrire les commandes maison effectivement présentes
avec leur syntaxe et leur responsabilité. Toute création, suppression ou
renommage autorisé d'une commande SHALL mettre à jour ce catalogue.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** `/cm` est consultée
- **THEN** elle décrit `/cm`, `/pllm` et `/tfl` conformément aux commandes présentes
- **AND** elle ne déclare pas une commande absente

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
