# LLM05 — Converger les états courants TFL/PLLM vers Medium

## Why

La règle Medium a été introduite, mais des commandes sources et des clauses
contradictoires subsistent dans les spécifications courantes. Le filtrage des
historiques PLLM vérifie la capacité annoncée sans toujours vérifier l'effort
réellement utilisé par un ancien résultat. Les fichiers de résultats livrés
avec les skills contiennent encore des sélections antérieures incompatibles.

## What Changes

- Définir Medium comme unique effort courant demandé, mesuré, sélectionné et
  réutilisable par TFL et PLLM, sans repli ni exception de mode ou de transport.
- Refuser dans les sorties courantes tout candidat et résultat historique dont
  l'effort effectivement enregistré n'est pas Medium, même si ses métadonnées
  indiquent aussi que Medium est pris en charge.
- Vider les rapports et mémoires PLLM livrés avec les skills afin qu'aucun
  résultat antérieur ne soit présenté comme courant ou réutilisé.
- Corriger les commandes, skills, références et cadrages actifs, synchroniser
  les distributions autonomes et embarquées, puis aligner la release sur
  0.7.15.

## Préservé

Les archives OpenSpec, les entrées historiques du changelog, les preuves
historiques fournisseur et les tests négatifs restent intacts. Les métadonnées
source peuvent décrire plusieurs capacités ; seule une preuve Medium autorise
la génération et la sélection courantes.

## Impact

Les anciens résultats qui ne prouvent pas un test Medium deviennent invalides
et sont écartés des tableaux et sélections. Les installations utilisateur ne
sont pas modifiées par cette livraison locale ; leurs prochains lancements
appliqueront le filtre corrigé. Aucun benchmark fournisseur ni publication
de profil utilisateur n'est inclus.

## Validation du développeur

Périmètre SCM validé le 27 octobre 2026 : Medium seul dans les comportements
courants ; correction des commandes, skills, scripts, spécifications actives
et documentation ; invalidation des états PLLM incompatibles ; synchronisation
des distributions et release 0.7.15. Les traces historiques restent
préservées. La création et l'archivage de ce change ont été validés séparément.
