# Statistiques — restore-mode5-paid-benchmark

Rapport établi le 2026-10-28T20:17:11+01:00. Session directe SCM Tools Codex ; version source 0.7.25. Change achevé et archivé. Périmètre de mesure : travail source, vérifications et archivage de cette invocation ; les évaluations TFL/PLLM précédentes sont exclues.

## 1. Statistiques générales et décisions

- Un agent de codage direct, aucun orchestrateur ni sous-agent. Aucun pilotage CAB ni sonde de session pilotée.
- Décision humaine : périmètre autonome explicitement validé ; version 0.7.25, tests, archivage et statistiques demandés.
- Change : restore-mode5-paid-benchmark ; archive : 2026-10-28-restore-mode5-paid-benchmark.
- Début et durée totale : N/A, aucune horloge de session instrumentée ; l'horodatage ci-dessus est celui du rapport. Tokens, quotas Codex et coût de cette session : N/A, aucun relevé disponible.
- Validation fonctionnelle : benchmark payant mode5 Medium et parcours tarifaire au premier succès, contrôles ressources et erreurs bloquantes, sans modifier les autres catégories ni TFL payant.

## 2. Types de messages et d'outils

Messages utilisateur de cadrage/validation, suivis de progression, outils de lecture, exécution Python et CLI OpenSpec. Nombre exact par type : N/A, aucun export exhaustif d'événements ; aucune estimation. Aucun outil CAB ni télémétrie de pilotage invoqué. Aucun secret transmis au modèle par les processus de cette réalisation.

## 3. Fichiers modifiés

| Groupe | Nombre | Périmètre |
|---|---:|---|
| Moteurs PLLM | 2 | evaluate.py autonome et embarqué |
| Instructions PLLM | 3 | Deux SKILL.md et commande source |
| Documentation | 4 | README, TECHNICAL, BUILD, CHANGELOG |
| Métadonnées release | 8 | VERSION, pyproject et six manifestes |
| Tests | 7 | Six suites adaptées et nouvelle suite mode5 |
| Spécifications courantes | 2 | pllm-evaluation et tfl-catalog |
| Artefacts archivés | 7 | proposal, design, tasks, deux deltas, VALIDATION et ce rapport |
| Total | 33 | Fichiers propres au périmètre SCM ; ne décrit pas un éventuel état Git antérieur |

Le détail des 24 fichiers source est dans [VALIDATION.md](VALIDATION.md). Les sept artefacts du change ont été créés puis déplacés par le CLI ; aucun fichier utilisateur supprimé. Aucun bilan de blocage présent, nettoyage non applicable.

## 4. Commandes

- Tests ciblés PLLM : exécutés et réussis après adaptation des anciennes attentes sans benchmark.
- `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests` : 366 tests réussis sous Python 3.14.10, 11,143 s.
- `/usr/bin/python3 -B -m unittest discover -s tests` : 366 tests réussis sous Python 3.13.5, 12,141 s.
- Total final : 732 exécutions, 366 tests distincts sur deux interpréteurs. Les essais intermédiaires ne sont pas additionnés.
- Compilation des 59 fichiers Python sur chaque version et ZoneInfo Europe/Paris : réussies.
- Parité des 10 fichiers distribués PLLM, alignement 0.7.25 et UTF-8/LF : réussis.
- OpenSpec cible strict : réussi ; global standard/strict avant archivage : 11/11 ; après archivage : 10/10 chacun.
- Archivage : réussi, trois exigences ajoutées et neuf modifiées. Avertissement proposal non bloquant détaillé dans VALIDATION.md.
- Nombre total de commandes : N/A, pas de trace instrumentée exhaustive. Étapes Git conditionnelles SCM postérieures : bilan dans la restitution finale ; elles ne constituent pas des tests de performance fournisseur.

## 5. Accès web

Aucune recherche web ni génération fournisseur réelle n'a été utilisée pour cette réalisation source. Réseau et trousseau sont isolés par les fixtures des tests. Les éventuels transports Git de clôture sont distincts et seront rapportés dans le bilan final. Aucun tarif ou débit fournisseur nouveau n'est déduit des tests hors ligne.

## 6. Synthèse globale

Source 0.7.25 qualifiée hors ligne sur Python 3.13/3.14, deux distributions alignées, documentation et spécifications cohérentes, archivage réussi. Matrice documentaire et preuves dans VALIDATION.md. Le rapport comporte six sections ; totaux fichiers 2+3+4+8+7+2+7=33 et tests 366×2=732 vérifiés. Installation dans le profil, activation runtime et benchmark réel : non exécutés, distincts de cette livraison source. Les statistiques ne déclarent pas une publication Git encore non observée à leur date de rédaction.
