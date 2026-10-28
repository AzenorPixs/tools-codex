# STATISTIQUES — add-pllm-free-fallback-auth-diagnostics

Projet : Tools Codex. Release locale : 0.6.0. Session SCM directe.
Périmètre validé explicitement : diagnostics d'authentification visibles,
repli gratuit Go/OpenCode général et OpenRouter après épuisement confirmé,
retour aux payants, classement débit maximal puis TTFT minimal et archivage.
La décision finale 0.6.0 remplace la proposition antérieure 0.6.6.
Rapport produit après l'archivage natif unique du 25 octobre 2026.

## 1. Statistiques générales

Modes 1/2 : comparaison des payants TFL Go quand les quotas sont disponibles ;
après épuisement confirmé, comparaison des seuls gratuits TFL Go puis OpenCode
général. Mode 3 : payants OpenRouter avec crédit, gratuits après épuisement.
Le rétablissement des ressources rétablit les payants. Les changements de
catégorie observés pendant les contrôles sont bornés et écartent les gagnants
de la catégorie précédente. Aucun refus d'authentification ni donnée manquante
ne déclenche de repli gratuit. Les gratuits du catalogue général sont inclus ;
leur accès effectif et Low restent nécessaires à une réussite.

Tous les candidats autorisés sont évalués. Les réussites sont classées par
débit décroissant, TTFT croissant puis ordre TFL stable. La priorité entre
modes reste 1 à 4. Les deux catalogues OpenCode utilisent le débit global ;
OpenRouter et DeepSeek le débit de réponse seule. Les seuils restent TTFT
strictement inférieur à 90 s et débit strictement supérieur à 15 tokens/s.
Les huit colonnes sont conservées, avec diagnostic dans État. Les quotas
réels restent affichés même si un gratuit rend la politique valide.

Dernières suites complètes : 156 tests réussis sous Python 3.13.5 et 156 sous
Python 3.14.9, soit 312 exécutions finales réussies pour 156 tests distincts.
La nouvelle suite contient 24 tests, exécutés sur les deux distributions par
sous-cas : sélection payante/gratuite, retour au payant, meilleur débit,
départage TTFT/ordre TFL, priorité, refus HTTP/SSE, secrets inaccessibles,
quotas indisponibles, absence de gratuit, échec de mesure, changement de
catégorie, oscillations bornées, forçages, même ID sur deux catalogues,
prix/contexte/modalités/route non admissibles, Low et mémoire par configuration.
Les flux simulés vérifient aussi le calcul du débit et l'en-tête de session,
sans publier sa valeur. Les tests existants sont adaptés au contrôle initial
et à la comparaison de tous les candidats ; aucun test n'est désactivé.

Cinq fichiers Python compilés sur chacune des deux branches ; deux scripts
importés par branche et fuseau Europe/Paris résolu. Deux SKILL.md validés.
Scripts et skills autonomes/embarqués identiques. Quatorze tâches préparatoires
cochées. Delta : quatre exigences ajoutées, six modifiées, zéro suppression ou
renommage. Avant archive : ciblé strict valide, global standard 9/9 et strict
9/9. Après correction documentaire post-fusion : global standard 8/8 et strict
8/8, sans avertissement ; aucun change actif.

Durée totale, temps modèle/outils, tokens, cache, coûts et quotas : N/A,
télémétrie non instrumentée. Les répétitions de suites ne sont pas comptées
comme des tests distincts. Aucune mesure fournisseur réelle n'est déduite des
tests simulés ou des évaluations PLLM antérieures à ce SCM.

## 2. Messages et outils

SCM résolu depuis le référentiel déclaré par DEVOPS.md avec le skill Prompt.
Le skill skill-creator encadre l'actualisation des consignes et leur validation.
Aucun sous-agent, pilotage OpenCode/CAB ni skill de statistiques pilotées.
Messages et appels exhaustifs : N/A, non agrégés. Commandes système exécutées
une par une. Aucune inspection de l'état Git, opération Git, installation de
profil ou modification de service. Aucun fichier du trousseau ni stockage
privé OpenCode n'est lu pendant la qualification SCM.

