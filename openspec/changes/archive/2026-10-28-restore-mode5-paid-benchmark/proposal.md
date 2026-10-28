# PLL10 — Rétablir le benchmark des payants OpenRouter en mode5

## Pourquoi
Le mode5 actuel valide un candidat sur le prix, le contexte et le solde sans vérifier sa génération. Le développeur a validé le retour du benchmark payant habituel et du passage au suivant après échec.

## Changement
- Demander Medium et exiger réponse complète, TTFT <90 s et débit réponse seule >15 tokens/s au protocole 8.
- Parcourir les payants par prix courant croissant, paliers 1024/2048/4096/8192, 120 s par requête, arrêt au premier succès.
- Recontrôler le solde avant chaque génération ; conserver plafond 0,10 EUR/M, contexte >=1M, LM, forçages et arrêt des erreurs bloquantes.
- Invalider les historiques sans preuve Medium et sans benchmark ; publier les mesures et mémoriser les réussites réelles.
- Conserver TFL comme catalogue tarifaire des payants sans benchmark.
- Aligner la release sur 0.7.25 et les distributions autonome et embarquée.

## Périmètre
Deux distributions PLLM, commande source PLLM, tests concernés, README, TECHNICAL, BUILD, CHANGELOG, VERSION, pyproject et six manifestes. Aucun profil installé, secret, configuration OpenCode ou timer modifié. Tests hors ligne ; aucune nouvelle qualification fournisseur implicite.

## Autorisation
Périmètre autonome explicitement validé par le développeur le 28 octobre 2026, incluant tests, archivage et statistiques ; clôture Git conditionnelle selon SCM.
