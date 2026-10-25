# pllm-evaluation Specification

## Purpose

Définir l’évaluation des politiques PLLM, leurs quotas et mesures, leur publication et la séparation des applications OpenCode autorisées.

## Requirements

### Requirement: Résolution explicite du catalogue TFL
PLLM SHALL accepter `--tfl-catalog CHEMIN` pour les modes OpenCode Go,
OpenRouter et les replis. Sans cette option, le chemin SHALL rester
`../tfl/data/tfl.json` relatif au skill PLLM. Un catalogue absent ou invalide
SHALL produire un diagnostic explicite sans sélection inventée.

#### Scenario: Plugins installés séparément
- **WHEN** le catalogue est fourni explicitement depuis un autre emplacement
- **THEN** la résolution utilise ce fichier pour le rang initial et les replis
- **AND** aucune recherche dans les configurations privées n'est nécessaire

### Requirement: Initialisation sans historique
Si `data/pllm-current.json` manque, PLLM SHALL initialiser les quatre modes,
priorités et critères définis, sans sélection, quota ou mesure historique.
Un fichier existant valide SHALL être chargé ; un fichier corrompu SHALL
produire un diagnostic explicite et SHALL NOT être écrasé.

#### Scenario: Première évaluation
- **WHEN** aucun fichier courant n'existe
- **THEN** les quatre modes sont disponibles pour les contrôles réels habituels
- **AND** aucun résultat valide n'est créé par l'initialisation seule

#### Scenario: Historique illisible
- **WHEN** le fichier courant contient du JSON ou des politiques invalides
- **THEN** l'évaluation échoue avant publication et préserve ce fichier

### Requirement: Politiques et sélection explicites
PLLM SHALL évaluer quatre modes par priorité 1 à 4 : comptes OpenCode Go pour
les modes 1 et 2, OpenRouter pour le mode 3 et DeepSeek direct pour le mode 4.
Les modèles des modes 1 à 3 SHALL provenir du catalogue TFL avec identifiant,
fournisseur, route et date exacts. Le raisonnement par défaut SHALL être Low.
La sélection SHALL retenir la première politique valide évaluée pendant
l'invocation, après classement des candidats de ce mode.

#### Scenario: Sélection selon la priorité
- **WHEN** plusieurs politiques satisfont leurs critères
- **THEN** seule la première par priorité croissante est sélectionnée
- **AND** le débit d'une autre politique ne change pas cette priorité

### Requirement: Quotas avant performance
PLLM SHALL consulter les quotas ou soldes actuels avant chaque test. Un
contrôle absent, refusé ou incohérent SHALL arrêter l'évaluation avant
performance. Un épuisement confirmé SHALL autoriser uniquement le repli
gratuit spécifié, sans ouvrir l'accès aux modèles payants.

#### Scenario: Quota épuisé ou non disponible
- **WHEN** un quota ne peut pas être établi ou l'authentification est refusée
- **THEN** la politique reste invalide avec une cause explicite
- **AND** aucun test ni repli gratuit n'est lancé

#### Scenario: Épuisement confirmé
- **WHEN** les données actuelles établissent l'épuisement des ressources
- **THEN** seuls les candidats gratuits admissibles peuvent être testés
- **AND** les quotas réels restent conservés sans inventer de disponibilité

### Requirement: Conditions de quota propres aux fournisseurs
Go payant SHALL exiger trois périodes disponibles, statut ok et usage <100 %.
OpenRouter payant SHALL exiger un solde >0. Seul un épuisement confirmé MAY
permettre une réussite gratuite pour ces modes. DeepSeek SHALL être disponible
avec au moins un solde utilisable >0, sans addition de devises. Une donnée
manquante, un refus ou un statut inconnu SHALL NOT prouver un épuisement.

#### Scenario: Limite de quota atteinte
- **WHEN** une utilisation Go atteint 100 % ou que le solde OpenRouter n'est pas positif
- **THEN** les candidats payants ne sont pas testés
- **AND** le repli gratuit exige ses propres mesures concluantes

