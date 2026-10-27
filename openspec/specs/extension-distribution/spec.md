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
Le skill CM SHALL afficher un tableau français avec Commande, Utilisation et
Description pour CM, PLLM, TFL, TCU, LM et PROMPT. Les deux copies SHALL
conserver les invocations $…, les arguments documentés et les déclencheurs
canoniques en majuscules, avec alias en minuscules. La consultation SHALL NOT
exécuter les actions listées ni inventer une slash native. Toute évolution
autorisée SHALL actualiser les deux catalogues.

#### Scenario: Consultation du catalogue des commandes
- **WHEN** $cm, /CM ou son alias /cm est invoqué
- **THEN** le tableau décrit les six invocations avec les libellés en majuscules
- **AND** aucune mise à jour, évaluation ou exécution de prompt n'est déclenchée

#### Scenario: Wrapper CM
- **WHEN** .codex/commands/CM.md est utilisé
- **THEN** il délègue au skill CM et conserve une seule entrée PROMPT dans chaque catalogue
- **AND** il ne lance pas le prompt et ne promet pas une slash native automatiquement enregistrée

### Requirement: Présentation native des commandes
CM SHALL référencer le SKILL.md réel de chaque skill disponible, avec le
libellé CM, PLLM, TFL, TCU, LM ou PROMPT dans Commande. Les syntaxes $… SHALL
rester dans Utilisation. Sans référence, CM SHALL afficher le nom seul, sans
URI ou icône inventée. Les six skills SHALL déclarer leur display_name en
majuscules dans agents/openai.yaml avec des copies identiques dans les deux
distributions.

#### Scenario: Présentation uniforme
- **WHEN** un des six skills est disponible dans la session lors de la consultation
- **THEN** sa première cellule porte son libellé en majuscules et référence son SKILL.md réel
- **AND** sa syntaxe $… reste dans Utilisation et aucune action n'est exécutée

#### Scenario: Présentation uniforme de TCU
- **WHEN** le skill TCU est disponible dans la session lors de la consultation
- **THEN** sa première cellule porte le libellé TCU et référence son SKILL.md réel, selon la même règle que les autres entrées
- **AND** $tcu [check] reste dans Utilisation et aucune mise à jour n'est exécutée

### Requirement: Préservation des copies et qualification de distribution
Les copies autonomes et embarquées de CM, PLLM, TFL, TCU, LM et prompt SHALL rester
cohérentes. Les skills et scripts TCU et prompt, ainsi que le skill CM, SHALL
être identiques dans les deux distributions. La qualification SHALL distinguer
contrôles locaux et exécution réelle d'un prompt ou installation dans une
nouvelle session. Les secrets et données personnelles SHALL rester exclus.

#### Scenario: Mise à jour d'instructions communes
- **WHEN** une ressource commune distribuée est modifiée
- **THEN** les deux copies sont actualisées et comparées sans prétendre à une installation réelle

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
La marketplace SHALL référencer ./plugins/tcu avec un manifeste de release
commune et skills: ./skills/. Elle SHALL conserver CM, PLLM, TFL, LM et prompt.
Le projet SHALL fournir skills/tcu/, sa copie embarquée, le lien relatif
.agents/skills/tcu et .codex/commands/TCU.md. Les six manifestes, VERSION,
README et pyproject.toml SHALL déclarer la même release commune.

#### Scenario: Résolution TCU
- **WHEN** le catalogue et le paquet TCU sont vérifiés
- **THEN** les six plugins, les sources et le script embarqué sont présents et leurs versions alignées
- **AND** le paquet TCU copié isolément résout son script sans dépendre du dépôt

### Requirement: Distribution du plugin prompt
La marketplace SHALL référencer ./plugins/prompt, avec un manifeste de release
commune et skills: ./skills/. Le projet SHALL fournir skills/prompt/, sa copie
embarquée, .codex/commands/PROMPT.md et le lien relatif .agents/skills/prompt.
Le manifeste et le skill SHALL afficher PROMPT. Le paquet SHALL contenir son
résolveur mais SHALL NOT embarquer les prompts du référentiel externe. Les
six plugins SHALL partager la release du projet.

#### Scenario: Paquet autonome
- **WHEN** le paquet prompt est copié isolément
- **THEN** son script fonctionne avec un projet explicite contenant DEVOPS.md
- **AND** aucun fichier du dépôt Tools Codex n'est nécessaire hors du paquet

### Requirement: Distribution LM dans la marketplace et découverte locale
La marketplace SHALL référencer ./plugins/lm, manifeste de release commune,
skills: ./skills/ et skill lm embarqué. Le projet SHALL fournir skills/lm/,
sa copie embarquée identique, .codex/commands/LM.md et le lien relatif
.agents/skills/lm vers ../../skills/lm. agents/openai.yaml SHALL afficher LM.
La commande source SHALL déléguer au skill sans promettre une slash native.
Les versions VERSION, pyproject.toml, README et six plugins SHALL être 0.7.6
pour cette livraison.

#### Scenario: Catalogue CM et paquet LM
- **WHEN** le catalogue CM et le paquet LM isolé sont contrôlés
- **THEN** LM et ses syntaxes sont présents dans les deux CM et le paquet résout ses scripts
- **AND** les six plugins partagent la release commune sans installation globale

### Requirement: Hooks et ordonnanceur embarqués
Les six plugins SHALL déclarer un hook SessionStart vers leur module local
d'ordonnancement. Les six skills autonomes et leurs plugins SHALL embarquer
un module identique, utilisable isolément. L'installation autonome SHALL
documenter le bootstrap ; la confiance native Codex SHALL rester requise.

#### Scenario: Plugin isolé et confiance
- **WHEN** un plugin est installé dans son propre cache puis son hook est approuvé
- **THEN** il peut enregistrer le même planning utilisateur sans dépendre du checkout
- **AND** l'absence de TFL ou PLLM reste signalée sans installation implicite

### Requirement: Déclarations canoniques des six commandes en majuscules
Tools Codex SHALL fournir exactement les six commandes sources CM.md, PLLM.md,
TFL.md, TCU.md, LM.md et PROMPT.md sous .codex/commands/. Les commandes SHALL
documenter /CM, /PLLM, /TFL, /TCU, /LM et /PROMPT comme déclencheurs canoniques.
Les identifiants techniques, chemins de skills et invocations $… SHALL rester
inchangés. Les déclarations SHALL NOT promettre une slash native automatiquement
enregistrée.

#### Scenario: Qualification du catalogue distribué
- **WHEN** les commandes, skills, métadonnées et manifestes de la release sont contrôlés
- **THEN** les six noms de commande et d'affichage sont en majuscules dans les deux distributions
- **AND** les identifiants techniques et les arguments restent inchangés

#### Scenario: Ancienne invocation
- **WHEN** une ancienne invocation /cm, /pllm, /tfl ou /prompt est reçue par le skill
- **THEN** elle conserve le comportement documenté de la commande canonique correspondante
- **AND** la consultation de CM ne lance aucune action
