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

### Requirement: Catalogue des commandes cohérent
Le skill `cm` SHALL afficher un tableau français concis avec Commande,
Utilisation et Description. Il SHALL présenter `$cm`, `$pllm`, `$tfl` et
`$tcu` avec leurs syntaxes documentées, dont le déclencheur `/TCU`. Il SHALL
NOT exécuter les commandes listées ni inventer de slash native. Toute évolution
autorisée des entrées SHALL actualiser les copies autonome et embarquée.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm est invoqué
- **THEN** le tableau contient `$cm`, `$pllm [active|MODE] [--tfl-catalog CHEMIN]`, `$tfl [auto|mode1|mode2]` et `$tcu [check]`
- **AND** la description TCU indique le déclencheur /TCU sans promettre une slash native
- **AND** aucune mise à jour ou évaluation n'est déclenchée

### Requirement: Préservation des copies et qualification de distribution
Les copies autonomes et embarquées de CM, PLLM, TFL et TCU SHALL rester
cohérentes. Les skills et scripts TCU, ainsi que le skill CM, SHALL être
identiques dans les deux distributions. La qualification SHALL distinguer
les contrôles locaux d'une installation réelle dans une nouvelle session.
Les secrets et données personnelles SHALL rester hors des artefacts publiés.

#### Scenario: Mise à jour d'instructions communes
- **WHEN** une ressource commune distribuée est modifiée
- **THEN** les deux copies sont actualisées et comparées
- **AND** cette comparaison n'est pas présentée comme une installation réussie

#### Scenario: Vérification du paquet CM isolé
- **WHEN** le seul répertoire du plugin CM est copié hors du dépôt
- **THEN** son manifeste et son skill sont résolus sans source externe

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

### Requirement: Distribution du plugin TCU
La marketplace SHALL référencer `./plugins/tcu` avec un manifeste de release
commune et `skills: ./skills/`. Elle SHALL conserver les plugins CM/PLLM/TFL.
Le projet SHALL fournir `skills/tcu/`, sa copie embarquée, le lien relatif
`.agents/skills/tcu` et `.codex/commands/TCU.md`. Les quatre manifestes, VERSION,
README et pyproject.toml SHALL déclarer la même release commune.

#### Scenario: Résolution TCU
- **WHEN** le catalogue et le paquet TCU sont vérifiés
- **THEN** les quatre plugins, les sources et le script embarqué sont présents et leurs versions alignées
- **AND** le paquet TCU copié isolément résout son script sans dépendre du dépôt
