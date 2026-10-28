# UPD02 — Gérer le composant PROMPT et les canaux indépendants dans TCU

## Why

Prompt est publié mais TCU ne l'installe pas lorsqu'il est absent. Un conflit
local bloque aussi les opérations indépendantes. CM contient déjà l'entrée
prompt ; son déclencheur /cm et son wrapper doivent être cohérents.

## What Changes

- Gérer le plugin prompt, son skill embarqué et le wrapper de commande comme
  un composant TCU ; installer uniquement ce plugin absent lors d'une application.
- Installer ou actualiser prompt.md avec provenance, sauvegarde et protection
  des liens ; conserver les autres briques absentes sans installation.
- Traiter les canaux indépendamment et rapporter les conflits préservés.
- Ajouter la commande source cm.md et reconnaître /cm sans dupliquer le catalogue.
- Porter la release commune des cinq plugins et du projet à 0.4.1.

## Capabilities

### Modified Capabilities

- tools-codex-update : composant prompt, installation et traitement indépendant.
- extension-distribution : wrapper CM et catalogue cohérent.

## Impact

Le périmètre a été explicitement validé avant écriture, y compris l'installation
future ciblée de prompt par TCU. La SCM livre les sources et les teste sur des
profils temporaires ; aucun profil réel, référentiel de prompts, lien existant,
service ou historique Git n'est modifié. Publication et installation réelles
restent des opérations distinctes.
