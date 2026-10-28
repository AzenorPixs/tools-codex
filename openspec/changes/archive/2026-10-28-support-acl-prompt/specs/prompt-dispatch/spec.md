## MODIFIED Requirements

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

