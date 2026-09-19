---
name: tfl
description: Générer un rapport autonome et unifié des LLM OpenCode Go puis OpenRouter, avec filtres de contexte, coût, multimédia, blacklist et code couleur communs. Utiliser pour /tfl, TFL ou « Test Fournisseur LLM ».
---

# TFL — Test Fournisseur LLM

Produire un rapport unifié, en français, des modèles LLM retenus chez deux
fournisseurs. L’ordre est obligatoire :

1. OpenCode Go ;
2. OpenRouter.

TFL est autonome : il interroge directement les deux APIs, applique ses propres
règles et ne dépend pas des skills ou plugins TOCG/TLOLC.

## Exécution

L’exécution de TFL est obligatoirement effectuée hors sandbox, car le générateur
doit accéder aux APIs OpenCode Go et OpenRouter. Dans Codex, lancer la commande
avec une exécution autorisée hors sandbox (par exemple
`sandbox_permissions=require_escalated`). Cette règle s’applique aux invocations
directes, aux commandes `/tfl` et à tout plugin qui charge cette skill. Ne pas
relancer TFL dans la sandbox si l’autorisation hors sandbox est refusée : arrêter
et restituer clairement l’erreur.

Depuis le dossier de ce skill :

```bash
python3 scripts/test_fournisseur_llm.py
python3 scripts/test_fournisseur_llm.py mode1
python3 scripts/test_fournisseur_llm.py mode2
python3 scripts/test_fournisseur_llm.py --policy auto
```

Lorsqu’une demande `/TFL`, `/tfl` ou « Test Fournisseur LLM » est exécutée
depuis la console, la sortie non sensible de la commande doit toujours être
restituée dans le message final visible de l’interface Codex, et pas seulement
dans la sortie technique d’un outil ou dans un message de progression :
tableaux, date d’actualisation, chemins des fichiers et messages d’erreur
éventuels. Ne pas exécuter silencieusement la commande ni renvoyer uniquement
les liens vers les fichiers. Les clés et toute autre donnée sensible restent
exclues de la restitution.

`auto` essaie la clé OpenCode Go du mode 1 puis celle du mode 2 et n’utilise
qu’une seule clé pour la requête réussie. La clé OpenRouter est lue depuis
`OPENROUTER_API_KEY`, puis `OPENROUTER_KEY`. Aucune clé ne doit apparaître dans
la sortie, les fichiers ou les journaux.

La commande écrit atomiquement :

- `data/tfl.json`, catalogue unifié et audit détaillé ;
- `data/tfl.md`, rapport complet dans l’ordre OpenCode Go puis OpenRouter.

## Colonnes communes

Les deux tableaux utilisent exactement les mêmes colonnes : `Rang`, `Modèle /
ID`, `Contexte`, `Sortie`, `Entrée $/M`, `Sortie $/M`, `Coût moyen $/M` et `Code
couleur`. Les métadonnées propres à un fournisseur restent dans le JSON, mais
ne sont jamais ajoutées à un seul des tableaux.

Le coût moyen est `(prix d'entrée + prix de sortie) / 2`, en USD par million de
tokens, et le classement est croissant sur cette valeur.

Code couleur commun : 🟢 jusqu’à 0.20 $/M inclus, 🟡 au-delà de 0.20 jusqu’à
0.40 $/M inclus, 🟠 au-delà de 0.40 jusqu’à 0.50 $/M inclus, ⚪ coût non
vérifié, 🔴 au-delà du seuil.

## Règles OpenCode Go

- Source de disponibilité : `https://opencode.ai/zen/go/v1/models`.
- Source complémentaire de contexte : `https://models.dev/api.json`, fournisseur
  `opencode-go`, champ `limit.context`.
- Le contexte est strictement vérifié et doit être supérieur ou égal à 1M de
  tokens. Un contexte absent ou inférieur à 1M exclut le modèle.
