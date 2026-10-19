## Why

Les plugins Tools Codex et les copies autonomes ont des canaux de distribution
distincts. TCU fournit une commande de mise à jour vérifiable de ces briques.
Le nom final TCU remplace le nom initial TFU dans ce périmètre.

## What Changes

- Ajouter le plugin `tcu`, le skill autonome et embarqué, leur script Python
  et la commande source `.codex/commands/TCU.md` ; exposer `$tcu` localement.
- Mettre à jour les plugins installés via la marketplace officielle et les
  copies autonomes déjà présentes via un instantané GitHub identifié par SHA.
- Fournir contrôle sans écriture, sauvegardes, gestion des conflits et bilan.
- Conserver les données générées, les secrets et les configurations hors des
  fichiers sources remplacés. Ne pas modifier le checkout de développement.
- Ajouter TCU aux deux catalogues CM et porter la release commune à 0.3.0.

## Capabilities

### New Capabilities

- `tools-codex-update` : mise à jour contrôlée des briques installées.

### Modified Capabilities

- `extension-distribution` : distribution TCU, quatre entrées CM et parité.

## Impact

Le périmètre autonome de spécification, implémentation, tests, documentation,
synchronisation, archivage et rapport est validé le 19 octobre 2026. Les
tests utilisent des installations contrôlées, sans mise à jour du profil réel
ni publication distante. Les fichiers de cadrage, README, CHANGELOG, catalogue
et versions sont adaptés. Aucun commit, push, dépendance supplémentaire ou
pilotage CAB n'est impliqué. La référence `/cab update` inspire la séparation
préparation/application ; ses services ne sont pas utilisés.
