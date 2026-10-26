## Purpose

Définir la gestion persistante d’une liste noire commune et son application avant toute sélection ou génération TFL/PLLM, indépendamment des distributions et historiques.

## ADDED Requirements

### Requirement: Gestion LM explicite et persistante
LM SHALL fournir /LM et $lm, LIST par défaut, ADD identifiant et REMOVE
identifiant. LIST SHALL rester sans écriture. Les mutations SHALL être
idempotentes, verrouillées et publiées atomiquement dans
CODEX_HOME/lm/blacklist.json, ou ~/.codex/lm/blacklist.json sans CODEX_HOME.
Le fichier SHALL déclarer schema_version=1 et une liste models canonique.
Sans fichier, les consommateurs SHALL utiliser mimo-v2.5 en mémoire sans
créer de fichier. Une liste vide valide SHALL rester vide.

#### Scenario: Première consultation
- **WHEN** LM est consulté et le fichier commun manque
- **THEN** mimo-v2.5 est affiché et aucun fichier utilisateur n'est créé

#### Scenario: Ajout et retrait partagés
- **WHEN** un modèle est ajouté puis retiré par LM depuis deux distributions
- **THEN** les deux distributions utilisent le même fichier et la modification est persistante
- **AND** une répétition ne duplique pas les entrées et ne corrompt pas les données

### Requirement: Identité commune sans recherche approximative
LM SHALL comparer sans distinction de casse l'identifiant après retrait du
préfixe fournisseur et des seuls suffixes :free ou -free. Les identifiants
SHALL être ASCII, bornés à 256 caractères et sans espaces ou contrôles.
Les autres variantes SHALL conserver leur identité distincte.
Les exclusions permanentes TFL historiques SHALL rester applicables.

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
hors cache et SHALL gérer LM présent selon les règles habituelles sans
installer LM absent. La livraison locale SHALL rester distincte de la
publication et de l'installation dans un profil réel.

#### Scenario: Plugins séparés
- **WHEN** TFL et PLLM sont placés dans deux caches de versions distincts
- **THEN** ils appliquent la même liste CODEX_HOME et ne dépendent pas du chemin du plugin LM

#### Scenario: Mise à jour LM
- **WHEN** TCU actualise une copie LM déjà présente
- **THEN** ses sources sont actualisées et les exclusions personnalisées restent intactes
