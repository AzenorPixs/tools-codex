---
description: Évaluer les six politiques PLLM avec prix prioritaire des payants qualifiés et performances des gratuits
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
seuils payants conservés (<90 s, >15 tokens/s comme 1/2), gratuits à <30 s et >20 tokens/s. Mode5 reste exclusivement payant ; un crédit épuisé le rend invalide sans repli gratuit. Les forçages OpenRouter 31–33 deviennent
51–53 ; 31–33 et 41–43 ciblent la liste gratuite admissible de 3/4.
Tous les tests demandent HIGH, puis XHIGH uniquement si HIGH est indisponible
et XHIGH pris en charge ; aucun repli inférieur.
Essayer les payants 1/2/5 par coût moyen TFL croissant (hors pointe Go,
prix de base OpenRouter), avec ordre TFL stable à prix égal. Essayer les
gratuits 3/4 dans l'ordre TFL Go puis général. Retenir le premier succès aux
tests actuels et arrêter le parcours du mode ; après échec, essayer le suivant
admissible avec ses propres contrôles. Le contexte ≥1M est une capacité
d'entrée vérifiée, sans requête d'un million de tokens. Les paliers, seuils
payants/gratuits et HIGH/XHIGH restent inchangés.
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

Exclure gratuits et payants sans preuve publiée HIGH/XHIGH avant test et
affichage, y compris dans les essais gratuits ; garder les motifs JSON.
OpenRouter applique la moyenne de base ≤0,20 EUR/M au dernier taux BCE
publié vérifié ; aucune conversion historique implicite.
