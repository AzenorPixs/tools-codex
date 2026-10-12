# tfl-catalog Specification

## Purpose

Définir la collecte, le filtrage, le classement et la publication vérifiable du catalogue TFL sans données sensibles.

## Requirements

### Requirement: Collecte complète et ordre des fournisseurs
TFL SHALL collecter les modèles OpenCode Go et OpenRouter, en utilisant
models.dev comme complément de contexte pour OpenCode Go. Une erreur de
collecte, d'authentification ou de données indispensables SHALL faire échouer
la génération, sans annoncer un rapport partiel comme complet. La restitution
SHALL présenter OpenCode Go avant OpenRouter.

#### Scenario: Collecte complète
- **WHEN** les deux collectes et leurs métadonnées indispensables réussissent
- **THEN** le rapport contient les deux tableaux dans l'ordre OpenCode Go puis OpenRouter

#### Scenario: Échec d'un fournisseur
- **WHEN** une collecte indispensable échoue
- **THEN** TFL signale l'échec et ne déclare pas le catalogue actualisé

### Requirement: Seuils de sélection vérifiables
TFL SHALL retenir les modèles dont le contexte vérifiable est au moins de
1 000 000 tokens et le coût moyen entrée/sortie au plus de 0,50 USD par million
de tokens. Les coûts OpenCode Go SHALL utiliser la référence hors pointe.
Les coûts inconnus et contextes inconnus ou insuffisants SHALL être exclus.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte ou le coût d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

### Requirement: Prix finis et JSON strict
TFL SHALL exclure avec un motif les prix OpenRouter non finis ou dont la
conversion par million ou le calcul de moyenne déborde. Le catalogue publié
SHALL être du JSON strict, sans `NaN` ni infini. Un échec de sérialisation
SHALL empêcher la publication d'un catalogue non conforme.

#### Scenario: Prix non exploitable
- **WHEN** un prix vaut `NaN`, un infini ou déborde lors du calcul
- **THEN** le modèle est exclu comme coût non vérifiable
- **AND** les prix finis admissibles restent classés selon les règles communes

### Requirement: Modalités et blacklists explicites
Les sorties déclarées audio, vidéo, speech ou sound SHALL être exclues. Une
entrée multimodale reste admissible ; une sortie inconnue SHALL être signalée
comme non vérifiée.
Les blacklists permanentes SHALL exclure `muse-spark-1.2-contributor` pour
OpenCode Go et `meta/muse-spark-1.2-contributor` pour OpenRouter.

#### Scenario: Modèle hors critères
- **WHEN** un modèle examiné ne satisfait pas un critère de sélection vérifiable
- **THEN** il ne figure pas dans le tableau retenu
- **AND** son motif d'exclusion est conservé dans le catalogue JSON

### Requirement: Sélection OpenRouter explicite
La sélection OpenRouter SHALL rester limitée à `qwen/qwen3.7-flash`,
`deepseek/deepseek-v4-flash-0731` et `deepseek/deepseek-v4-flash`, sous réserve
des filtres communs. L'absence d'un de ces identifiants dans la réponse API
SHALL produire un échec explicite, sans remplacement silencieux.

#### Scenario: Identifiant fixé absent
- **WHEN** un identifiant de la sélection fixée manque dans la réponse API
- **THEN** TFL échoue explicitement sans lui substituer un autre modèle

### Requirement: Classement et colonnes communes
TFL SHALL classer les modèles par coût moyen croissant. Les deux tableaux
SHALL partager les colonnes rang, modèle/ID, contexte, sortie, prix d'entrée,
prix de sortie, coût moyen et code couleur.

#### Scenario: Comparaison des tableaux fournisseurs
- **WHEN** les deux tableaux sont restitués
- **THEN** leurs colonnes sont identiques et chaque classement suit le coût moyen croissant

### Requirement: Publication des fichiers courants
TFL SHALL publier un catalogue
`tfl.json` et son rapport `tfl.md`, horodatés, dans `data/` ou dans le répertoire
demandé par `--output-dir`. Chaque fichier SHALL être remplacé atomiquement.

#### Scenario: Publication du catalogue
- **WHEN** la génération et la publication réussissent
- **THEN** les deux fichiers décrivent la même collecte et ses filtres
- **AND** la restitution indique la date et les chemins des fichiers sans exposer de secret

### Requirement: Métadonnées auditables
Le JSON SHALL conserver les sources, exclusions et champs de routage OpenCode Go
`api_endpoint`, `api_protocol` et `endpoint_source`, sans valeur secrète.

#### Scenario: Consultation du routage d'un modèle OpenCode Go
- **WHEN** un consommateur examine un modèle retenu du catalogue
- **THEN** il retrouve les champs de routage et leurs sources sans déduire le protocole du seul nom commercial

### Requirement: Accès aux secrets et repli auto limité
TFL SHALL conserver les secrets hors du contexte du modèle et des sorties.
En mode `auto`, la recherche du secret OpenCode Go SHALL essayer le mode 1,
puis le mode 2 si le premier est inaccessible. Après sélection du premier
secret accessible, une erreur API SHALL être rapportée sans repli vers
l'autre secret. Les invocations SHALL respecter les autorisations
d'exécution hors sandbox et ne pas contourner un refus de la plateforme.

#### Scenario: Secret du mode 1 inaccessible
- **WHEN** le mode `auto` ne peut pas récupérer le secret du mode 1
- **THEN** TFL tente de récupérer celui du mode 2 sans afficher aucune valeur

#### Scenario: Refus API après sélection du secret
- **WHEN** la requête API utilisant le secret sélectionné échoue
- **THEN** TFL rapporte l'erreur sans essayer l'autre secret pour cette requête
