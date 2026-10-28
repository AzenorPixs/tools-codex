# prompt-dispatch Specification

## Purpose
Résoudre et lancer un prompt du projet courant depuis le seul référentiel
déclaré dans DEVOPS.md, avec liste dynamique, RUN exact et conditions de fin.

## Requirements

### Requirement: Référentiel du projet courant
Le dispatcher SHALL lire le dossier et l'index des prompts exclusivement dans
DEVOPS.md du projet courant. Il SHALL résoudre les fichiers depuis les entrées
de cet index, sans chemin global de repli ni copie embarquée des prompts. Le
répertoire d'installation du skill SHALL NOT être pris comme projet courant.

#### Scenario: Deux projets distincts
- **WHEN** deux projets désignent des référentiels différents
- **THEN** chaque invocation utilise uniquement le DEVOPS et l'index de son projet

### Requirement: Arguments explicites en majuscules
Le dispatcher SHALL accepter LIST, ACL, les autres codes directs existants et CISMPx /
1CISMPx pour tout entier décimal ASCII positif sans zéro initial, sans borne
supérieure ni conversion numérique. Il SHALL refuser les autres arguments
avant toute lecture de configuration par CLI et API Python. Les alias GCM et
GCMP SHALL sélectionner les entrées GSCM.md et GSCMP.md de l'index.

#### Scenario: Alias validés
- **WHEN** GCM ou GCMP est invoqué
- **THEN** GSCM.md ou GSCMP.md est chargé depuis l'entrée correspondante du référentiel

#### Scenario: Argument invalide
- **WHEN** un argument inconnu, une minuscule, CISMP sans numéro ou un suffixe nul, signé, décimal, non ASCII ou avec zéro initial est fourni
- **THEN** le dispatcher retourne une erreur sans lancer de prompt

#### Scenario: Résolution ACL en lecture seule
- **WHEN** ACL est invoqué par CLI ou API avec une entrée ACL pointant vers ACL.md dans le référentiel déclaré
- **THEN** le dispatcher SHALL retourner le texte complet et un état ready sans RUN, limite de change ni action de clôture
- **AND** il SHALL NOT exécuter le texte ni modifier les fichiers

#### Scenario: Source ACL indisponible
- **WHEN** ACL est invoqué sans entrée ACL ou avec un fichier ACL.md absent
- **THEN** le dispatcher SHALL retourner une erreur explicite sans recherche de repli

### Requirement: Liste dynamique sans exécution
LIST SHALL restituer les sigles, intitulés et fichiers de la table de l'index
déclaré, avec leur disponibilité vérifiée. Il SHALL NOT lire les corps de
prompts, lancer un processus de travail ou modifier un fichier. Une évolution
de l'index SHALL être visible sans réédition du plugin.

#### Scenario: Liste du référentiel
- **WHEN** /prompt LIST est invoqué
- **THEN** la liste provient de l'index du projet et aucun prompt n'est exécuté

### Requirement: Résolution bornée et erreurs explicites
Le dispatcher SHALL refuser les déclarations absentes ou ambiguës, les sigles
dupliqués et les chemins sortant du dossier de prompts déclaré. Un lancement
SHALL exiger le fichier attendu, lisible, UTF-8 et non vide. Un lien déclaré
MAY être suivi en lecture si le fichier final reste dans le dossier déclaré.
Les erreurs SHALL NOT déclencher une recherche dans un autre référentiel.

#### Scenario: Source manquante ou hors référentiel
- **WHEN** l'entrée manque, le fichier est indisponible ou sort du dossier déclaré
- **THEN** le dispatcher décrit le blocage sans substitution ni effet de bord

### Requirement: RUN CISMP exact
Les arguments CISMPx et 1CISMPx pour tout suffixe positif valide SHALL charger CISMP.md et
transmettre le RUN exact CISMPn. Le dispatcher SHALL NOT créer un nouveau
numéro, supprimer le suffixe ou confondre deux RUN. La résolution SHALL
préserver le texte du prompt et la directive utilisateur associée.

#### Scenario: RUN trois
- **WHEN** /prompt CISMP3 est invoqué
- **THEN** CISMP.md est chargé avec le RUN CISMP3, sans limite à un change ajoutée

### Requirement: Variantes limitées à un change
1CISMPx pour tout suffixe positif valide SHALL borner le RUN à un seul change complet. Après ses
validations, l'exécution SHALL effectuer l'archivage, générer les statistiques
puis arrêter la session de codage selon le protocole du prompt. Elle SHALL
NOT sélectionner un deuxième change ni prétendre avoir terminé tout le dépôt.
Les accords et barrières applicables SHALL rester requis.

#### Scenario: Un change pour le RUN trois
- **WHEN** /prompt 1CISMP3 est invoqué
- **THEN** le RUN est CISMP3 et la limite est un change
- **AND** l'ordre demandé est change complet, archivage, statistiques, arrêt de la session de codage

#### Scenario: RUN supérieur à huit et très grand numéro
- **WHEN** CISMP9, CISMP12345 ou 1CISMP suivi de 5000 chiffres ASCII valides est fourni
- **THEN** le RUN conserve chaque chiffre et le prompt CISMP.md est sélectionné
- **AND** seule la variante 1CISMPx impose un seul change et les actions de clôture

### Requirement: Exécution par le skill après résolution
Le skill SHALL lire intégralement le prompt sélectionné et exécuter son
processus jusqu'à une condition terminale ou une condition imposant de rendre
la main. Le résolveur SHALL retourner un état prêt à exécuter, jamais une
preuve d'achèvement. Il SHALL NOT exécuter lui-même les actions du texte.

#### Scenario: Condition demandant une décision
- **WHEN** le prompt impose une validation ou une information manquante
- **THEN** le skill respecte cette condition et ne déclare pas le travail achevé
