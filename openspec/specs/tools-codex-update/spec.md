# tools-codex-update Specification

## Purpose
Définir la gestion contrôlée des briques Tools Codex depuis la marketplace
officielle et GitHub, avec installation ciblée du composant prompt, provenance,
sauvegardes, protection des données et bilan des versions réellement observées.

## Requirements

### Requirement: Invocation explicite et contrôle préalable
TCU SHALL fournir un skill autonome et embarqué invocable avec `$tcu` et
reconnaissant `/TCU`, plus une commande source de même rôle. Le script SHALL
vérifier sans mutation par défaut ; `--apply` SHALL appliquer ; `check` et `--check`
SHALL rester sans écriture. La combinaison `check --apply` SHALL être refusée
avant tout appel du moteur. Le skill SHALL lancer l'application pour une
demande explicite de mise à jour et SHALL NOT muter pour une explication.

#### Scenario: Contrôle seul
- **WHEN** TCU est lancé avec check ou --check
- **THEN** les sources distantes et versions peuvent être lues sans rafraîchir la marketplace ni écrire dans le profil
- **AND** les briques absentes sont signalées sans installation

#### Scenario: Modes contradictoires
- **WHEN** check et --apply sont fournis ensemble
- **THEN** le parseur refuse avant tout appel réseau, CLI ou écriture

### Requirement: Source GitHub officielle vérifiée
TCU SHALL résoudre un SHA du dépôt public AzenorPixs/tools-codex et vérifier
l'archive HTTPS avec limites de taille, chemins sûrs et fichiers réguliers.
Il SHALL valider la release commune, les manifestes et les sources Python
avant application. Il SHALL NOT exécuter le code téléchargé, charger des
secrets ni sélectionner les données générées pour remplacement.

#### Scenario: Source invalide
- **WHEN** une requête échoue, une archive est dangereuse ou les versions divergent
- **THEN** TCU retourne un diagnostic sans afficher de contenu sensible et n'applique pas de source autonome

### Requirement: Mise à jour des plugins installés
TCU SHALL limiter le rafraîchissement à la marketplace officielle tools-codex
et vérifier les versions avant et après. Il SHALL préserver l'activation et
les données générées. Il MAY installer le seul plugin prompt absent, lorsque
ce composant est présent dans le catalogue validé. Il SHALL NOT installer les
autres briques absentes ni écrire le code dans le cache géré par Codex.

#### Scenario: Installation ciblée
- **WHEN** une application trouve prompt absent dans un catalogue officiel complet
- **THEN** le CLI installe prompt et son skill embarqué, puis TCU vérifie leur version réelle
- **AND** aucun autre plugin absent n'est installé

#### Scenario: Rafraîchissement partiel
- **WHEN** une opération CLI a un effet mais une vérification échoue
- **THEN** le bilan décrit cet effet et l'échec sans annoncer une annulation globale

### Requirement: Provenance et conflits des copies autonomes
TCU SHALL actualiser les copies autonomes présentes selon leurs reçus et
empreintes. Il MAY créer le seul wrapper prompt absent dans sa racine cible.
Une copie différente sans reçu SHALL exiger une adoption explicite ; un
fichier suivi modifié SHALL rester en conflit avec ou sans adoption. Les
liens, autres fichiers et checkouts de développement SHALL rester préservés.

#### Scenario: Modification locale
- **WHEN** un fichier suivi est modifié ou une cible est liée ou dans un checkout
- **THEN** la cible reste inchangée et son conflit est rapporté

#### Scenario: Adoption historique
- **WHEN** une copie sans reçu est explicitement adoptée
- **THEN** les remplacements sont sauvegardés et la provenance établie sans modifier les autres fichiers

### Requirement: Sauvegardes et repli borné
TCU SHALL préparer les remplacements et sauvegardes avant application,
verrouiller l'application et remplacer atomiquement chaque fichier. Un
échec autonome SHALL restaurer les fichiers déjà remplacés et conserver la
sauvegarde. TCU SHALL conserver les anciens fichiers retirés en amont et
SHALL NOT effacer les données, secrets ou configurations personnelles.

#### Scenario: Erreur pendant un remplacement
- **WHEN** une écriture échoue après un premier remplacement
- **THEN** les sources autonomes antérieures sont restaurées et l'échec reste explicite
- **AND** une mise à jour CLI déjà réussie n'est pas annoncée annulée

### Requirement: Bilan et qualification véridiques
TCU SHALL présenter pour chaque brique l'état, la version avant/après
lorsqu'elle est vérifiable et la cause d'un blocage. Un conflit ou échec
SHALL produire un code non nul. Les tests SHALL isoler réseau, CLI et
répertoires utilisateur. Une qualification locale SHALL NOT être présentée
comme une publication ou une mise à jour effective du profil réel.

#### Scenario: Fin d'exécution
- **WHEN** les opérations de mise à jour sont terminées
- **THEN** le bilan distingue mise à jour, état courant, absence, conflit et échec
- **AND** une nouvelle session est indiquée pour charger les skills actualisés

