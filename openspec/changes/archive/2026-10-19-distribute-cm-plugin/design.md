## Context

La marketplace publie deux plugins au format `.codex-plugin/plugin.json`.
CM est conservé dans `skills/cm/SKILL.md`, exposé localement par
`.agents/skills/cm -> ../../skills/cm`. La release initiale est 0.2.2 et
aucun change actif n'existe au début de cette session.

## Goals / Non-Goals

Ajouter CM au catalogue comme plugin contenant le même skill, conserver la
distribution autonome et passer à 0.2.3. Préserver les syntaxes `$cm`, `$pllm`
et `$tfl`, le tableau français et l'absence d'exécution des générateurs lors
de la consultation. Aucun nouveau runtime, serveur MCP ou service externe.

## Decisions

- Utiliser le manifeste de compatibilité existant, avec `name: cm`, version
  0.2.3, auteur et URLs du projet, `skills: ./skills/` et interface CM.
- Ajouter une entrée locale `./plugins/cm`, catégorie Productivity, avec les
  politiques AVAILABLE et ON_INSTALL comme les entrées existantes. CM ne
  déclare aucune application, connexion ni authentification externe.
- Embarquer un fichier ordinaire dans `plugins/cm/skills/cm/SKILL.md` afin que
  le paquet copié soit autonome, sans lien vers l'extérieur du plugin.
- Garder `skills/cm/SKILL.md` comme source d'édition ; synchroniser sa copie
  embarquée après chaque modification autorisée et vérifier leur égalité.
- Préserver le lien de découverte local existant. Documenter qu'une copie
  autonome et un plugin simultanément chargés peuvent créer deux entrées CM ;
  ne supprimer ni désactiver automatiquement une distribution existante.
- Appliquer la release 0.2.3 à VERSION, pyproject.toml, README et aux trois
  manifestes. Les exigences de release-versioning restent inchangées.

## Risks / Trade-offs

Deux copies impliquent un contrôle de parité à chaque évolution. Une copie
régulière conserve la portabilité du plugin indépendamment du dépôt. La
double découverte reste un choix de déploiement documenté. Le contrôle local
du paquet et du manifeste ne démontre ni une publication GitHub, ni une
installation réelle, ni une invocation dans une nouvelle session Codex.

## Migration Plan

Valider ce change avant les écritures d'implémentation. Créer le plugin et
son entrée, synchroniser les skills, mettre à jour la release et les documents.
Contrôler les artefacts, les tests existants et OpenSpec, puis synchroniser et
archiver uniquement ce change. Produire ensuite STATISTIQUES.md dans l'archive.

Repli local : retirer le nouveau plugin et son entrée de marketplace, restaurer
la règle de maintenance autonome, les versions, les documents et les exigences
associés. Le lien autonome reste inchangé. Aucune migration de données.

## Validation

- Analyser le catalogue et les manifestes JSON : trois plugins et chemins
  relatifs valides ; vérifier les six supports de release à 0.2.3 et le TOML.
- Valider le format des deux skills CM et leur égalité octet pour octet.
- Copier le seul paquet CM dans un répertoire temporaire contrôlé sous tests,
  résoudre son manifeste et son skill sans source externe, puis nettoyer.
- Vérifier le lien local, les syntaxes du catalogue, UTF-8/LF et les empreintes
  des sources préservées sans inspection de l'état Git.
- Exécuter les 19 tests existants sur Python 3.13 et 3.14.
- Exécuter OpenSpec strict avant et après archivage, et contrôler la matrice
  documentaire et les six sections du rapport final.
- Distinguer ces preuves locales d'une installation réelle dans le profil
  Codex, exclue du périmètre et non exécutée.

## Preuves de validation du 19 octobre 2026

