# Changelog

## Unreleased

- Gérer prompt comme composant TCU : installation ciblée du plugin absent, vérification du skill embarqué et déploiement du wrapper avec provenance dédiée ; conserver les autres briques absentes.
- Laisser les opérations indépendantes continuer malgré un conflit local, préserver les liens et rapporter les succès partiels avec un code non nul.
- Ajouter le wrapper `/cm` et son déclencheur dans le skill, en conservant une seule entrée prompt ; aligner les cinq plugins et la release commune sur 0.4.1.

- Ajouter le plugin et le skill prompt, leur résolveur et la commande source `/prompt`, avec référentiel exclusif DEVOPS.md du projet courant et LIST issu de son index.
- Ajouter les 38 actions en MAJUSCULE, les alias GCM/GCMP et les variantes 1CISMP1 à 1CISMP8 : un change complet, archivage, statistiques puis arrêt de la session de codage.
- Ajouter prompt au catalogue CM et aligner les cinq plugins, VERSION et la métadonnée Python sur 0.4.0.

- Accepter `/tcu check` et `$tcu check` sans tirets pour le contrôle sans écriture ; conserver `--check` compatible et refuser `check --apply` avant toute opération.

- Ajouter TCU (nom final de TFU), son plugin, son skill autonome et embarqué, son script et la commande source `/TCU` ; `$tcu` met à jour les briques présentes depuis marketplace et GitHub.
- Ajouter le contrôle `--check`, les sauvegardes, la provenance, l’adoption explicite et la gestion des conflits ; préserver les données générées et distinguer les succès partiels.
- Ajouter TCU au catalogue CM et aligner les quatre plugins, VERSION et la métadonnée Python sur 0.3.0.

- Ajouter le plugin `cm` à la marketplace Tools Codex en conservant le skill autonome et son lien local ; synchroniser les deux copies du catalogue.
- Documenter l'installation et la mise à jour du plugin CM ainsi que le risque de double entrée avec une copie autonome ; distinguer les contrôles locaux d'une installation réelle.
- Aligner la release commune, la métadonnée Python et les trois manifestes CM/PLLM/TFL sur 0.2.3.

- Remplacer `/cm` par le skill `$cm`, avec un catalogue français des invocations `$cm`, `$pllm` et `$tfl`, sans lancer les générateurs. Supprimer l'ancienne commande source.
- Exposer `skills/cm/` dans le projet par le lien relatif `.agents/skills/cm` et documenter l'installation autonome ; le contrôle local ne prouve pas une invocation dans une nouvelle session Codex.
- Aligner la release Tools Codex, les manifestes PLLM/TFL et la métadonnée Python sur 0.2.2.

- Déclarer le support Python 3.13/3.14 (`>=3.13,<3.15`) et aligner la métadonnée Python sur la release 0.2.1 de VERSION, sans packaging ou publication Python supplémentaire.

- Ajouter `--tfl-catalog CHEMIN` à PLLM en conservant le chemin voisin par défaut, et initialiser les quatre politiques lorsqu'aucun fichier courant n'existe ; préserver les fichiers corrompus.
- Recalculer les paliers après repli HTTP 429 et exiger les mesures du remplaçant avant toute sélection valide.
- Exclure les prix OpenRouter non finis et les débordements ; empêcher la publication d'un catalogue TFL non conforme au JSON strict.
- Qualifier ces comportements hors ligne dans les deux distributions ; l'installation réelle et les accès fournisseurs restent non vérifiés.

## 0.2.1 — 2026-10-10

- Porter le seuil strict de TTFT PLLM de 60 à 90 secondes, avec couleur et critères publiés cohérents.
- Aligner la release du projet et les manifestes PLLM/TFL sur 0.2.1.
