## ADDED Requirements

### Requirement: Récupération limitée de mémoire sans version
PLLM SHALL récupérer sans écriture une mémoire sans schema_version seulement si elle contient uniquement policies vide ou un mode7 DeepSeek Medium identifiable au protocole 8. Ses succès et configurations SHALL être cohérents. Un format ambigu ou invalide SHALL être refusé et préservé avant tout appel fournisseur.

#### Scenario: Mémoire mode7 identifiable
- **WHEN** seul mode7 contient un succès DeepSeek Medium cohérent au protocole 8 sans version
- **THEN** le chargement ajoute schema_version=3 en mémoire et conserve les octets du fichier
- **AND** le palier reste limité à une configuration identique et ne valide aucune mesure actuelle

#### Scenario: Mémoire vide sans version
- **WHEN** la mémoire sans version contient seulement policies vide
- **THEN** le chargement initialise le schéma 3 sans inventer de succès

#### Scenario: Mémoire ambiguë ou corrompue
- **WHEN** la version manque avec un ancien mode ambigu, une identité incohérente ou un succès malformé
- **THEN** le fichier est préservé et aucun appel fournisseur ni publication n'a lieu

### Requirement: Écriture rechargeable de la mémoire
PLLM SHALL valider et normaliser la mémoire avant d'enregistrer un succès. Toute écriture réussie SHALL publier atomiquement un schéma 3 rechargeable avec les succès antérieurs conservés. Les migrations explicites 1/2 SHALL rester applicables ; une mémoire invalide SHALL NOT être écrasée.

#### Scenario: Succès après récupération
- **WHEN** un nouveau succès est enregistré avec une mémoire récupérable sans version
- **THEN** la mémoire publiée porte schema_version=3 et sa relecture conserve les configurations et paliers

#### Scenario: Argument invalide de l'écrivain
- **WHEN** une mémoire ambiguë ou de schéma inconnu est passée à l'enregistrement
- **THEN** l'enregistrement échoue avant mutation et préserve le fichier existant
