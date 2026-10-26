# Planifier TFL puis PLLM dans la session utilisateur

## Why
Les installations actuelles ne créent aucun ordonnanceur. La mention PLLM
de quatre horaires dans le skill n'est pas une planification réelle. Le
développeur demande une installation idempotente pour 00 h et 12 h Paris,
uniquement si Codex est ouvert et si son quota restant est positif.

## What Changes
- Ajouter un timer systemd utilisateur, un runner stable et des hooks natifs
  SessionStart aux six plugins ; intégrer le bootstrap à TCU --apply.
- Détecter l'application ou le CLI interactif du même utilisateur, puis lire
  les quotas Codex en direct avant TFL et à nouveau avant PLLM normal.
- Ignorer les quotas épuisés ou non vérifiables, les échéances hors session,
  les composants manquants et les chevauchements ; aucun rattrapage.
- Résoudre les paquets installés sans figer une version de cache, partager
  une seule installation et préserver secrets et planifications étrangères.
- Qualifier les paquets isolés, leurs hooks et les profils temporaires,
  documenter et aligner la release locale sur 0.7.8, puis archiver.

## Capabilities
### New Capabilities
- `llm-refresh-scheduling`: installation et exécution conditionnelle TFL/PLLM.
### Modified Capabilities
- `tools-codex-update`: installation du planning et bilan sans exécution LLM.
- `extension-distribution`: hooks et modules autonomes/embarqués.
- `pllm-evaluation`: séquence planifiée avec catalogue frais explicite.

## Impact
Nouveau scripts/scheduler.py dans les six skills et leurs six copies plugin,
six hooks/hooks.json et manifestes ; updater TCU et copie ; skills TCU/TFL/PLLM
et copies ; tests d'ordonnancement, TCU, qualification et attentes de release.
PROJECT, TECHNICAL, BUILD, README, CHANGELOG, VERSION, pyproject.toml et OpenSpec.
AGENTS et DEVOPS restent applicables sans modification. Python standard et
systemd utilisateur existants ; aucune dépendance Python supplémentaire.

## Autorisation et limites
Périmètre autonome validé le 26 octobre 2026, avec condition complémentaire
explicite : ne lancer ni TFL ni PLLM lorsque le quota Codex restant vaut zéro.
Codex actif signifie application ou session CLI ouverte, même sans tâche en
cours. La livraison et ses tests restent locaux, sans publication Git,
installation réelle dans le profil ni génération fournisseur non demandée.
Les hooks restent soumis à la confiance native Codex, jamais auto-approuvée.
