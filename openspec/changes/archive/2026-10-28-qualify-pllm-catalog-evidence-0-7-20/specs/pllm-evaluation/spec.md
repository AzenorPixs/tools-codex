## MODIFIED Requirements

### Requirement: Effort vérifiable indépendant du catalogue et de l'historique
PLLM SHALL demander le paramètre `medium` pour tout candidat benchmarké,
y compris DeepSeek direct au mode7. Le mode5 est exempté de cette exigence et
de toute génération. La preuve que l'API accepte `medium` SHALL suffire,
y compris si le fournisseur le convertit, l'ignore ou ne l'applique pas en
interne. Cette acceptation ne SHALL NOT être présentée comme une mesure de
l'effort interne. Une requête réelle complète avec le paramètre `medium`
acceptée par l'API SHALL établir cette preuve. Un refus explicite du paramètre
SHALL invalider le candidat. Un exclu SHALL NOT être sélectionné ou affiché
dans les tableaux ; son motif précis et sa preuve SHALL rester dans le JSON.
Les sept politiques SHALL rester présentes dans l'état interne.
TFL et PLLM SHALL utiliser la même empreinte source : SHA-256 du texte HTML
visible normalisé en UTF-8 NFC avec espaces consécutifs réduits, ou SHA-256
des octets reçus pour les sources non HTML. Chaque source SHALL déclarer
`fingerprint_method`. Le recontrôle SHALL ignorer les changements de balisage
ou de scripts qui préservent le texte visible.

#### Scenario: Mapping Medium vers High
- **WHEN** une source officielle prouve que l'API accepte Medium comme alias de High
- **THEN** le candidat satisfait l'exigence d'acceptation du paramètre, sous réserve des ressources, du contexte, de la réponse et des seuils de performance
- **AND** le rapport conserve le mapping sans prétendre que l'effort interne est Medium

#### Scenario: Paramètre Medium refusé par l'API
- **WHEN** un appel réel avec le paramètre Medium reçoit un refus de compatibilité reconnu
- **THEN** le candidat reste invalide sans reprise avec un autre effort
- **AND** le diagnostic précis et les preuves filtrées restent dans les exclusions JSON

#### Scenario: Nettoyage d'une exclusion historique
- **WHEN** le nettoyage de publication retire un candidat qui n'a aucune preuve d'acceptation du paramètre
- **THEN** le rapport conserve le motif dans la cause de la politique et dans les exclusions JSON
- **AND** l'identifiant du candidat reste absent des colonnes utilisateur

#### Scenario: Preuve publiée et métadonnées invalides
- **WHEN** supported_efforts publie medium, null explicite, ou une requête courante avec medium est acceptée par l'API
- **THEN** le candidat satisfait le critère d'acceptation du paramètre sous réserve des autres critères
- **AND** une métadonnée absente ou invalide seule ne prouve pas l'acceptation, mais ne bloque pas un test réel

#### Scenario: Ancien catalogue ou résultat historique
- **WHEN** un candidat benchmarké précédemment retenu n'a pas de preuve d'effort admissible
- **THEN** il ne peut être sélectionné, généré ou affiché malgré son historique
- **AND** cette exigence ne s'applique pas au mode5, qui ne benchmarke pas

#### Scenario: Cible forcée sans effort vérifiable
- **WHEN** un rang forcé désigne un modèle sans preuve Medium
- **THEN** seule la candidate forcée est testée avec le paramètre medium, sans substitution
- **AND** elle reste invalide si l'API refuse ce paramètre
- **AND** un rang du mode5 reste soumis seulement au plafond de coût et au contexte

#### Scenario: Candidat direct sans preuve
- **WHEN** le modèle DeepSeek direct n'a pas de capacité Medium vérifiable
- **THEN** PLLM envoie medium sur la route directe publiée et vérifie la réponse réelle
- **AND** une réponse API complète établit l'acceptation, même si le fournisseur mappe ou ignore medium

#### Scenario: Preuve publiée liée au transport
- **WHEN** un candidat TFL publie une preuve d'acceptation Medium pour son identifiant et son protocole courants
- **THEN** PLLM recontrôle cette source avant génération et conserve le résultat dans l'audit
- **AND** l'absence ou l'inaccessibilité de cette preuve déclenche un essai API avec medium, sans conclure à un refus

