# LLM06 — Basculer TFL et PLLM vers le raisonnement Medium

## Why

TFL et PLLM demandent actuellement HIGH, puis peuvent utiliser XHIGH comme
repli. Leur admission, les transports API, les rapports et la documentation
répercutent ce choix. Le contrat évolue pour demander et vérifier Medium dans
les deux composants.

## What Changes

- Exiger une preuve publiée de prise en charge de Medium avant classement,
  génération, sélection ou affichage d'un candidat TFL/PLLM.
- Envoyer `medium` par le paramètre d'effort propre à chaque protocole. Ne plus
  tenter HIGH ou XHIGH en repli après un refus.
- Exclure les candidats qui ne déclarent que HIGH/XHIGH ; préserver les
  rapports d'exclusion et les preuves dans les audits JSON.
- Conserver les résultats et mémoires HIGH/XHIGH comme données historiques,
  sans les réutiliser pour une configuration Medium.
- Synchroniser les distributions autonomes et embarquées, les tests et les
  documents de référence.
- Incrémenter la release commune de 0.7.13 à 0.7.14.

## Capacités modifiées

- `tfl-catalog` : preuve et exécution Medium au lieu de HIGH/XHIGH.
- `pllm-evaluation` : sélection et tests Medium sans repli vers HIGH/XHIGH.

## Impact

Des modèles actuellement admissibles uniquement en HIGH ou XHIGH sortiront
des catalogues et sélections. Les mesures historiques restent inchangées ;
les prochaines exécutions autorisées produiront de nouvelles mesures Medium.
La qualification fournisseur réelle et les profils installés ne font pas
partie de cette livraison locale.

## Validation du développeur

Périmètre SCM validé le 27 octobre 2026 : changement de TFL et PLLM vers
Medium, mise à jour des spécifications, sources, distributions, tests,
documentation et incrément de version.
