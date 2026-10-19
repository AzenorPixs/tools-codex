---
description: Évaluer en temps réel les politiques PLLM et sélectionner le premier modèle valide
---

Utilise obligatoirement la skill `pllm` installée par Tools Codex.

À chaque invocation, exécute réellement le script d’évaluation :

- sans argument : `python3 scripts/evaluate.py`
- avec l’argument `active` : `python3 scripts/evaluate.py active`

Transmettre les modes numériques de forçage documentés par le skill et
l'option `--tfl-catalog CHEMIN` au même script, sans modifier leur valeur.
Le chemin explicite s'applique aussi aux replis ; sans option, le chemin
voisin du skill reste utilisé.

Exécute la commande depuis le répertoire du skill PLLM installé. Ne remplace pas cette exécution par une lecture des anciens fichiers `data/pllm-current.*`. Le script contrôle les quotas avant les tests, publie les résultats et ne doit jamais afficher de secret.

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
