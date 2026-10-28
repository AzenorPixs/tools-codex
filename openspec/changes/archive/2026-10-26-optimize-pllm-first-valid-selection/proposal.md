# PLL04 — Arrêter la sélection PLLM au premier candidat valide

## Why

PLLM compare actuellement tous les candidats admissibles, même après une
réussite. Cette comparaison prolonge l'évaluation alors que le développeur
demande le premier candidat conforme dans un ordre déterministe.

## What Changes

- Essayer les payants des modes 1/2/5 par coût moyen TFL croissant, avec ordre
  TFL stable à prix égal, et arrêter le mode au premier succès.
- Essayer les gratuits des modes 3/4 dans l'ordre TFL Go puis OpenCode général
  et arrêter le mode au premier succès.
- Réserver le mode5 aux payants OpenRouter : crédit épuisé, mode invalide sans
  repli gratuit. Retester les ressources à l'invocation suivante.
- Conserver les tests actuels, leurs seuils distincts, HIGH/XHIGH, paliers,
  transports, références de secrets, mémoire et publication.
- Après qualification du correctif, incrémenter les briques Tools Codex de
  0.7.4 à 0.7.5, sans publication distante ni installation utilisateur.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `pllm-evaluation`: sélection du premier succès et mode5 exclusivement payant.

## Impact

Scripts et instructions PLLM autonomes et embarqués, tests hors ligne,
commande source PLLM, README, TECHNICAL, BUILD, CHANGELOG et métadonnées de
release communes. Aucun changement de TFL, du moteur de mesures partagé, des
interfaces publiques, du schéma 2 ou de la configuration OpenCode. Les
forçages de rang gardent leur cible ; un gratuit OpenRouter forcé est désormais
incompatible avec le mode5. Le mode6 conserve son candidat unique.

L'ordre remplace le départage par performances entre candidats. Les résultats
déjà publiés restent datés ; ils ne sont pas réévalués pendant cette livraison
hors ligne. Le retour arrière consiste à restaurer les sources de la release
précédente, sans migration des données utilisateur.
