# lm-blacklist Specification

## Purpose
Définir la gestion persistante d’une liste noire commune et son application avant toute sélection ou génération TFL/PLLM, indépendamment des distributions et historiques.

## Requirements

### Requirement: Gestion LM explicite et persistante
LM SHALL fournir /LM et $lm : LIST par défaut sans écriture, ADD et REMOVE.
Les mutations SHALL être atomiques, idempotentes et verrouillées dans
CODEX_HOME/lm/blacklist.json (repli ~/.codex/lm/blacklist.json), avec
schema_version=1 et models canonique. Sans fichier, mimo-v2.5 et
muse-spark-1.2-contributor SHALL être les défauts retirables, sans écriture.
Une liste vide valide SHALL rester vide.

#### Scenario: Première consultation
- **WHEN** LM est consulté et le fichier commun manque
- **THEN** mimo-v2.5 et muse-spark-1.2-contributor sont affichés et aucun fichier utilisateur n'est créé

#### Scenario: Ajout et retrait partagés
- **WHEN** un modèle est ajouté puis retiré par LM depuis deux distributions
- **THEN** les deux distributions utilisent le même fichier et la modification est persistante
- **AND** une répétition ne duplique pas les entrées et ne corrompt pas les données

### Requirement: Identité commune sans recherche approximative
LM SHALL comparer sans distinction de casse l'identifiant après retrait du
préfixe fournisseur et des seuls suffixes :free ou -free. Les identifiants
SHALL être ASCII, bornés à 256 caractères et sans espaces ou contrôles.
Les autres variantes SHALL conserver leur identité distincte.
LM SHALL être la seule liste d'exclusion par identifiant de TFL/PLLM,
sans liste permanente supplémentaire.

#### Scenario: Retrait de l'ancienne exclusion permanente
- **WHEN** LM retire muse-spark-1.2-contributor de la liste commune
- **THEN** ses identifiants fournisseur et variantes gratuites ne sont plus exclus par une liste noire
- **AND** les autres filtres TFL et PLLM restent applicables

#### Scenario: Variantes du modèle initial
- **WHEN** mimo-v2.5, xiaomi/mimo-v2.5:free ou MIMO-V2.5-FREE est rencontré
- **THEN** l'exclusion mimo-v2.5 s'applique
- **AND** mimo-v2.50 et mimo-v2.5-pro ne sont pas exclus par cette seule entrée

### Requirement: Erreur bloquante sans perte de données
Un fichier illisible, un schéma inconnu, des clés dupliquées ou des modèles
invalides SHALL provoquer un diagnostic sûr. LM SHALL NOT remplacer le
fichier invalide ; TFL et PLLM SHALL bloquer avant tout appel fournisseur.
Les consommateurs SHALL lire la liste sans mutation du profil.

#### Scenario: JSON corrompu
- **WHEN** le fichier commun est corrompu avant une invocation
- **THEN** l'invocation échoue explicitement sans réinitialiser le fichier ni appeler un fournisseur

### Requirement: Autonomie des paquets et conservation des données
LM, TFL et PLLM SHALL embarquer le même module de liste noire dans leurs
paquets autonomes et plugins. Un paquet isolé SHALL appliquer la liste sans
installation d'un plugin voisin. TCU SHALL conserver le stockage utilisateur
hors cache et SHALL actualiser LM présent ou installer LM absent selon les
règles TCU, sans créer ni remplacer les exclusions personnalisées. La livraison locale SHALL rester distincte de la
publication et de l'installation dans un profil réel.

#### Scenario: Plugins séparés
- **WHEN** TFL et PLLM sont placés dans deux caches de versions distincts
- **THEN** ils appliquent la même liste CODEX_HOME et ne dépendent pas du chemin du plugin LM

#### Scenario: Mise à jour LM
- **WHEN** TCU actualise une copie LM déjà présente
- **THEN** ses sources sont actualisées et les exclusions personnalisées restent intactes

#### Scenario: Installation LM absente
- **WHEN** TCU installe les sources LM absentes dans un profil ayant déjà des exclusions personnalisées
- **THEN** le plugin et les copies autonomes demandées sont installés sans modifier le stockage de la liste noire

### Requirement: Préfixe fournisseur OpenRouter marqué
LM SHALL accepter un unique `~` initial devant un segment fournisseur valide
suivi de `/`. Le marqueur SHALL disparaître avec le préfixe lors de la
canonicalisation. Les exclusions et validations existantes SHALL rester
applicables ; la limite de 256 caractères SHALL inclure le marqueur.

#### Scenario: Modèle autorisé avec préfixe marqué
- **WHEN** ~vendor/model est comparé à vendor/model ou model
- **THEN** leur identité canonique est identique et idempotente

#### Scenario: Exclusion marquée non contournable
- **WHEN** un identifiant marqué désigne un modèle exclu, avec casse ou suffixes gratuits
- **THEN** les exclusions configurées dans LM restent applicables
- **AND** les noms voisins restent distincts, sans recherche approximative

#### Scenario: Marqueur mal placé ou identifiant invalide
- **WHEN** un identifiant vaut ~model, ~~vendor/model ou vendor/~model, ou viole les limites ASCII existantes
- **THEN** il est rejeté avec un diagnostic sûr et sans mutation de la politique

#### Scenario: Persistance canonique
- **WHEN** LM ajoute ou retire ~vendor/model:free
- **THEN** il utilise la même entrée canonique que model et préserve les autres exclusions

### Requirement: LM unique et retrait effectif
LM SHALL être la seule liste noire de TFL et PLLM. Les valeurs initiales sans
fichier SHALL être mimo-v2.5 et muse-spark-1.2-contributor, toutes deux
retirables. Une liste existante ou vide SHALL rester souveraine. Une migration
explicitement demandée SHALL utiliser ADD atomique sans perte des autres entrées.

#### Scenario: Ancienne exclusion permanente retirée
- **WHEN** LM REMOVE retire muse-spark-1.2-contributor
- **THEN** les six distributions cessent de l'exclure par identifiant
- **AND** aucune liste permanente ne subsiste dans les consommateurs
