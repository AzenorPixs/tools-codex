# codex-usage-reporting Specification

## Purpose

Définir la lecture des quotas Codex, leur restitution et les limites d’interprétation de l’historique du compte partagé.

## Requirements

### Requirement: Quotas actuels depuis la source Codex
CGPT SHALL appeler `mcp__codex_app__get_usage_limits` à chaque invocation et
préférer `rateLimitsByLimitId` lorsqu'il est disponible, avec repli vers
`rateLimits`. Les fenêtres SHALL être identifiées par leur durée et leur
compteur, sans déduire leur durée du nom primary ou secondary. Une donnée
absente SHALL rester indisponible et ne pas être remplacée par zéro ou une
ancienne observation. La commande SHALL rester en lecture seule sur le compte.

#### Scenario: Source de quotas indisponible
- **WHEN** l'outil de quotas échoue ou ne fournit pas une fenêtre
- **THEN** CGPT indique l'indisponibilité et sa cause sans présenter un ancien quota comme actuel
- **AND** aucun achat, crédit de réinitialisation ou réglage de compte n'est modifié

### Requirement: Restitution des utilisations et réinitialisations
CGPT SHALL distinguer le pourcentage utilisé du pourcentage restant, calculé
par `max(0, min(100, 100 - utilisé))`. Les couleurs SHALL porter sur le restant :
vert à partir de 75 %, jaune de 50 % inclus à 75 % exclu, orange de 25 % inclus
à 50 % exclu et rouge sous 25 %. Les dates de consultation et de
réinitialisation SHALL être affichées en Europe/Paris. Une valeur manquante
SHALL rester sans couleur inventée.

#### Scenario: Quota partiellement utilisé
- **WHEN** une fenêtre actuelle fournit 40 % utilisés
- **THEN** CGPT restitue 40 % utilisés et 60 % restants avec la couleur jaune
- **AND** les dates correspondent aux horodatages fournis, convertis en Europe/Paris

### Requirement: Vue hebdomadaire précise
La vue `/cgpt 7u` SHALL restituer uniquement le pourcentage utilisé du compteur
`codex` pour la fenêtre de 10 080 minutes, ou `Non disponible` si ce quota
manque. Elle SHALL effectuer une nouvelle consultation, sans substituer un
compteur Spark, le restant ou une autre durée.

#### Scenario: Plusieurs compteurs présents
- **WHEN** les quotas contiennent plusieurs compteurs et durées
- **THEN** la vue `7u` sélectionne uniquement `codex` et 10 080 minutes
- **AND** sa sortie ne contient ni tableau ni commentaire supplémentaire sauf instruction supérieure

### Requirement: Historique local et publication
CGPT SHALL conserver les observations dans `quota-history.jsonl` et publier
`cgpt-current.json` et `cgpt-current.md`, avec remplacement atomique de chaque
fichier courant. La restitution normale SHALL présenter les quotas et les
statistiques réellement disponibles.

#### Scenario: Nouvelle observation publiée
- **WHEN** une observation est enregistrée
- **THEN** les fichiers courants représentent cette observation et l'historique la conserve
- **AND** la restitution normale distingue les quotas des statistiques disponibles

### Requirement: Portée des statistiques du compte
Une variation SHALL comparer des
observations du même compteur et de la même fenêtre de réinitialisation, sans
addition au travers d'une réinitialisation ni attribution exclusive à la
conversation. Aucune durée active ou consommation de tokens SHALL être
inventée depuis ces observations de compte partagé.

#### Scenario: Réinitialisation entre deux observations
- **WHEN** deux observations n'appartiennent pas à la même fenêtre de réinitialisation
- **THEN** elles ne sont pas utilisées pour calculer une variation comparable de quota
- **AND** leur différence n'est pas présentée comme la consommation de cette session
