## MODIFIED Requirements

### Requirement: Seuils de sélection vérifiables
TFL SHALL retenir un contexte vérifiable ≥1M et un coût moyen entrée/sortie
≤0,50 USD/M, hors pointe pour Go. Prix ou contextes inconnus SHALL être exclus.
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
Les trois tableaux SHALL partager les colonnes rang, modèle/ID, contexte,
sortie, prix d'entrée, prix de sortie, coût moyen et code couleur. TFL SHALL ajouter un tableau commun des essais gratuits, avec fournisseur, modèle, TTFT, débit, raisonnement et état/cause, incluant les exclus.

#### Scenario: Comparaison des tableaux fournisseurs
- **WHEN** les trois tableaux sont restitués
- **THEN** leurs colonnes sont identiques et chaque classement suit le coût moyen croissant

### Requirement: Métadonnées auditables
Le JSON SHALL conserver les sources, exclusions et champs de routage OpenCode Go
`api_endpoint`, `api_protocol` et `endpoint_source`, sans valeur secrète. Les tests gratuits SHALL tracer critères, niveau effectif, paliers, tentatives, mesures et causes. Une mesure historique SHALL NOT valider une collecte actuelle.

#### Scenario: Consultation du routage d'un modèle OpenCode Go
- **WHEN** un consommateur examine un modèle retenu du catalogue
- **THEN** il retrouve les champs de routage et leurs sources sans déduire le protocole du seul nom commercial

### Requirement: Accès aux secrets et repli auto limité
TFL SHALL garder les secrets en mémoire et hors du modèle et des sorties.
En auto, il SHALL essayer le secret 1 puis 2 si inaccessible ; une erreur API
après sélection SHALL NOT déclencher l'autre secret. Les gratuits SHALL
utiliser les clés existantes sans quota ni solde. OpenRouter SHALL utiliser
son environnement puis sa référence historique PLLM. Les autorisations
hors sandbox SHALL être respectées sans contournement.

#### Scenario: Secret du mode 1 inaccessible
- **WHEN** le mode `auto` ne peut pas récupérer le secret du mode 1
- **THEN** TFL tente de récupérer celui du mode 2 sans afficher aucune valeur

#### Scenario: Refus API après sélection du secret
- **WHEN** la requête API utilisant le secret sélectionné échoue
- **THEN** TFL rapporte l'erreur sans essayer l'autre secret pour cette requête
