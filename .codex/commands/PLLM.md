---
description: Évaluer les sept politiques PLLM avec prix prioritaire des payants qualifiés et performances des gratuits
---

Utilise obligatoirement la skill `pllm` installée par Tools Codex pour `/PLLM`
(alias `/pllm`).

À chaque invocation, exécute réellement le script d’évaluation :

- sans argument : `python3 scripts/evaluate.py`
- avec l’argument `active` : `python3 scripts/evaluate.py active`

Transmettre les modes numériques de forçage documentés par le skill et
l'option `--tfl-catalog CHEMIN` au même script, sans modifier leur valeur.
Le chemin explicite s'applique aussi aux replis ; sans option, le chemin
voisin du skill reste utilisé.

Vérifier la date du catalogue réellement produit par TFL avant de choisir son
chemin. Une copie autonome récente et une copie de plugin ancienne peuvent
diverger malgré une même release. Transmettre explicitement la collecte connue,
sans recherche privée ni collecte TFL implicite. Le JSON trace catalog_source,
catalog_selection et les refus de ressources dans resource_control ; une absence
de gratuit concerne ce catalogue, et HTTP 401 au quota n'est pas un épuisement.

Exécute la commande depuis le répertoire du skill PLLM installé. Ne remplace pas cette exécution par une lecture des anciens fichiers `data/pllm-current.*`. Le script contrôle les ressources applicables avant les tests (aucun quota en 3/4/6), publie les résultats et ne doit jamais afficher de secret.

Modes 1/2 : payants Go seulement ; quota épuisé → rouge et invalide sans repli.
Modes 3/4 : gratuits vérifiés Go exclusivement avec les comptes de 1/2,
sans aucun appel de quota ou solde, contexte ≥1M, Medium, réponse complète, TTFT <30 s
et débit >20 tokens/s. Mode5 : payants OpenRouter, solde positif, contexte ≥1M, coût moyen ≤0,10 EUR/M, avec benchmark payant Medium, TTFT <90 s et débit >15 tokens/s. Mode6 : gratuits OpenRouter, contexte ≥1M, Medium et tests gratuits. Mode7 : DeepSeek direct et contrôles payants. Mode5 reste exclusivement payant ; un crédit épuisé le rend invalide sans repli gratuit. Les forçages OpenRouter payants restent 51–53 ; 61–63 ciblent les gratuits OpenRouter de 6, et 7 DeepSeek.
Tous les benchmarks demandent exclusivement Medium, y compris le mode5 payant OpenRouter.
Essayer les payants Go 1/2 par coût moyen croissant. Le mode5 sélectionne les payants OpenRouter admissibles au coût moyen ≤0,10 EUR/M et contexte ≥1M avec benchmark payant Medium et passage au suivant après échec non bloquant. Essayer les gratuits 3/4/6 dans l'ordre TFL de leur fournisseur. Retenir le premier succès aux
tests actuels et arrêter le parcours du mode ; après échec, essayer le suivant
admissible avec ses propres contrôles. Le contexte ≥1M est une capacité
d'entrée vérifiée, sans requête d'un million de tokens. Les paliers, seuils
payants/gratuits et les autres seuils restent inchangés.
Les priorités restent 1 à 7, l'authentification et les limites HTTP sont
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

Exiger Medium vérifiable pour les politiques benchmarkées et les candidats gratuits. Le mode5 payant OpenRouter exige aussi Medium, réponse complète, TTFT <90 s et débit >15 tokens/s, avec contrôle du solde avant chaque essai. Garder les motifs JSON.
OpenRouter applique la moyenne de base ≤0,10 EUR/M au dernier taux BCE
publié vérifié ; aucune conversion historique implicite.

Les preuves TFL et les niveaux reasoning_options publiés sont conservés.
Seule une capacité Medium vérifiée est admissible pour les benchmarks ; utiliser et tracer les
paramètres Medium propres au protocole publié. Le mode5 exige prix/contexte/solde, Medium et mesures concluantes ; un ancien succès sans benchmark ne suffit plus. Toute métadonnée de contexte inconnue impose
une analyse et une recherche du LLM selon le protocole de preuve du skill,
quel que soit le fournisseur. Le mode7 conserve sa preuve DeepSeek dans le
registre de référence du skill. Un alias Medium mappé vers un effort supérieur
reste invalide ; le diagnostic exact accompagne l'exclusion et aucun benchmark
n'est envoyé. Un contexte encore invérifiable après investigation exclut le
modèle. Respecter la restitution exacte du script.
LM est l'unique liste noire et toutes ses entrées sont retirables.

Les modes 1/2 sont exclusivement payants Go, 3/4 gratuits Go, 5 payants OpenRouter benchmarkés, 6 gratuits OpenRouter benchmarkés et 7 DeepSeek. Une ancienne section opencode ne fournit aucun candidat.