### Requirement: Mesures concluantes du modèle sélectionné
Une politique SHALL être valide uniquement après réponse complète, comptage
fiable, TTFT <90 s et débit >15 tokens/s du modèle effectivement retenu.
Une troncature, erreur ou mesure absente SHALL NOT devenir un succès ou être
remplacée par une ancienne mesure. Les candidats suivants de la catégorie
autorisée SHALL être évalués même après une réussite, hors invocation forcée.

#### Scenario: Candidat limité ou incomplet
- **WHEN** un candidat échoue après ses paliers ou reçoit une limitation fournisseur
- **THEN** seul un autre candidat de la catégorie autorisée peut le remplacer
- **AND** le remplaçant exige ses propres contrôles et mesures

#### Scenario: Limites strictes
- **WHEN** le TTFT atteint 90 s ou le débit atteint au plus 15 tokens/s
- **THEN** ce candidat est invalide même si ses ressources sont disponibles

#### Scenario: Repli après limitation fournisseur
- **WHEN** une limitation HTTP 429 conduit à choisir un autre modèle de la catégorie autorisée
- **THEN** ce candidat exige ses propres contrôles et mesures concluantes
- **AND** l'épuisement du dernier palier ne transforme pas le repli en réussite

#### Scenario: Mesure non concluante
- **WHEN** la réponse est tronquée, incomplète ou sans comptage exploitable
- **THEN** le candidat reste invalide avec une cause distinguant mesure absente et seuil non satisfait

#### Scenario: TTFT sous la nouvelle limite
- **WHEN** les autres critères sont satisfaits et le TTFT visible vaut 70,4 secondes
- **THEN** le seuil de TTFT est satisfait

#### Scenario: Limite stricte de TTFT atteinte
- **WHEN** le TTFT visible atteint ou dépasse 90 secondes
- **THEN** le candidat reste invalide malgré des ressources et un débit suffisants

### Requirement: Protocole des mesures traçable
Les mesures SHALL employer une horloge monotone et un flux réel ; le TTFT
SHALL porter sur le premier contenu visible. Le JSON SHALL conserver la
portée du débit : raisonnement et réponse pour Go et OpenCode général,
réponse seule pour OpenRouter et DeepSeek. Le classement interne SHALL
comparer uniquement des débits de même portée.

#### Scenario: Deux catalogues OpenCode
- **WHEN** les candidats gratuits Go et OpenCode général sont comparés
- **THEN** leurs débits utilisent la même portée raisonnement et réponse
- **AND** leurs fournisseurs, routes et comptages restent distincts

#### Scenario: Mesures provenant de fournisseurs différents
- **WHEN** des mesures OpenCode et OpenRouter sont restituées
- **THEN** le JSON conserve leur portée sans les présenter comme une mesure identique

### Requirement: Paliers et mémoire de performance bornés
PLLM SHALL utiliser les paliers 1024, 2048, 4096 et 8192 tokens, 120 s par
requête. Sans réussite mémorisée de même configuration, commencer à 1024.
Les reprises SHALL contrôler les quotas avant chaque requête. La mémoire
SHALL enregistrer uniquement des réussites complètes liées à la configuration,
sans remplacer un succès par un échec ni afficher un palier d'un autre modèle.

#### Scenario: Plusieurs candidats et retour à une configuration connue
- **WHEN** plusieurs configurations ont été évaluées avec succès
- **THEN** leurs paliers mémorisés sont distincts et réutilisables par configuration
- **AND** un candidat changé sans réussite correspondante repart à 1024

#### Scenario: Réutilisation d'un palier réussi
- **WHEN** une réussite mémorisée correspond à la même configuration
- **THEN** l'évaluation peut reprendre à ce palier avec de nouveaux contrôles
- **AND** un échec ne remplace pas la dernière réussite

