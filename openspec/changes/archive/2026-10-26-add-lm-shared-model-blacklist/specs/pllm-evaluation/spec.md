## ADDED Requirements

### Requirement: Exclusion LM indépendante des catalogues et historiques
PLLM SHALL charger LM avant tout appel fournisseur et exclure les modèles
interdits de tout test et sélection : candidats TFL, rangs, replis, mode6
et frontière de génération, même avec un ancien catalogue ou une mémoire.
Une cible forcée interdite SHALL être refusée sans substitution.

#### Scenario: Candidat interdit
- **WHEN** un candidat figure dans LM avant sa génération
- **THEN** aucune requête de génération ni sélection n'est effectuée

### Requirement: Historique interdit invalidé sans destruction
PLLM SHALL invalider les entrées historiques interdites et les retirer des
listes de candidats publiées. Les exclusions SHALL conserver leur motif ;
le fichier mémoire historique SHALL rester préservé.

#### Scenario: Politique non visitée
- **WHEN** active ou un forçage ne visite pas une politique historique interdite
- **THEN** cette politique reste non évaluée et invalide sans mesure actuelle héritée

#### Scenario: Ancien catalogue et réussite mémorisée
- **WHEN** un ancien catalogue ou historique conserve mimo-v2.5 comme valide
- **THEN** PLLM l'exclut de la sélection et de la génération et conserve une cause explicite

#### Scenario: Rang forcé interdit
- **WHEN** un rang forcé désigne un modèle interdit
- **THEN** ce mode reste invalide sans génération ni choix d'un autre rang

#### Scenario: Candidat direct interdit
- **WHEN** LM contient deepseek-v4-flash
- **THEN** le mode6 ne génère aucune requête et ne sélectionne pas ce candidat
