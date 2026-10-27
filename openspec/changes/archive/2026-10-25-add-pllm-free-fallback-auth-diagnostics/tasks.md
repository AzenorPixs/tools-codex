## 1. Contrat
- [x] 1.1 Consigner le périmètre validé et la version finale 0.6.0.
- [x] 1.2 Valider le delta OpenSpec avant code et tests.

## 2. Implémentation
- [x] 2.1 Distinguer épuisement, authentification, accès et données manquantes.
- [x] 2.2 Filtrer payants/gratuits selon les ressources et inclure OpenCode général.
- [x] 2.3 Classer toutes les réussites par débit puis TTFT et conserver leurs preuves.
- [x] 2.4 Préserver forçages, active, mémoire, secrets et publication.
- [x] 2.5 Synchroniser scripts et consignes des deux distributions.

## 3. Qualification et release
- [x] 3.1 Tester les replis, le retour au payant, les erreurs et le classement.
- [x] 3.2 Exécuter tests, syntaxe et imports sur Python 3.13/3.14.
- [x] 3.3 Vérifier skills, parité, versions 0.6.0, encodage et périmètre.
- [x] 3.4 Actualiser les documents concernés et leur matrice de cohérence.

## 4. Clôture
- [x] 4.1 Valider OpenSpec ciblé, global standard et global strict.
- [x] 4.2 Préparer l’archivage natif et la synchronisation du seul change finalisé.
- [x] 4.3 Préparer les métriques et la matrice du rapport à produire après archive unique.

## Preuves avant archive

- Delta strict validé avant toute écriture de code ou test, puis revalidé.
- Suites complètes finales : 156 tests sur Python 3.13.5 et 156 sur Python 3.14.9.
- Les 24 nouveaux tests couvrent les deux distributions ; les tests existants
  sont adaptés au contrôle initial et à l’examen de tous les candidats.
- Cinq fichiers Python compilés et deux scripts importés sur chaque branche.
- Deux SKILL.md validés par quick_validate.py ; scripts et skills identiques.
- Release 0.6.0 : VERSION, pyproject.toml, README et cinq manifestes alignés.
- Contrôle ciblé de 43 empreintes : 18 modifications prévues et 25 fichiers
  inchangés avant synchronisation ; nouvelle suite et quatre artefacts du
  change comptés séparément. Ancienne archive et cadrages non concernés préservés.
- OpenSpec ciblé strict valide, global standard 9/9, global strict 9/9.
- Les lectures documentaires publiques ne qualifient pas les accès réels :
  aucune consultation de quota, génération, installation de profil ou opération Git.
- Premières validations corrigées : scénarios OpenSpec conservés, attente de
  test forcé adaptée au contrôle de quota initial et fixtures HTTP fermées.
  Aucun échec ni avertissement non résolu dans les suites complètes finales.

## Matrice documentaire avant archive

| Élément | État et preuve |
|---|---|
| Projet réel | Replis et classement couverts par les 156 tests ; qualification hors ligne. |
| AGENTS.md | Inchangé ; règles de périmètre, secrets et OpenSpec appliquées. |
| PROJECT.md | Inchangé ; Catalogue actuel décrit toujours l’évaluation PLLM et ses distributions. |
| TECHNICAL.md | Mis à jour ; Prérequis, catégorie, routage, mémoire et validation PLLM. |
| BUILD.md | Mis à jour ; catalogue requis, repli gratuit et limite de qualification réelle. |
| DEVOPS.md | Inchangé ; chemins Python/OpenSpec et référentiel SCM utilisés. |
| README.md | Mis à jour ; release 0.6.0, retour au payant et classement interne. |
| CHANGELOG.md | Mis à jour ; quatre entrées Unreleased, sans publication distante annoncée. |
| openspec/specs | Delta validé ; six exigences modifiées et quatre ajoutées à synchroniser par archive. |

La production du rapport final et les contrôles post-archive sont requis avant
la clôture, sans réarchiver. Aucun profil Codex/OpenCode installé n’est modifié.

## Clôture observée

Archivage natif unique réussi, specsUpdated=true, quatre ajouts et six
modifications. Un paragraphe trop long détecté après fusion a été raccourci
sans changement de règle dans la spécification et le delta archivé.
Contrôles globaux finaux standard et strict : 8/8, sans avertissement.
Dix blocs normatifs identiques ; aucun change actif. Rapport STATISTIQUES.md
produit après l'archive avec six sections et totaux 19 fichiers initiaux
modifiés + six nouveaux chemins = 25. Aucun échec final ni réarchivage.
