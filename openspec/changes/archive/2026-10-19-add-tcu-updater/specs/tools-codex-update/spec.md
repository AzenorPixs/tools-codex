## Purpose

Définir la mise à jour contrôlée des briques Tools Codex déjà installées depuis
la marketplace officielle et GitHub, avec provenance, sauvegardes, protection
des données locales et bilan des versions réellement observées.

## ADDED Requirements

### Requirement: Invocation explicite et contrôle préalable
TCU SHALL fournir un skill autonome et embarqué invocable avec `$tcu` et
reconnaissant `/TCU`, plus une commande source de même rôle. Le script SHALL
vérifier sans mutation par défaut ; `--apply` SHALL appliquer et `--check`
SHALL rester sans écriture. Le skill SHALL lancer l'application pour une
demande explicite de mise à jour et SHALL NOT muter pour une explication.

#### Scenario: Contrôle seul
- **WHEN** TCU est lancé avec --check
- **THEN** les sources distantes et versions peuvent être lues sans rafraîchir la marketplace ni écrire dans le profil
- **AND** les briques absentes sont signalées sans installation

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
TCU SHALL limiter le rafraîchissement CLI à la marketplace officielle
tools-codex et vérifier les versions installées avant et après. Il SHALL
préserver leur activation et leurs données générées par sauvegarde et
restitution. Il SHALL NOT installer une brique absente ni écrire directement
le code dans le cache géré par Codex.

#### Scenario: Rafraîchissement partiel
- **WHEN** la marketplace change mais une vérification ultérieure échoue
- **THEN** le bilan décrit les versions réellement observées et l'échec
- **AND** il ne déclare pas une atomicité globale ni un succès complet

### Requirement: Provenance et conflits des copies autonomes
TCU SHALL actualiser uniquement les skills et commandes déjà présents dans
les racines identifiées. Il SHALL suivre leurs empreintes dans un reçu de
provenance. Une copie différente sans reçu SHALL être ambiguë sauf adoption
explicite avec sauvegarde. Une modification d'un fichier suivi SHALL rester
en conflit même avec adoption. Les liens et checkouts de développement
SHALL être préservés sans modification.

#### Scenario: Modification locale
- **WHEN** un fichier suivi diffère de son empreinte ou la cible est un lien ou checkout
- **THEN** TCU signale le conflit et conserve les fichiers locaux

#### Scenario: Adoption historique
- **WHEN** une copie ancienne sans reçu est explicitement adoptée
- **THEN** TCU sauvegarde les sources remplacées puis établit le reçu de provenance
- **AND** les données et fichiers hors sources gérées restent préservés

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
