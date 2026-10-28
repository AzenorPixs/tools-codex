# EXT02 — Proposition

## Why

Tools Codex distribue PLLM et TFL, conserve quatre skills autonomes et trois
commandes maison, mais sa seule spécification principale porte sur la version
de release. Le diagnostic CGP du 10 octobre 2026 a également relevé des
prérequis peu explicites, des instructions contradictoires et des écarts
PLLM qui nécessitent un travail fonctionnel distinct.

## What Changes

- Clarifier les prérequis, les limites de qualification et le statut observé
  des archives CAB dans les cadrages, sans attribuer une provenance non prouvée.
- Harmoniser les instructions PLLM : protocole 5, type de débit dans le JSON
  et mode `active` silencieux. Décrire le repli TFL sur l'accès au secret.
- Préparer cinq contrats OpenSpec fondés sur les capacités documentées et
  observables, avec exigences et scénarios vérifiables.
- Conserver explicitement les écarts d'implémentation et les décisions non
  prises comme travaux non achevés ; une validation structurelle ne les résout pas.

## Capabilities

### New Capabilities

- `extension-distribution`: catalogue, organisation des ressources et limites
  entre installation des plugins, skills autonomes et commandes maison.
- `tfl-catalog`: collecte, filtrage, classement et publication du catalogue TFL.
- `pllm-evaluation`: quotas, mesures concluantes, sélection, publication et
  séparation entre évaluation et application OpenCode autorisée.
- `codex-usage-reporting`: quotas actuels, historique local et restitution CGPT.
- `coding-session-statistics`: rapport de session fondé sur des preuves,
  métriques disponibles et statistiques d'archivage.

### Modified Capabilities

- `release-versioning`: ajouter l'alignement de la métadonnée Python sur
  `VERSION`, conformément à la décision CGP-07 validée lors de la clôture.

## Impact

Les lots L1 à L3 ont été explicitement validés par le développeur le
10 octobre 2026. L1 concerne `PROJECT.md`, `TECHNICAL.md` et `BUILD.md` ;
L2 concerne les deux copies de chacun des skills PLLM et TFL ; L3 concerne
uniquement les métadonnées, cette proposition, le design, les tâches et les
cinq deltas de ce change.

Aucun script, manifeste, dépendance, configuration locale ou archive n'est
modifié. Aucun test fournisseur, installation, effet externe, commit ou push
n'est inclus. La synchronisation vers `openspec/specs/` et l'archivage exigent
des autorisations distinctes et sont exclus des lots validés.

## Extension ciblée demandée le 10 octobre 2026

Le développeur a ensuite demandé de porter le seuil PLLM à 90 secondes et
d’incrémenter la version des briques de 0.0.1. Ce périmètre distinct des lots
documentaires ci-dessus couvre les deux scripts PLLM, leurs instructions, le
delta `pllm-evaluation`, des tests hors ligne et la release 0.2.1 dans `VERSION`,
`README.md`, `CHANGELOG.md` et les manifestes PLLM/TFL. Le seuil reste strict ;
les quotas, le débit minimal et la limite de requête de 120 secondes sont
conservés. Les autres écarts CGP, la synchronisation et l’archivage restent
hors de cette demande.

## Extension SCM validée — CGP-03 à CGP-05 et CGP-10

Le développeur a validé la résolution de ces quatre écarts, puis le périmètre
précis incluant `--tfl-catalog CHEMIN` et l'initialisation automatique des
quatre politiques. Cette extension couvre les deux scripts PLLM, les deux
générateurs TFL, les instructions PLLM, les commandes `/pllm` et `/cm`, les
tests hors ligne et les mises à jour de `TECHNICAL.md`, `BUILD.md`, `README.md`
et `CHANGELOG.md`. Les contrats PLLM et TFL sont complétés avant le code.

Le chemin voisin reste le défaut ; le fichier courant valide est préservé et
un fichier corrompu n'est pas remplacé. Chaque modèle de repli exige ses propres
mesures. Les prix non finis sont exclus et le catalogue TFL reste du JSON strict.
La release 0.2.1, TTFT < 90 secondes, le débit > 15 tokens/s, les modes forcés
et le silence du mode `active` sont préservés. Aucun appel fournisseur, secret,
installation réelle, opération Git ou nouvelle dépendance n'est inclus.
L'archivage reste suspendu à la tâche 3.4 et aux décisions CGP-07/08 ; le
développeur a validé cette limite de terminaison.

## Clôture Python et cycle OpenSpec autorisés

Le développeur valide ensuite les deux décisions CGP-07/08 et les trois lots
de clôture : `project.version = "0.2.1"`,
`requires-python = ">=3.13,<3.15"`, qualification hors ligne des deux branches,
synchronisation des contrats, archivage de ce seul change et production de
son `STATISTIQUES.md`. Cette décision remplace la limite d'archivage du lot
précédent, sans autoriser publication, Git, fournisseur ou installation réelle.

`VERSION` reste la source de vérité. Le rôle de `pyproject.toml` est de
déclarer les métadonnées et prérequis Python du dépôt ; aucun packaging ni
publication Python n'est ajouté. Les branches antérieures à 3.13 et à partir
de 3.15 sont explicitement exclues de la plage revendiquée. Les dépendances et
les scripts restent inchangés. La qualification couvre les 19 tests existants,
la compilation de tous les scripts et tests, les imports et le fuseau Paris.

Les documents concernés sont `pyproject.toml`, `TECHNICAL.md`, `BUILD.md`,
`README.md`, `CHANGELOG.md` et les artefacts de ce change. La synchronisation
crée les cinq specs préparées et complète `release-versioning`. L'archivage
déplace ce dossier dans `openspec/changes/archive/` ; le rapport y est produit
avec six sections, des preuves et des `N/A` motivés pour les mesures absentes.
