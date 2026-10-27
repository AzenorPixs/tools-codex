# Design

## Context

Voir `proposal.md` pour le motif. `performance.py` est partagé à l'identique par les quatre distributions TFL/PLLM. Les rapports PLLM peuvent transporter des champs de provenance anciens à côté des candidats évalués dans l'invocation courante.

## Goals / Non-Goals

**Goals:**

- Empêcher qu'une provenance historique modifie l'admission Medium de la mesure courante.
- Conserver les décimales USD TFL dans les moyennes, le classement et le contrôle du plafond EUR.
- Garder les quatre modules partagés synchronisés et couvrir les deux régressions par des tests hors ligne.

**Non-Goals:**

- Changer les modèles, routes, seuils, paliers, contrôles de ressources ou règles de sélection.
- Lancer un nouveau benchmark fournisseur, installer la release dans le profil utilisateur ou modifier OpenCode.
- Incrémenter au-delà de 0.7.16, déjà présent dans les sources préparées pour cette correction.

## Decisions

1. `_recorded_effort_is_medium` ignore uniquement `user_override` et `performance_attempts`, qui sont des traces historiques de provenance. Il continue de vérifier les champs d'effort du candidat et de sa `performance_test` courante ; un effort courant autre que Medium reste exclu.
2. `native_openrouter_prices` vérifie que les prix décimaux canoniques et leurs projections flottantes sont finies, non négatives et proches avec `rel_tol=1e-12`, `abs_tol=0.0`. Il retourne ensuite les valeurs décimales canoniques. Le classement, les conversions et le plafond ne consomment donc jamais les projections flottantes.
3. Les quatre distributions conservent un contenu identique. Les tests de régression couvrent une représentation flottante compatible, un écart réel, l'historique XHigh et une tentative courante non Medium.
4. Les artefacts de release restent sur 0.7.16. L'archivage du change synchronisera ses deltas dans les specs principales ; aucune migration de rapports historiques n'est requise.

## Risks / Trade-offs

- [Une tolérance trop large pourrait masquer une différence de prix] → La tolérance est relative à 1e-12 sans tolérance absolue ; les calculs utilisent les décimales exactes et les tests rejettent un prix matériellement différent.
- [Ignorer les traces historiques pourrait sembler élargir l'admission] → Seuls les champs de provenance hérités sont ignorés ; la requête et les tentatives de performance courantes doivent explicitement rester Medium.

## Migration Plan

Aucune migration de données. Qualifier les sources et la version, archiver le change puis publier le rapport de statistiques requis. La copie personnelle installée n'est pas actualisée par la seule modification du dépôt.

## Open Questions

Aucune.
