# STATISTIQUES — harmonize-free-model-performance

Projet : Tools Codex. Release locale : 0.7.2. Session SCM directe.
Périmètre validé par le développeur, avec deux corrections explicites :
exclure de TFL les gratuits échoués et demander HIGH, avec le seul repli XHIGH
lorsque pris en charge. Rapport produit après l'archive native unique du
25 octobre 2026. Aucune compétence de statistiques pilotées n'a été invoquée.

## 1. Statistiques générales

Tous les gratuits PLLM/TFL exigent prix d'entrée/sortie nuls vérifiés et
variantes compatibles, contexte ≥1M, réponse complète et comptage fiable,
TTFT <30 s et débit >20 tokens/s. Le repli gratuit OpenRouter de PLLM 5 utilise
ces mêmes seuils ; les payants PLLM gardent <90 s et >15 tokens/s.

TFL mesure les gratuits des trois catalogues sans consulter quota, crédit ou
solde. Les gratuits échoués ou non mesurables sont retirés de models ; leurs
preuves restent dans excluded_models et free_performance_results. Le tableau
commun des essais gratuits suit les trois tableaux fournisseurs, dont les
huit colonnes sont conservées. Une section vide après qualification bloque
la publication et préserve les rapports précédents.

Tous les benchmarks PLLM et les gratuits TFL demandent HIGH. XHIGH est le seul
repli autorisé lorsque HIGH est indisponible et XHIGH pris en charge. Une
annonce explicite peut choisir XHIGH avant requête ; un HTTP 400 propre au
paramètre d'effort permet un unique passage XHIGH annoncé, avec ses propres
paliers. Aucun repli sur 401/403/429, troncature ou seuil non satisfait, aucun
niveau inférieur. Les paliers restent 1024, 2048, 4096, 8192 et 120 s par
requête ; un changement d'effort peut recalculer cette séquence.
Le niveau effectif et les paramètres demandés sont tracés ; ils ne prouvent
pas une profondeur interne de raisonnement mesurée.

Le moteur performance.py est embarqué à l'identique dans les quatre paquets
PLLM/TFL. Les comptes partagés 1/3 et 2/4, les priorités, routes et contrôles
de ressources applicables sont préservés. TFL utilise la clé Go sélectionnée
pour Go/général et la clé OpenRouter existante, environnement puis référence
historique du trousseau. Aucune valeur de clé n'est passée au modèle ou aux
rapports. La mémoire distingue Low, HIGH et XHIGH ; un ancien succès Low ne
valide ni n'amorce un benchmark HIGH. Les paquets restent autonomes.

La qualification TFL est datée et dépend du compte utilisé. Un échec peut
supprimer du catalogue un candidat accessible avec un autre compte jusqu'à
une nouvelle collecte TFL. PLLM ne réintègre pas les exclus. Cette limite
résulte de la correction de périmètre explicitement demandée.

Suites finales : 208 tests sous Python 3.13.5 et 208 sous Python 3.14.9,
soit 416 exécutions finales pour 208 tests distincts. Dix-sept nouveaux tests
avec sous-cas sur les distributions ; les 191 tests antérieurs sont conservés.
Quatre fichiers de tests existants sont adaptés pour HIGH, les ressources
embarquées et le fixture JSON strict, sans test désactivé ni attente affaiblie.

24 compilations par branche, soit 48 au total. Treize imports de scripts par
branche, soit 26, et Europe/Paris résolu. Six SKILL.md validés. Quinze tâches
préparatoires cochées. Neuf exigences synchronisées (cinq PLLM, quatre TFL),
aucune exigence ajoutée, supprimée ou renommée ; scénarios conservés et enrichis.
Le titre historique du contrat Low est conservé, son texte impose désormais
explicitement HIGH/XHIGH.

Avant archive : ciblé strict valide, global standard et strict 9/9.
Après archive : standard et strict 8/8 sans avertissement. L'archive renvoie
specsUpdated=false et des totaux nuls parce que les neuf exigences étaient
déjà synchronisées avant son exécution ; aucun delta supplémentaire à fusionner.

Durée totale de session, temps modèle/outils, tokens, cache, coûts et quotas :
N/A, télémétrie non instrumentée. Les essais intermédiaires ne créent pas de
tests distincts supplémentaires.

## 2. Messages et outils

Session SCM directe lancée via le skill prompt, référentiel résolu depuis
DEVOPS.md. Le skill skill-creator guide la mise à jour des instructions et
leur validation. Aucun sous-agent, pilotage OpenCode/CAB ou collecte de
statistiques pilotées. Messages et appels exhaustifs : N/A, non agrégés.