#### Scenario: Configuration remplacée après HTTP 429
- **WHEN** un autre candidat autorisé remplace le modèle limité
- **THEN** ses paliers sont recalculés selon son identité
- **AND** sans réussite correspondante, il commence à 1024 tokens
- **AND** l'épuisement des candidats reste un échec sans sélection valide

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

### Requirement: Catégories payante et gratuite exclusives
Quand les ressources sont disponibles, les modes 1/2 SHALL examiner seulement
les payants TFL Go et le mode 3 seulement les payants TFL OpenRouter. Après
épuisement confirmé, les modes 1/2 SHALL examiner les gratuits TFL Go puis
OpenCode général, et le mode 3 les gratuits TFL OpenRouter.

#### Scenario: Retour au payant après repli général
- **WHEN** une invocation précédente a retenu un gratuit OpenCode général et que les quotas Go reviennent
- **THEN** le compte Go du même mode est contrôlé à nouveau
- **AND** seuls les candidats payants Go sont évalués pour ce mode

#### Scenario: Crédit épuisé et modèle payant au nom free
- **WHEN** le solde OpenRouter est nul et qu'un nom free porte un prix non nul
- **THEN** ce candidat est exclu du repli gratuit
- **AND** aucun candidat payant n'est appelé

### Requirement: Gratuité vérifiable et retour au payant
La gratuité SHALL être vérifiée par les prix publiés d'entrée et sortie nuls,
jamais par le nom. Les filtres TFL, les accès et Low SHALL être préservés.
Au rétablissement des ressources, la sélection SHALL revenir aux payants.
Un changement de catégorie SHALL écarter les gagnants de la précédente ;
les transitions SHALL être bornées.

#### Scenario: Quotas rétablis pendant les tests gratuits
- **WHEN** le contrôle actuel retrouve des ressources disponibles
- **THEN** seuls les candidats payants peuvent représenter la politique
- **AND** des oscillations répétées invalident l'évaluation sans boucle illimitée

### Requirement: Classement interne par performances
Hors forçage, PLLM SHALL tester tous les candidats admissibles de la catégorie
autorisée. Les réussites SHALL être classées par débit décroissant, TTFT
croissant puis ordre stable TFL, Go avant général pour le repli modes 1/2.
Le premier de ce classement SHALL représenter le mode. Le JSON SHALL tracer
tous les candidats et leurs tentatives ; active SHALL s'arrêter uniquement
après classement complet du premier mode valide.

#### Scenario: Un candidat plus rapide après la première réussite
- **WHEN** deux candidats valides ont des débits distincts
- **THEN** celui au débit maximal est retenu indépendamment de son rang tarifaire

#### Scenario: Départage à débit égal
- **WHEN** plusieurs candidats ont le même débit valide
- **THEN** le TTFT minimal puis l'ordre TFL les départagent

### Requirement: Diagnostic visible et sûr
La colonne État SHALL afficher le diagnostic d'authentification ou d'accès
refusé sur la ligne de politique concernée, sans colonne supplémentaire.
Les codes HTTP et SSE SHALL être distingués sans publier de corps brut,
secret ou compte. Un succès gratuit SHALL afficher Valide et repli gratuit ;
les quotas épuisés SHALL rester visibles et exacts. Le JSON SHALL garder
state Valide/Invalide, cause structurée, preuves et mesures null si absentes.

#### Scenario: Authentification refusée
- **WHEN** le contrôle ou un flux renvoie un refus d'authentification HTTP 401
- **THEN** la ligne affiche Invalide et Authentification refusée (HTTP 401)
- **AND** aucun ancien gagnant ni repli gratuit ne masque ce refus

#### Scenario: Réussite gratuite avec quota épuisé
- **WHEN** le meilleur candidat gratuit satisfait tous les critères
- **THEN** la ligne affiche Valide — repli gratuit et ses mesures actuelles
- **AND** le quota ou solde épuisé reste affiché sans être rendu disponible
