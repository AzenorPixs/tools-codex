# STATISTIQUES — fix-pllm-request-and-rate-limit-diagnostics

Projet : Tools Codex. Release locale : 0.6.1. Session SCM directe.
Périmètre et version explicitement validés par le développeur avant écriture :
contrats Low, diagnostics HTTP filtrés, traitement de Retry-After, arrêt des
paliers HTTP 400/429, tests, synchronisation des distributions et archivage.
Rapport produit après l'archivage natif unique du 25 octobre 2026.

## 1. Statistiques générales

Chat Completions OpenCode Go et général envoie reasoning_effort=low sans
thinking. Responses, Messages, DeepSeek direct et OpenRouter conservent leurs
contrats propres. Un protocole OpenCode inconnu ne reçoit pas les paramètres
DeepSeek. Low, le prompt, les seuils et les types de débit sont préservés.

Les erreurs HTTP sont lues sur au plus 64 Kio puis fermées. Le rapport conserve
uniquement statut, code connu, paramètre connu, indicateurs de limitation et
Retry-After exploitable. Les secondes entières et dates HTTP avec fuseau sont
acceptées ; absence, format invalide et débordement restent indisponibles.
Un HTTP 400 ou 429 arrête les paliers de ce candidat, puis les autres candidats
autorisés continuent avec leurs propres contrôles. Aucun message libre, corps
brut, compte, clé ou valeur de session n'est publié. L'échéance affichée en
heure de Paris n'est pas une garantie de succès futur.

Dernières suites complètes : 178 tests réussis sous Python 3.13.5 et 178 sous
Python 3.14.9, soit 356 exécutions finales pour 178 tests distincts. La nouvelle
suite contient 22 tests avec sous-cas pour les deux distributions. Les 156 tests
existants sont conservés sans modification ni désactivation.

Couverture nouvelle : corps Chat Completions et Low, autres contrats préservés,
paramètre refusé, codes connus, absence de fuite, erreurs privées ou non JSON,
corps vide/fermé/interrompu, lecture bornée et réutilisation du diagnostic,
Retry-After numérique/date HTTP, dates passées ou hors plage, HTTP/SSE,
authentification et accès refusés, arrêt au premier 400/429, poursuite d'un
autre candidat, progression après troncature, mémoire du seul succès et
publication JSON/Markdown de l'échec sans contenu privé.

Trois fichiers Python compilés sur chaque branche ; deux scripts importés
par branche et fuseau Europe/Paris résolu. Deux SKILL.md validés. Scripts et
skills autonomes/embarqués identiques. Treize tâches préparatoires cochées.
Delta : deux exigences ajoutées, deux modifiées, zéro suppression ou renommage.
Avant archive : ciblé strict valide, global standard 9/9 et strict 9/9.
Après archive : global standard 8/8 et strict 8/8, sans avertissement ; quatre
blocs normatifs identiques au delta archivé et aucun change actif.

Durée totale, temps modèle/outils, tokens, cache, coûts et quotas : N/A,
télémétrie non instrumentée. Les répétitions de suites ne créent pas de tests
distincts supplémentaires. Les mesures réelles du diagnostic préalable ne
sont pas présentées comme une nouvelle évaluation de disponibilité.

## 2. Messages et outils

SCM est conduit directement avec le référentiel résolu via DEVOPS.md et le
skill Prompt. Les consignes distribuées suivent le skill skill-creator déjà
chargé dans cette conversation. Aucun sous-agent, pilotage OpenCode/CAB ou
skill de statistiques pilotées. Messages et appels exhaustifs : N/A, non agrégés.
Commandes système exécutées une par une ; aucune inspection ou opération Git,
installation de profil, modification de clé, de service ou d'agent OpenCode.

Les tests simulent réseau et trousseau. Les temporaires de tests et compilation
restent sous tests puis sont nettoyés. Les simulations vérifient que les
diagnostics ne publient ni message privé ni valeur de session et ne relisent
pas les corps déjà fermés. Aucune requête fournisseur réelle pendant cette
implémentation et cette qualification hors ligne.

## 3. Fichiers

Racine : /home/devops/datas/tools-codex. Chemins finaux relatifs ci-dessous.