Les tests simulent réseau, trousseau, erreurs et streaming. Les temporaires
de tests et compilation sont créés sous tests puis nettoyés. Les contrôles
vérifient les clés différentes par fournisseur, l'absence de secret/message
privé publié et l'absence d'appels de quotas pendant les tests gratuits TFL.
Les corps d'erreurs restent filtrés et les routes OpenCode sont validées.

Aucune inspection ou opération Git, installation de profil, exécution TCU,
activation, génération fournisseur réelle, modification de service ou d'agent
OpenCode. Aucune lecture de clé par l'agent. La documentation officielle est
consultée en lecture seule pour les contrats HIGH/XHIGH.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins finaux relatifs :

| Chemin | Opération |
|---|---|
| .codex/commands/pllm.md | Modifié |
| .codex/commands/tfl.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| openspec/specs/pllm-evaluation/spec.md | Modifié |
| openspec/specs/tfl-catalog/spec.md | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/cm/skills/cm/SKILL.md | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/skills/tfl/SKILL.md | Modifié |
| plugins/tfl/skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| pyproject.toml | Modifié |
| skills/cm/SKILL.md | Modifié |
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| skills/tfl/SKILL.md | Modifié |
| skills/tfl/scripts/test_fournisseur_llm.py | Modifié |
| tests/test_extension_qualification.py | Modifié |
| tests/test_pllm_free_fallback.py | Modifié |
| tests/test_pllm_http_diagnostics.py | Modifié |
| tests/test_pllm_ttft.py | Modifié |
| plugins/pllm/skills/pllm/scripts/performance.py | Créé |
| plugins/tfl/skills/tfl/scripts/performance.py | Créé |
| skills/pllm/scripts/performance.py | Créé |
| skills/tfl/scripts/performance.py | Créé |
| tests/test_free_performance.py | Créé |
| openspec/changes/archive/2026-10-25-harmonize-free-model-performance/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-harmonize-free-model-performance/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-harmonize-free-model-performance/tasks.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-harmonize-free-model-performance/specs/pllm-evaluation/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-harmonize-free-model-performance/specs/tfl-catalog/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-harmonize-free-model-performance/STATISTIQUES.md | Créé après archive |

Totaux : 29 fichiers initiaux modifiés + onze nouveaux chemins = 40 livrables.
Les onze nouveaux chemins sont quatre moteurs, un fichier de tests et six
fichiers finaux dans l'archive. Aucun fichier initial supprimé ; les artefacts
déplacés par l'archivage sont comptés une seule fois à leur destination finale.

Contrôle ciblé de 50 empreintes initiales : 29 modifications attendues et
21 fichiers inchangés, aucun chemin initial manquant. Les références API,
AGENTS.md, PROJECT.md, DEVOPS.md et les métadonnées de nom visible PLLM
restent préservés. Ce contrôle est ciblé, sans inventaire récursif global ni
inspection de l'état Git. Les installations utilisateur ne sont pas actualisées.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate harmonize-free-model-performance --strict. |
| Python 3.14.9 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 208 tests. |
| Python 3.13.5 | Exécutée et réussie : /usr/bin/python3.13 -B -m unittest discover -s tests -q ; 208 tests. |
| Syntaxe et imports | Exécutée et réussie : py_compile avec cfile temporaire sous tests ; 24 fichiers compilés, 13 scripts importés et Europe/Paris résolu par branche. |
| Skills | Exécutée et réussie : quick_validate.py sur les deux distributions de PLLM, TFL et CM, soit six validations. |
| Parité | Exécutée et réussie : scripts/skills PLLM et TFL, skills CM et quatre moteurs identiques. |
| Release | Exécutée et réussie : VERSION, pyproject.toml, README et cinq manifestes à 0.7.2. |
| Encodage avant archive | Exécutée et réussie : 39 livrables UTF-8/LF sans BOM. |
| Périmètre ciblé | Exécutée et réussie : 50 empreintes, 29 modifications prévues, 21 fichiers inchangés et aucune suppression initiale. |
| OpenSpec avant archive | Exécutée et réussie : ciblé strict, global standard 9/9 et global strict 9/9 sans avertissement final. |
| État préparatoire | Exécutée et réussie : openspec status --change harmonize-free-model-performance --json ; isComplete=true. |
| Archive native unique | Exécutée et réussie : openspec archive harmonize-free-model-performance --json --yes ; archive 2026-10-25-harmonize-free-model-performance. |
| OpenSpec après archive | Exécutée et réussie : openspec validate --all et --all --strict ; 8/8 sans avertissement dans les deux cas. |
| Rapport final | Exécutée et réussie : six sections, 40 chemins uniques présents, totaux 29 + 11, quinze tâches, UTF-8/LF, neuf blocs identiques et aucun change actif. |

