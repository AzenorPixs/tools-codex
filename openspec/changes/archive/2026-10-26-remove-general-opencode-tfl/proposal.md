# Retrait du catalogue général OpenCode de TFL

## Why
Le développeur demande de ne plus collecter, tester ni lister OpenCode général,
de conserver Go et OpenRouter, et de placer les familles Thinking Machines
actuelles dans la liste LM utilisateur. Le 26 octobre 2026, il valide le périmètre
SCM et ajoute explicitement la restriction des payants PLLM 1/2 à Go, même avec
un ancien catalogue contenant OpenCode général.

## What Changes
- TFL ne publie plus que opencode_go et openrouter ; aucun appel aux collecteurs généraux.
- PLLM 1/2 ne sélectionne que les payants Go et 3/4 les gratuits Go ; toute ancienne section opencode est ignorée, y compris pour les rangs forcés.
- Le planning valide les deux sections courantes sans changer horaires, quotas ni activation.
- LM reçoit inkling et inkling-small via ADD, sans modifier les défauts ni les autres entrées ; les variantes payantes et gratuites sont couvertes par l'identité canonique existante.
- La release commune passe de 0.7.11 à 0.7.12 ; distributions et documentation restent synchronisées.

## Impact
Les anciens rapports restent historiques. Les consommateurs doivent accepter
l'absence de opencode. Les six modes, comptes, secrets, seuils, HIGH/XHIGH,
protocole 8, prix, transports Go/OpenRouter et garde-fous restent conservés.
La qualification est hors ligne ; aucun benchmark fournisseur, installation de
profil, activation de timer ou effet Git ne fait partie de cette livraison.
L'ajout LM utilisateur est explicitement autorisé et retirable avec REMOVE.
Le défaut de restitution tarifaire OpenRouter constaté précédemment reste hors périmètre.

## Validation du périmètre
Périmètre autonome validé dans la conversation par le développeur, avec ajout
Go exclusif aux payants 1/2. Création, réalisation, synchronisation, archivage
et rapport STATISTIQUES.md du seul change sont inclus.
