# PLL03 — Séparer les politiques PLLM gratuites

## Why

Les gratuits Go et OpenCode général dépendent aujourd'hui de l'épuisement des
comptes des modes 1/2. Le développeur a validé le 25 octobre 2026 leur séparation
en deux politiques autonomes, avec des seuils plus exigeants et une release
0.7.1 (0.6.1 + 0.1.0).

## What Changes

- Les modes 1/2 MUST rester payants Go ; un quota épuisé les rend invalides et
  rouges, sans essai gratuit dans ces modes.
- Les nouveaux modes 3/4 MUST comparer les gratuits vérifiés Go puis OpenCode
  général avec les comptes des modes 1/2 respectivement, sans contrôle de quota
  ni de solde. Leur validité MUST exiger contexte ≥1M, réponse complète,
  TTFT <30 s et débit >20 tokens/s.
- L'ancien mode 3 MUST devenir mode 5 (OpenRouter) et l'ancien mode 4 MUST
  devenir mode 6 (DeepSeek), avec leurs contrôles et seuils existants.
- Les priorités MUST être 1 à 6 ; les forçages, l'historique, la mémoire et
  les rapports MUST distinguer les deux générations de politiques.
- Les sources autonomes et embarquées, la documentation et les cinq
  manifestes MUST être cohérents avec VERSION et pyproject.toml à 0.7.1.

## Capabilities

### Modified Capabilities
- `pllm-evaluation` : six politiques, séparation des gratuits et migration
  compatible des historiques à quatre politiques.

## Impact

Sources PLLM autonome/embarquée, wrapper PLLM, quatre suites PLLM existantes,
nouveaux tests des six modes, TECHNICAL, BUILD, README, CHANGELOG, VERSION,
pyproject.toml et cinq manifestes. TFL, les secrets et la configuration
OpenCode ne changent pas. Le cycle inclut synchronisation, archivage et rapport
STATISTIQUES.md ; il exclut Git, installation et appels fournisseurs réels.
