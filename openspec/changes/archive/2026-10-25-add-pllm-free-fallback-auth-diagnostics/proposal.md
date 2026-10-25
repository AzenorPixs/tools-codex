# PLLM : repli gratuit et sélection par performances

## Why

Le rapport masque les erreurs d'authentification dans un état Invalide générique.
Les quotas épuisés bloquent aussi les modèles gratuits et le premier modèle
gratuit TFL peut être choisi alors que des quotas payants sont disponibles.
Le développeur a validé le périmètre SCM, le classement débit maximal puis
TTFT minimal et le cycle jusqu'à l'archivage. Sa dernière décision fixe
explicitement la release à 0.6.0.

## What Changes

- Contrôler les quotas avant génération et distinguer épuisement confirmé,
  authentification refusée, accès refusé et donnée indispensable indisponible.
- Modes 1/2 : candidats payants Go quand les quotas sont disponibles ; repli
  exclusivement gratuit Go puis OpenCode général après épuisement confirmé.
- Mode 3 : candidats payants OpenRouter avec crédit, gratuits après épuisement.
- Évaluer tous les candidats de la catégorie autorisée, retenir le meilleur
  débit valide puis le TTFT minimal et l'ordre TFL pour départager les égalités.
- Revenir aux candidats payants après rétablissement des quotas/crédits.
- Conserver les huit colonnes, avec diagnostic explicite dans État et mention
  du repli gratuit ; garder quotas réels et preuves de tous les candidats.
- Conserver priorités, active silencieux, forçages sans substitution, DeepSeek,
  secrets confinés, mémoire liée à la configuration et publication atomique.
- Synchroniser les distributions, documentation et cinq plugins en 0.6.0.

## Impact

Delta pllm-evaluation, ses deux scripts et SKILL.md, tests PLLM existants et
tests/test_pllm_free_fallback.py, wrapper PLLM, README, TECHNICAL, BUILD,
CHANGELOG, VERSION, pyproject.toml et cinq manifestes. TFL fournit déjà les
prix et routes : son moteur et son contrat restent inchangés. Aucun profil
installé, secret, service, historique Git ou archive précédente n'est modifié.

## Validation

Périmètre explicitement validé dans la conversation avant écriture. Delta
validé avant code/tests. Qualification déterministe hors réseau/trousseau sur
Python 3.13/3.14, syntaxe, parité, skills, versions, encodage, contrôle ciblé
des fichiers, OpenSpec ciblé puis standard/strict global, archive native unique
et rapport à six sections. Aucune génération fournisseur réelle ni installation
de profil n'est assimilée à ces preuves hors ligne.
