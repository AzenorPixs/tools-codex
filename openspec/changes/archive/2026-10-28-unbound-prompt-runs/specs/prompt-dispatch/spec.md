## MODIFIED Requirements

### Requirement: Arguments explicites en majuscules
Le dispatcher SHALL accepter LIST, les codes directs existants et CISMPx /
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
