# STATISTIQUES — fix-buffered-stream-throughput

Projet : Tools Codex. Release locale : 0.7.3. Session SCM directe.
Le développeur a validé la méthode sur la durée totale et le périmètre
autonome jusqu'à l'archive et au rapport. L'incrément est exactement 0.0.1 :
0.7.2 → 0.7.3. Rapport produit après l'archive native unique du 25 octobre 2026.

## 1. Statistiques générales

Le protocole 8 calcule le débit moyen observé côté client sur la requête
complète, attente et TTFT inclus. Go/général : completion_tokens /
request_seconds ; OpenRouter/DeepSeek : (completion_tokens -
reasoning_tokens) / request_seconds, selon les règles de comptage fiable.
Le premier token n'est plus soustrait. La durée monotone non arrondie sert
au calcul ; duration_seconds reste un affichage arrondi et generation_seconds
une observation entre fragments. Une réponse complète en un bloc reste
mesurable. Durée invalide ou compteur incohérent : débit indisponible et
cause explicite, sans ancienne valeur reprise, plafond ou plancher artificiel.

Le profil request_average_v1/request_total et measurement_protocol_version=8
sont tracés dans les mesures, les publications et l'identité de mémoire.
Les anciens succès restent historiques sans amorcer le nouveau profil ;
un succès de même profil peut réutiliser son palier. HIGH et XHIGH restent
distincts. Les six priorités, comptes partagés 1/3 et 2/4, quotas, seuils
15/20 tokens/s et TTFT 90/30 s sont conservés. Le nouveau sens du débit peut
modifier classement et éligibilité ; il n'est pas directement comparable
à l'ancienne extrapolation entre fragments.

Diagnostic historique du mode 5, publié le 25 octobre 2026 à 13:18:19 Paris :
715 tokens de sortie, dont 462 de raisonnement ; durée totale 1,7751 s ;
fenêtre de contenu arrondie à 0,0001 s ; ancien débit 2 147 441,04 tokens/s.
Le test déterministe reproduit la rafale et obtient 253/1,7751 =
142,527 tokens/s. C'est une reproduction simulée des compteurs enregistrés,
pas un nouveau benchmark fournisseur ni une promesse de performance actuelle.

Suites finales : 222 tests sous Python 3.13.5 et 222 sous Python 3.14.9,
soit 444 exécutions finales pour 222 tests distincts. Quatorze nouveaux tests,
avec sous-cas sur les quatre moteurs et les transports. Les 208 tests
antérieurs sont conservés ; deux fichiers existants sont adaptés à la
nouvelle formule et à la traçabilité de publication, sans désactivation.

25 compilations par branche, soit 50 ; treize imports de scripts par branche,
soit 26 ; Europe/Paris résolu. Quatre SKILL.md validés. Quatorze tâches
préparatoires cochées. Quatre exigences modifiées et synchronisées :
trois PLLM et une TFL, aucune exigence ajoutée, supprimée ou renommée.
Les scénarios existants sont conservés et enrichis.

Avant archive : ciblé strict valide, global standard et strict 9/9.
Après archive : standard et strict 8/8 sans avertissement.
specsUpdated=false dans l'archive native signifie que les quatre exigences
étaient déjà synchronisées ; les totaux natifs nuls ne signifient pas
absence de modification des spécifications.

Durée totale, temps modèle/outils, tokens, cache, coûts, quotas consommés et
couverture de lignes : N/A, télémétrie non instrumentée. Les répétitions
de suites ne sont pas ajoutées au nombre de tests distincts.

## 2. Messages et outils

SCM exécutée directement avec le skill prompt et le référentiel résolu depuis
DEVOPS.md. La validation des instructions utilise skill-creator et son
quick_validate.py déjà chargé dans la conversation. Aucun sous-agent,
pilotage OpenCode/CAB ou compétence de statistiques pilotées.
Messages et appels exhaustifs : N/A, non agrégés.

