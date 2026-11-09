## ADDED Requirements

### Requirement: Normalisation des modalités Go
TFL SHALL normaliser les types MIME connus en catégories communes avant
comparaison. `image/*`, `audio/*`, `video/*`, `text/*` et
`application/pdf` SHALL correspondre respectivement à `image`, `audio`,
`video`, `text` et `pdf`. Les valeurs inconnues SHALL rester explicites,
sans catégorie inventée. Le JSON SHALL conserver les valeurs déclarées par
chaque source, leur provenance et leur date.

#### Scenario: Types MIME et catégories équivalentes
- **WHEN** l'API publie `image/jpeg`, `application/pdf` et `text`, tandis que models.dev publie `image`, `pdf` et `text`
- **THEN** TFL résout les deux déclarations en catégories équivalentes et poursuit la collecte
- **AND** le JSON conserve les valeurs déclarées par chaque source et leur provenance

### Requirement: Contrôle des modalités canoniques
TFL SHALL bloquer la publication lorsque les ensembles canoniques des
déclarations de modalités diffèrent entre sources ou au sein d'une source.
Les sorties audio, vidéo, speech et sound SHALL rester exclues après
normalisation des types MIME.

#### Scenario: Modalités réellement contradictoires
- **WHEN** les ensembles canoniques des déclarations API et models.dev diffèrent
- **THEN** TFL bloque explicitement la publication avant d'écrire les rapports

#### Scenario: Valeur multimédia de sortie normalisée
- **WHEN** une sortie API déclare un type MIME `audio/*` ou `video/*`
- **THEN** TFL résout sa catégorie et applique le filtre des sorties non textuelles