| Chemin | Opération |
|---|---|
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
| skills/pllm/SKILL.md | Modifié |
| skills/pllm/scripts/evaluate.py | Modifié |
| plugins/pllm/skills/pllm/SKILL.md | Modifié |
| plugins/pllm/skills/pllm/scripts/evaluate.py | Modifié |
| openspec/specs/pllm-evaluation/spec.md | Synchronisé par archive native |
| tests/test_pllm_http_diagnostics.py | Créé |
| openspec/changes/archive/2026-10-25-fix-pllm-request-and-rate-limit-diagnostics/proposal.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-pllm-request-and-rate-limit-diagnostics/design.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-pllm-request-and-rate-limit-diagnostics/tasks.md | Créé puis archivé et complété |
| openspec/changes/archive/2026-10-25-fix-pllm-request-and-rate-limit-diagnostics/specs/pllm-evaluation/spec.md | Créé puis archivé |
| openspec/changes/archive/2026-10-25-fix-pllm-request-and-rate-limit-diagnostics/STATISTIQUES.md | Créé après archive |

Totaux SCM : 16 fichiers initiaux modifiés et six nouveaux chemins, soit
22 chemins livrés. Aucun fichier initial supprimé ; les artefacts déplacés
par l'archive sont comptés une seule fois à leur destination finale.

Contrôle ciblé de 44 empreintes initiales : avant archive, 15 changements SCM,
un changement externe et 28 fichiers inchangés ; après synchronisation,
16 changements SCM, un externe et 27 inchangés. Les six nouveaux chemins sont
comptés séparément. Les fichiers Markdown contrôlés de l'archive précédente
add-pllm-free-fallback-auth-diagnostics restent identiques. Le contrôle est
ciblé et n'est pas un inventaire global de l'état Git.

Écart externe préservé : DEVOPS.md porte désormais le début de relevé
2026-10-25T08:34:09Z au lieu de 2026-10-24T21:55:33Z. Substituer uniquement ce
champ dans une copie en mémoire retrouve exactement l'empreinte initiale :
aucun autre contenu n'a changé. Le SCM n'a pas écrit ce fichier ; il ne fait
pas partie des 22 chemins livrés. Les chemins d'outils et prérequis demeurent
cohérents. Les copies installées dans le profil utilisateur restent inchangées.

## 4. Commandes et validations

| Validation | État et preuve |
|---|---|
| Delta avant code | Exécutée et réussie : openspec validate fix-pllm-request-and-rate-limit-diagnostics --strict. |
| Tests ciblés initiaux | Exécutée et réussie : Python 3.14, unittest discover -s tests -p test_pllm_http_diagnostics.py -v ; 19 tests avant trois ajouts de revue. |
| Suite finale Python 3.13 | Exécutée et réussie : /usr/bin/python3 -B -m unittest discover -s tests -q ; 178 tests. |
| Suite finale Python 3.14 | Exécutée et réussie : /home/devops/python/current/bin/python3 -B -m unittest discover -s tests -q ; 178 tests. |
| Syntaxe et imports | Exécutée et réussie : py_compile des deux scripts et du nouveau test, cfile temporaire sous tests ; deux scripts importés et fuseau résolu par branche. |
| Skills | Exécutée et réussie : quick_validate.py sur skills/pllm et plugins/pllm/skills/pllm. |
| Release et parité | Exécutée et réussie : 0.6.1 dans VERSION, pyproject.toml, README et cinq manifestes ; scripts et skills identiques. |
| Encodage | Exécutée et réussie : 20 fichiers contrôlés avant archive en UTF-8/LF sans BOM, puis rapport et chemins finaux. |
| Périmètre | Exécutée et réussie : 44 empreintes, seules modifications SCM prévues et variation externe d'horodatage DEVOPS identifiée puis préservée. |
| OpenSpec avant archive | Exécutée et réussie : ciblé strict, global standard 9/9, global strict 9/9. |
| Statut ciblé | Exécutée et réussie : openspec status --change fix-pllm-request-and-rate-limit-diagnostics --json ; isComplete=true. |
| Archive unique | Exécutée et réussie : openspec archive fix-pllm-request-and-rate-limit-diagnostics --json --yes ; specsUpdated=true, deux ajouts et deux modifications. |
| OpenSpec après archive | Exécutée et réussie : openspec validate --all et --all --strict ; 8/8 dans les deux cas, sans avertissement. |
| Delta synchronisé | Exécutée et réussie : quatre blocs identiques au delta archivé ; aucun change actif. |
| Rapport final | Six sections, 22 chemins existants et uniques, totaux SCM 16 + 6, treize tâches préparatoires, écart externe séparé et UTF-8/LF vérifiés. |

