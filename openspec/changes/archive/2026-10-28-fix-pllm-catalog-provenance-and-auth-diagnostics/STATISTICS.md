# STATISTIQUES — fix-pllm-catalog-provenance-and-auth-diagnostics

Projet : Tools Codex (`tools-codex`). Session SCM directe du 28 octobre 2026.
Release locale : 0.7.23. Archive native : `2026-10-28-fix-pllm-catalog-provenance-and-auth-diagnostics`.

## 1. Statistiques générales

La copie TFL du plugin consommée à 11:28 était datée du 14 septembre. La collecte autonome du 28 octobre à 11:06 retient un gratuit Go et deux gratuits OpenRouter. Le correctif rend observables le chemin, la date, l'âge, les avertissements et les compteurs du catalogue choisi, avec priorité au chemin explicite et sans collecte implicite. Un refus de ressource est localisé par phase, endpoint et statut HTTP filtré. Les modes gratuits restent indépendants des quotas et les résultats/mémoires PLLM sont exclus de Git en conservant les fichiers locaux.

Les modes3/6 réussissent la nouvelle évaluation réelle. Les modes2/4 restent refusés en HTTP 401 avec leur accès associé : quota pour mode2, génération pour mode4. Ce refus externe est distinct des critères de qualification du correctif et ne constitue pas une mesure de performance. Aucun secret n'a été remplacé ni emprunté.

| Mesure | Total vérifié |
|---|---:|
| Nouveaux tests distincts | 5 |
| Tests ciblés PLLM réussis | 90 |
| Tests globaux distincts | 352 |
| Exécutions globales finales réussies | 704 (352 par branche) |
| Fichiers Python modifiés compilés | 5 par branche, 10 compilations |
| Paires de distribution vérifiées | 2 |
| Métadonnées de release alignées | 8 |
| Exigences OpenSpec ajoutées | 3 |
| Politiques réellement évaluées | 7 |
| Tentatives de génération tracées | 9 |

Les 90 tests ciblés et les cinq nouveaux tests sont inclus dans les 352, sans addition aux tests distincts. Durée totale de session, tokens et coût : N/A, aucune télémétrie exhaustive SCM instrumentée.

## 2. Messages et outils

Session exécutée directement, sans sous-agent, OpenCode ou CAB. Outils employés : lectures ciblées, apply_patch, scripts Python locaux, unittest, py_compile et CLI OpenSpec. L'accès aux secrets s'effectue uniquement dans le processus local de diagnostic/évaluation, en mémoire et sans sortie des valeurs. Messages et appels d'outils exhaustifs : N/A, aucun agrégat fiable instrumenté. La compétence de statistiques de pilotage n'a pas été utilisée.

## 3. Fichiers

Code : deux evaluate.py synchronisés. Tests : test_pllm_catalog_provenance.py ajouté ; attentes de release de test_lm_blacklist.py et test_tcu_update.py alignées. Instructions : deux SKILL PLLM et commande PLLM alignés. Documentation : README, TECHNICAL, BUILD et CHANGELOG. Release : VERSION, pyproject.toml et six manifestes. Git : trois motifs précis ajoutés à .gitignore pour préserver localement les sorties PLLM sans publication des quotas/historiques. OpenSpec : proposition, conception, tâches, delta, VALIDATION.md, trois exigences principales synchronisées et ce rapport.

AGENTS, PROJECT et DEVOPS restent inchangés. Les résultats courants et mémoires restent locaux ; ils ne font pas partie des sources du correctif. Lignes ajoutées/supprimées : N/A, aucun diff Git de contenu utilisé sous SCM. La liste exacte des chemins du commit est vérifiée à l'étape Git suivante.

## 4. Commandes et validations

