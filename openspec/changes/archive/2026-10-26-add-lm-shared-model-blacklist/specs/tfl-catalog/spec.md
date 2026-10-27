## ADDED Requirements

### Requirement: Exclusion LM avant sélection et test
TFL SHALL charger la liste commune LM avant tout appel fournisseur et
l'appliquer à Go, OpenCode général et OpenRouter avant tout classement et
test gratuit. Les modèles interdits SHALL être absents de models et
free_performance_results ; excluded_models SHALL conserver leur motif.
Le JSON SHALL tracer la liste appliquée sans données personnelles.
Les seuils, prix, transports, ordre et exclusions permanentes SHALL rester inchangés.

#### Scenario: Modèle interdit pourtant admissible
- **WHEN** mimo-v2.5 satisfait prix, contexte et modalités dans un catalogue
- **THEN** il est exclu avant tout test gratuit et absent des tableaux retenus
- **AND** son exclusion est auditée sans requête de génération

#### Scenario: Liste utilisateur modifiée
- **WHEN** LM ajoute un modèle avant la nouvelle invocation TFL
- **THEN** les trois catalogues appliquent la liste courante sans mise à jour du code