OpenSpec utilise /home/devops/.local/npm/bin/openspec. Les compilations
emploient explicitement les deux interpréteurs. La clôture a vérifié six
sections, 40 chemins uniques présents, totaux 29 + 11, quinze tâches,
UTF-8/LF sans BOM, neuf blocs identiques aux deltas et aucun change actif.

Couverture nouvelle : prix/variantes et contexte, limites 30/20 strictes,
réponse complète/troncature, mesures absentes ou non finies, métadonnées
invalides, HIGH/XHIGH et budgets documentés, refus HTTP ciblés, mémoire Low,
clés distinctes, publication TFL filtrée, audit des exclus, aucune fuite,
rapports préservés si vide et paquet isolé avec moteur local.

Échecs intermédiaires corrigés : le même fixture volontairement non JSON
strict manquait d'id dans les deux distributions ; son id est ajouté et sa
valeur NaN est conservée pour vérifier le rejet avant publication. Quatre
avertissements de paragraphes normatifs trop longs ont été résolus en
déplaçant les détails dans les scénarios. Aucun échec ou avertissement final.

Non exécutés : benchmarks fournisseurs authentifiés, installation dans une
nouvelle session Codex, mise à jour TCU, publication distante et adoption
OpenCode. Non pertinents : frontend, ShellCheck et migration système.
Aucun outil de lint/types supplémentaire n'est configuré dans pyproject.toml.

## 5. Accès web

Documentation primaire consultée pour vérifier les paramètres et capacités
de raisonnement :

- OpenRouter : https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
- Claude : https://platform.claude.com/docs/en/build-with-claude/effort
- DeepSeek : https://api-docs.deepseek.com/guides/thinking_mode/

Deux appels à l'outil web : recherche technique, puis ouverture de la page
OpenRouter. Le nombre de requêtes HTTP internes, temps et volumes web : N/A,
non instrumentés. Aucun appel de génération ou de quota fournisseur réel.
Les exemples et essais de code utilisent uniquement des données simulées.

Les sources distinguent niveaux demandés, budgets et capacités par modèle :
HIGH/XHIGH ne sont pas supposés disponibles sur tout modèle. Les paramètres
réellement demandés sont conservés et aucun repli inférieur n'est effectué.

## 6. Synthèse et cohérence documentaire

L'évolution 0.7.2 est livrée localement et archivée. Tous les gratuits
partagent les seuils renforcés ; TFL exclut ses échecs avec preuves ; les
benchmarks demandent HIGH avec le seul repli XHIGH pris en charge. Les
payants conservent leurs seuils et contrôles. Les preuves locales qualifient
l'implémentation, sans annoncer une disponibilité fournisseur réelle.

| Élément | État et preuve |
|---|---|
| Projet réel | 208 tests sur chacune des branches Python 3.13/3.14 ; filtrage gratuit et raisonnement couverts. |
| AGENTS.md | Inchangé, empreinte conservée ; périmètre, secrets et OpenSpec appliqués. |
| PROJECT.md | Inchangé, empreinte conservée ; organisation, catalogue et rôles restent exacts. |
| TECHNICAL.md | Mis à jour ; moteur commun, HIGH/XHIGH, seuils, authentification et exclusions. |
| BUILD.md | Mis à jour ; empaquetage, benchmarks gratuits et limites par compte. |
| DEVOPS.md | Inchangé, empreinte conservée ; chemins des outils et prompts utilisés. |
| README.md | Mis à jour ; 0.7.2, seuils, raisonnement et comportement TFL. |
| CHANGELOG.md | Mis à jour dans Unreleased ; quatre entrées, sans publication distante annoncée. |
| openspec/specs | Cinq exigences PLLM et quatre TFL synchronisées ; global standard/strict 8/8 après archive. |

ORCHESTRATED_CODING.md est non applicable à cette SCM directe.
La compatibilité HIGH/XHIGH réelle dépend du modèle et du fournisseur.
Une qualification TFL dépend du compte ; un autre compte peut avoir des accès
différents. Les échecs sont conservés comme preuves datées. Installation,
activation et performances fournisseur actuelles restent distinctes.
État : TERMINÉ pour le périmètre local validé, son archive unique et son rapport.