### Requirement: Contrat Medium propre au transport
PLLM SHALL envoyer le paramètre `medium` sur le protocole publié avant tout
benchmark. Les métadonnées et sources officielles peuvent documenter son
acceptation ; à défaut, une réponse API complète à la requête Medium SHALL
établir que le paramètre a été accepté. L'acceptation SHALL
suffire même si le fournisseur convertit, ignore ou ne l'applique pas en
interne ; le rapport SHALL NOT présenter cette acceptation comme une mesure de
l'effort interne. Envoyer `reasoning_effort` (Chat Completions/DeepSeek),
`reasoning.effort` (Responses) ou `output_config.effort` (Messages) selon le
transport publié. Un refus de Medium SHALL NOT retenter avec un autre effort.

#### Scenario: Gratuit OpenCode en Chat Completions
- **WHEN** un candidat OpenCode utilise chat_completions sans équivalence documentée
- **THEN** la requête contient reasoning_effort=medium sans thinking
- **AND** le modèle doit réussir ses mesures actuelles avant de devenir valide

#### Scenario: Autres transports et DeepSeek
- **WHEN** Responses, Messages ou DeepSeek direct sont évalués
- **THEN** leurs paramètres Medium propres au transport restent préservés

#### Scenario: Medium non publié
- **WHEN** les métadonnées n'annoncent pas Medium
- **THEN** le candidat est essayé avec le paramètre Medium sur sa route publiée
- **AND** l'absence de métadonnées seule ne prouve pas un refus

#### Scenario: Aucun niveau autorisé
- **WHEN** l'API refuse explicitement le paramètre Medium
- **THEN** le candidat est invalide sans repli vers un autre effort

### Requirement: Effort demandé exclusivement Medium
PLLM SHALL demander exclusivement le paramètre `medium` pour les politiques
benchmarkées, les forçages de rang et chaque transport. Le mode5 ne demande
pas d'effort et n'exécute aucune génération. Une réponse API complète SHALL
établir l'acceptation du paramètre même si l'effort interne est converti,
ignoré ou non appliqué. Un refus de Medium SHALL invalider le candidat sans
repli vers un autre effort.

#### Scenario: Demande forcée ou transport non compatible
- **WHEN** une cible forcée ou un transport refuse le paramètre medium
- **THEN** le candidat est déclaré invalide sans génération à un autre effort

### Requirement: Historique limité aux résultats Medium
PLLM SHALL NOT valider un résultat historique benchmarké dont le paramètre
`medium` demandé ou son acceptation API n'est pas explicitement établi. PLLM SHALL
invalider ces résultats avant affichage et sélection, conserver leur motif
dans les exclusions et ne pas réutiliser leurs paliers. Une mesure historique
ne prouve pas l'acceptation API courante. Cette règle ne s'applique pas au
mode5 non benchmarké.

#### Scenario: Historique incompatible malgré une capacité Medium
- **WHEN** le résultat ou une de ses tentatives historiques n'enregistre pas explicitement la demande medium et son acceptation API
- **THEN** PLLM l'invalide avant affichage et sélection
- **AND** conserve le motif d'exclusion sans réutiliser son palier

### Requirement: Effort courant séparé des traces historiques
PLLM SHALL valider la demande courante du paramètre Medium et son acceptation
API sans traiter les métadonnées d'override ou d'anciennes tentatives comme
preuve actuelle. Une réponse complète établit l'acceptation du paramètre ;
elle ne mesure pas l'effort interne appliqué. Des métadonnées ou une source
officielle actuelle et propre au transport peuvent aussi établir l'acceptation.

#### Scenario: Candidat Medium avec anciennes traces XHigh
- **WHEN** la requête courante demande et l'API accepte medium, mais que `user_override` ou `performance_attempts` historiques contiennent XHigh
- **THEN** PLLM conserve et évalue le candidat courant sans reprendre ces anciennes traces comme mesure ou palier valide

#### Scenario: Tentative courante non Medium
- **WHEN** la requête courante ne demande pas medium ou l'API ne l'accepte pas
- **THEN** PLLM exclut le résultat courant malgré une capacité fournisseur historique qui inclut Medium
