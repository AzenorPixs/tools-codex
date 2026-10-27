## ADDED Requirements

### Requirement: Effort vérifiable avant admission
TFL SHALL exiger une capacité HIGH ou XHIGH vérifiable pour chaque gratuit
ou payant, avant génération et classement. HIGH SHALL être préféré et XHIGH
SHALL être le seul repli. Les modèles exclus SHALL rester auditables dans
le JSON et SHALL NOT apparaître dans les tableaux, essais gratuits compris.

#### Scenario: Modèle payant ou gratuit sans preuve
- **WHEN** HIGH et XHIGH ne sont pas vérifiables dans les sources publiées
- **THEN** le modèle est exclu avant toute génération, absent des tableaux et motivé dans le JSON

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie une liste contenant high ou xhigh, ou null explicite signifiant tous les efforts
- **THEN** le candidat satisfait le filtre d'effort sous réserve des autres critères
- **AND** une clé absente, une valeur invalide, un booléen reasoning ou supports_max_tokens seul reste exclu

#### Scenario: XHIGH seul ou tous les efforts
- **WHEN** seuls XHIGH ou tous les efforts via null explicite sont publiés
- **THEN** le modèle est admissible respectivement en XHIGH ou HIGH sous réserve des autres critères

#### Scenario: Budget seul
- **WHEN** le modèle ne publie qu'un budget de raisonnement sans preuve d'effort HIGH/XHIGH
- **THEN** il est exclu sans équivalence de niveau inventée

### Requirement: Plafond OpenRouter en EUR
TFL SHALL appliquer une moyenne de base OpenRouter <= 0,20 EUR/M après
conversion au dernier taux BCE USD par EUR, positif et fini. Comparaison
non arrondie, prix natifs USD, prix EUR, source et dates de publication et de
récupération SHALL être tracés. Une conversion invérifiable SHALL bloquer
la publication et préserver les rapports précédents.

#### Scenario: Limite inclusive et montant supérieur
- **WHEN** la moyenne convertie atteint exactement 0,20 EUR/M ou dépasse ce seuil avant arrondi
- **THEN** seul le premier montant est admissible sous réserve des autres filtres

#### Scenario: Conversion non vérifiable
- **WHEN** le cours BCE est absent, invalide ou inaccessible
- **THEN** aucun nouveau rapport n'est publié et les fichiers précédents restent préservés

### Requirement: Deux tableaux fournisseurs et catalogue général préservé
TFL SHALL afficher uniquement Go puis OpenRouter, suivis des essais gratuits
admissibles à l'effort. Chaque tableau fournisseur SHALL garder huit colonnes,
Go en USD/M et OpenRouter en EUR/M avec taux daté. La collecte et la section
JSON opencode SHALL rester disponibles aux modes PLLM 3/4. Les plafonds Go et
général SHALL rester 0,50 USD/M. Une section vide SHALL bloquer la publication.

#### Scenario: Publication à deux tableaux
- **WHEN** les trois collectes satisfont les nouveaux critères
- **THEN** le rapport affiche Go puis OpenRouter, aucun tableau général, et le JSON conserve les trois sections

#### Scenario: Aucune preuve d'effort dans une section
- **WHEN** tous ses candidats sont exclus faute de preuve HIGH/XHIGH
- **THEN** TFL signale la sélection vide avant publication sans réutiliser d'anciennes qualifications

## MODIFIED Requirements

### Requirement: Collecte complète et ordre des fournisseurs
TFL SHALL collecter Go, le catalogue général OpenCode et OpenRouter, avec
models.dev comme complément de métadonnées OpenCode. Une erreur de collecte,
d'authentification ou de données indispensables SHALL faire échouer la
génération sans rapport partiel complet. La restitution SHALL présenter
OpenCode Go puis OpenRouter ; OpenCode général reste dans le JSON.

#### Scenario: Collecte complète
- **WHEN** les trois collectes et leurs métadonnées indispensables réussissent
- **THEN** le rapport contient les deux tableaux Go puis OpenRouter et conserve opencode dans le JSON

#### Scenario: Échec d'un fournisseur
- **WHEN** une collecte indispensable échoue
- **THEN** TFL signale l'échec et ne déclare pas le catalogue actualisé

### Requirement: Seuils de sélection vérifiables
TFL SHALL retenir un contexte vérifiable ≥1M et un coût moyen entrée/sortie
≤0,50 USD/M pour Go et général, hors pointe pour Go ; OpenRouter SHALL appliquer ≤0,20 EUR/M au taux BCE vérifié. Prix ou contextes inconnus SHALL être exclus.
Les gratuits vérifiés SHALL réussir une réponse complète en HIGH ou son repli
XHIGH autorisé, TTFT <30 s et débit >20 tokens/s avant inclusion dans models.
Leurs échecs SHALL rester dans excluded_models avec leurs preuves.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte ou le coût d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

#### Scenario: Gratuit échoué ou non mesurable
- **WHEN** le gratuit échoue sur un seuil, le raisonnement, l'accès, HTTP ou la mesure
- **THEN** il est exclu de models avec sa cause, ses tentatives et ses mesures disponibles

#### Scenario: Seuils gratuits stricts
- **WHEN** le TTFT atteint 30 s ou le débit atteint au plus 20 tokens/s
- **THEN** le gratuit est exclu même si ses prix et contexte sont admissibles

### Requirement: Classement et colonnes communes
TFL SHALL classer les modèles de chaque catalogue par coût moyen croissant.
Les deux tableaux fournisseurs SHALL garder les colonnes rang, modèle/ID, contexte,
sortie, prix d'entrée, prix de sortie, coût moyen et code couleur. TFL SHALL ajouter un tableau commun des essais gratuits, avec fournisseur, modèle, TTFT, débit, raisonnement et état/cause, incluant les échecs dont l'effort est vérifiable ; les exclus HIGH/XHIGH SHALL rester seulement dans le JSON.

#### Scenario: Comparaison des tableaux fournisseurs
- **WHEN** les deux tableaux fournisseurs sont restitués
- **THEN** leurs huit colonnes ont la même structure, avec Go en USD et OpenRouter en EUR et chaque classement suit le coût moyen croissant
