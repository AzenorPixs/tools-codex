# Design

## Context

Le périmètre approuvé est documentaire et spécificatif. Les scripts se trouvent
dans les skills autonomes et leurs copies embarquées ; `src/` et `tests/`
étaient vides lors de l'analyse. OpenSpec contenait une spécification principale
`release-versioning`, aucune évolution active et huit archives, dont sept
relatives à CAB. L'état Git, les données générées et les configurations locales
n'ont pas été inspectés.

## Goals / Non-Goals

**Goals:** rendre les prérequis et limites explicites, supprimer les
contradictions documentaires arbitrées et préparer des contrats traçables aux
capacités existantes. Distinguer contrats, lecture de code, validations
structurelles et preuves de fonctionnement.

**Non-Goals:** corriger le code, initialiser des données, modifier les versions,
choisir une version minimale de Python, installer des outils, accéder aux
fournisseurs, créer une automatisation, synchroniser les specs ou archiver.
Les archives CAB sont préservées ; aucune provenance n'est déduite et aucune
tâche historique non cochée ne justifie leur réouverture.

## Decisions

- Préparer les cinq capacités dans les deltas de ce seul change. Leur présence
  et leur validation stricte ne signifient ni synchronisation des specs
  principales ni conformité fonctionnelle des scripts.
- Reprendre les contrats des skills et cadrages, avec les arbitrages de L2 :
  PLLM `active` reste silencieux, le type de débit reste dans le JSON, le
  protocole documentaire porte le numéro 5 et TFL `auto` ne bascule de secret
  que lors de sa récupération. Aucun repli après refus API n'est ajouté.
- Ne pas transformer une limite de code en exigence fonctionnelle souhaitée.
  Les chemins actuels et le fichier initial PLLM sont documentés comme
  dépendances observées. Une politique valide exige des mesures concluantes
  du modèle effectivement sélectionné, y compris après un repli.
- Conserver le registre ci-dessous et des tâches non cochées pour le travail
  non prouvé. Aucune correction fonctionnelle n'est autorisée par ce design.

## Registre de suivi CGP

| ID | Faits et sources | État après les lots documentaires | Suite et dépendances |
|---|---|---|---|
| CGP-01 | `PROJECT.md` décrit des capacités absentes des specs principales. | Cinq contrats préparés ici, sans synchronisation. | Contrôler les écarts, puis demander les autorisations de synchronisation et d'archivage distinctes. |
| CGP-02 | Sept archives décrivent CAB hors du catalogue actuel. | Statut historique observé explicité dans `PROJECT.md` ; provenance non vérifiée. | Aucune modification des archives ; leur provenance reste à trancher si nécessaire. |
| CGP-03 | `skills/pllm/scripts/evaluate.py`, fonction `tfl_opencode_model_at`, cherche un skill TFL voisin ; les plugins sont séparés. | Limite documentée dans `TECHNICAL.md` et `BUILD.md`. | SCM pour qualifier l'installation réelle et corriger le chemin si nécessaire. |
| CGP-04 | `main` charge `data/pllm-current.json` avant toute évaluation, sans initialisation de remplacement. | Dépendance documentée ; disponibilité des données non inspectée. | SCM pour qualifier le démarrage et décider du traitement d'une installation sans données initiales. |
| CGP-05 | Dans `skills/pllm/scripts/evaluate.py`, `main` peut atteindre `state='Valide'` après HTTP 429 au dernier palier sans benchmark du remplaçant. Le remplacement ne recalcule pas non plus la séquence issue de `budgets_for` pour la nouvelle configuration. | Divergences probables relevées par lecture, non reproduites ni corrigées. | SCM avec tests isolés de la validité et des paliers après remplacement ; aucune déclaration de validité sans mesures concluantes. |
| CGP-06 | Les instructions PLLM contredisaient les règles de débit et de silence ; leur titre indiquait le protocole 4. La reprise a relevé une contradiction résiduelle entre l'affichage utilisé/restant demandé et `quota_display`, limité au restant. | L2 a harmonisé le débit, le silence et le protocole. L5 est appliqué et vérifié : les deux copies demandent d'afficher le restant et de conserver l'utilisation dans les quotas bruts du JSON, sans changer le rendu. | Contradiction documentaire résolue ; structure des deux skills validée et copies identiques. Fonctionnement réel non testé. |
| CGP-07 | `pyproject.toml` déclare `0.0.0`, `VERSION` déclare `0.2.0`. | Valeurs préservées ; rôle de la métadonnée Python non tranché. | Décision du développeur avant toute modification. |
| CGP-08 | Plage Python absente et recours à `secret-tool` peu explicite ; aucune suite identifiée dans le périmètre examiné. | Prérequis et limites de qualification explicités. | Décider de la plage supportée et qualifier l'environnement et les comportements dans une session distincte. |
| CGP-09 | TFL `select_secret` choisit un secret avant `fetch_models`, sans repli sur erreur API. | Documentation alignée sur ce comportement. | Aucune extension du repli ; une évolution exigerait une demande distincte. |
| CGP-10 | Dans `skills/tfl/scripts/test_fournisseur_llm.py`, `openrouter_number` convertit les prix par `float()` sans contrôle de finitude ; `build_openrouter_rows` ne rejette pas explicitement `NaN` au seuil maximal. | Risque probable pour les seuils, le classement et le catalogue JSON, relevé par lecture sans reproduction ni correction. | SCM avec tests isolés de prix non finis ; une valeur non exploitable ne doit pas devenir un coût vérifié. |

