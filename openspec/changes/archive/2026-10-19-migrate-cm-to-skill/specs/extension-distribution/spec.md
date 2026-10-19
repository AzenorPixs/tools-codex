## MODIFIED Requirements

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

## ADDED Requirements

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
