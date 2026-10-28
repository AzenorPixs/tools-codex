# PRM02 — Lever la borne des RUN PROMPT et uniformiser leurs libellés

# Why
La borne de huit RUN empêche de lancer CISMP9 ou 1CISMP9 alors que le suffixe identifie seulement le RUN. Les bilans de briques doivent présenter le nom PROMPT uniformément.

# What Changes
- Accepter CISMPx et 1CISMPx pour tout entier décimal strictement positif sans zéro initial, sans borne supérieure applicative ni conversion en entier.
- Préserver exactement le RUN et le cycle à un seul change de 1CISMPx.
- Afficher PROMPT dans les présentations du plugin, du skill et de la commande, tout en préservant identifiants, chemins, alias et reçus.
- Livrer la release commune 0.7.22, qualifier les distributions, synchroniser et archiver ce change avec statistiques puis appliquer la clôture SCM.

# Impact
Résolveurs PROMPT, instructions PROMPT/CM/TCU, présentation TCU, tests, cadrages et documentation, VERSION, pyproject.toml et six manifestes. Aucun nouveau fournisseur, dépendance, migration de profil ou lancement de RUN réel.