| Contrôle | État et résultat |
|---|---|
| OpenSpec ciblé avant implémentation | Exécuté et réussi : `openspec validate distribute-cm-plugin --strict`. |
| Format des skills | Exécuté et réussi sur les deux copies avec `validate_skill` du validateur quick_validate.py de skill-creator, appelé par Python stdin sans bytecode. |
| Catalogue et release | Exécuté et réussi : trois plugins locaux résolus, JSON/TOML analysés, six supports à 0.2.3, plage Python inchangée. |
| Paquet CM isolé | Exécuté et réussi : seul le paquet copié dans un chemin avec espaces ; manifeste et skill résolus dans la copie, deux fichiers réguliers, sans source externe ; temporaire nettoyé. |
| Skill autonome | Exécuté et réussi : égalité octet pour octet, lien local préservé, trois syntaxes conservées. |
| Tests Python système | Exécutés et réussis : `/usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v`, 19 tests. |
| Tests Python DevOps | Exécutés et réussis : `/home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v`, 19 tests. |
| Périmètre et encodage | Exécuté et réussi : 103 fichiers initiaux observés, 11 changements attendus et 92 fichiers préservés avant synchronisation ; 67 fichiers d'anciennes archives préservés ; UTF-8/LF sur 18 fichiers. |
| Versions seules | Exécuté et réussi par reconstruction des empreintes initiales : VERSION, pyproject.toml et manifestes PLLM/TFL ne changent que de release. |
| OpenSpec global avant archive | Exécuté et réussi : `openspec validate --all --strict`, sept éléments valides. |
| Compilation Python modifiée, build web et navigateurs | Non pertinents : aucun fichier Python modifié, aucune interface web. |
| Publication, installation réelle et invocation dans une nouvelle session | Non exécutées, effets externes exclus du périmètre local validé. |

Les commandes OpenSpec utilisent le chemin `/home/devops/.local/npm/bin/openspec`
déclaré dans DEVOPS.md, avec OPENSPEC_TELEMETRY=0 et DO_NOT_TRACK=1. Les
contrôles par stdin n'ajoutent pas de script permanent. Le CLI local confirme
la syntaxe d'installation via `codex plugin add --help` ; aucune installation
n'a été lancée. Aucune nouvelle dépendance n'est introduite.

## Matrice de cohérence documentaire

| Élément | État et preuve |
|---|---|
| Projet réel | Plugin CM à deux fichiers présent, entrée locale résolue, copie autonome et lien conservés ; six supports de release contrôlés. |
| AGENTS.md | Inchangé, empreinte conservée ; les sections 5–6, 8, 12 et 21 couvrent le périmètre et ses contrôles sans nouvelle règle. |
| PROJECT.md | Mis à jour : Organisation et Catalogue actuel présentent les trois plugins et les deux distributions CM. |
| TECHNICAL.md | Mis à jour : Arborescence, Structure des plugins, Commandes et skills autonomes, Validation précisent copie embarquée, parité et paquet isolé. |
| BUILD.md | Mis à jour : tableau des plugins, Skill catalogue cm et Mise à jour couvrent installation, rafraîchissement, choix de distribution et double entrée. |
| DEVOPS.md | Inchangé, empreinte conservée ; aucun nouveau prérequis, chemins des outils existants utilisés. |
| README.md | Mis à jour : release 0.2.3, plugin CM, source autonome, renvoi à BUILD et limite d'installation. |
| CHANGELOG.md | Mis à jour : trois nouvelles entrées Unreleased ; historique préservé. |
| openspec/specs/ | Extension-distribution synchronisée : deux exigences ajoutées et deux modifiées ; égalité des quatre exigences avec le delta archivé contrôlée. Release-versioning inchangée car ses invariants sont respectés. |

La cohérence locale est établie pour l'éligibilité à l'archivage. La publication
et l'installation réelle restent des étapes distinctes, sans être annoncées
réussies. Les scripts PLLM/TFL et les autres skills observés sont préservés.

## Clôture OpenSpec

`openspec archive distribute-cm-plugin --json --yes` a créé l'archive
`2026-10-19-distribute-cm-plugin` et synchronisé deux exigences ajoutées et deux
modifiées, sans suppression ni renommage. La confirmation d'archivage appartient
au périmètre autonome validé. Le contrôle global strict post-archive réussit
sur les six spécifications. Les onze tâches sont terminées ; aucun change actif
ne reste. L'audit final identifie douze fichiers initiaux modifiés et 91
préservés sur 103 observés, dont les 67 fichiers d'archives précédentes.

Le rapport STATISTIQUES.md est produit dans cette archive après l'opération,
puis contrôlé pour ses six sections, ses chemins, ses totaux et UTF-8/LF.
