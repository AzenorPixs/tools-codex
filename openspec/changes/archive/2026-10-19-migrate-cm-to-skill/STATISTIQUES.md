# STATISTIQUES — migrate-cm-to-skill

Projet : Tools Codex (`tools-codex`). Racine : `/home/devops/datas/tools-codex`.
Archive : `openspec/changes/archive/2026-10-19-migrate-cm-to-skill`.
Release livrée dans les sources : 0.2.2. Date : 19 octobre 2026.

Rapport de la reprise SCM autorisée : réalisation, contrôles et archivage.
Les compteurs exhaustifs de messages, outils, tokens, coûts et temps de
génération n'ont pas été collectés : ils restent N/A. Aucune compétence de
statistiques pilotées, sonde CAB/OpenCode ou délégation n'a été utilisée.

## 1. Statistiques générales et décisions

Le périmètre couvre le remplacement de `/cm` par `$cm`, sa découverte locale,
la release 0.2.2, les spécifications, les documents et le cycle d'archivage.
La source du catalogue reste unique ; aucune installation globale ni
publication externe n'a été réalisée.

| Mesure vérifiée | Résultat |
|---|---|
| Tests distincts de la suite existante | 19 |
| Interpréteurs effectivement utilisés | Python 3.13.5 et 3.14.8 |
| Exécutions de tests réussies | 38 sur 38, soit 100 % |
| Tâches du change terminées | 11 sur 11 |
| Éléments OpenSpec valides avant archivage | 7 sur 7 |
| Spécifications valides au dernier contrôle après archivage | 6 sur 6 |
| Changements actifs après archivage | 0 |
| Exigences synchronisées | 1 ajoutée, 2 modifiées, 0 supprimée, 0 renommée |
| Fichiers initiaux suivis par empreintes dans le périmètre observé | 97 |
| Chemins initiaux changés, dont la commande supprimée | 11 |
| Fichiers initiaux préservés | 86, dont 61 fichiers des archives préexistantes |

Les 97 fichiers sont un ensemble ciblé de cadrages, commandes, spécifications,
archives, manifestes, skills, scripts et tests. Il ne s'agit pas d'un inventaire
récursif de toutes les sources du dépôt. Les empreintes préservent notamment
AGENTS.md, DEVOPS.md, .gitignore, ORCHESTRATED_CODING.md, la marketplace, les
sources PLLM/TFL et les deux modules de tests observés.

Modèle exact, fournisseur détaillé, raisonnement, TTMT, débit de génération,
temps de service, tokens, cache, coûts et variation de quotas : N/A,
télémétrie comparable non disponible. Agent de codage : Codex, exécution
directe. Agent orchestrateur et sous-agents : non applicables.

## 2. Types de messages et d'outils

| Domaine | Observation | Comptage exhaustif |
|---|---|---|
| Messages humains | Périmètre autonome et archivage explicitement validés avant écriture | N/A, pas de collecte agrégée |
| Messages de suivi | Progression, contrôles et correction de l'écart OpenSpec | N/A, pas de collecte agrégée |
| Commandes locales | Lectures ciblées, édition, validation, tests et archive | N/A pour l'ensemble ; sous-ensemble borné en section 4 |
| Édition | apply_patch et traitements Python locaux | Tentatives et pourcentages N/A ; chemins finaux en section 3 |
| Horloge | Deux bornes partielles de la phase d'implémentation | Intervalle décrit en section 6 |
| Git | Aucune opération depuis la reprise autorisée ; état Git non inspecté dans cette phase | Non applicable |
| Pilotage, CAB, OpenCode, délégation | Non déclenchés | Non applicable |

L'erreur de confirmation de l'outil OpenSpec et l'échec de validation de
longueur sont des résultats distincts ; ils ne sont ni masqués ni assimilés à
des refus de sécurité. L'autorisation d'archiver était acquise dans le périmètre.

## 3. Fichiers modifiés

Les chemins ci-dessous sont relatifs à la racine indiquée en tête du rapport.

