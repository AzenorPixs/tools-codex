## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: LM unique et retrait effectif
LM SHALL être la seule liste noire de TFL et PLLM. Les valeurs initiales sans
fichier SHALL être mimo-v2.5 et muse-spark-1.2-contributor, toutes deux
retirables. Une liste existante ou vide SHALL rester souveraine. Une migration
explicitement demandée SHALL utiliser ADD atomique sans perte des autres entrées.

#### Scenario: Ancienne exclusion permanente retirée
- **WHEN** LM REMOVE retire muse-spark-1.2-contributor
- **THEN** les six distributions cessent de l'exclure par identifiant
- **AND** aucune liste permanente ne subsiste dans les consommateurs
