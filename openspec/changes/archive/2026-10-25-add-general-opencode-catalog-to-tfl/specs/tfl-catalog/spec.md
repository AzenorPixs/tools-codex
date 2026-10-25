## MODIFIED Requirements

### Requirement: Collecte complète et ordre des fournisseurs
TFL SHALL collecter Go, le catalogue général OpenCode et OpenRouter, avec
models.dev comme complément de métadonnées OpenCode. Une erreur de collecte,
d'authentification ou de données indispensables SHALL faire échouer la
génération sans rapport partiel complet. La restitution SHALL présenter
OpenCode Go, puis OpenCode général, puis OpenRouter.

#### Scenario: Collecte complète
- **WHEN** les trois collectes et leurs métadonnées indispensables réussissent
- **THEN** le rapport contient les trois tableaux dans l'ordre Go, OpenCode général, OpenRouter

#### Scenario: Échec d'un fournisseur
- **WHEN** une collecte indispensable échoue
- **THEN** TFL signale l'échec et ne déclare pas le catalogue actualisé

### Requirement: Modalités et blacklists explicites
Les sorties déclarées audio, vidéo, speech ou sound SHALL être exclues. Une
entrée multimodale reste admissible ; une sortie inconnue SHALL être signalée
comme non vérifiée. Les blacklists permanentes SHALL exclure
muse-spark-1.2-contributor pour Go et OpenCode général, et
meta/muse-spark-1.2-contributor pour OpenRouter.

#### Scenario: Modèle hors critères
- **WHEN** un modèle examiné ne satisfait pas un critère de sélection vérifiable
- **THEN** il ne figure pas dans le tableau retenu
- **AND** son motif d'exclusion est conservé dans le catalogue JSON

### Requirement: Classement et colonnes communes
TFL SHALL classer les modèles de chaque catalogue par coût moyen croissant.
Les trois tableaux SHALL partager les colonnes rang, modèle/ID, contexte,
sortie, prix d'entrée, prix de sortie, coût moyen et code couleur.

#### Scenario: Comparaison des tableaux fournisseurs
- **WHEN** les trois tableaux sont restitués
- **THEN** leurs colonnes sont identiques et chaque classement suit le coût moyen croissant

### Requirement: Actualisation tarifaire sans repli historique
TFL SHALL collecter à chaque génération les tarifs Go et OpenCode général
dans leurs documentations officielles respectives, et OpenRouter dans son
API modèles. TFL MUST NOT utiliser de table statique ou ancien catalogue
comme repli. Chaque catalogue SHALL exposer la source et la date de
récupération tarifaire dans le JSON.

#### Scenario: Nouveau modèle et nouveau prix
- **WHEN** un modèle disponible possède un tarif officiel exploitable ou son tarif change
- **THEN** la génération utilise ce tarif sans modification du code
- **AND** les filtres existants restent applicables

#### Scenario: Source tarifaire inexploitable
- **WHEN** une source indispensable est inaccessible, invalide ou de format non reconnu
- **THEN** TFL échoue explicitement avant publication
- **AND** les rapports précédents restent inchangés

## ADDED Requirements

### Requirement: Catalogue général OpenCode indépendant
TFL SHALL ajouter une section opencode distincte de opencode_go et openrouter.
Disponibilité, tarifs et métadonnées opencode de models.dev SHALL être
collectés indépendamment de Go. Le contexte vérifiable SHALL être ≥ 1M et
la moyenne entrée/sortie comprise entre zéro et 0,50 USD/M inclus. Les
sections existantes SHALL rester compatibles avec leurs consommateurs.

#### Scenario: Modèle gratuit trop court
- **WHEN** une variante gratuite possède seulement 200 000 tokens de contexte
- **THEN** elle est exclue avec le motif de contexte sans abaisser le seuil 1M

#### Scenario: Même identifiant dans deux catalogues
- **WHEN** Go et le catalogue général publient le même identifiant avec des tarifs ou métadonnées distincts
- **THEN** chaque section conserve ses propres données et sources sans emprunt à l'autre

#### Scenario: Compatibilité des consommateurs existants
- **WHEN** un consommateur lit opencode_go ou openrouter dans le catalogue enrichi
- **THEN** il retrouve leurs champs et classements sans dépendre de la nouvelle section opencode

#### Scenario: Plusieurs variantes publiées
- **WHEN** le catalogue général publie plusieurs variantes de contexte ou de période
- **THEN** son prix de classement est la moyenne maximale des variantes publiées
- **AND** la référence hors pointe de Go reste inchangée
