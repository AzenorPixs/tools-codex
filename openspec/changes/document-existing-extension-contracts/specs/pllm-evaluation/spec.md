## ADDED Requirements

### Requirement: Politiques et sélection explicites
PLLM SHALL évaluer les quatre modes définis dans l'ordre de priorité 1 à 4 :
OpenCode Go pour les modes 1 et 2, OpenRouter pour le mode 3 et DeepSeek direct
pour le mode 4. Les modèles des modes 1 à 3 SHALL être résolus depuis le
catalogue TFL selon le rang demandé, avec identifiant exact et date du
catalogue. Le raisonnement par défaut SHALL être Low. La sélection SHALL
retenir la première politique valide réellement évaluée pendant l'invocation.

#### Scenario: Sélection selon la priorité
- **WHEN** plusieurs politiques évaluées satisfont leurs critères
- **THEN** seule la première par priorité croissante est sélectionnée
- **AND** la sélection ne dépend pas du débit le plus élevé

### Requirement: Quotas avant performance
PLLM SHALL consulter les quotas ou soldes actuels avant chaque test de
performance. Un contrôle indispensable absent ou invalide SHALL arrêter
l'évaluation de la politique avant la performance.

#### Scenario: Quota épuisé ou non disponible
- **WHEN** un quota indispensable est épuisé ou ne peut pas être établi
- **THEN** la politique est invalide avec une cause explicite
- **AND** aucun test de performance n'est lancé pour cette politique

### Requirement: Conditions de quota propres aux fournisseurs
Pour OpenCode Go, les périodes 5 heures, semaine et mois SHALL
être disponibles, avec statut `ok` et utilisation strictement inférieure à
100 %. OpenRouter SHALL avoir un solde strictement positif. DeepSeek SHALL
être disponible avec au moins un solde utilisable strictement positif, sans
additionner des devises différentes.

#### Scenario: Limite de quota atteinte
- **WHEN** une utilisation OpenCode Go atteint 100 % ou qu'un solde requis n'est pas positif
- **THEN** la politique ne satisfait pas les conditions de quota de son fournisseur

### Requirement: Mesures concluantes du modèle sélectionné
Une politique SHALL être déclarée valide uniquement après une réponse complète
du modèle effectivement évalué, un comptage fiable, un TTFT strictement
inférieur à 90 secondes et un débit strictement supérieur à 15 tokens/seconde.
Une troncature ou une mesure absente SHALL NOT être traitée comme un succès
ou remplacée par une ancienne mesure.

#### Scenario: Repli après limitation fournisseur
- **WHEN** une limitation HTTP 429 conduit à choisir un autre modèle OpenCode Go
- **THEN** ce candidat ne peut être déclaré valide qu'après ses propres contrôles et mesures concluantes
- **AND** l'épuisement du dernier palier ne transforme pas le repli en réussite

#### Scenario: Mesure non concluante
- **WHEN** la réponse est tronquée, incomplète ou sans comptage exploitable
- **THEN** la politique reste invalide avec une cause qui distingue l'absence de mesure d'un seuil mesuré non satisfait

#### Scenario: TTFT sous la nouvelle limite
- **WHEN** les autres critères sont satisfaits et le TTFT visible vaut 70,4 secondes
- **THEN** le seuil de TTFT est satisfait

#### Scenario: Limite stricte de TTFT atteinte
- **WHEN** le TTFT visible atteint ou dépasse 90 secondes
- **THEN** la politique reste invalide malgré des quotas disponibles et un débit suffisant

### Requirement: Protocole des mesures traçable
Les mesures SHALL employer une horloge monotone et un flux réel. Le TTFT SHALL
porter sur le premier contenu visible. Le type de débit SHALL être conservé
dans le JSON : raisonnement et réponse pour OpenCode Go, réponse seule pour
OpenRouter et DeepSeek.

#### Scenario: Mesures provenant de fournisseurs différents
- **WHEN** des mesures OpenCode Go et OpenRouter sont restituées
- **THEN** le JSON conserve leur type de débit respectif sans les présenter comme une mesure identique

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL utiliser les paliers 1 024, 2 048, 4 096 et 8 192 tokens avec une
limite de 120 secondes par requête. En l'absence de réussite mémorisée pour
la même configuration, l'évaluation SHALL commencer à 1 024. Les reprises
SHALL contrôler les quotas avant toute nouvelle performance. La mémoire
SHALL enregistrer seulement une réussite complète et son identité de
configuration ; elle ne remplace jamais un nouveau contrôle réel.

#### Scenario: Réutilisation d'un palier réussi
- **WHEN** une réussite mémorisée correspond à la même identité de configuration
- **THEN** l'évaluation peut reprendre à ce palier avec de nouveaux contrôles
- **AND** un échec ne remplace pas la dernière réussite mémorisée

### Requirement: Publication traçable
PLLM SHALL publier `pllm-current.json` et `pllm-current.md` par remplacement
atomique de chaque fichier, sans secret. Le JSON SHALL tracer les horodatages,
critères, résultats, causes, sélection et type de débit.

#### Scenario: Résultats publiés
- **WHEN** l'évaluation se termine et la publication réussit
- **THEN** les deux fichiers décrivent la même évaluation sans valeur secrète

### Requirement: Invocation normale et mode active silencieux
L'invocation normale SHALL évaluer les quatre modes et restituer le tableau
et les quotas. Le mode
`active` SHALL s'arrêter à la première politique valide et publier sans sortie
console ni tableau dans la conversation.

#### Scenario: Mode active avec politiques non visitées
- **WHEN** le mode `active` sélectionne une politique et s'arrête
- **THEN** les politiques non visitées sont signalées par `evaluated_this_run=false`
- **AND** leurs résultats historiques ne sont pas présentés comme des contrôles actuels ni sélectionnés
- **AND** les fichiers sont publiés sans restitution console ou conversationnelle

### Requirement: Invocation forcée sans repli automatique
Une invocation forcée SHALL limiter l'évaluation à la politique et au rang
demandés, sans repli automatique vers un autre moteur.

#### Scenario: Échec d'une politique forcée
- **WHEN** la politique explicitement forcée échoue
- **THEN** PLLM ne teste pas un autre moteur pour remplacer celui demandé

### Requirement: Absence de sélection valide
L'absence de politique valide SHALL effacer l'ancienne sélection avec
`selected_mode=null` et `selection_status=no_valid_model`.

#### Scenario: Aucune politique valide
- **WHEN** aucune politique évaluée ne satisfait les critères
- **THEN** le résultat indique l'absence de politique valide sans conserver une ancienne sélection

### Requirement: Application OpenCode distincte et autorisée
Une simple évaluation PLLM SHALL NOT modifier la configuration OpenCode.
L'application à une session SHALL exiger une autorisation explicite et les
contrôles décrits par le skill, avec les secrets confinés au processus dédié.
Les réglages du développeur SHALL prévaloir sur les valeurs par défaut.

#### Scenario: Évaluation sans demande de bascule
- **WHEN** PLLM est invoquée uniquement pour évaluer ou publier une politique
- **THEN** elle ne modifie pas les agents ou l'authentification OpenCode

### Requirement: Continuité de session OpenCode et CAB
Une interdiction d'arrêter OpenCode SHALL préserver son processus et son
interface. Toute reprise sous CAB après une bascule autorisée SHALL
réconcilier la session et ses autorisations avant de poursuivre.

#### Scenario: Rechargement interne pendant une bascule autorisée
- **WHEN** le contexte est rechargé sans autorisation d'arrêter le processus
- **THEN** le processus et son interface sont préservés
- **AND** la session CAB est réconciliée avant la reprise des mandats
