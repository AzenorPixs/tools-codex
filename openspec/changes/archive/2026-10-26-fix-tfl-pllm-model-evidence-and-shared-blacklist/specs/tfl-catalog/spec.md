## ADDED Requirements

### Requirement: Investigation des preuves manquantes
Pour Go, OpenCode général et OpenRouter, un contexte ou un effort invérifiable
SHALL déclencher une analyse et une recherche du LLM dans les sources
officielles. Le catalogue SHALL tracer fournisseur, ID exact, champ, sources,
dates, empreintes et conclusion. Une absence de preuve SHALL NOT être présentée
comme une incapacité démontrée. L'agent SHALL terminer l'investigation avant
la restitution finale, ou déclarer explicitement son blocage.

#### Scenario: Contexte encore invérifiable
- **WHEN** l'investigation ne permet pas de vérifier le contexte
- **THEN** le modèle reste exclu avec les sources examinées et la conclusion
- **AND** aucun contexte ni seuil plus faible n'est inventé

#### Scenario: Source devenue différente ou inaccessible
- **WHEN** une preuve supplémentaire ne correspond plus à sa source courante
- **THEN** elle ne permet aucune admission et une nouvelle investigation est requise

### Requirement: Efforts publiés et équivalences documentées
Les niveaux de reasoning_options type=effort/values SHALL être normalisés.
HIGH/XHIGH officiellement acceptés SHALL être admissibles même si plusieurs
niveaux produisent le même comportement. Une équivalence documentée vers un
interrupteur SHALL être tracée avec son protocole, ses paramètres et ses
sources, sans inventer un endpoint ni une intensité distincte.

#### Scenario: HIGH équivaut au raisonnement activé
- **WHEN** les sources officielles du modèle établissent cette équivalence sur le protocole utilisé
- **THEN** HIGH est admissible et le paramètre équivalent documenté est envoyé
- **AND** les autres critères et contrôles restent obligatoires

### Requirement: Source unique LM
TFL SHALL appliquer uniquement la liste LM, sans liste permanente intégrée.

#### Scenario: Retrait d'une ancienne exclusion permanente
- **WHEN** LM retire muse-spark-1.2-contributor
- **THEN** aucune liste TFL résiduelle ne l'exclut, y compris avec préfixe fournisseur
