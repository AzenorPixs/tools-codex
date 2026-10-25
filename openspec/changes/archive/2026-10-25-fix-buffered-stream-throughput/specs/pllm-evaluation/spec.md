## MODIFIED Requirements

### Requirement: Protocole des mesures traçable
Les mesures SHALL utiliser une horloge monotone. Le TTFT SHALL porter sur
le premier contenu visible. Le débit SHALL être le comptage de sortie divisé
par la durée totale non arrondie de la requête, TTFT inclus : global pour
Go/général, réponse seule pour OpenRouter/DeepSeek. Une réponse complète en
un bloc SHALL être mesurable. Durée ou comptage invalides SHALL produire
une mesure indisponible. Le JSON SHALL tracer profil, formule et durées.

#### Scenario: Deux catalogues OpenCode
- **WHEN** les candidats gratuits Go et OpenCode général sont comparés
- **THEN** leurs débits utilisent la même portée raisonnement et réponse
- **AND** leurs fournisseurs, routes et comptages restent distincts

#### Scenario: Mesures provenant de fournisseurs différents
- **WHEN** des mesures OpenCode et OpenRouter sont restituées
- **THEN** le JSON conserve leur portée sans les présenter comme une mesure identique


#### Scenario: Fragments reçus en rafale
- **WHEN** un flux complet est reçu sur une fenêtre de contenu très courte
- **THEN** les tokens/s utilisent la durée complète de la requête sans extrapolation entre fragments

#### Scenario: Un bloc complet
- **WHEN** une réponse complète est reçue en un seul bloc avec compteur et durée fiables
- **THEN** le débit moyen est calculé sans exiger plusieurs fragments

#### Scenario: Durée invalide
- **WHEN** la durée totale est nulle, négative ou non finie
- **THEN** aucun débit n'est fabriqué et le candidat reste invalide avec cause explicite

#### Scenario: Durée non arrondie
- **WHEN** l'affichage arrondit la durée
- **THEN** le calcul utilise encore la durée monotone non arrondie

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL garder les paliers 1024, 2048, 4096, 8192 et 120 s par requête.
Les contrôles applicables SHALL précéder chaque requête, sans quota en 3/4.
Un HTTP 400/429 SHALL arrêter le candidat, hors repli XHIGH autorisé.
La mémoire SHALL distinguer modèle, raisonnement et profil de débit, garder
les succès historiques sans les réutiliser pour un autre profil. Une mémoire
invalide SHALL NOT être écrasée ; un ancien succès SHALL NOT valider l'invocation.

#### Scenario: Nouvelle politique gratuite
- **WHEN** mode3 ou mode4 est évalué pour la première fois après migration
- **THEN** son premier palier est 1024, sans réutiliser l'ancien OpenRouter ou DeepSeek
- **AND** la mémoire des anciens 3/4 est déplacée vers 5/6 lors du passage du schéma 1 au schéma 2

#### Scenario: Reprise de configuration connue
- **WHEN** une configuration possède un succès mémorisé
- **THEN** son palier peut être repris avec des mesures actuelles et les contrôles applicables

#### Scenario: HTTP 400 ou 429
- **WHEN** un candidat reçoit ce refus sans repli d'effort XHIGH autorisé
- **THEN** aucun budget supérieur n'est tenté pour ce candidat
- **AND** les autres candidats admissibles gardent leurs propres tests

#### Scenario: Troncature ou seuil non satisfait
- **WHEN** le résultat est incomplet ou hors seuil
- **THEN** le palier suivant reste possible après les contrôles applicables


#### Scenario: Plusieurs candidats et retour à une configuration connue
- **WHEN** plusieurs configurations ont été évaluées avec succès
- **THEN** leurs paliers mémorisés sont distincts et réutilisables par configuration
- **AND** un candidat changé sans réussite correspondante repart à 1024

#### Scenario: Réutilisation d'un palier réussi
- **WHEN** une réussite mémorisée correspond à la même configuration
- **THEN** l'évaluation peut reprendre à ce palier avec de nouveaux contrôles applicables
- **AND** un échec ne remplace pas la dernière réussite

#### Scenario: Configuration remplacée après HTTP 429
- **WHEN** un autre candidat autorisé remplace le modèle limité
- **THEN** ses paliers sont recalculés selon son identité
- **AND** sans réussite correspondante, il commence à 1024 tokens
- **AND** l'épuisement des candidats reste un échec sans sélection valide

#### Scenario: HTTP 400 ou 429 au premier palier
- **WHEN** une requête reçoit HTTP 400 ou HTTP 429 sans repli d'effort XHIGH autorisé
- **THEN** aucun budget supérieur n'est testé pour ce candidat dans cette invocation
- **AND** les autres candidats autorisés gardent leurs propres contrôles et tests

#### Scenario: Troncature ou seuil mesuré non satisfait
- **WHEN** le candidat reçoit une réponse tronquée ou échoue sur un seuil mesuré
- **THEN** les paliers suivants restent disponibles après les contrôles applicables

#### Scenario: Repli d'effort après refus ciblé
- **WHEN** HIGH reçoit HTTP 400 sur son paramètre d'effort et XHIGH est annoncé
- **THEN** un seul repli XHIGH est autorisé avec ses propres paliers
- **AND** HTTP 401/403/429, troncature ou seuil ne déclenchent aucun repli d'effort



#### Scenario: Nouveau profil après un ancien succès
- **WHEN** un succès utilise l'ancien débit entre fragments
- **THEN** il reste historique et n'amorce pas le nouveau protocole
- **AND** sans succès du nouveau profil, le premier palier est 1024

#### Scenario: Réutilisation du nouveau profil
- **WHEN** une réussite mémorisée correspond à la même configuration et au même profil de débit
- **THEN** son palier peut être repris avec des mesures actuelles

### Requirement: Publication traçable
PLLM SHALL publier pllm-current.json et pllm-current.md atomiquement par
fichier, sans secret. Le JSON SHALL tracer horodatages, critères, causes,
sélection, comptages, profil de débit et durée totale non arrondie utilisée.
Les rapports SHALL indiquer que le débit moyen inclut l'attente et le TTFT.
Les anciens débits SHALL NOT être présentés comme comparables ou actuels.

#### Scenario: Résultats publiés
- **WHEN** l'évaluation se termine et la publication réussit
- **THEN** les deux fichiers décrivent la même évaluation sans valeur secrète