Les sources des scripts cités ont des copies embarquées identiques au début
de la session ; elles restent inchangées. Les contrats ne fournissent pas de
preuve d'exécution des scénarios ci-dessus.

Les lots L4 et L5 ont été explicitement validés par le développeur lors de la
reprise CGP du 10 octobre 2026. L4 complète ce registre, les tâches de
qualification et les limites de `TECHNICAL.md`. L5 harmonise uniquement
l'instruction d'affichage des quotas dans les deux copies de PLLM. Ces lots
ne modifient ni les scripts ni les exigences des deltas ; ils n'autorisent
aucune qualification fournisseur, synchronisation ou archive.

## Validation Strategy

- Valider les quatre skills modifiés avec le vérificateur de `skill-creator`
  et comparer les copies autonomes et embarquées.
- Vérifier UTF-8/LF, les liens internes ajoutés, les scénarios de chaque
  exigence, la correspondance entre proposition et deltas et le périmètre des
  fichiers touchés sans inspecter Git.
- Employer le chemin OpenSpec déclaré par `DEVOPS.md` pour la validation
  stricte du change, puis des specs principales et changes actifs.
- N'exécuter aucun script fournisseur ni test d'installation pendant ces lots.
  Aucun test de comportement n'est remplacé par une validation de syntaxe.

## Résultats observés le 10 octobre 2026

- L1 et L2 sont appliqués : trois cadrages et quatre fichiers de skills
  modifiés, sans modification de script. Les deux paires de skills restent
  identiques octet pour octet.
- Les quatre contrôles `quick_validate.py` ont réussi avec `/usr/bin/python3`,
  sans écriture de bytecode. Le premier essai avec le Python DevOps a échoué
  car `PyYAML` y est absent ; aucune dépendance n'a été installée. Ce repli
  concerne le vérificateur documentaire, pas une qualification Python du projet.
- Le premier contrôle OpenSpec strict a retourné 1 pour dix avertissements
  de longueur d'exigence. Après leur scission sans changement de contrat,
  les cinq deltas contiennent 38 exigences et 41 scénarios ; aucune exigence
  ne dépasse 500 caractères.
- `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate document-existing-extension-contracts --strict`
  a retourné 0, sans avertissement.
