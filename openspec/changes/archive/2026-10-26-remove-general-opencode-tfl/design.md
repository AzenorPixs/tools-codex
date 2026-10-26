# Conception

## Décisions
1. Retirer le catalogue général du parcours main TFL et du JSON ; préserver les helpers historiques pour ne pas refactorer les parseurs hors périmètre.
2. Construire les candidats PLLM 1 à 4 depuis la seule section opencode_go. Une section générale ancienne, valide ou malformée, ne devient jamais un repli.
3. Adapter toutes les copies identiques du scheduler aux deux listes non vides opencode_go/openrouter. Les conditions activité/quota/fraîcheur restent strictes.
4. Réutiliser LM ADD pour les deux familles Inkling actuelles ; aucun joker fournisseur ni nouvelle politique intégrée.
5. Conserver les versions Python 3.13/3.14 et la bibliothèque standard. Mettre à jour toutes les distributions et les six manifestes à 0.7.12.

## Unités et preuves
- U1 : TFL, PLLM et scheduler sont un lot indissociable de contrat producteur/consommateurs. Tests ciblés sans réseau ni secret, incluant les anciens catalogues pour 1/2 et 3/4.
- U2 : politique LM utilisateur indépendante ; ADD atomique/idempotent puis assertions sur les variantes, conservation des entrées initiales et absence d'effet de bord sur les anciens rapports.
- U3 : documentation, métadonnées de release, parités puis suite globale Python 3.13 et 3.14, compilation, UTF-8/LF et OpenSpec strict.
- U4 : synchronisation, archivage ciblé et rapport statistique à six sections.

## Repli et limites
Les sources restent examinables ; aucun commit ou reset n'est exécuté. Les
rapports et historiques utilisateur ne sont pas réécrits. Une entrée LM peut
être retirée explicitement par REMOVE. Les nouvelles versions de sources ne
mettent pas à jour les profils installés. Toute écriture inattendue concurrente
est signalée avant remplacement. DEVOPS.md est conservé.

## Revue documentaire
AGENTS.md et DEVOPS.md : inchangés, règles/environnement préservés.
PROJECT.md, TECHNICAL.md, BUILD.md, README.md, CHANGELOG.md et les instructions
CM/TFL/PLLM : ajustements nécessaires au retrait général et à la nouvelle release.
Spécifications : tfl-catalog, pllm-evaluation et llm-refresh-scheduling.