| Chemin final ou supprimé | Opération |
|---|---|
| VERSION | Modifié : 0.2.2 |
| pyproject.toml | Modifié : version 0.2.2, plage Python inchangée |
| plugins/pllm/.codex-plugin/plugin.json | Modifié : version 0.2.2 uniquement |
| plugins/tfl/.codex-plugin/plugin.json | Modifié : version 0.2.2 uniquement |
| PROJECT.md | Modifié : organisation et catalogue |
| TECHNICAL.md | Modifié : découverte, invocations, prérequis et validation |
| BUILD.md | Modifié : installation et contrôle du catalogue cm |
| README.md | Modifié : release, usage et installation |
| CHANGELOG.md | Modifié : trois entrées Unreleased |
| openspec/specs/extension-distribution/spec.md | Modifié : deux exigences et une nouvelle |
| .codex/commands/cm.md | Supprimé après transfert du catalogue |
| skills/cm/SKILL.md | Créé : source canonique |
| .agents/skills/cm | Lien créé vers ../../skills/cm |
| openspec/changes/archive/2026-10-19-migrate-cm-to-skill/.openspec.yaml | Créé puis archivé |
| openspec/changes/archive/2026-10-19-migrate-cm-to-skill/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-19-migrate-cm-to-skill/design.md | Créé puis archivé, preuves complétées |
| openspec/changes/archive/2026-10-19-migrate-cm-to-skill/tasks.md | Créé puis archivé, onze tâches terminées |
| openspec/changes/archive/2026-10-19-migrate-cm-to-skill/specs/extension-distribution/spec.md | Créé puis archivé, rédaction alignée sur la spec principale |
| openspec/changes/archive/2026-10-19-migrate-cm-to-skill/STATISTIQUES.md | Créé après archivage |

| Catégorie de chemin final | Nombre |
|---|---:|
| Fichier existant modifié | 10 |
| Fichier existant supprimé | 1 |
| Nouveau fichier | 7 |
| Nouveau lien symbolique | 1 |
| Total | 19 |

Les cinq fichiers du change ont été créés à son emplacement actif puis
déplacés par OpenSpec. Ce déplacement n'ajoute pas cinq autres chemins au
total final. Le rapport est créé après l'archivage. Aucun nouveau test ni
script permanent n'est ajouté pour cette modification documentaire de skill.

## 4. Commandes

Sous-ensemble borné aux dix appels de validation et de cycle identifiables
jusqu'au premier contrôle strict post-archive entièrement réussi. Les
lectures, éditions, aides CLI, commandes de version et audits de clôture
supplémentaires ne sont pas inclus dans ce total. Les commandes OpenSpec
utilisent `/home/devops/.local/npm/bin/openspec`, avec
`OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1`.

| Commande ou contrôle | Exécutions | Réussites | Échecs |
|---|---:|---:|---:|
| python3 -B quick_validate.py skills/cm, chemin du skill-creator indiqué dans design.md | 1 | 1 | 0 |
| /usr/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v | 1 | 1 | 0 |
| /home/devops/python/current/bin/python3 -B -W error::ResourceWarning -m unittest discover -s tests -v | 1 | 1 | 0 |
| Python DevOps par stdin : structure, portabilité, catalogue, JSON/TOML et UTF-8/LF | 1 | 1 | 0 |
| openspec validate migrate-cm-to-skill --strict | 1 | 1 | 0 |
| openspec validate --all --strict | 3 | 2 | 1 |
| openspec archive migrate-cm-to-skill --json | 1 | 0 | 1 |
| openspec archive migrate-cm-to-skill --json --yes | 1 | 1 | 0 |
| Total borné | 10 | 8 | 2 |

Taux dans ce sous-ensemble : 80 % de réussites, 20 % d'échecs initiaux résolus.
Ce taux mesure des appels de commandes ; il ne décrit pas le taux des tests,
qui est de 38 réussites sur 38 exécutions.

Échecs et corrections :

- L'archive JSON sans `--yes` a retourné `archive_confirmation_required` sans
  créer d'archive. La relance confirmée dans le périmètre validé a créé
  l'archive et synchronisé les spécifications.
- Le contrôle strict immédiatement après l'archive a refusé une exigence
  dépassant 500 caractères. Les syntaxes ont été transférées dans son scénario
  dans la spec principale et le delta archivé ; l'exigence compte 438
  caractères et conserve son comportement. Le contrôle strict suivant a réussi.

Contrôles supplémentaires exécutés et réussis : empreintes sur les 97 fichiers
initiaux observés ; préservation des 61 fichiers d'anciennes archives ; égalité
des trois exigences entre la spec principale et le delta archivé ; mots-clés
RFC 2119 en majuscules ; onze tâches terminées ; absence de change actif.
Le lien résout la source canonique et une copie temporaire du projet dans un
chemin contenant des espaces ; cette copie a été nettoyée. Les trois syntaxes
du catalogue et les cinq supports de version sont contrôlés.

