## RENAMED Requirements
- FROM: `### Requirement: Deux tableaux fournisseurs et catalogue général préservé`
- TO: `### Requirement: Deux tableaux fournisseurs sans catalogue général`


## MODIFIED Requirements

### Requirement: Collecte complète et ordre des fournisseurs
TFL SHALL collecter exclusivement OpenCode Go et OpenRouter, avec
models.dev comme complément de métadonnées OpenCode. Une erreur de collecte,
d'authentification ou de données indispensables SHALL faire échouer la
génération sans rapport partiel complet. La restitution SHALL présenter
OpenCode Go puis OpenRouter ; le JSON SHALL NOT contenir de section opencode.

#### Scenario: Collecte complète
- **WHEN** les deux collectes et leurs métadonnées indispensables réussissent
- **THEN** le rapport contient les deux tableaux Go puis OpenRouter et conserve seulement opencode_go et openrouter dans le JSON

#### Scenario: Échec d'un fournisseur
- **WHEN** une collecte indispensable échoue
- **THEN** TFL signale l'échec et ne déclare pas le catalogue actualisé

### Requirement: Seuils de sélection vérifiables
TFL SHALL retenir un contexte vérifiable ≥1M et un coût moyen entrée/sortie
≤0,50 USD/M hors pointe pour Go ; OpenRouter SHALL appliquer ≤0,20 EUR/M au taux BCE vérifié. Prix ou contextes inconnus SHALL être exclus.
Les gratuits vérifiés SHALL réussir une réponse complète en HIGH ou son repli
XHIGH autorisé, TTFT <30 s et débit >20 tokens/s avant inclusion dans models.
Leurs échecs SHALL rester dans excluded_models avec leurs preuves.

#### Scenario: Modèle hors seuils
- **WHEN** le contexte ou le coût d'un modèle examiné ne satisfait pas les seuils vérifiables
- **THEN** il est exclu avec son motif dans le catalogue JSON

#### Scenario: Gratuit échoué ou non mesurable
- **WHEN** le gratuit échoue sur un seuil, le raisonnement, l'accès, HTTP ou la mesure
- **THEN** il est exclu de models avec sa cause, ses tentatives et ses mesures disponibles

#### Scenario: Seuils gratuits stricts
- **WHEN** le TTFT atteint 30 s ou le débit atteint au plus 20 tokens/s
- **THEN** le gratuit est exclu même si ses prix et contexte sont admissibles

### Requirement: Modalités et liste noire LM explicites
Les sorties déclarées audio, vidéo, speech ou sound SHALL être exclues. Une
entrée multimodale reste admissible ; une sortie inconnue SHALL être signalée
comme non vérifiée. TFL SHALL appliquer exclusivement la liste noire partagée
LM aux deux catalogues, sans liste propre ni exclusion permanente intégrée.
muse-spark-1.2-contributor SHALL être géré comme une entrée LM ordinaire,
avec la même identité pour Go et OpenRouter.

#### Scenario: Retrait LM respecté dans les trois catalogues
- **WHEN** muse-spark-1.2-contributor est retiré de LM
- **THEN** aucune liste interne TFL ne l'exclut dans les deux catalogues
- **AND** les autres critères de contexte, coût, modalités et effort restent obligatoires

#### Scenario: Modèle hors critères
- **WHEN** un modèle examiné ne satisfait pas un critère de sélection vérifiable
- **THEN** il ne figure pas dans le tableau retenu
- **AND** son motif d'exclusion est conservé dans le catalogue JSON

### Requirement: Actualisation tarifaire sans repli historique
TFL SHALL collecter à chaque génération les tarifs Go
dans sa documentation officielle, et OpenRouter dans son
API modèles. TFL MUST NOT utiliser de table statique ou ancien catalogue
comme repli. Chaque catalogue SHALL exposer la source et la date de
récupération tarifaire dans le JSON.

#### Scenario: Nouveau modèle et nouveau prix
- **WHEN** un modèle disponible possède un tarif officiel exploitable ou son tarif change
- **THEN** la génération utilise ce tarif sans modification du code
- **AND** les filtres existants restent applicables

#### Scenario: Source tarifaire inexploitable
- **WHEN** une source indispensable est inaccessible, invalide ou de format non reconnu
- **THEN** TFL échoue explicitement avant publication
- **AND** les rapports précédents restent inchangés

### Requirement: Exclusion LM avant sélection et test
TFL SHALL charger la liste commune LM avant tout appel fournisseur et
l'appliquer à Go et OpenRouter avant tout classement et
test gratuit. Les modèles interdits SHALL être absents de models et
free_performance_results ; excluded_models SHALL conserver leur motif.
Le JSON SHALL tracer la liste appliquée sans données personnelles.
Les seuils, prix, transports et ordre SHALL rester inchangés. Les exclusions
par identifiant SHALL dépendre exclusivement de LM.

#### Scenario: Modèle interdit pourtant admissible
- **WHEN** mimo-v2.5 satisfait prix, contexte et modalités dans un catalogue
- **THEN** il est exclu avant tout test gratuit et absent des tableaux retenus
- **AND** son exclusion est auditée sans requête de génération

#### Scenario: Liste utilisateur modifiée
- **WHEN** LM ajoute un modèle avant la nouvelle invocation TFL
- **THEN** les deux catalogues appliquent la liste courante sans mise à jour du code