Le diagnostic lit uniquement les champs utiles du rapport PLLM enregistré.
Les tests injectent réseau, horloge, flux et erreurs simulés, avec clés de
fixture sans valeur réelle. Les temporaires de tests et compilation sont
créés sous tests puis nettoyés. Les assertions vérifient aussi l'absence de
valeur de session publiée et de mesure périmée.

Aucun accès web, appel fournisseur, nouvelle évaluation authentifiée,
inspection/opération Git, installation, TCU, activation ou modification
d'agent/service OpenCode. Aucun accès aux valeurs de clés par l'agent.
Les rapports et mémoires installés ne sont pas réécrits pendant cette livraison.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins finaux relatifs :

| Chemin | Opération |
|---|---|
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| openspec/specs/pllm-evaluation/spec.md | Modifié |
| openspec/specs/tfl-catalog/spec.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| plugins/pllm/skills/pllm/scripts/performance.py | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/skills/tfl/SKILL.md | Modifié |
| plugins/tfl/skills/tfl/scripts/performance.py | Modifié |
| plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| pyproject.toml | Modifié |
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| skills/pllm/scripts/performance.py | Modifié |
| skills/tfl/SKILL.md | Modifié |
| skills/tfl/scripts/performance.py | Modifié |
| skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| tests/test_free_performance.py | Modifié |
| tests/test_pllm_free_fallback.py | Modifié |
| tests/test_throughput_measurement.py | Créé |
| openspec/changes/archive/2026-10-25-fix-buffered-stream-throughput/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-buffered-stream-throughput/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-buffered-stream-throughput/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-buffered-stream-throughput/specs/pllm-evaluation/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-buffered-stream-throughput/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-buffered-stream-throughput/STATISTIQUES.md | Créé après archive |

Totaux : 27 fichiers initiaux modifiés + sept nouveaux chemins = 34 livrables.
Les nouveaux chemins sont un test et six fichiers finaux dans l'archive.
Aucun fichier initial supprimé ; les cinq artefacts déplacés par l'archive
sont comptés une seule fois à leur destination finale.

Contrôle ciblé de 58 empreintes initiales : 27 modifications attendues et
31 fichiers inchangés, aucun chemin initial manquant. AGENTS.md, PROJECT.md,
DEVOPS.md, CM, wrappers et références API conservent leurs empreintes.
Le contrôle est ciblé, sans inventaire récursif global ni inspection Git.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate fix-buffered-stream-throughput --strict. |
| Python 3.14.9 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 222 tests. |
| Python 3.13.5 | Exécutée et réussie : /usr/bin/python3.13 -B -m unittest discover -s tests -q ; 222 tests. |
| Syntaxe et imports | Exécutée et réussie : py_compile avec cfile temporaire sous tests ; 25 fichiers compilés, treize scripts importés et Europe/Paris résolu par branche. |
| Skills | Exécutée et réussie : quick_validate.py sur les deux distributions PLLM/TFL, quatre validations. |
| Parité | Exécutée et réussie : quatre moteurs identiques ; scripts et SKILL.md PLLM/TFL identiques entre distributions. |
| Ancienne formule | Recherche ciblée sans résultat dans les sources/documentations concernées ; aucune division par la fenêtre de contenu pour les tokens/s. |
| Release | Exécutée et réussie : VERSION, pyproject.toml, README et cinq manifestes à 0.7.3. |
| Encodage avant archive | Exécutée et réussie : 33 livrables UTF-8/LF sans BOM. |
| Périmètre | Exécutée et réussie : 58 empreintes, 27 modifications prévues, 31 fichiers inchangés et aucune suppression initiale. |
| OpenSpec avant archive | Exécutée et réussie : ciblé strict, global standard 9/9 et strict 9/9 sans avertissement. |
| État préparatoire | Exécutée et réussie : openspec status --change fix-buffered-stream-throughput --json ; isComplete=true. |
| Archive unique | Exécutée et réussie : openspec archive fix-buffered-stream-throughput --json --yes ; 2026-10-25-fix-buffered-stream-throughput. |
| OpenSpec après archive | Exécutée et réussie : openspec validate --all et --all --strict ; 8/8 sans avertissement dans les deux cas. |
| Rapport final | Exécutée et réussie : six sections, 34 chemins uniques présents, totaux 27 + 7, quatorze tâches, UTF-8/LF, quatre blocs identiques et aucun change actif. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
Les compilations utilisent explicitement chaque interpréteur et ne laissent
pas de bytecode dans les sources. Les modifications après les suites finales
concernent les textes et un commentaire, sans changement de logique.

