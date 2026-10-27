# Conception

## Résultat valide et erreur

Un résultat vide est distinct d'une erreur de collecte, d'authentification,
de taux BCE, de routage sûr ou de données indispensables. Seuls les arrêts
dus à l'absence de modèles retenus sont retirés. Les autres erreurs conservent
leur code non nul et la préservation des rapports précédents.

## Publication

Les trois sections gardent models, source_model_count, excluded_model_count
et excluded_models. Deux champs additifs indiquent selection_status
(available ou empty) et exclusion_summary (motif vers nombre de modèles).
Le rapport conserve les deux tableaux à huit colonnes, même sans ligne de
modèle, puis indique « Aucun modèle admissible » et la synthèse des motifs.
Le JSON conserve les motifs détaillés ; les modèles exclus d'effort restent
absents des tableaux et des essais gratuits. Le taux BCE daté est affiché
même si OpenRouter est vide. Les essais gratuits restent après les tableaux.

Une collecte valide entièrement vide publie des fichiers frais et retourne
zéro. Aucun ancien catalogue n'est utilisé pour remplir une section vide.
Chaque fichier reste remplacé atomiquement selon le mécanisme existant.

## Compatibilité et limites

Le schéma JSON reste additif. Les sélecteurs PLLM rendent une absence de
candidat explicite sans réintégrer de modèle exclu ou historique ; les modes
gratuits conservent leur recherche Go puis général. Le contrôle du planning exige toujours trois listes non vides
et reste inchangé : la disponibilité du rapport manuel ne prouve pas une
admission du catalogue par le planning. Les filtres HIGH/XHIGH et les seuils
de performance restent identiques.

## Validation et retour

Les tests hors ligne couvrent chaque section vide avant qualification,
l'absence de preuve HIGH/XHIGH, chaque section vidée par les essais gratuits,
les trois sections vides, les sources et exclusions courantes, les tableaux,
les consommateurs PLLM et les erreurs réelles. La parité des distributions,
la syntaxe, les versions et UTF-8/LF sont contrôlés avant archivage.
Aucune migration de données n'est nécessaire. Le retour à une distribution
antérieure rétablit le comportement bloquant ; aucun automatisme de retour
ni modification d'installation utilisateur n'est introduit.

## Preuves de validation locale

- Change validé en mode strict avant toute écriture de code ou de test.
- Tests ciblés Python 3.14.10 : 56 tests TFL et 17 tests du moteur gratuit
  réussis. Les tests existants d'arrêt sur sélection vide sont remplacés par
  des attentes de publication conformes au périmètre validé ; les tests
  d'échec sur les vraies erreurs restent conservés.
- État final : 305 tests réussis sous Python 3.14.10 (10,798 s), puis 305
  sous Python 3.13.5 (9,590 s), sans réseau ni trousseau réel.
- Les sept fichiers Python modifiés compilent sur les deux branches.
- VERSION, pyproject.toml, README et six manifestes alignés sur 0.7.10 ;
  générateur et SKILL.md TFL identiques entre distributions.

Le test de lecture PLLM a révélé une limite préexistante distincte : pour les
prix de fixture 0,0000001 et 0,0000002 USD/token, l'ancienne conversion
flottante TFL peut diverger des prix natifs exacts contrôlés par PLLM, qui
rejette alors le candidat comme contradictoire. Le moteur tarifaire est
inchangé ; le test de sections vides emploie 0,000000125 et 0,00000025,
exactement représentables après conversion, afin d'isoler son objet. Cette
limite reste signalée hors périmètre, sans prétendre qualifier tous les prix.
