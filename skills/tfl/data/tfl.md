# TFL — Test Fournisseur LLM

## Rapport des LMM OpenCode Go les moins onéreux

Code couleur : 🟢 ≤ 0.20 $/M · 🟡 > 0.20 à 0.40 $/M · 🟠 > 0.40 à 0.50 $/M.

| Rang | Modèle / ID | Contexte | Sortie | Entrée $/M | Sortie $/M | Coût moyen $/M | Code couleur |
|---:|---|---:|---|---:|---:|:---:|:---:|
| 1 | beam-free (beam-free) | 1.05M | Texte | $0 | $0 | $0 | 🟢 |
| 2 | muse-spark-1.3-contributor (muse-spark-1.3-contributor) | 1.05M | Texte | $0.1 | $0.2 | $0.15 | 🟢 |
| 3 | mimo-v2.6-flash (mimo-v2.6-flash) | 1.05M | Texte | $0.14 | $0.28 | $0.21 | 🟡 |
| 4 | qwen3.8-flash (qwen3.8-flash) | 1M | Texte | $0.15 | $0.47 | $0.31 | 🟡 |
| 5 | glm-5.3-flash (glm-5.3-flash) | 1M | Texte | $0.15 | $0.5 | $0.325 | 🟡 |
| 6 | deepseek-v4.1-flash (deepseek-v4.1-flash) | 1M | Texte | $0.15 | $0.6 | $0.375 | 🟡 |
| 7 | minimax-m3.1-flash (minimax-m3.1-flash) | 1M | Texte | $0.15 | $0.6 | $0.375 | 🟡 |
| 8 | gpt-6-luna (gpt-6-luna) | 1.05M | Texte | $0.2 | $0.75 | $0.475 | 🟠 |

Actualisé le 2026-10-28T11:06:15+01:00 avec la clé mode1; classement par coût moyen hors pointe croissant, après filtres contexte ≥ 1M et coût moyen ≤ 0.5 $/M.
Les tarifs sont des références OpenCode Go et peuvent évoluer. Les modèles exclus ne sont pas affichés dans les tableaux fournisseurs; leurs motifs restent disponibles dans le catalogue JSON.
Tarifs collectés dans la documentation officielle; les variantes et la provenance restent dans le JSON. Pour plusieurs paliers de contexte, le coût moyen hors pointe maximal est retenu. Estimations de requêtes non collectées : N/A.
Modalités et routage collectés sans liste de modèles; les sources et dates restent dans le JSON. Les routes documentées ne constituent pas un test de génération.

## Rapports des LMM OpenRouter les moins onéreux

Code couleur : 🟢 coût moyen ≤ 0.20 €/M ; montants convertis au taux BCE publié.

| Rang | Modèle / ID | Contexte | Sortie | Entrée €/M | Sortie €/M | Coût moyen €/M | Code couleur |
|---:|---|---:|---|---:|---:|:---:|:---:|
| 1 | NVIDIA: Nemotron 3 Ultra (free) (nvidia/nemotron-3-ultra-550b-a55b:free) | 1M | Texte | €0 | €0 | €0 | 🟢 |
| 2 | NVIDIA: Nemotron 3.5 Super VL (free) (nvidia/nemotron-3.5-super-vl:free) | 1M | Texte | €0 | €0 | €0 | 🟢 |
| 3 | ScaleDown: Extract (scaledown/extract) | 1M | Texte | €0.0359 | €0 | €0.0179 | 🟢 |
| 4 | ScaleDown: Summarize (scaledown/summarize) | 1M | Texte | €0.0359 | €0 | €0.0179 | 🟢 |
| 5 | Z.ai: GLM Flash Latest (~z-ai/glm-flash-latest) | 1.05M | Texte | €0.0213 | €0.0935 | €0.0574 | 🟢 |
| 6 | Qwen: Qwen3.7 Flash (qwen/qwen3.7-flash) | 1M | Texte | €0.0269 | €0.1166 | €0.0717 | 🟢 |
| 7 | DeepSeek: DeepSeek V4.1 Flash (batch) (deepseek/deepseek-v4.1-flash:batch) | 1.05M | Texte | €0.0448 | €0.1345 | €0.0897 | 🟢 |
| 8 | DeepSeek: DeepSeek V4 Flash Latest (~deepseek/deepseek-v4-flash-latest) | 1.05M | Texte | €0.0426 | €0.1406 | €0.0916 | 🟢 |

Taux BCE du 2026-10-27 : 1 EUR = 1.1150 USD ; source : https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml.
Les modèles multimodaux en entrée sont conservés; les métadonnées et capacités OpenRouter restent disponibles dans le catalogue JSON TFL.
Sélection dynamique sur tout le catalogue API, sans liste prédéfinie; les modèles gratuits vérifiés sont admissibles et les exclusions restent auditables dans le JSON.

## Tests de performance des modèles gratuits

Critères : contexte ≥1M, gratuité vérifiée, paramètre Medium accepté par l’API, réponse complète, TTFT <30 s et débit >20 tokens/s. Aucun contrôle de quota.
Débit moyen sur la requête complète, attente et TTFT inclus.

| Fournisseur | Modèle / ID | TTFT (s) | Tokens/s | Raisonnement | État / cause |
|---|---|---:|---:|---|---|
| opencodego | beam-free | 2.1640 | 236.1950 | MEDIUM | 🟢 Valide — Tous les critères gratuits satisfaits |
| openrouter | nvidia/nemotron-3-ultra-550b-a55b:free | 1.0013 | 32.8240 | MEDIUM | 🟢 Valide — Tous les critères gratuits satisfaits |
| openrouter | nvidia/nemotron-3.5-lightning:free | 40.1858 | 5.4880 | MEDIUM | 🔴 Exclu — Seuil gratuit non satisfait : TTFT <30 s et débit >20 tokens/s requis |
| openrouter | nvidia/nemotron-3.5-super-vl:free | 4.2606 | 37.8880 | MEDIUM | 🟢 Valide — Tous les critères gratuits satisfaits |

Investigations du LLM requises : 1. Le rapport reste provisoire pour ces exclusions. Examiner model_investigations dans le JSON et les sources officielles ; compléter model-evidence.json avant restitution finale ou signaler le blocage.
