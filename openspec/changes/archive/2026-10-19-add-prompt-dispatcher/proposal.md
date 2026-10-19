## Why

Une invocation courte doit charger le prompt du projet et poursuivre son
processus selon ses conditions terminales. Le référentiel unique reste celui
déclaré par DEVOPS.md ; aucun prompt n'est embarqué ou dupliqué dans le plugin.

## What Changes

- Ajouter le plugin prompt, son skill autonome et embarqué, un résolveur Python,
  la commande source /prompt et un lien local de découverte.
- Fournir LIST, les trente arguments d'exécution initialement demandés et les
  huit variantes 1CISMP1 à 1CISMP8 ajoutées au périmètre.
- Appliquer les alias validés GCM vers GSCM.md et GCMP vers GSCMP.md.
- Pour 1CISMPn : un change complet du RUN CISMPn, archivage, statistiques,
  puis arrêt de la session de codage, sans sélectionner un deuxième change.
- Porter la release commune de Tools Codex à 0.4.0 et actualiser le catalogue CM.

## Capabilities

### New Capabilities

- prompt-dispatch : résolution, liste et lancement d'un prompt du projet courant.

### Modified Capabilities

- extension-distribution : cinquième plugin, catalogue CM et parité des copies.

## Impact

Le périmètre autonome a été validé le 19 octobre 2026, puis complété par les
huit variantes à un change. Les sources de prompts externes, leurs index et
DEVOPS.md restent inchangés. Aucun RUN réel n'est lancé pendant les tests.
La publication et l'installation dans un profil Codex sont des opérations
distinctes, exclues de cette livraison locale. Aucun changement de CAB, des
liens existants ou du moteur de mise à jour TCU n'est nécessaire.
