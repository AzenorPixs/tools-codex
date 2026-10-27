# Commandes Tools Codex en majuscules

## Why
Les commandes sources mêlent LM.md et TCU.md à quatre noms en minuscules.
CM et PROMPT ne déclarent pas de nom de skill affiché ; le manifeste prompt
affiche Prompt. Cette présentation doit être uniforme dans les deux distributions.

## What Changes
- Déclarer CM, PLLM, TFL, TCU, LM et PROMPT ; renommer les quatre commandes sources encore en minuscules et harmoniser leurs déclencheurs et libellés.
- Conserver les identifiants techniques cm, pllm, tfl, tcu, lm et prompt, les invocations $… et les anciens déclencheurs comme alias compatibles.
- Adapter TCU aux sources en majuscules et aux anciennes copies installées : nouveaux wrappers PROMPT.md, mises à jour à leur emplacement existant, reçus, sauvegardes et conflits préservés.
- Aligner VERSION, pyproject.toml, README et les six manifestes sur 0.7.13 ; actualiser uniquement la documentation concernée.

## Capabilities
### Modified Capabilities
- extension-distribution : commandes et affichage uniformes, distributions identiques.
- tools-codex-update : résolution des commandes canoniques et des anciennes copies.

## Impact
Les scripts métier, arguments, seuils, rapports, blacklist et planning restent
inchangés. Les installations utilisateur ne sont pas migrées par cette livraison
des sources. TCU ne renomme ni ne supprime les anciennes copies et ne suit pas
leurs liens. Aucun benchmark fournisseur ni installation système n'est requis.
Les chemins sources changent ; les liens externes dirigés directement vers
les anciens chemins doivent être réorientés explicitement lors d'une migration.

## Validation
Le périmètre couvre la spécification, l'implémentation, les tests hors ligne,
la revue documentaire, la synchronisation et l'archivage de ce seul change,
son rapport STATISTIQUES.md puis les étapes Git conditionnelles du prompt SCM.
