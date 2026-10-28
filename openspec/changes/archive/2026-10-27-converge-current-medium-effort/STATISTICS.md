# STATISTIQUES — converge-current-medium-effort

Projet : Tools Codex (`tools-codex`). Session SCM directe du 27 octobre 2026.
Release locale : 0.7.15. Rapport produit après l'archive native
`2026-10-27-converge-current-medium-effort`.

## 1. Statistiques générales

Un change TFL/PLLM spécifié, corrigé, validé et archivé. Les générations,
mesures et sélections courantes demandent exclusivement Medium. Les résultats
PLLM anciens sans preuve explicite de cet effort sont invalidés avant affichage
et sélection ; les données PLLM livrées sont réinitialisées sans résultat
inventé.

La suite complète a réussi : 330 tests sous Python 3.13.5 en 8,321 s. Les
quatre suites ciblées totalisent 53 tests, inclus dans ces 330. Quatorze
fichiers Python ont passé `py_compile`. Quatorze paires de copies autonomes et
embarquées ont été comparées ; les six manifestes, `VERSION`, `pyproject.toml`
et la version du README sont alignés sur 0.7.15. L'encodage UTF-8/LF a été
vérifié pour 52 fichiers avant l'ajout du présent rapport.

OpenSpec strict : 11/11 avant archivage et 10/10 spécifications après
synchronisation. Le change a ajouté deux exigences et scénarios PLLM, ainsi
qu'une exigence et deux scénarios TFL. Durée de session, tokens, coût et cache :
N/A, télémétrie non instrumentée dans SCM.

## 2. Messages et outils

J'ai exécuté directement la session SCM, sans sous-agent, pilotage CAB, session
OpenCode ni compétence de statistiques réservée à SCMP. Le prompt SCM a été
résolu depuis le référentiel indiqué par `DEVOPS.md`. Le périmètre validé couvre
les commandes, skills, scripts, états PLLM distribués, spécifications actives,
cadrages, documentation et release 0.7.15 ; les preuves et historiques restent
préservés.

Les premiers contrôles ont révélé des attentes de version 0.7.14 dans deux
tests, ainsi qu'un filtrage partagé trop strict qui affectait TFL. J'ai corrigé
les attentes et limité la vérification d'effort enregistré aux historiques
PLLM. Un test du registre a aussi conduit à conserver les listes source valides
sans Medium comme preuves historiques, tout en exigeant une preuve Medium pour
l'admission. Les contrôles finaux ont ensuite tous réussi. Agrégat exhaustif
des messages et appels d'outils : N/A, aucune télémétrie SCM disponible.

L'archivage a signalé les intitulés attendus par son modèle et une tâche de
postcondition encore ouverte. J'ai corrigé les intitulés de la proposition,
puis complété la postcondition après création et vérification de ce rapport.
La vérification groupée des archives signale aussi un change antérieur sans
dernière tâche cochée ; cette anomalie du 11 septembre est hors périmètre et
n'affecte pas la validation de la présente archive.

## 3. Fichiers

Inventaire des destinations de ce change, y compris le présent rapport :

| Ensemble | Nombre | Opération |
|---|---:|---|
| Scripts TFL/PLLM, moteurs partagés, preuves et évaluateurs dans les deux distributions | 10 | Validation des efforts historiques, diagnostic générique et parité |
| Tests Python | 4 | Régression historique, registre de preuves et attentes de release |
| Commandes sources | 2 | Contrat Medium des commandes TFL et PLLM |
| Skills autonomes et embarqués | 4 | Consignes opérationnelles harmonisées |
| Références de preuves autonomes et embarquées | 4 | Clarification de l'admission Medium en préservant les sources |
| Cadrages, README, CHANGELOG, VERSION et pyproject.toml | 7 | Cohérence documentaire et release 0.7.15 |
| Manifestes des plugins | 6 | Alignement de la release commune |
| Données PLLM autonomes et embarquées | 6 | Rapports initiaux sans sélection et mémoires vides |
| Spécifications principales | 2 | Contrats PLLM et TFL synchronisés |
| Archive OpenSpec, hors présent rapport | 7 | Métadonnées, README, proposition, conception, tâches et deux deltas |
| Présent rapport | 1 | `STATISTIQUES.md` créé après l'archive |
| **Total** | **53** | **Destinations écrites ou créées par ce change** |

