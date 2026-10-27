## MODIFIED Requirements

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

## ADDED Requirements

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
Le wrapper SHALL provenir de .codex/commands/prompt.md de l'instantané validé.
La cible par défaut SHALL être CODEX_HOME/prompts/prompt.md, remplaçable par
un --commands-dir explicite. Son reçu SHALL être propre au composant et ne
pas écraser les reçus d'autres commandes. Le wrapper SHALL déléguer au skill,
sans copier ni modifier le référentiel métier désigné dans DEVOPS.md.

#### Scenario: Dossier avec anciennes commandes liées
- **WHEN** la racine régulière contient des liens pour d'autres commandes
- **THEN** le wrapper prompt peut être installé sans suivre ni modifier ces liens
- **AND** un lien sur la cible prompt elle-même reste un conflit

### Requirement: Application indépendante et bilan partiel
Un conflit local SHALL préserver sa cible et SHALL NOT empêcher les opérations
indépendantes de marketplace, du composant prompt ou des plans locaux valides.
Une erreur de source, sauvegarde ou vérification CLI SHALL rester explicite.
Le bilan SHALL conserver les effets réels et retourner un code non nul si un
conflit ou échec subsiste, même si certains composants ont été mis à jour.

#### Scenario: Succès indépendant
- **WHEN** une ancienne copie est en conflit et le composant prompt est valide
- **THEN** prompt peut être installé ou actualisé, la copie reste intacte et le bilan est partiel