- `python3 -B -m unittest discover -s tests -p 'test_pllm*.py' -v` : 90 réussites.
- `/home/devops/python/current/bin/python3 -B -m unittest discover -s tests` : 352 réussites sous Python 3.14.10, durée 15,668 s.
- `/usr/bin/python3.13 -B -m unittest discover -s tests` : 352 réussites sous Python 3.13.5, durée 17,134 s.
- Premier passage global : deux échecs d'attentes de version 0.7.22, corrigés pour la release demandée. Les deux passages finaux réussissent sans affaiblissement des contrôles.
- Compilation py_compile des cinq fichiers Python modifiés sous les deux branches, avec cfile temporaire et nettoyage. Parité evaluate.py / SKILL.md et huit métadonnées vérifiées.
- `openspec validate --all --strict` : 11/11 avant archivage ; archivage natif réussi avec trois exigences ajoutées ; 10/10 après archivage.
- Rapport : six sections, UTF-8/LF et totaux contrôlés ; aucun BLOCKER.md ou BLOCKERS.md dans l'archive.

La validation hors ligne distingue chemin explicite récent et voisin ancien, dates non vérifiables/futures, absence de gratuit, indépendance mode4 et diagnostics filtrés, sans réseau ni trousseau réels. Shell, navigateur et SQL : non pertinents.

## 5. Accès web et fournisseurs

Quatre lectures diagnostiques authentifiées : /usage et /models Go répondent 200 avec l'accès mode1 et 401 avec l'accès mode2. L'évaluation normale a ensuite consommé explicitement le catalogue autonome daté du 28 octobre à 11:06:15, sans lancer TFL. Les neuf tentatives de génération tracées se répartissent par mode : 2 + 0 + 3 + 1 + 0 + 2 + 1 = 9. Le nombre exhaustif des lectures internes d'évaluation n'est pas agrégé : N/A ; aucun total réseau global n'est inventé.

Résultats de 11:40 à 11:41 Europe/Paris : mode1 valide, mode2 refusé au quota (401), mode3 beam-free valide (3,1 s ; 306,5 tokens/s), mode4 beam-free refusé à la génération (401), mode5 valide sans génération, mode6 nemotron-3-ultra-550b-a55b:free valide (0,9 s ; 35,4 tokens/s), mode7 valide. Aucune lecture de quota/solde en modes3/4/6 : quotas null et contrôle non applicable. Les résultats détaillés restent dans les sorties locales exclues de Git ; aucun montant ni compte n'est reproduit ici.

Les performances sont datées et ne garantissent pas la disponibilité future. La cause privée du refus des modes2/4 n'est pas établie ; la vérification de leur accès fournisseur reste une action externe. Aucun changement du trousseau, des agents OpenCode, du timer ou des profils installés n'a été effectué.

## 6. Synthèse et cohérence documentaire

| Document | État et preuve |
|---|---|
| AGENTS.md | Inchangé : règles de secrets, validation et clôture préservées. |
| PROJECT.md | Inchangé : architecture et séparation des installations conservées. |
| TECHNICAL.md | Données générées : provenance, ressources et exclusions Git documentées. |
| BUILD.md | Installation : divergence des catalogues et refus d'accès documentés. |
| DEVOPS.md | Inchangé : chemins réels Python/OpenSpec utilisés, aucune dépendance ajoutée. |
| README.md | Release 0.7.23 et choix du catalogue explicités. |
| CHANGELOG.md | Entrée Unreleased pour le comportement livré et la release. |
| OpenSpec | Trois exigences synchronisées par archivage natif, validation stricte réussie. |
| Distributions et commande | Deux paires identiques, huit colonnes et commande PLLM préservées. |
| .gitignore | Trois motifs de sorties PLLM locales, sans suppression de leurs copies. |

Ce rapport prouve la qualification et l'archivage. Le commit local, le tag et les publications conditionnelles SCM sont exécutés après sa vérification et restitués séparément ; ils ne sont pas présumés réalisés ici. Aucune installation utilisateur n'est déduite de la qualification des sources.