- Le coût de référence hors pointe doit être vérifiable et sa moyenne doit être
  inférieure ou égale à 0.5 $/M. Les coûts inconnus ou supérieurs sont exclus.
- Les sorties audio, vidéo, speech et sound sont exclues. Une capacité
  multimodale uniquement en entrée reste admissible ; une sortie non fournie
  est affichée `Non vérifié` sans être inventée.
- `muse-spark-1.2-contributor` est une blacklist permanente et reste auditable
  dans `excluded_models`.
- Les tarifs pointe/hors pointe, estimations rolling/weekly/monthly, sources de
  contexte et motifs d’exclusion sont conservés dans le JSON, pas dans le
  tableau commun.
- La source tarifaire de référence est `https://opencode.ai/docs/go/`.

La clé est recherchée avec `service=pllm`, `policy=mode1|mode2`,
`provider=opencodego` et le compte associé, sans afficher sa valeur.

### Routage API par modèle

OpenCode Go ne fournit pas un protocole de génération uniforme. Pour chaque
modèle retenu, le script publie `api_endpoint`, `api_protocol` et
`endpoint_source=opencode-go-docs` dans le catalogue JSON ; les consommateurs
doivent utiliser ces champs et ne jamais déduire la route depuis le nom.

- `muse-spark-1.3-contributor`, `muse-spark-1.2-contributor`,
  `gpt-5.6-luna` et `grok-4.6` utilisent
  `https://opencode.ai/zen/go/v1/responses` (`responses`).
- Les familles MiniMax et Qwen prises en charge utilisent `/messages`
  (`messages`).
- Les autres modèles texte retenus utilisent `/chat/completions`
  (`chat_completions`).

Pour `responses`, le corps utilise `input`, `max_output_tokens`, `stream=true`,
`store=false` et `reasoning.effort=low`. Pour `chat_completions`, il utilise
`messages` et `max_tokens`. Toute requête OpenCode Go de complétion doit porter
`x-opencode-session`. Une route absente ou inconnue doit être signalée et ne
doit pas être remplacée silencieusement par une autre.

## Règles OpenRouter

- Source API : `https://openrouter.ai/api/v1/models`.
- La sélection reste volontairement figée sur les identifiants validés par le
  catalogue programmation économique :
  `qwen/qwen3.7-flash`, `deepseek/deepseek-v4-flash-0731` et
  `deepseek/deepseek-v4-flash`.
- Les modèles multimodaux en entrée sont conservés ; le tableau commun affiche
  uniquement la modalité de sortie. Les sorties non textuelles audio, vidéo,
  speech ou sound sont exclues.
- Le contexte doit être au moins de 1M et le coût moyen au plus de 0.5 $/M.
- `meta/muse-spark-1.2-contributor` est une blacklist permanente.
- Les modalités d’entrée/sortie, capacités (`tools`, `reasoning`, `JSON`),
  paramètres API et motifs d’exclusion restent dans la section OpenRouter du
  JSON.
- Si un identifiant figé est absent de l’API, TFL échoue explicitement et ne le
  remplace pas silencieusement.

## Robustesse et présentation

TFL exécute et affiche le tableau OpenCode Go avant celui d’OpenRouter. Une
erreur d’authentification, de réseau, de JSON ou de filtre fait échouer la
génération plutôt que de produire un classement partiel silencieux.

Le rapport commence par `# TFL — Test Fournisseur LLM`, puis affiche les titres
`Rapport des LMM OpenCode Go les moins onéreux` et `Rapports des LMM OpenRouter
les moins onéreux`. Il restitue la date de récupération, les filtres appliqués,
les chemins des fichiers et les exclusions dans le JSON.

TFL ne mesure ni la qualité de code, ni la latence, ni le débit. Les tarifs sont
des références fournisseur susceptibles d’évoluer. Le catalogue TFL est la
source à utiliser par `/pllm` pour son modèle OpenRouter économique, via
`~/.codex/skills/tfl/data/tfl.json`, section `openrouter.models`.
