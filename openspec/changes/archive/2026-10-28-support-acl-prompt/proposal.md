# PRM03 — Prise en charge d’ACL dans PROMPT

## Why
ACL.md est référencé dans l’index déclaré mais rejeté par la liste des codes directs. Le développeur a validé SCM-ACL-R1 le 28 octobre 2026, y compris spécification, implémentation, release 0.7.26, tests et archivage.

## What Changes
- Accepter ACL en majuscules via CLI et API et résoudre ACL.md depuis DEVOPS et son index.
- Préserver la lecture seule du résolveur, les erreurs sans repli, les alias et les RUN CISMP.
- Aligner les deux distributions, leur documentation et la release commune 0.7.26.

## Capabilities
### Modified Capabilities
- `prompt-dispatch`: ajouter ACL aux codes directs et qualifier son absence de RUN et d’effets.

## Impact
Deux résolveurs et deux SKILL.md, tests PROMPT et attente de release LM, documentation et métadonnées de release. Maintenance ciblée des registres existants avec entrée provisoire code non attribué. Aucun profil installé modifié. Aucun code de lot attribué. Aucun benchmark ni pilotage.
