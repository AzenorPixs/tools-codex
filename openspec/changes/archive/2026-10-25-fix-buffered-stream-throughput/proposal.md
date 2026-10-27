# Corriger le débit face aux flux reçus en rafale

## Why
La mesure mode5 du 25 octobre 2026, publiée à 13:18:19 Europe/Paris, utilise
715 tokens de sortie dont 462 de raisonnement, 1,7751 s de durée totale et
une fenêtre de contenu arrondie à 0,0001 s. La formule actuelle produit
2 147 441,04 tokens/s en extrapolant les fragments reçus sur cette fenêtre.
Le développeur a validé le 25 octobre 2026 la méthode sur la durée totale et
le périmètre SCM jusqu'à l'archive et STATISTIQUES.md, version 0.7.3.

## What Changes
- PLLM/TFL MUST calculer les tokens/s sur la durée totale non arrondie de la
  requête, TTFT et attente compris, sans plafond ni durée minimale arbitraire.
- Go/général MUST compter toute la sortie ; OpenRouter/DeepSeek MUST compter
  la réponse seule, raisonnement soustrait lorsque applicable.
- Une réponse complète en un bloc MUST être mesurable si durée et comptage
  sont fiables ; une durée invalide MUST produire une mesure indisponible.
- Le protocole et la mémoire MUST distinguer ce débit moyen de l'ancien débit
  entre fragments ; aucune ancienne réussite ne valide le nouveau protocole.
- Les seuils, HIGH/XHIGH, comptes, quotas et interfaces MUST être préservés.
- La release commune MUST passer de 0.7.2 à 0.7.3.

## Capabilities
### Modified Capabilities
- pllm-evaluation : mesure, traçabilité, mémoire et classement.
- tfl-catalog : qualification gratuite et traçabilité de la mesure.

## Impact
Quatre moteurs performance.py, scripts et skills PLLM/TFL dans les deux
distributions, tests, TECHNICAL, BUILD, README, CHANGELOG, VERSION,
pyproject.toml et cinq manifestes. Aucun appel fournisseur réel, installation,
activation, opération Git ou modification de secret. Le protocole change
le classement et peut rendre un candidat non admissible aux seuils conservés.
