## MODIFIED Requirements

### Requirement: Modes de distribution distincts
Tools Codex SHALL distinguer les plugins sous `plugins/`, les skills autonomes
sous `skills/` et les commandes sources sous `.codex/commands/`. L'installation
d'un plugin SHALL NOT être présentée comme installant les copies autonomes ou
les commandes sources. La documentation SHALL expliquer les deux distributions
CM, la découverte locale et l'installation autonome hors du projet, sans
prétendre qu'un fichier de commande enregistre une slash native.

#### Scenario: Installation d'un plugin seul
- **WHEN** un utilisateur suit la procédure d'installation d'un plugin
- **THEN** la documentation distingue son skill embarqué des copies autonomes
- **AND** elle ne prétend pas que les commandes sources sont automatiquement disponibles

#### Scenario: Installation autonome du catalogue
- **WHEN** un utilisateur souhaite utiliser CM hors de Tools Codex
- **THEN** il peut choisir le plugin CM ou l'installation de `skills/cm/` dans un emplacement reconnu
- **AND** l'installation de PLLM ou TFL seule ne fournit pas CM

### Requirement: Préservation des copies et qualification de distribution
Les copies autonomes et embarquées de CM, PLLM et TFL SHALL rester cohérentes.
Le skill CM embarqué SHALL être identique à `skills/cm/SKILL.md`. La
qualification SHALL distinguer le contrôle local des sources et du paquet d'un
test réel d'installation dans une nouvelle session Codex. Les secrets et
données personnelles SHALL rester hors des artefacts publiés.

#### Scenario: Mise à jour d'instructions communes
- **WHEN** les instructions communes CM, PLLM ou TFL sont modifiées
- **THEN** leurs copies autonomes et embarquées sont mises à jour et comparées
- **AND** cette comparaison n'est pas présentée comme une installation réussie

#### Scenario: Vérification du paquet CM isolé
- **WHEN** le seul répertoire du plugin CM est copié hors de son emplacement source
- **THEN** son manifeste et son skill sont résolus dans cette copie sans dépendre de `skills/cm/` externe
- **AND** le comportement et le catalogue restent ceux du skill autonome

## ADDED Requirements

### Requirement: Plugin CM dans la marketplace
La marketplace Tools Codex SHALL référencer `cm` via `./plugins/cm`. Le plugin
SHALL fournir `.codex-plugin/plugin.json` déclarant `name: cm`, la release
commune et `skills: ./skills/`, ainsi que `skills/cm/SKILL.md`. Il SHALL
conserver la distribution autonome et son lien de découverte local. Il SHALL
NOT ajouter de script, serveur MCP, application ou service externe.

#### Scenario: Résolution du catalogue CM
- **WHEN** le catalogue de marketplace est contrôlé
- **THEN** il contient CM, PLLM et TFL avec leurs chemins, manifestes et skills présents
- **AND** les trois manifestes déclarent la même release que VERSION et pyproject.toml

### Requirement: Choix de distribution CM documenté
La documentation SHALL présenter l'installation et la mise à jour du plugin
CM via la marketplace, en conservant l'installation autonome. Elle SHALL
signaler que le chargement des deux distributions peut produire deux entrées
CM. La livraison SHALL NOT supprimer ni désactiver automatiquement une copie
autonome ou un plugin installé.

#### Scenario: Deux distributions disponibles
- **WHEN** un utilisateur prépare l'installation du catalogue CM
- **THEN** il peut choisir la distribution adaptée et identifier le risque de double entrée
- **AND** les contrôles locaux ne sont pas annoncés comme une publication ou une installation réelle
