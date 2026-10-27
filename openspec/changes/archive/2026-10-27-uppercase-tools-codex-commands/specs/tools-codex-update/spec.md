## MODIFIED Requirements

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

## ADDED Requirements

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
