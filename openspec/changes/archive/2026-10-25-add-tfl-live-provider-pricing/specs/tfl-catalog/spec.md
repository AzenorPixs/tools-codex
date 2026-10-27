## ADDED Requirements

### Requirement: Actualisation tarifaire sans repli historique
TFL SHALL collecter à chaque génération les tarifs OpenCode Go dans sa
documentation officielle et les tarifs OpenRouter dans son API modèles.
TFL MUST NOT utiliser une table tarifaire statique ou un ancien catalogue
comme repli lorsque cette collecte échoue. Chaque fournisseur SHALL exposer
la source et la date de récupération tarifaire dans le JSON.

#### Scenario: Nouveau modèle et nouveau prix
- **WHEN** un modèle disponible possède un tarif officiel exploitable ou son tarif change
- **THEN** la génération utilise ce tarif sans modification du code
- **AND** les filtres existants restent applicables

#### Scenario: Source tarifaire inexploitable
- **WHEN** une source indispensable est inaccessible, invalide ou de format non reconnu
- **THEN** TFL échoue explicitement avant publication
- **AND** les rapports précédents restent inchangés

### Requirement: Correspondances tarifaires non ambiguës
TFL SHALL associer les tarifs Go aux identifiants disponibles par une
correspondance vérifiable de nom ou d'identifiant. Une absence de tarif SHALL
produire une exclusion motivée. Une collision de correspondances ou des
tarifs contradictoires pour une même variante SHALL produire un échec explicite.
Les prix utilisés SHALL être finis, non négatifs et exprimés en USD par
million de tokens. Les montants barrés MUST NOT servir de prix courant.

#### Scenario: Tarif introuvable
- **WHEN** aucun tarif ne correspond à un modèle disponible
- **THEN** le modèle est exclu avec le motif tarifaire dans le JSON

#### Scenario: Prix contradictoires
- **WHEN** deux tableaux donnent des prix différents pour la même variante
- **THEN** la génération échoue sans choisir silencieusement l'un des tableaux

### Requirement: Variantes tarifaires auditables
TFL SHALL conserver séparément les prix d'entrée, sortie, cache et les variantes
pointe/hors pointe ou de contexte disponibles dans le JSON. Pour Go, le
classement SHALL utiliser le hors pointe et le coût moyen maximal entre
paliers de contexte lorsqu'il en existe plusieurs. Une estimation non
collectée SHALL rester non vérifiée.

#### Scenario: Pointe et paliers de contexte
- **WHEN** la source publie plusieurs variantes tarifaires pour un modèle
- **THEN** le JSON conserve les variantes et la règle ayant déterminé le prix de classement
- **AND** le cache et les prix pointe ne sont pas confondus avec l'entrée hors pointe

### Requirement: Compatibilité du rafraîchissement
Les identifiants OpenRouter, filtres, colonnes communes, interfaces CLI et
champs consommés par PLLM SHALL rester compatibles. Une route Go inconnue
SHALL être signalée sans protocole inventé.

#### Scenario: OpenRouter actualisé
- **WHEN** la réponse API OpenRouter change les prix d'un identifiant sélectionné
- **THEN** le classement utilise les nouveaux prix convertis par million
- **AND** le JSON conserve leur provenance et les prix de cache disponibles
