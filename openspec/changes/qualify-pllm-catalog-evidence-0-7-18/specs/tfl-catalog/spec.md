## MODIFIED Requirements

### Requirement: Investigation des preuves manquantes
Pour Go et OpenRouter, un contexte ou un effort invérifiable SHALL déclencher
une analyse et une recherche du LLM dans les sources officielles. Le catalogue
SHALL tracer fournisseur, ID exact, champ, protocole, sources, dates,
empreintes et conclusion. Une absence de preuve SHALL NOT être présentée comme
la preuve d'une incapacité. L'agent SHALL terminer l'investigation avant la
restitution finale, ou déclarer explicitement son blocage. Une preuve de
raisonnement SHALL s'appliquer au modèle et au protocole exacts publiés dans
le catalogue ; une preuve d'un autre identifiant ou transport SHALL NOT être
transposée.

#### Scenario: Contexte encore invérifiable
- **WHEN** l'investigation ne permet pas de vérifier le contexte
- **THEN** le modèle reste exclu avec les sources examinées et la conclusion
- **AND** aucun contexte ni seuil plus faible n'est inventé

#### Scenario: Source devenue différente ou inaccessible
- **WHEN** une preuve supplémentaire ne correspond plus à sa source courante
- **THEN** elle ne permet aucune admission et une nouvelle investigation est requise

#### Scenario: Preuve d'effort sur le transport exact
- **WHEN** l'investigation établit Medium pour l'identifiant exact et le protocole publié
- **THEN** TFL enregistre cette preuve avec sa provenance et peut admettre le candidat sous réserve des autres filtres
- **AND** une preuve provenant d'un transport différent ne permet pas cette admission

#### Scenario: Redirection HTTPS de source sur la même origine
- **WHEN** la vérification d'une URL officielle suit une redirection HTTPS vers le même hôte avec un paramètre de cache ou d'empreinte
- **THEN** l'empreinte porte sur le contenu reçu après redirection
- **AND** une redirection vers un autre hôte, un protocole HTTP, un port non standard, des identifiants ou un fragment reste bloquée
