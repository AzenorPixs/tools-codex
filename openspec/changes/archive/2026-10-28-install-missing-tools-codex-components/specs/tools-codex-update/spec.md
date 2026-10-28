## MODIFIED Requirements

### Requirement: Mise à jour des plugins installés
TCU SHALL limiter le rafraîchissement à la marketplace officielle tools-codex
et vérifier les versions avant et après. Il SHALL préserver l'activation et
les données générées. Il SHALL installer tous les plugins absents du catalogue validé via le CLI
Codex et vérifier leur version réelle et leur activation. Il SHALL NOT écrire
le code dans le cache géré par Codex.

#### Scenario: Installation ciblée
- **WHEN** une application trouve des plugins absents dans le catalogue officiel validé
- **THEN** le CLI installe chacun de ces plugins et ses skills embarqués, puis TCU vérifie les versions réelles
- **AND** l'activation des plugins déjà présents reste inchangée

#### Scenario: Rafraîchissement partiel
- **WHEN** une opération CLI a un effet mais une vérification échoue
- **THEN** le bilan décrit cet effet et l'échec sans annoncer une annulation globale

### Requirement: Provenance et conflits des copies autonomes
TCU SHALL actualiser les copies selon leurs reçus et empreintes et installer
les skills et commandes absents dans toutes les racines configurées, même
absentes ou explicites, avec reçu de provenance. Check SHALL annoncer sans
écrire. Une copie différente sans reçu SHALL exiger --adopt ; un fichier suivi
modifié SHALL rester en conflit, même avec adoption. Les liens, checkouts,
fichiers et données non concernés SHALL rester préservés.

#### Scenario: Modification locale
- **WHEN** un fichier suivi est modifié ou une cible est liée ou dans un checkout
- **THEN** la cible reste inchangée et son conflit est rapporté

#### Scenario: Adoption historique
- **WHEN** une copie sans reçu est explicitement adoptée
- **THEN** les remplacements sont sauvegardés et la provenance établie sans modifier les autres fichiers

#### Scenario: Profil vide et racines multiples
- **WHEN** TCU applique un instantané valide dans des racines sans copie autonome ni commande
- **THEN** tous les skills et commandes sources sont installés dans chacune des racines configurées avec leurs reçus
- **AND** une seconde application constate les copies courantes sans réinstallation ni doublon

### Requirement: Bilan et qualification véridiques
TCU SHALL présenter pour chaque brique l'état, la version avant/après
lorsqu'elle est vérifiable et la cause d'un blocage. Le bilan SHALL distinguer
installation prévue, installation réalisée et mise à jour, avec version cible
séparée de la version appliquée. Un conflit ou échec
SHALL produire un code non nul. Les tests SHALL isoler réseau, CLI et
répertoires utilisateur. Une qualification locale SHALL NOT être présentée
comme une publication ou une mise à jour effective du profil réel.

#### Scenario: Fin d'exécution
- **WHEN** les opérations de mise à jour sont terminées
- **THEN** le bilan distingue installation, mise à jour, état courant, installation prévue en contrôle seul, conflit et échec
- **AND** une nouvelle session est indiquée pour charger les skills actualisés

### Requirement: Wrapper prompt déployé avec provenance
Le wrapper SHALL provenir de .codex/commands/PROMPT.md de l'instantané validé.
Il SHALL être créé sous PROMPT.md dans chaque racine sans graphie existante :
CODEX_HOME/prompts et CODEX_HOME/commands par défaut, ou --commands-dir.
Son reçu dédié SHALL NOT écraser les autres reçus. Il SHALL déléguer au skill
sans copier ni modifier le référentiel DEVOPS.md et conserver les noms
historiques et leurs gardes.

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

### Requirement: Bootstrap du planning sans génération
Après vérification des sources installées, TCU --apply SHALL installer ou
actualiser le planning avec son module local. Check SHALL seulement décrire
l'état et l'opération prévue. TCU SHALL NOT exécuter TFL, PLLM ou du code
téléchargé pour ce bootstrap. L'installation des paquets absents SHALL relever
du moteur TCU avant le bootstrap ; le module d'ordonnancement SHALL NOT
installer lui-même ces paquets.

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
locales. Si aucune graphie n'existe, il SHALL installer la commande sous son
nom canonique dans chaque racine configurée. Il SHALL NOT créer une seconde
graphie ni forcer une adoption.

#### Scenario: Mise à jour d'une ancienne commande
- **WHEN** cm.md, pllm.md ou tfl.md est une copie suivie valide et la source distante porte le nom en majuscules
- **THEN** le fichier existant reçoit la source correspondante et conserve son nom et sa provenance
- **AND** les commandes absentes sont installées sous leur nom canonique et les fichiers non concernés restent inchangés
