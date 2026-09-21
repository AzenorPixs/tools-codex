# TFL — Test Fournisseur LLM

## Rapport des LMM OpenCode Go les moins onéreux

Code couleur : 🟢 ≤ 0.20 $/M · 🟡 > 0.20 à 0.40 $/M · 🟠 > 0.40 à 0.50 $/M.

| Rang | Modèle / ID | Contexte | Sortie | Entrée $/M | Sortie $/M | Coût moyen $/M | Code couleur |
|---:|---|---:|---|---:|---:|:---:|:---:|
| 1 | muse-spark-1.3-contributor (muse-spark-1.3-contributor) | 1.05M | Texte | $0.1 | $0.2 | $0.15 | 🟢 |
| 2 | mimo-v2.5 (mimo-v2.5) | 1M | Texte | $0.14 | $0.28 | $0.21 | 🟡 |
| 3 | qwen3.8-flash (qwen3.8-flash) | 1M | Texte | $0.15 | $0.47 | $0.31 | 🟡 |
| 4 | glm-5.3-flash (glm-5.3-flash) | 1M | Texte | $0.15 | $0.5 | $0.325 | 🟡 |
| 5 | deepseek-v4-flash (deepseek-v4-flash) | 1M | Texte | $0.22 | $0.66 | $0.44 | 🟠 |
| 6 | deepseek-v4-flash-vision-exp (deepseek-v4-flash-vision-exp) | 1M | Texte | $0.22 | $0.66 | $0.44 | 🟠 |

Actualisé le 2026-09-14T08:15:03+02:00 avec la clé mode1; classement par coût moyen hors pointe croissant, après filtres contexte ≥ 1M et coût moyen ≤ 0.5 $/M.
Les tarifs et estimations sont des références OpenCode Go et peuvent évoluer. Les modèles exclus ne sont pas affichés dans le rapport Markdown; leurs motifs restent disponibles dans le catalogue JSON.

## Rapports des LMM OpenRouter les moins onéreux

Code couleur : 🟢 ≤ 0.20 $/M · 🟡 > 0.20 à 0.40 $/M · 🟠 > 0.40 à 0.50 $/M.

| Rang | Modèle / ID | Contexte | Sortie | Entrée $/M | Sortie $/M | Coût moyen $/M | Code couleur |
|---:|---|---:|---|---:|---:|:---:|:---:|
| 1 | Qwen: Qwen3.7 Flash (qwen/qwen3.7-flash) | 1M | Texte | $0.03 | $0.13 | $0.08 | 🟢 |
| 2 | DeepSeek: DeepSeek V4 Flash 0731 (deepseek/deepseek-v4-flash-0731) | 1.31M | Texte | $0.06 | $0.12 | $0.09 | 🟢 |
| 3 | DeepSeek: DeepSeek V4 Flash 0423 (deepseek/deepseek-v4-flash) | 1.05M | Texte | $0.0886 | $0.1772 | $0.1329 | 🟢 |

Actualisé le 2026-09-14T08:15:03+02:00; classement par coût moyen entrée/sortie croissant, après filtres contexte ≥ 1M et coût moyen ≤ 0.5 $/M.
Les modèles multimodaux en entrée sont conservés; les métadonnées et capacités OpenRouter restent disponibles dans le catalogue JSON TFL.