Les commandes OpenSpec utilisent /home/devops/.local/npm/bin/openspec.
Aucun échec ni avertissement dans les tests et validations exécutés. La revue
a complété les tests après les premiers passages réussis, sans affaiblissement
des attentes. Les mesures finales ne confondent pas les 19, 21 puis 22 nouveaux
tests présents aux différentes étapes.

Non exécutés pendant ce SCM : nouvelle évaluation authentifiée des fournisseurs,
mise à jour TCU, publication, installation dans un profil et adoption OpenCode.
Non pertinents : build frontend et ShellCheck. Aucun lint ni outil de types
supplémentaire n'est configuré pour ce périmètre Python.

## 5. Accès web

Aucun nouvel accès web pendant l'implémentation et la qualification. Sources
du diagnostic préalable : documentation Go et catalogue général OpenCode,
RFC 6585 section 4, corps d'erreurs filtrés et cinq sondes de génération
bornées avec quotas contrôlés avant chaque sonde. Les clés sont restées dans
le processus local et aucun résultat PLLM publié n'a été remplacé par ces sondes.

Preuve préalable : retirer uniquement thinking de Beam Go, Low conservé,
budget 1024, donne une réponse complète de 505 tokens, TTFT 1,6694 s et débit
global 388,52 tokens/s. Pour Beam général, le Retry-After de 56249 secondes
indiquait le 26 octobre à 01:00 Europe/Paris ; il ne garantissait pas un succès.
Nemotron général avait également un Retry-After, dont la valeur n'a pas été
extraite. Le compteur exact et sa clé compte/IP restent inconnus.

Références : https://opencode.ai/v2/docs/console/go/ ;
https://opencode.ai/v2/docs/console/models/ ;
https://www.rfc-editor.org/info/rfc6585/ .
Temps et volumes web, consommation et coûts de ces sondes : N/A, non agrégés.
Ces preuves précèdent le code 0.6.1 et ne qualifient pas sa disponibilité actuelle.

## 6. Synthèse et cohérence documentaire

Le correctif 0.6.1 est livré localement et archivé. Les paramètres propres aux
transports sont séparés, les erreurs ne divulguent pas le corps brut et les
400/429 ne provoquent plus d'escalade de budget. Les reprises après troncature,
quotas, catégories payante/gratuite, priorités, classement, mémoire, forçages,
silence de active et publication atomique restent couverts par les suites.

| Élément | État et preuve |
|---|---|
| Projet réel | Correctif couvert par 178 tests sur deux branches Python ; aucun changement d'agent ou service. |
| AGENTS.md | Inchangé, empreinte conservée ; périmètre, secrets et cycle OpenSpec appliqués. |
| PROJECT.md | Inchangé, empreinte conservée ; Catalogue actuel et organisation restent exacts. |
| TECHNICAL.md | Mis à jour ; contrats Low, lecture filtrée, Retry-After et qualification. |
| BUILD.md | Mis à jour ; diagnostics, arrêt des paliers et JSON additif sans migration. |
| DEVOPS.md | Non modifié par SCM ; seul horodatage externe du relevé préservé et contrôlé par empreinte. |
| README.md | Mis à jour ; release 0.6.1 et comportement des refus HTTP. |
| CHANGELOG.md | Mis à jour ; quatre entrées Unreleased, sans publication distante annoncée. |
| openspec/specs | Deux ajouts et deux modifications synchronisés ; quatre blocs identiques, global standard et strict 8/8. |

ORCHESTRATED_CODING.md est non applicable à cette session SCM directe.
État : TERMINÉ pour le périmètre local validé, son archive unique et son
rapport. Aucun blocage final ; la variation externe d'horodatage est signalée.
Les profils installés, la publication et les accès fournisseurs réels restent
distincts et n'ont pas été actualisés pendant cette implémentation.