### Requirement: Catalogue OpenRouter avec préfixes marqués
TFL SHALL examiner les identifiants OpenRouter à préfixe `~` valide sans
échec de grammaire LM. Les exclusions LM SHALL précéder métadonnées, tri
et génération. Les autres filtres, seuils, identifiants publiés et règles
de publication atomique SHALL rester inchangés.

#### Scenario: Catalogue mélangeant identifiants ordinaires et marqués
- **WHEN** le catalogue contient un modèle marqué autorisé et un modèle marqué exclu
- **THEN** le premier est évalué selon les filtres habituels en conservant son identifiant fournisseur
- **AND** le second figure dans les exclusions sans génération ni examen de ses prix

#### Scenario: Collecte complète sans génération interdite
- **WHEN** les deux catalogues valides sont collectés avec ces identifiants OpenRouter
- **THEN** TFL peut publier les deux sections avec leurs filtres et exclusions inchangés
- **AND** les modèles interdits restent absents des listes retenues et des tests gratuits

### Requirement: Publication explicite des sélections vides
Chaque catalogue valide SHALL publier models éventuellement vide,
selection_status (available ou empty), exclusion_summary (motif vers nombre),
compteurs et exclusions détaillées. Un tableau vide SHALL afficher
« Aucun modèle admissible » et la synthèse, sans fausse ligne de modèle.
Deux sélections vides valides SHALL produire les fichiers frais et un code
zéro. Les erreurs réelles SHALL rester bloquantes ; le planning contrôle les deux sections courantes.

#### Scenario: Go vide et OpenRouter admissible
- **WHEN** les collectes sont valides, Go ne retient aucun modèle et OpenRouter en retient
- **THEN** les deux tableaux sont publiés dans l'ordre Go puis OpenRouter et le second contient ses modèles admissibles
- **AND** Go expose son état vide, sa synthèse et ses exclusions courantes

#### Scenario: Catalogue général vide
- **WHEN** TFL publie une nouvelle collecte
- **THEN** aucune section opencode ni donnée générale ne figure dans le JSON ou les essais
- **AND** Go et OpenRouter sont les deux seuls catalogues courants

#### Scenario: Section vidée par la qualification gratuite
- **WHEN** tous les modèles d'une section sont des gratuits échoués ou non mesurables
- **THEN** models est vide et les essais, leurs causes filtrées et les exclusions sont publiés
- **AND** les autres sections et leurs qualifications continuent

#### Scenario: Trois sélections vides
- **WHEN** les deux collectes sont valides mais aucun modèle ne reste après filtrage ou qualification
- **THEN** TFL publie les sections vides, les deux tableaux explicites, les exclusions et les essais effectués avec un code de sortie zéro

#### Scenario: Erreur réelle
- **WHEN** une source indispensable, une authentification, une conversion BCE ou une donnée de sécurité est invalide
- **THEN** TFL signale l'erreur, retourne un code non nul et préserve les rapports précédents

### Requirement: Investigation des preuves manquantes
Pour Go et OpenRouter, un contexte ou un effort invérifiable
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

### Requirement: Deux tableaux fournisseurs sans catalogue général
TFL SHALL afficher Go puis OpenRouter, puis les essais gratuits admissibles
à l'effort. Les tableaux SHALL garder huit colonnes, Go en USD/M et OpenRouter
en EUR/M avec taux daté, même vides. La collecte, les essais et le JSON SHALL exclure OpenCode général. Go SHALL garder le plafond 0,50 USD/M.
Une sélection vide après filtrage ou qualification SHALL NOT bloquer les
autres sections. Les filtres et validations indispensables SHALL rester inchangés.

#### Scenario: Publication à deux tableaux
- **WHEN** les deux collectes satisfont les critères de validité
- **THEN** le rapport affiche Go puis OpenRouter, aucun tableau général, et le JSON conserve les deux sections

#### Scenario: Aucune preuve d'effort dans une section
- **WHEN** tous ses candidats sont exclus faute de preuve HIGH/XHIGH
- **THEN** TFL publie la sélection vide et ses motifs sans réutiliser d'anciennes qualifications
- **AND** les exclus restent absents des tableaux et des essais gratuits


## ADDED Requirements

### Requirement: Retrait intégral du catalogue général
TFL SHALL NOT appeler les collecteurs de disponibilité, prix ou métadonnées
du catalogue général OpenCode, ni qualifier ou lister ses modèles. Seules les
métadonnées opencode-go de models.dev SHALL servir à Go. Les sections, ordres,
investigations et essais publiés SHALL concerner exclusivement Go/OpenRouter.

#### Scenario: Collecteurs généraux interdits
- **WHEN** les trois collecteurs généraux sont configurés pour échouer s'ils sont appelés
- **THEN** une collecte Go/OpenRouter valide réussit sans aucun appel général
- **AND** le JSON, le Markdown et stdout ne contiennent aucun modèle général


## REMOVED Requirements

### Requirement: Catalogue général OpenCode indépendant
**Reason**: Le catalogue général est retiré par décision explicite du développeur.
**Migration**: Les nouveaux catalogues ne publient que Go/OpenRouter ; les anciens rapports restent historiques.