Couverture nouvelle : cas Mercury, invariance au regroupement des fragments,
bloc unique, durée non arrondie, Chat Completions/Responses/Messages,
comptages global et réponse, durées nulles/négatives/non finies, compteurs
invalides, flux tronqués/incomplets, absence d'ancienne mesure, classement,
exclusion TFL sur débit moyen, séparation de mémoire et publication du profil.
Aucun échec ni avertissement dans les tests et validations exécutés.

Le contrôle de clôture a vérifié les six sections, 34 chemins uniques présents,
totaux 27 + 7, quatorze tâches, UTF-8/LF sans BOM, quatre blocs synchronisés,
versions et parité, puis l'absence de change actif.

Non exécutés : benchmarks fournisseurs réels, installation dans une nouvelle
session Codex, mise à jour TCU, publication distante ou adoption OpenCode.
Non pertinents : frontend, ShellCheck et migration système. Aucun outil
supplémentaire de lint/types n'est configuré dans pyproject.toml.

## 5. Accès web

Aucun accès web pendant cette SCM. Le diagnostic utilise le rapport local
du test réel précédent et le code existant. Les essais de correction sont
déterministes et hors ligne. La durée et les volumes web, ainsi que les coûts
fournisseur de cette qualification : N/A, aucune collecte réelle instrumentée.
Les résultats antérieurs ne sont pas recyclés comme validation actuelle.

## 6. Synthèse et cohérence documentaire

La correction 0.7.3 est livrée localement et archivée. Le débit moyen sur la
requête complète évite l'amplification par la fenêtre de réception des
fragments ; les portées de comptage restent distinctes et la méthode est
explicite. Ce débit ne prétend pas mesurer une vitesse intrinsèque fournisseur.

| Élément | État et preuve |
|---|---|
| Projet réel | Correction et intégrations couvertes par 222 tests sur chaque branche Python. |
| AGENTS.md | Inchangé, empreinte conservée ; règles de périmètre, secrets et cycle OpenSpec appliquées. |
| PROJECT.md | Inchangé, empreinte conservée ; architecture, catalogue et version commune restent exacts. |
| TECHNICAL.md | Mis à jour, Prérequis d'exécution et Validation : durée, protocole, mémoire et tests. |
| BUILD.md | Mis à jour, Protocole 8 de débit moyen : distribution et relance après installation distincte. |
| DEVOPS.md | Inchangé, empreinte conservée ; chemins Python/OpenSpec et référentiel de prompts utilisés. |
| README.md | Mis à jour ; 0.7.3, sens du débit et comparabilité historique. |
| CHANGELOG.md | Mis à jour dans Unreleased ; quatre entrées correction/profil/mémoire/release. |
| openspec/specs | Quatre exigences ciblées synchronisées ; global standard/strict 8/8 après archive. |

Écart documentaire préexistant hors périmètre, signalé sans correction :
« Classement interne par performances » mentionne encore « Go avant général
pour le repli modes 1/2 », alors que 1/2 sont payants et les gratuits autonomes
sont en 3/4. Ce libellé reste intact et ne change pas le calcul ni l'ordre
effectivement exécuté. La cohérence affirmée porte sur le périmètre corrigé.

ORCHESTRATED_CODING.md est non applicable à cette SCM directe.
Les seuils numériques sont préservés, mais classement et éligibilité peuvent
changer. Les anciens débits ne sont pas directement comparables. Les preuves
locales qualifient le code ; installation, activation et mesures fournisseur
actuelles restent des étapes distinctes.
État : TERMINÉ pour le périmètre local validé, son archive unique et son rapport.

