---
name: cgpt
description: Afficher les quotas Codex du compte connecté avec couleurs, réinitialisations et disponibilité des statistiques hebdomadaires. Utiliser pour /cgpt ou une demande explicite de tableau de quotas CGPT.
---

# CGPT — Quotas et statistiques Codex

À chaque invocation, appeler `mcp__codex_app__get_usage_limits` pour récupérer les quotas actuels. Ce sont les quotas partagés du compte, pas les seuls coûts de cette conversation. Ne jamais utiliser `consume_usage_reset`, acheter des crédits ou modifier les réglages.

Préférer `rateLimitsByLimitId` s’il est renseigné, sinon utiliser `rateLimits`. Parcourir chaque fenêtre primary et secondary présente ; utiliser `windowDurationMins` pour sa durée, jamais son nom pour supposer 5 heures ou une semaine. Une fenêtre absente n’est pas un quota à zéro. `usedPercent` est consommé ; restant = max(0, min(100, 100 - usedPercent)). Conserver les valeurs manquantes comme null.

Couleurs sur le restant : 🟢 >=75 %, 🟡 >=50 et <75 %, 🟠 >=25 et <50 %, 🔴 <25 %. Afficher la date de consultation et la réinitialisation convertie de `resetsAt` (secondes Unix) en Europe/Paris, avec date, heure et fuseau. Aucune couleur inventée si la valeur manque.

Transmettre à `python3 scripts/render.py` via stdin un JSON normalisé : `observed_at` (ISO 8601), `windows` (liste de `bucket`, `duration_minutes`, `used_percent`, `resets_at`). Ne transmettre ni identifiant de compte, ni crédits de réinitialisation individuels, ni secret. Le script publie `data/cgpt-current.json`, `data/cgpt-current.md` et conserve `data/quota-history.jsonl`. Les anciens points ne remplacent jamais la consultation en direct. En cas d’échec du tool, fournir `windows: []` et `error` avec une cause non sensible ; ne pas présenter un résultat ancien comme actuel.

Restituer uniquement les deux tableaux produits, sauf information imposée par une instruction supérieure : quotas actuels et statistiques effectivement disponibles.

Le tableau supplémentaire contient uniquement des statistiques disponibles : nombre de crédits de réinitialisation (`rateLimitResetCredits.availableCount`, sans identifiants), nombre de consultations locales sur les sept derniers jours, dates de la période observée et variation du quota en points de pourcentage lorsque les observations appartiennent à la même fenêtre de réinitialisation. Ajouter `reset_credits_available` au JSON normalisé lorsque fourni par le tool.

Supprimer le tableau de durées/tokens/raisonnement indisponibles. Ne jamais afficher une variation comme du temps de travail ou une consommation propre à cette tâche. Ne pas calculer de variation entre deux fenêtres de réinitialisation différentes. Zéro point de variation signifie uniquement que le compteur à la précision fournie n’a pas changé. Les quotas restent partagés entre toutes les tâches du compte.

L’historique ne constitue pas une télémétrie exhaustive ; ne pas attribuer les variations du compte à cette tâche ou à un niveau de raisonnement, ni sommer des pourcentages au travers de réinitialisations. Si une source de télémétrie détaillée est rendue disponible ultérieurement, vérifier son périmètre, la couverture des sept jours, l’absence de double comptage des compteurs cumulatifs et la définition des durées avant d’enrichir le second tableau.


## Vue `/cgpt 7u`

L’argument `7u` affiche uniquement le pourcentage **utilisé** du compteur Codex pour la fenêtre de 7 jours : par exemple `50 %`. Effectuer une nouvelle lecture de `get_usage_limits`, sans utiliser un ancien résultat et sans sélectionner le compteur Spark. Identifier précisément le bucket `limitId=codex` et la fenêtre `windowDurationMins=10080`, indépendamment de primary/secondary. Dans le JSON normalisé, utiliser `bucket=codex` pour ce compteur même si son `limitName` change.

Exécuter `python3 scripts/render.py 7u` avec le même JSON normalisé via stdin. La publication complète et l’historique sont conservés, mais la sortie de cette vue est seulement le pourcentage utilisé, sans tableaux ni commentaire supplémentaire (sauf instruction supérieure). Si ce quota est absent ou inconnu, afficher `Non disponible`, jamais zéro ni le quota Spark. Sans argument, conserver les deux tableaux habituels.
