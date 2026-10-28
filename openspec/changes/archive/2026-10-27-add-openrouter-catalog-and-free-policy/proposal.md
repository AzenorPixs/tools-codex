# PLL06 — Étendre PLLM aux modèles OpenRouter payants et gratuits

## Why

Le mode OpenRouter précédent tentait des générations Medium et des mesures de
performance sur les modèles payants. Cela excluait des modèles payants qui ne
publient pas cette capacité, alors que la sélection demandée doit pouvoir
retenir tous les modèles satisfaisant le prix et le contexte fixés.

## What Changes

- Le mode 5 retient les payants OpenRouter de contexte ≥1M et de coût moyen
  de base ≤0,20 EUR/M, après contrôle de solde, sans génération, Medium ou
  benchmark.
- Le mode 6 accueille les gratuits OpenRouter de contexte ≥1M, avec Medium et
  les tests gratuits actuels.
- Le mode 7 reprend DeepSeek direct. TFL conserve les payants OpenRouter sans
  preuve Medium ; les historiques PLLM migrent au schéma 3.
- Les distributions et documentation sont alignées sur la release 0.7.17.

## Non-Goals

- Modifier le plafond de coût ou les seuils gratuits.
- Modifier les paramètres de confidentialité OpenRouter, installer les
  extensions dans un profil utilisateur ou publier à distance.
