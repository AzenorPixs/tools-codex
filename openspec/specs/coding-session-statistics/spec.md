# coding-session-statistics Specification

## Purpose

Définir les rapports de session et d’archivage fondés sur les preuves, les métriques disponibles et les limites de collecte.

## Requirements

### Requirement: Rapport fondé sur les preuves de session
Le rapport de statistiques SHALL identifier la session concernée et utiliser
ses preuves persistantes autorisées, sans secrets ni lecture de sources
exclues. Il SHALL distinguer les opérations approuvées et exécutées, les
refus de permission et les erreurs techniques. Les effectifs, pourcentages et
totaux croisés SHALL être cohérents ; toute mesure absente SHALL être indiquée
par `N/A` avec sa cause plutôt qu'estimée sans preuve.

#### Scenario: Mesure absente de l'historique
- **WHEN** l'historique ne fournit pas une métrique nécessaire au rapport
- **THEN** le rapport affiche `N/A` et la cause de cette absence
- **AND** il ne reconstitue pas artificiellement une mesure ou une opération exécutée

### Requirement: Structure et domaines du rapport
Le rapport SHALL comporter exactement six sections de niveau 2 : statistiques
générales et décisions, types de messages et d'outils, fichiers modifiés,
commandes, accès web et synthèse globale. Les tableaux d'agents de codage et
d'orchestrateurs SHALL les précéder avec des titres de niveau 3.

#### Scenario: Structure du rapport produit
- **WHEN** le rapport est restitué
- **THEN** les deux tableaux d'agents précèdent exactement les six sections de niveau 2

### Requirement: Libellés et statuts sans ambiguïté
Les chemins des fichiers SHALL être complets ; commandes et URL affichées SHALL être
limitées à 100 caractères chacune, troncature comprise. Une URL refusée SHALL
être distinguée d'un accès effectivement réalisé.

#### Scenario: Restitution d'une commande refusée
- **WHEN** une commande a été refusée sans exécution
- **THEN** le rapport la classe parmi les refus et respecte la limite de libellé
- **AND** elle ne figure pas comme une commande exécutée avec succès

### Requirement: Métriques issues de télémétries identifiables
Les versions, TTMT, débits et temps de service des agents SHALL provenir de
télémétries identifiables. Les sondes manquées SHALL rester signalées comme
manquées, sans reconstruction rétroactive.

#### Scenario: Collecte de métriques commencée trop tard
- **WHEN** des sondes n'ont pas été collectées à temps
- **THEN** leurs données restent indisponibles et les relèves manquées sont signalées

### Requirement: Sondes bornées aux agents de codage
Lorsque les sondes peuvent être préparées, elles SHALL mesurer les seuls
agents de codage au début, toutes les 30 minutes et à la fin, dans des
sessions dédiées sans outils, accès aux fichiers ni accès réseau.

#### Scenario: Préparation des sondes
- **WHEN** la collecte est préparée avant les travaux
- **THEN** la cadence et les sessions dédiées respectent ces limites sans sonder l'orchestrateur

### Requirement: Durée sans reconstruction rétroactive
La durée globale SHALL
résulter des bornes calendaires vérifiables et ne pas additionner les durées
d'agents simultanés ni confondre les attentes avec leur temps de génération.

#### Scenario: Collecte commencée après le début
- **WHEN** les sondes ou une borne de session n'ont pas été collectées à temps
- **THEN** les données absentes sont signalées et ne sont pas recréées rétroactivement
- **AND** une durée finale n'est pas annoncée si la borne de fin manque encore

### Requirement: Quota partagé et comparaison bornée
Le suivi d'une session de codage SHALL conserver les relevés réels `/cgpt 7u`
avant et après les travaux, avec horodatages et réinitialisations. La
différence SHALL être exprimée en points de pourcentage utilisé, uniquement
pour un même compte et une même fenêtre comparable. Elle SHALL être présentée
comme une variation du compte partagé, sans attribution exclusive non prouvée.

#### Scenario: Relevés comparables
- **WHEN** les relevés réels avant et après concernent le même compte et la même fenêtre
- **THEN** leur différence est calculée en points de pourcentage utilisé avec mention de sa portée partagée

### Requirement: Comparaisons de quota non disponibles
Une réinitialisation, une différence négative ou une borne absente SHALL
rendre la différence de quota indisponible avec sa cause. Les pourcentages
SHALL NOT être convertis en tokens ou en euros.

#### Scenario: Quota réinitialisé pendant la session
- **WHEN** les réinitialisations des relevés avant et après diffèrent
- **THEN** le rapport affiche `N/A` pour la différence et explique la réinitialisation
- **AND** il ne convertit pas les pourcentages en tokens ou en euros

### Requirement: Rapport après archivage autorisé
Après un archivage OpenSpec autorisé et réussi, un rapport distinct SHALL être
produit dans le dossier de cette archive sous `STATISTIQUES.md`, selon les
autorisations du projet. Il SHALL être vérifié en UTF-8/LF avec ses six
sections et ses totaux. Un échec du rapport SHALL conduire à reprendre le
seul rapport, sans réarchiver le change ni déclarer la clôture complète.

#### Scenario: Échec du rapport après archivage
- **WHEN** l'archivage a réussi mais la production du rapport échoue
- **THEN** seul le rapport reste à reprendre avec l'autorisation applicable
- **AND** le change n'est pas archivé une seconde fois
