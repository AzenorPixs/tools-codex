## MODIFIED Requirements

### Requirement: Seuils de sélection vérifiables
TFL SHALL retenir un contexte vérifiable ≥1M et un coût moyen entrée/sortie
≤0,50 USD/M hors pointe pour Go ; OpenRouter SHALL appliquer ≤0,20 EUR/M au
taux BCE vérifié. Prix ou contextes inconnus SHALL être exclus. Les gratuits
vérifiés SHALL réussir une réponse complète en Medium, TTFT <30 s et débit
>20 tokens/s avant inclusion dans models. Leurs échecs SHALL rester dans
excluded_models avec leurs preuves.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte, le coût ou l'effort Medium d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

#### Scenario: Gratuit échoué ou non mesurable
- **WHEN** le gratuit échoue sur un seuil, l'effort Medium, l'accès, HTTP ou la mesure
- **THEN** il est exclu de models avec sa cause, ses tentatives et ses mesures disponibles

#### Scenario: Seuils gratuits stricts
- **WHEN** le TTFT atteint 30 s ou le débit atteint au plus 20 tokens/s
- **THEN** le gratuit est exclu même si ses prix, contexte et effort Medium sont admissibles

### Requirement: Classement et colonnes communes
TFL SHALL classer les modèles de chaque catalogue par coût moyen croissant.
Les deux tableaux fournisseurs SHALL garder les colonnes rang, modèle/ID,
contexte, sortie, prix d'entrée, prix de sortie, coût moyen et code couleur.
TFL SHALL ajouter un tableau commun des essais gratuits, avec fournisseur,
modèle, TTFT, débit, raisonnement et état/cause, incluant les échecs dont
l'effort Medium est vérifiable ; les exclus faute de preuve Medium SHALL
rester seulement dans le JSON.

#### Scenario: Comparaison des tableaux fournisseurs
- **WHEN** les deux tableaux fournisseurs sont restitués
- **THEN** leurs huit colonnes ont la même structure, avec Go en USD et OpenRouter en EUR et chaque classement suit le coût moyen croissant

### Requirement: Effort vérifiable avant admission
TFL SHALL exiger une capacité Medium vérifiable pour chaque gratuit ou
payant, avant génération et classement. Les modèles exclus SHALL rester
auditables dans le JSON et SHALL NOT apparaître dans les tableaux, essais
gratuits compris.

#### Scenario: Modèle payant ou gratuit sans preuve
- **WHEN** Medium n'est pas vérifiable dans les sources publiées
- **THEN** le modèle est exclu avant toute génération, absent des tableaux et motivé dans le JSON

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie une liste contenant medium, ou null explicite signifiant tous les efforts
- **THEN** le candidat satisfait le filtre d'effort sous réserve des autres critères
- **AND** une clé absente, une valeur invalide, un booléen reasoning ou supports_max_tokens seul reste exclu

#### Scenario: XHIGH seul ou tous les efforts
- **WHEN** seuls XHIGH ou tous les efforts via null explicite sont publiés
- **THEN** une liste contenant seulement HIGH/XHIGH est exclue ; null explicite est admissible et le test est demandé en Medium

#### Scenario: Budget seul
- **WHEN** le modèle ne publie qu'un budget de raisonnement sans preuve d'effort Medium
- **THEN** il est exclu sans équivalence de niveau inventée

### Requirement: Efforts publiés et équivalences documentées
Les niveaux reasoning_options type=effort/values SHALL être normalisés.
Medium SHALL être admissible uniquement s'il est déclaré ou si null explicite
signifie tous les efforts. Une équivalence documentée vers un interrupteur
SHALL être tracée avec son protocole, ses paramètres et ses sources, sans
inventer un endpoint ni une intensité distincte.

#### Scenario: HIGH équivaut au raisonnement activé
- **WHEN** les sources officielles du modèle établissent une équivalence Medium sur le protocole utilisé
- **THEN** Medium est admissible et le paramètre équivalent documenté est envoyé
- **AND** les autres critères et contrôles restent obligatoires
