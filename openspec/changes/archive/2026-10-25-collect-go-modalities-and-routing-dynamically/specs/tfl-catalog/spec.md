## ADDED Requirements

### Requirement: Modalités Go collectées sans liste de modèles
TFL SHALL résoudre les modalités Go depuis les déclarations courantes de
l'API et de models.dev, sans liste statique de modèles ni inférence par nom.
Les modalités connues SHALL conserver leur source ; une modalité absente
SHALL rester non vérifiée. Des déclarations contradictoires SHALL produire
une erreur explicite avant publication.

#### Scenario: Modèle inédit documenté
- **WHEN** un modèle inédit possède des modalités publiées dans models.dev
- **THEN** TFL les restitue avec leur provenance sans ajout de son identifiant au code

#### Scenario: Modalité absente ou contradictoire
- **WHEN** les sources n'indiquent aucune sortie ou indiquent des sorties contradictoires
- **THEN** une absence reste non vérifiée et une contradiction bloque explicitement la publication

### Requirement: Transport Go résolu sans liste de modèles
TFL SHALL résoudre le transport Go depuis des métadonnées explicites de
protocole/SDK et de base API, sans liste statique de modèles. Les champs
api_endpoint, api_protocol et endpoint_source SHALL conserver un contrat
compatible avec les consommateurs. Un protocole non reconnu ou une base
manquante SHALL rester non vérifié avec un motif, sans repli implicite.

#### Scenario: Nouvelle route publiée
- **WHEN** la source publie une nouvelle base API et un transport reconnu pour un modèle
- **THEN** TFL actualise ses champs de routage et leur provenance sans modifier de liste de modèles

#### Scenario: Protocole inconnu
- **WHEN** le transport publié n'est pas reconnu ou manque
- **THEN** TFL signale une route non vérifiée sans en inventer une autre

### Requirement: Origine sûre des endpoints Go
TFL SHALL valider HTTPS et l'origine OpenCode des endpoints publiés. Une URL
avec identifiants utilisateur, query, fragment ou origine étrangère SHALL
être rejetée explicitement avant publication. La résolution documentaire
SHALL être distinguée d'une qualification réelle de génération.

#### Scenario: Source de routage non sûre
- **WHEN** une métadonnée désigne une URL non sûre ou extérieure à l'origine OpenCode
- **THEN** la génération échoue avant publication sans restituer de secret

#### Scenario: Route documentée
- **WHEN** une route est résolue depuis les sources publiées
- **THEN** le catalogue indique ses sources et sa date sans prétendre à un test de génération
