# Installation systématique des briques Tools Codex absentes

## Why
TCU conserve actuellement les composants absents, sauf PROMPT. Le développeur a validé le 28 octobre 2026 un mandat SCM pour installer systématiquement ces composants, conserver les mises à jour et incrémenter la release 0.7.23 en 0.7.24.

## What Changes
- Installer tous les plugins absents du catalogue officiel par le CLI Codex.
- Installer les skills autonomes absents dans chaque racine configurée et les commandes sources absentes dans chaque racine de commandes configurée.
- Conserver les noms historiques, liens, checkouts, données utilisateur, sauvegardes, reçus et conflits sans adoption forcée.
- Garder check sans écriture ; distinguer installation prévue et version effectivement appliquée.
- Préserver le bootstrap local du planning sans exécution de TFL/PLLM ; les paquets peuvent être installés par TCU avant le bootstrap.
- Aligner les deux distributions TCU, la commande, le catalogue CM, les cadrages et la release commune 0.7.24.

## Impact
Capacités : tools-codex-update, lm-blacklist. Distributions TCU et CM, tests TCU et attente de release du test LM, documentation, VERSION, pyproject.toml et six manifestes. La présence de plusieurs distributions peut afficher plusieurs entrées ; aucune installation existante ne sera supprimée ou désactivée.

## Autorisation
Périmètre présenté puis explicitement validé par le développeur (« Je valide »). Le cycle inclut validations, synchronisation, archivage, STATISTICS.md puis les opérations Git conditionnelles SCM. Les tests restent isolés ; aucune application au profil réel ni évaluation fournisseur n'est autorisée par la qualification.