Nombre de lignes ajoutées ou supprimées : N/A, aucun comptage de lignes de
référence n'a été capturé. Aucun secret, profil utilisateur, timer, configuration
personnelle ou rapport fournisseur en cours n'a été modifié. Les preuves
officielles et archives historiques ont été conservées.

## 4. Commandes et validations

| Contrôle | Résultat réel |
|---|---|
| Tests ciblés | `python3 -B -m unittest discover -s tests -p 'test_reasoning_admission.py' -v` : 8 réussis ; `test_model_evidence.py` : 13 ; `test_free_performance.py` : 17 ; `test_extension_qualification.py` : 15 |
| Tests globaux | `python3 -B -m unittest discover -s tests -v` : 330 tests réussis sous Python 3.13.5 |
| Syntaxe Python | `python3 -B -m py_compile` sur 14 scripts et tests modifiés : réussite |
| Versions et parité | Contrôle programmatique : VERSION et pyproject 0.7.15, six manifestes 0.7.15, 14 paires identiques ; réussite |
| Données et encodage | Les rapports PLLM ont six politiques non évaluées en Medium, sélection vide et mémoire vide ; 52 fichiers UTF-8/LF sans CRLF : réussite |
| OpenSpec avant archive | `openspec validate --all --strict` : 11/11 réussis |
| Archivage | `openspec archive converge-current-medium-effort --yes` : réussite ; deux spécifications synchronisées et archive unique créée |
| OpenSpec après archive | `openspec validate --all --strict` : 10/10 réussis ; `openspec validate --archived --strict` : 35/36 réussis, la présente archive est valide, un change du 11 septembre a une tâche incomplète |
| Rapport | Six sections présentes ; UTF-8/LF et totaux vérifiés après écriture |
| Git SCM | Étape distincte après production et vérification du présent rapport, selon les conditions du prompt SCM ; résultat consigné dans la restitution finale |

Binaire OpenSpec : `/home/devops/.local/npm/bin/openspec`. La validation ciblée
du change archivé ne trouve plus de deltas après leur synchronisation native ;
le contrôle de tâches groupé confirme que la présente archive est complète.
Aucun outil ou paquet ajouté. Tests navigateur, SQL, ShellCheck et lint/types :
non pertinents pour ce périmètre Python/Markdown/JSON.

## 5. Accès web

Aucune recherche web, collecte fournisseur, génération de modèle, lecture de
quota, crédit ou solde n'a été lancée. Les preuves de capacités fournisseur
ont été préservées. Qualification de performances réelle et coût fournisseur :
N/A, aucun appel fournisseur.

## 6. Synthèse et cohérence documentaire

| Élément | État et preuve |
|---|---|
| Comportement TFL/PLLM | Medium seul est demandé et admis ; une preuve de capacité ne valide pas un résultat historique dont l'effort effectif n'est pas enregistré comme Medium |
| `AGENTS.md` | Inchangé ; règles de sécurité, OpenSpec, tests et encodage appliquées |
| `PROJECT.md` | Mis à jour : admission fondée sur Medium et mesures antérieures décrites sans en faire des résultats actuels |
| `TECHNICAL.md` | Mis à jour : effort unique, transports, preuves et mémoire PLLM |
| `BUILD.md` | Mis à jour : commandes et qualification actuelle Medium |
| `DEVOPS.md` | Inchangé ; l'inventaire d'environnement reste valable |
| `README.md` | Mis à jour : effort unique et version 0.7.15 |
| `CHANGELOG.md` | Entrée Unreleased ajoutée pour l'invalidation des résultats et la release 0.7.15 ; les entrées historiques restent inchangées |
| OpenSpec | Deux spécifications principales synchronisées ; dix spécifications validées après archive |
| Distributions | Skills, moteurs, preuves et données PLLM autonomes/embarqués alignés ; 14 comparaisons réussies |
| Traces restantes | Les mentions dans les archives, anciennes entrées du changelog, preuves de capacités fournisseur et tests négatifs sont conservées selon le périmètre validé. Une occurrence dans l'URL de tarification `pricing-low-to-high` n'est pas un effort de raisonnement. |

Les installations utilisateur n'ont pas été mises à jour ; elles restent
distinctes de la release locale 0.7.15. Leur prochain lancement avec les
sources corrigées invalidera les anciens résultats incompatibles avant de
publier une nouvelle sélection.
