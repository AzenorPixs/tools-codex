## Context

TFL publie déjà un classement tarifaire. PLLM vérifie les prix mais ne les
conserve pas dans ses candidats, puis choisit le débit maximal. Les tests
restent la barrière d'admissibilité ; le prix devient le premier critère de
classement pour les payants uniquement.

## Goals / Non-Goals

Objectif : garantir qu'un payant plus rapide mais plus cher ne remplace jamais
un payant moins cher valide dans la même politique. Conserver les performances
pour les gratuits, les six priorités et toutes les règles d'accès.

Hors périmètre : modifier TFL, les seuils, les transports, le raisonnement,
les secrets, les agents OpenCode, les installations ou la release distante.

## Decisions

1. Conserver la moyenne des prix d'entrée/sortie TFL vérifiés dans
   `average_price_usd_per_million_tokens`, avec les prix et la provenance dans
   `model_source`. Go utilise sa référence hors pointe ; OpenRouter ses prix
   de base. Calcul décimal à partir des valeurs validées pour éviter qu'une
   égalité tarifaire soit rompue par l'addition binaire de flottants.
2. Modes 1/2 et catégorie payante de 5 : coût moyen croissant, débit
   décroissant, TTFT croissant et ordre stable du catalogue. Tous les
   candidats admissibles restent évalués, hors forçage.
3. Modes 3/4 et repli gratuit de 5 : débit décroissant, TTFT croissant et
   ordre stable. Mode6 garde son candidat DeepSeek direct unique, sans prix
   inventé. Les prix inconnus/non finis sont toujours exclus par le filtre.
4. Garder le schéma JSON 2 et les huit colonnes du rapport. Les champs de
   prix sont additifs et retirés lors de la réinitialisation d'une politique
   pour ne pas hériter d'un prix périmé. Aucune mémoire de débit n'est migrée.

## Risks / Trade-offs

Un gagnant payant peut être plus lent que précédemment tout en satisfaisant
les seuils obligatoires : c'est le comportement demandé. Les tarifs restent
ceux du catalogue TFL daté. Un prix égal conserve le départage existant ; la
réussite sur un test borné ne constitue pas une mesure de qualité du code.

## Validation et retour

Tests hors ligne sur les deux distributions : moins cher mais plus lent,
moins cher invalide, prix égaux, gratuits, ordre stable, forçages et active.
Exécuter la suite applicable sur Python 3.13 et 3.14, la syntaxe, la parité et
OpenSpec strict. Rejouer ensuite les six politiques avec le catalogue TFL
actuel et les accès autorisés, sans utiliser une mesure historique comme
résultat courant. Le retour consiste à restaurer le classement antérieur dans
les sources ; aucun stockage utilisateur ni schéma n'est détruit.

## Preuves locales et cohérence documentaire

Avant évaluation réelle : 230 tests réussis sous Python 3.14.10 et 230 sous
Python 3.13.5. Huit nouveaux tests, avec sous-cas sur les deux distributions,
couvrent le prix prioritaire des payants, les seuils, les égalités décimales,
les gratuits et le repli de 5, les prix absents, active, le forçage et le prix
périmé. La fixture de test_pllm_ttft.py reçoit les champs de prix et catégorie
désormais requis par le contrat des candidats ; ses assertions de seuils sont
conservées. L'essai complet initial échouait sur cette fixture, puis passe
après adaptation. Aucun test n'est désactivé ni affaibli.

Les quatre fichiers Python touchés sont compilés sous les deux branches dans
des temporaires sous tests, nettoyés à la sortie. Les deux scripts et les deux
SKILL.md sont identiques octet pour octet. Seize fichiers source/change sont
contrôlés UTF-8/LF sans BOM avant synchronisation de la spec et archivage.
OpenSpec ciblé strict puis global standard et strict réussissent ; les deux
globaux passent 9/9 avant archivage. Le premier contrôle ciblé a signalé une
exigence trop longue ; elle a été scindée avant toute écriture de code.

| Document | État et justification |
|---|---|
| AGENTS.md | Inchangé ; règles de sécurité, périmètre et archivage appliquées. |
| PROJECT.md | Inchangé ; catalogue, organisation et rôles des extensions préservés. |
| TECHNICAL.md | Mis à jour ; coût, classement par catégorie et nouvelle suite de tests. |
| BUILD.md | Mis à jour ; sélection des payants qualifiés et limites de distribution. |
| DEVOPS.md | Inchangé ; interpréteurs et CLI OpenSpec déclarés utilisés. |
| README.md | Mis à jour ; tests d'admissibilité puis prix des payants, performances gratuites. |
| CHANGELOG.md | Mis à jour dans Unreleased, avec la release locale 0.7.4 explicitement demandée. |
| openspec/specs/pllm-evaluation/spec.md | Synchronisée par l'archive native unique : quatre exigences ajoutées, l'ancienne règle retirée. |

Le développeur a étendu le périmètre à l'incrément de release : VERSION,
pyproject.toml, README, BUILD et les cinq manifestes passent de 0.7.3 à 0.7.4,
conformément à release-versioning. Aucune installation utilisateur ni
publication distante n'est incluse. Le comportement TFL reste inchangé.
L'évaluation réelle demandée utilise le script corrigé de skills/pllm et le
catalogue /home/ade/.codex/skills/tfl/data/tfl.json ; ses données sont générées
sous skills/pllm/data et ne sont pas des sources à publier.

## Résultat de l'évaluation réelle demandée

Exécution complète réussie, code 0 ; publication le 26 octobre 2026 à
00:44:49+01:00. Cinquante-deux candidats examinés, vingt-sept valides et
vingt-cinq invalides ; soixante-dix-neuf tentatives de benchmark tracées,
vingt-sept complètes et cinquante-deux en échec. Ces tentatives ne comptent
pas les contrôles de ressources et métadonnées, dont le total n'est pas
instrumenté. Les six politiques sont marquées évaluées dans cette invocation.

Mode1 est invalide, quota hebdomadaire épuisé, sans génération. Mode2 choisit
muse-spark-1.3-contributor à 0,15 USD/M, TTFT 5,533 s et débit 140,540 tokens/s.
MiMo-v2.6-flash est valide et plus rapide (0,6664 s, 191,437 tokens/s) mais
coûte 0,21 USD/M : il ne peut donc pas passer devant Muse. Modes 3/4 gardent
beam-free avec leurs mesures actuelles et sans contrôle de quota. Mode5
choisit ~z-ai/glm-flash-latest, le moins cher de ses seize payants qualifiés.
Mode6 garde DeepSeek direct, valide sans prix inventé.

Le contrôle indépendant des preuves JSON recalcule chaque gagnant avec la
règle propre à sa catégorie, vérifie les priorités 1 à 6, les champs de quota
non applicables en 3/4 et les huit colonnes/six lignes Markdown. Aucun champ
de compte, clé, corps brut ou identifiant de session interdit n'est publié.
Les fichiers installés dans le profil Codex ne sont pas modifiés par cette
évaluation des sources ; une livraison/installation ultérieure reste distincte.

## Archivage

Archive native unique réussie sous 2026-10-26-prioritize-paid-model-price,
specsUpdated=true, quatre exigences ajoutées et une retirée. Après archive,
les validations OpenSpec globale standard et stricte passent chacune 8/8.
Les quinze tâches sont clôturées ; le rapport STATISTIQUES.md conserve le
bilan documentaire, les fichiers, les validations et leurs limites.
