# Changelog

## Unreleased

- Ajouter le catalogue général OpenCode à TFL par collecte publique indépendante de Go, avec tarifs Console et métadonnées `opencode` ; conserver contexte ≥ 1M, coût moyen maximal 0,50 USD/M, modalités, blacklist et exclusions motivées, y compris variantes gratuites 200K.
- Restituer Go, OpenCode général puis OpenRouter avec trois tableaux aux colonnes identiques ; ajouter la section JSON `opencode` sans changer les sections ni politiques PLLM existantes, et préserver les rapports si une collecte indispensable échoue.
- Aligner la release commune, pyproject.toml, README et les cinq plugins sur 0.5.6 ; synchroniser distributions, wrapper et descriptions CM/TFL, sans installation de profil ni publication distante.

- Collecter les modalités et le routage OpenCode Go depuis les déclarations API et models.dev, sans listes statiques de modèles ; conserver sources, dates, surcharges SDK/base API et informations inconnues explicites.
- Vérifier les contradictions de modalités, les contrats de transport génériques et les URL HTTPS d'origine OpenCode avant publication ; distinguer route documentée et génération testée, avec compatibilité des consommateurs PLLM inchangés.
- Qualifier les deux distributions TFL et aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.5.5, sans installation de profil, génération ni consultation des quotas.

- Sélectionner dynamiquement tous les modèles OpenRouter admissibles du catalogue API, sans liste d'identifiants, catégorie ni limite artificielle de nombre ; appliquer contexte ≥ 1M, moyenne de base ≤ 0,50 USD/M, modalités et blacklist, modèles gratuits vérifiés inclus.
- Supprimer l'échec lié à la disparition d'un ancien identifiant ; conserver les exclusions auditables, le tri, la provenance tarifaire, les variantes conditionnées par jours/horaires UTC et la préservation des rapports si aucun modèle n'est admissible.
- Qualifier cette sélection dans les deux distributions TFL et aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.5.3, sans modifier la précédente archive ni les installations utilisateur.

- Actualiser les tarifs OpenCode Go depuis sa documentation officielle à chaque exécution TFL, sans table statique ni repli historique ; vérifier unité, correspondances et doublons, ignorer les prix barrés et conserver les variantes dans le JSON.
- Tracer source et date tarifaires des deux fournisseurs ; conserver les prix de cache et les paliers OpenRouter sans changer son classement de base. Signaler les prix absents, préserver les rapports si la collecte échoue et laisser N/A les estimations Go non collectées.
- Qualifier les deux distributions TFL hors ligne et par une collecte réelle ; aligner VERSION, pyproject.toml, README et les cinq plugins sur 0.5.2. Les installations utilisateur ne sont pas modifiées par cette livraison locale.

- Uniformiser la première colonne de CM avec des références aux skills et leurs noms lisibles, dont TCU ; conserver les syntaxes dans Utilisation et déclarer le nom d'affichage TCU dans les deux distributions.
- Aligner les cinq plugins, VERSION et la métadonnée Python sur 0.4.2.

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