Invocation réelle de `$cm` dans une nouvelle session : non exécutée. Le contrôle
du format et du lien est exécuté et réussi. Compilation de fichiers Python
modifiés : non pertinente, aucun fichier Python n'a été modifié. Build web,
tests navigateur, tests fournisseurs et publication : non pertinents pour
cette livraison locale, et non exécutés.

## 5. Accès web

| Périmètre | Accès | Refus | Erreurs |
|---|---:|---:|---:|
| Reprise autorisée couverte par ce rapport | 0 | 0 | 0 |

Les références officielles de découverte des skills avaient été consultées
lors du diagnostic antérieur. Les liens des documents ne constituent pas de
nouvelles visites. Aucun fournisseur ni secret n'a été sollicité ; la
télémétrie OpenSpec a été désactivée. Taux de réussite web : N/A,
dénominateur nul. Statistiques exhaustives du diagnostic antérieur : N/A,
hors de la phase mesurée ici.

## 6. Synthèse globale

| Repère temporel partiel | Heure Europe/Paris |
|---|---|
| Avant création du skill et modification des versions | 2026-10-19 13:38:31 CEST |
| Après archivage, correction et contrôle strict réussi, avant rédaction du rapport | 2026-10-19 13:41:54 CEST |
| Intervalle entre ces bornes | 00 h 03 min 23 s |
| Durée totale de la SCM | N/A, borne initiale complète non instrumentée |

Cet intervalle inclut les outils et les attentes ; il ne mesure pas le temps
de génération et exclut la préparation OpenSpec antérieure, la rédaction du
rapport et les contrôles finaux ultérieurs.

| Document de la matrice SCM | Bilan et preuve |
|---|---|
| Projet réel | Source canonique et lien relatifs vérifiés ; ancienne commande absente ; cinq supports de release alignés à 0.2.2. |
| AGENTS.md | Inchangé, empreinte conservée ; sections 5–6, 8, 12 et 21 applicables sans adaptation. |
| PROJECT.md | Mis à jour, Organisation et Catalogue actuel : cm est un skill, les commandes sources PLLM/TFL sont distinguées. |
| TECHNICAL.md | Mis à jour, Arborescence, Commandes et skills autonomes, Prérequis et Validation : lien, invocations, source unique et limite de qualification. |
| BUILD.md | Mis à jour, Skill catalogue cm : découverte locale, copie dans un autre projet ou emplacement personnel et test effectif distinct. |
| DEVOPS.md | Inchangé, empreinte conservée ; chemins Python, OpenSpec et Prompts utilisés ; aucun nouveau prérequis. |
| README.md | Mis à jour, release 0.2.2 et usage `$cm`, lien vers la source et BUILD. |
| CHANGELOG.md | Mis à jour, trois entrées Unreleased pour la migration et la release ; historique conservé. |
| openspec/specs/ | Extension-distribution synchronisée ; égalité avec le delta archivé vérifiée ; six specs strictes valides. Release-versioning inchangée, ses invariants sont respectés. |

Le remplacement de `/cm` par `$cm` est l'impact de compatibilité prévu.
PLLM/TFL et les autres skills observés sont préservés. Le catalogue s'affiche
sans lancer leurs générateurs. Hors du projet, l'installation autonome reste
une action distincte, documentée dans BUILD. Le repli local est décrit dans
design.md ; aucune migration irréversible de données n'a été effectuée.

Le contrôle final après écriture est exécuté et réussi : six sections,
encodage UTF-8/LF de tous les fichiers finaux concernés, 19 chemins réels,
catégories 10/1/7/1 et totaux de commandes 10/8/2. Les deux manifestes, le
TOML et VERSION ne changent que de version ; les répertoires contrôlés ne
contiennent aucun artefact temporaire restant. Aucun écart documentaire restant identifié
dans le périmètre ; les deux échecs ont été résolus. L'essai effectif de `$cm`
dans une nouvelle session reste non exécuté et n'est pas annoncé comme réussi.

État : TERMINÉ pour le périmètre local SCM, rapport vérifié. Archivage unique effectué ; aucun
nouvel archivage, publication, commit ou push n'est requis pour cette clôture.
