# Corriger les requêtes Low et les diagnostics HTTP PLLM

## Why

Le diagnostic réel du mode 1 a établi deux causes : Beam Free Go refuse le
paramètre thinking, et les modèles gratuits du catalogue général renvoient
HTTP 429 avec Retry-After. PLLM perd ces détails puis rejoue quatre budgets.
Le développeur a validé ce périmètre SCM et la release 0.6.1, avec tests,
archivage et rapport de statistiques.

## What Changes

- Séparer les paramètres Low selon fournisseur et protocole ; ne plus envoyer
  thinking sur Chat Completions OpenCode, préserver DeepSeek et Messages.
- Extraire localement des diagnostics HTTP bornés et filtrés : statut, code
  connu, paramètre connu refusé et délai Retry-After, sans corps brut ni secret.
- Arrêter les paliers du candidat sur HTTP 400 ou 429, poursuivre les autres
  candidats autorisés sans changer de catégorie et publier la reprise indiquée.
- Préserver les reprises de performance, Low, quotas, classement, mémoire,
  priorités, forçages, active silencieux et publication atomique.
- Qualifier les deux distributions et aligner les cinq plugins en 0.6.1.

## Impact

Deux evaluate.py et SKILL.md PLLM ; nouvelle suite HTTP ciblée et adaptations
de fixtures nécessaires ; README, TECHNICAL, BUILD, CHANGELOG, VERSION,
pyproject.toml et cinq manifestes. Delta pllm-evaluation, synchronisation
native, archive unique et STATISTIQUES.md. Aucun TFL, profil installé,
stockage de clé, agent OpenCode, service ou état Git modifié.

## Validation

Validation explicite du périmètre et de 0.6.1 dans la conversation. Delta
strict avant code/tests ; tests déterministes sur Python 3.13/3.14, syntaxe,
imports, skills, parité, versions, encodage et contrôle ciblé du périmètre.
OpenSpec ciblé puis global standard/strict avant et après archivage. Les
preuves réelles préalables sont distinguées des suites hors ligne ; elles
ne remplacent jamais un nouveau contrôle de disponibilité.