Les suites simulent réseau, quotas et trousseau. Les temporaires sont créés
sous tests puis nettoyés. Le moteur confine les clés aux processus locaux,
filtre les erreurs HTTP/SSE et conserve seulement le nom de l'en-tête de
session. Les tests vérifient l'absence de message privé dans les diagnostics.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins finaux relatifs ci-dessous.

| Chemin | Opération |
|---|---|
| .codex/commands/pllm.md | Modifié |
| BUILD.md | Modifié |
| CHANGELOG.md | Modifié |
| README.md | Modifié |
| TECHNICAL.md | Modifié |
| VERSION | Modifié |
| pyproject.toml | Modifié |
| plugins/cm/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/.codex-plugin/plugin.json | Modifié |
| plugins/prompt/.codex-plugin/plugin.json | Modifié |
| plugins/tcu/.codex-plugin/plugin.json | Modifié |
| plugins/tfl/.codex-plugin/plugin.json | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| tests/test_extension_qualification.py | Modifié |
| tests/test_pllm_ttft.py | Modifié |
| openspec/specs/pllm-evaluation/spec.md | Synchronisé puis texte raccourci |
| tests/test_pllm_free_fallback.py | Créé |
| openspec/changes/archive/2026-10-25-add-pllm-free-fallback-auth-diagnostics/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-pllm-free-fallback-auth-diagnostics/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-add-pllm-free-fallback-auth-diagnostics/tasks.md | Créé puis archivé et complété |
| openspec/changes/archive/2026-10-25-add-pllm-free-fallback-auth-diagnostics/specs/pllm-evaluation/spec.md | Créé puis archivé et texte raccourci |
| openspec/changes/archive/2026-10-25-add-pllm-free-fallback-auth-diagnostics/STATISTIQUES.md | Créé après archive |

Totaux finaux : 19 fichiers initiaux modifiés et six nouveaux chemins, soit
25 chemins livrés. Aucun fichier initial supprimé ; les artefacts déplacés par
l'archive sont comptés une seule fois à leur destination finale.

Contrôle ciblé initial de 43 empreintes : 18 modifications prévues et 25 fichiers
inchangés avant archive ; après synchronisation, 19 modifications et 24 fichiers
inchangés. La spécification principale explique l'unique modification
supplémentaire. Les six nouveaux chemins sont comptés séparément. L'archive
précédente contrôlée, add-general-opencode-catalog-to-tfl, reste identique.
Il s'agit d'un contrôle ciblé sans inspection Git ; aucun inventaire global de
l'état Git n'est revendiqué. Aucune copie installée dans un profil n'est actualisée.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate add-pllm-free-fallback-auth-diagnostics --strict, après conservation des scénarios existants. |
| PLLM ciblé initial | Exécutée et réussie : Python 3.14, unittest discover -s tests -p 'test_pllm*.py' -v ; 23 tests à ce stade, avant cinq ajouts complémentaires. |
| Suite finale Python 3.13 | Exécutée et réussie : /usr/bin/python3 -B -m unittest discover -s tests -q ; 156 tests. |
| Suite finale Python 3.14 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 156 tests. |
| Syntaxe et imports | Exécutée et réussie : py_compile des deux scripts PLLM et trois tests concernés, cfile temporaire sous tests, puis imports des deux scripts, sur les deux branches. |
| Format des skills | Exécutée et réussie : quick_validate.py du skill-creator sur skills/pllm et plugins/pllm/skills/pllm. |
| Release et parité | Exécutée et réussie : VERSION, pyproject.toml, README et cinq manifestes à 0.6.0 ; scripts et skills identiques. |
| Encodage | Exécutée et réussie : UTF-8/LF sans BOM sur les 23 fichiers contrôlés avant archive, puis rapport et artefacts finaux. |
| Périmètre | Exécutée et réussie : comparaison des 43 empreintes initiales avec les seules modifications attendues. |
| OpenSpec avant archive | Exécutée et réussie : ciblé strict, global standard 9/9, global strict 9/9. |
| Statut ciblé | Exécutée et réussie : openspec status --change add-pllm-free-fallback-auth-diagnostics --json ; isComplete=true. |
| Archive native unique | Exécutée et réussie : openspec archive add-pllm-free-fallback-auth-diagnostics --json --yes ; specsUpdated=true, quatre ajouts et six modifications. |
| OpenSpec après archive | Exécutée et réussie après correction du paragraphe trop long : openspec validate --all et --all --strict ; 8/8 dans les deux cas. |
| Cohérence du delta | Exécutée et réussie : dix blocs normatifs identiques entre delta archivé et spécification principale ; aucun change actif. |
| Rapport final | Six sections, 25 chemins existants et uniques, totaux 19 + 6, quatorze tâches préparatoires et UTF-8/LF vérifiés. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
Échecs intermédiaires corrigés : scénarios omis du premier delta, assertion de
test forcé devenue inexacte avec le contrôle initial, avertissements de fermeture
des fixtures HTTP, puis texte normatif trop long détecté après fusion. Ce
dernier texte a été raccourci dans la spécification et le delta archivé sans
changement de règle et sans réarchivage. Aucun échec ou avertissement final.