### Requirement: Ressources du composant prompt
TCU SHALL vérifier la disponibilité de la source du wrapper et du résolveur
avant mutation. Après opération CLI, il SHALL vérifier le manifeste, le skill
et le résolveur réellement installés, avec leur version et leurs sources.
Le bilan SHALL distinguer plugin, skill embarqué et commande, avec versions
observées et cible prévue ; check SHALL NOT créer ou installer une ressource.

#### Scenario: Cache incomplet
- **WHEN** le plugin est déclaré installé mais son skill ou son résolveur ne correspond pas à la source validée
- **THEN** le composant est signalé incomplet et aucun wrapper trompeur n'est installé

### Requirement: Wrapper prompt déployé avec provenance
Le wrapper SHALL provenir de .codex/commands/PROMPT.md de l'instantané validé.
Pour une nouvelle copie, la cible SHALL être CODEX_HOME/prompts/PROMPT.md,
remplaçable par un --commands-dir explicite. Son reçu dédié SHALL NOT écraser
les reçus d'autres commandes. Le wrapper SHALL déléguer au skill sans copier
ni modifier le référentiel de DEVOPS.md. TCU SHALL conserver les copies
historiques et leurs gardes, selon les scénarios ci-dessous.

#### Scenario: Source antérieure
- **WHEN** la source canonique manque et que .codex/commands/prompt.md existe dans l'instantané validé
- **THEN** TCU MAY lire cette source historique sans contourner les gardes de version

#### Scenario: Nouvelle installation
- **WHEN** aucune des deux graphies du wrapper n'existe dans la racine cible
- **THEN** TCU crée uniquement PROMPT.md avec son reçu dédié lors d'un apply autorisé
- **AND** check ne crée aucun fichier

#### Scenario: Copie historique suivie
- **WHEN** prompt.md existe et son reçu correspond à ses empreintes
- **THEN** la source canonique actualise prompt.md avec sauvegarde et provenance
- **AND** aucun PROMPT.md supplémentaire n'est créé, aucun fichier n'est renommé ni supprimé

#### Scenario: Deux graphies ou copie liée
- **WHEN** les deux graphies existent ou une cible est un lien
- **THEN** les deux fichiers réguliers sont vérifiés dans le même plan et le même reçu dédié avec les gardes habituelles
- **AND** un lien ou une modification locale reste un conflit sans écrasement ni adoption forcée

#### Scenario: Dossier avec anciennes commandes liées
- **WHEN** la racine régulière contient des liens pour d'autres commandes
- **THEN** le wrapper PROMPT peut être installé sans suivre ni modifier ces liens
- **AND** un lien sur la cible PROMPT ou prompt elle-même reste un conflit

### Requirement: Application indépendante et bilan partiel
Un conflit local SHALL préserver sa cible et SHALL NOT empêcher les opérations
indépendantes de marketplace, du composant prompt ou des plans locaux valides.
Une erreur de source, sauvegarde ou vérification CLI SHALL rester explicite.
Le bilan SHALL conserver les effets réels et retourner un code non nul si un
conflit ou échec subsiste, même si certains composants ont été mis à jour.

#### Scenario: Succès indépendant
- **WHEN** une ancienne copie est en conflit et le composant prompt est valide
- **THEN** prompt peut être installé ou actualisé, la copie reste intacte et le bilan est partiel

### Requirement: Bootstrap du planning sans génération
Après vérification des sources installées, TCU --apply SHALL installer ou
actualiser le planning avec son module local. Check SHALL seulement décrire
l'état et l'opération prévue. TCU SHALL NOT exécuter TFL, PLLM ou du code
téléchargé pour ce bootstrap, ni installer leurs paquets absents.

#### Scenario: Application avec TFL et PLLM présents
- **WHEN** TCU applique une mise à jour avec les deux composants utilisables
- **THEN** le planning est vérifié ou actualisé et son résultat figure dans le bilan
- **AND** aucune évaluation LLM n'est déclenchée par TCU

#### Scenario: Contrôle ou composants manquants
- **WHEN** TCU vérifie seulement ou qu'un composant nécessaire manque
- **THEN** aucune planification n'est activée implicitement et l'état explique le résultat

### Requirement: Compatibilité des noms historiques des autres commandes
Pour une source de commande canonique en majuscules, TCU SHALL sélectionner
les copies déjà installées sous le nom canonique ou son ancien nom en
minuscules. Il SHALL conserver leurs noms et reçus, sauvegarder les
remplacements et préserver les liens, fichiers inconnus et modifications
locales. Il SHALL NOT créer une autre commande absente ni forcer une adoption.

#### Scenario: Mise à jour d'une ancienne commande
- **WHEN** cm.md, pllm.md ou tfl.md est une copie suivie valide et la source distante porte le nom en majuscules
- **THEN** le fichier existant reçoit la source correspondante et conserve son nom et sa provenance
- **AND** les commandes absentes et fichiers non concernés restent inchangés