- `OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 /home/devops/.local/npm/bin/openspec validate --all --strict`
  a retourné 0 : le change et `release-versioning` sont validés, soit 2 éléments
  réussis et 0 échec.
- Le contrôle des sources autorisées par empreintes a constaté sept fichiers
  existants modifiés, neuf fichiers ajoutés dans ce seul change, aucune
  suppression et 78 fichiers préexistants inchangés. Les 16 fichiers touchés
  sont en UTF-8/LF ; les liens Markdown internes contrôlés sont présents.
- Aucun test fournisseur, test d'installation, accès aux secrets, contrôle Git,
  synchronisation ni archivage n'a été effectué. Les écarts CGP-03 à CGP-05
  ne sont pas corrigés et les décisions de CGP-07 et CGP-08 restent ouvertes.

## Résultats des lots L4 et L5 le 10 octobre 2026

- L4 complète CGP-05, CGP-06 et CGP-10, le suivi de qualification et les
  limites techniques. L5 applique l'arbitrage d'affichage aux deux copies de
  PLLM. Aucun script ni contrat normatif n'est modifié.
- Les deux contrôles `quick_validate.py` ont retourné 0 avec
  `/usr/bin/python3 -B`. Les copies PLLM sont identiques octet pour octet.
- Les validations OpenSpec strictes du change et de `--all` ont retourné 0,
  sans avertissement : 2 éléments réussis et 0 échec pour le contrôle global.
- Le contrôle par empreintes des 43 sources autorisées suivies constate
  exactement les cinq fichiers approuvés modifiés et 38 sources inchangées.
  Les cinq fichiers sont en UTF-8/LF. Les six tâches cochées sont préservées ;
  les huit tâches ouvertes incluent la nouvelle qualification CGP-10.
- Aucun test fonctionnel ou fournisseur, installation, accès aux secrets,
  contrôle Git, synchronisation ni archivage n'a été effectué. CGP-03 à
  CGP-05 et CGP-10 restent à qualifier dans une session SCM ; les décisions
  de CGP-07 et CGP-08 restent ouvertes. Ces résultats clôturent les seuls
  lots documentaires approuvés et ne prouvent pas la conformité fonctionnelle.

## Risks / Trade-offs

L'absence de synchronisation laisse volontairement les contrats dans ce
change actif. Le risque principal est de confondre ce dossier préparé avec une
livraison fonctionnelle : les tâches de qualification et de cycle restent
non achevées. La compatibilité Python et le rôle de la version Python ne sont
pas déduits de l'environnement inventorié.

## Migration Plan

Aucune migration runtime ni reprise de données. Appliquer les seuls lots
approuvés, contrôler leurs résultats et conserver le change préparé. Une
session SCM distincte doit traiter les écarts fonctionnels avant toute
affirmation de conformité. La synchronisation et l'archivage sont des lots
ultérieurs distincts ; aucun archivage n'est actuellement autorisé.

## Évolution ciblée du seuil et de la release — 10 octobre 2026

La demande ultérieure du développeur autorise uniquement le passage du TTFT
strict à moins de 90 secondes et la release 0.2.1 pour le projet et ses deux
plugins. Une constante commune au contrôle et à la couleur porte ce seuil
dans chaque copie du script. Les critères JSON sont actualisés pour les
politiques réellement réévaluées ; les rapports historiques ne sont pas
réécrits. Des tests hors ligne couvrent les bornes, le débit inchangé et
l’arrêt avant benchmark lorsque le quota est invalide. Cette extension ne
résout pas les autres écarts CGP et n’autorise ni publication, installation,
synchronisation ni archivage.

Validation de cette évolution : les quatre tests hors ligne réussissent pour
les deux distributions ; les trois fichiers Python compilent. Les contrôles
de structure des deux skills, UTF-8/LF, d’identité des copies et de version
0.2.1 réussissent. La validation OpenSpec stricte globale réussit avec deux
éléments et zéro échec. Aucun rapport fournisseur historique n’est régénéré.