Non exécutés : authentification et benchmarks réels des fournisseurs,
installation de profil, publication et invocation dans une nouvelle session.
Non pertinents : build frontend et ShellCheck. Aucun lint ni outil de types
supplémentaire n'est configuré pour ce périmètre Python.

## 5. Accès web

Lectures des documentations officielles publiques Go, catalogue général OpenCode
et variantes gratuites OpenRouter. Elles décrivent les routes, le client propre,
la session, les restrictions de certains gratuits au client natif et les limites
propres aux variantes gratuites. Le développeur confirme l'inclusion du
catalogue général pour son agent de codage natif. Le moteur conserve son
User-Agent PLLM et ne fabrique aucune identité de client.

Sources : https://opencode.ai/v2/docs/console/go/ ;
https://opencode.ai/v2/docs/console/models/ ;
https://openrouter.ai/docs/guides/routing/model-variants/free .
Ces lectures ne prouvent ni accès authentifié ni mesure de génération.
Nombre de requêtes HTTP effectives, temps et volumes web : N/A, non agrégés.
Aucune requête authentifiée, de quota ou de génération pendant ce SCM.

## 6. Synthèse et cohérence documentaire

Le correctif est livré localement en 0.6.0. Les catégories sont exclusives,
les erreurs d'authentification visibles et les mesures actuelles nécessaires.
Le repli gratuit n'altère pas les quotas affichés. Le classement est interne
au mode et les priorités restent fixes. La mémoire liée à chaque configuration,
les forçages, le silence de active et les remplacements atomiques sont conservés.
La qualification hors ligne ne garantit pas l'accès réel des fournisseurs.

| Élément | État et preuve |
|---|---|
| Projet réel | Replis, classement et diagnostics couverts par les suites finales ; aucun changement de service ou de profil. |
| AGENTS.md | Inchangé, empreinte conservée ; périmètre, secrets et cycle OpenSpec appliqués. |
| PROJECT.md | Inchangé, empreinte conservée ; Objectif et Catalogue actuel restent exacts pour PLLM. |
| TECHNICAL.md | Mis à jour ; catégories exclusives, fournisseur réel, mémoire, mesures et qualification. |
| BUILD.md | Mis à jour ; catalogue requis, repli général et limites d'accès réel. |
| DEVOPS.md | Inchangé, empreinte conservée ; outils déclarés et référentiel de prompt utilisés. |
| README.md | Mis à jour ; 0.6.0, payants/gratuits, retour des ressources et classement. |
| CHANGELOG.md | Mis à jour ; quatre entrées Unreleased pour comportement, diagnostics et version. |
| openspec/specs | Six modifications et quatre ajouts synchronisés ; dix blocs identiques au delta archivé, standard et strict 8/8. |

ORCHESTRATED_CODING.md est non applicable à cette session SCM directe.
État : TERMINÉ pour la livraison locale et son archivage unique. Aucun blocage
final ; installation, publication et qualification fournisseur réelle restent
distinctes et n'ont pas été effectuées.
