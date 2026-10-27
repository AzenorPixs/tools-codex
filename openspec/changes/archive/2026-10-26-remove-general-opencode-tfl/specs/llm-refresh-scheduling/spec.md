## ADDED Requirements

### Requirement: Validation des deux catalogues courants
Après une publication fraîche réussie TFL, le runner SHALL exiger les listes
models non vides de opencode_go et openrouter. Il SHALL NOT exiger ni consommer
une section opencode. Les horaires, contrôles d'activité, quotas, verrouillages
et interdiction de réutiliser un ancien catalogue SHALL rester inchangés.

#### Scenario: Nouveau catalogue à deux sections
- **WHEN** TFL publie uniquement Go et OpenRouter avec des listes non vides
- **THEN** le contrôle de catalogue autorise la suite sous réserve des autres gardes

#### Scenario: Section courante absente ou vide
- **WHEN** Go ou OpenRouter manque, est malformé ou possède models vide
- **THEN** PLLM n'est pas lancé même si un ancien opencode est présent
