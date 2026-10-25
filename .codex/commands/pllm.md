---
description: Évaluer les six politiques PLLM avec gratuits autonomes et classement débit puis TTFT
---

Utilise obligatoirement la skill `pllm` installée par Tools Codex.

À chaque invocation, exécute réellement le script d’évaluation :

- sans argument : `python3 scripts/evaluate.py`
- avec l’argument `active` : `python3 scripts/evaluate.py active`

Transmettre les modes numériques de forçage documentés par le skill et
l'option `--tfl-catalog CHEMIN` au même script, sans modifier leur valeur.
Le chemin explicite s'applique aussi aux replis ; sans option, le chemin
voisin du skill reste utilisé.

Exécute la commande depuis le répertoire du skill PLLM installé. Ne remplace pas cette exécution par une lecture des anciens fichiers `data/pllm-current.*`. Le script contrôle les ressources applicables avant les tests (aucun quota en 3/4), publie les résultats et ne doit jamais afficher de secret.

Modes 1/2 : payants Go seulement ; quota épuisé → rouge et invalide sans repli.
Modes 3/4 : gratuits vérifiés Go puis OpenCode général avec les comptes de 1/2,
sans aucun appel de quota ou solde, contexte ≥1M, réponse complète, TTFT <30 s
et débit >20 tokens/s. Modes 5/6 : anciens OpenRouter/DeepSeek, contrôles et
seuils conservés (<90 s, >15 tokens/s comme 1/2). Seul mode5 conserve son repli
gratuit OpenRouter sur crédit épuisé. Les forçages OpenRouter 31–33 deviennent
51–53 ; 31–33 et 41–43 ciblent la liste gratuite admissible de 3/4.
Classer les réussites par débit maximal, TTFT minimal puis ordre TFL stable.
Les priorités restent 1 à 6, l'authentification et les limites HTTP sont
explicites, active reste silencieux. Les secrets gardent leurs références
historiques ; les anciens historiques sont adaptés sans sélection actuelle héritée.

Restitue exactement la sortie produite par le script, sans ajouter de titre, commentaire, légende ou conclusion. Si l’exécution échoue, indique l’erreur réelle et ne présente pas les fichiers comme actualisés.

Une bascule OpenCode explicitement demandée suit la procédure d’application
du skill, avec le modèle et le raisonnement imposés par le développeur. Une
interdiction de fermer ou redémarrer le processus ne prohibe ni le chargement
d’une clé fournisseur ni son stockage privé standard par OpenCode. Respecte
toute restriction distincte de stockage et conserve le secret hors des sorties,
journaux, arguments de commande et contexte des modèles. Un rechargement
interne du contexte préserve le processus et l’interface ; réconcilie MCP et
CAB avant la reprise.

Argument reçu : `$ARGUMENTS`
