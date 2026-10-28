# Codes de lot — Tools Codex

## Périmètre et autorisation

Relevé et annotation rétrospective : **28 octobre 2026** (Europe/Paris).
Plan **ACL-TOOLS-20261028-R1**, validé intégralement par le développeur dans la conversation ACL.
Couverture : **0 change actif, 45 archives codées, 45 correspondances code/change vérifiées**.
Aucun code antérieur attesté lors du relevé initial, aucune consolidation, aucune réservation supplémentaire.
Amendement **ACL-PRM03-R1**, validé par le développeur : attribution rétrospective de PRM03
à support-acl-prompt le **28 octobre 2026**, sans modification des 44 codes précédents.

Chaque attribution ci-dessous est une annotation rétrospective du 28 octobre 2026,
pas le code d’origine de l’archive. La preuve est le titre principal du proposal.md lié.
Les dates de création, identifiants, dossiers, tâches et preuves historiques restent inchangés.

## Convention

Préfixe significatif suivi d’un numéro séquentiel sur deux chiffres, extensible
au-delà de 99 sans renuméroter les codes acquis. Le rattachement suit la responsabilité
principale documentée dans les cadrages et dans la proposition liée à chaque ligne.
Les libellés génériques Proposal et Proposition sont conservés lorsqu’ils existaient.

Tri initial dans chaque famille : date du dossier d’archive, puis identifiant technique
par ordre lexicographique. Cette date sert au tri ; elle ne certifie ni date de création,
ni priorité, ni dépendance. Les codes sont désormais occupés dans tous les états.
Toute extension devra vérifier aussi les réservations et partir au-delà du maximum
utilisé ou réservé ; aucune renumérotation pour combler les trous.

| Famille | Responsabilité et rattachement | Nombre |
|---|---|---:|
| CAB | Pont d’approbation, contrôleur et distribution historiques | 7 |
| EXT | Contrats transverses, versionnement, présentation et distribution | 5 |
| PRM | Résolution et lancement des prompts depuis DEVOPS | 3 |
| UPD | Mise à jour et installation des briques par TCU | 4 |
| TFL | Collecte, sélection et publication des catalogues | 6 |
| PLL | Politiques, sélection, diagnostics et mémoire propres à PLLM | 10 |
| LLM | Mesures, efforts et preuves partagés TFL/PLLM | 7 |
| LM | Gestion et normalisation de la liste noire partagée | 2 |
| SCH | Ordonnancement conditionnel de TFL puis PLLM | 1 |
| **Total** | | **45** |

## Correspondances vérifiées

Chemins relatifs à openspec/. État constaté le 28 octobre 2026.

| Code | Identifiant technique | Titre | État | Dossier | Preuve d’attribution |
|---|---|---|---|---|---|
| CAB01 | correct-plugin-layout-traceability | Corriger la traçabilité de l’arborescence du plugin CAB | Archivé | [2026-09-11-correct-plugin-layout-traceability](changes/archive/2026-09-11-correct-plugin-layout-traceability/) | [Titre principal](changes/archive/2026-09-11-correct-plugin-layout-traceability/proposal.md) |
| CAB02 | establish-project-consistency | Établir la cohérence du projet CAB | Archivé | [2026-09-11-establish-project-consistency](changes/archive/2026-09-11-establish-project-consistency/) | [Titre principal](changes/archive/2026-09-11-establish-project-consistency/proposal.md) |
| CAB03 | fix-decision-request-id-correlation | Corriger la corrélation des décisions par requestId | Archivé | [2026-09-11-fix-decision-request-id-correlation](changes/archive/2026-09-11-fix-decision-request-id-correlation/) | [Titre principal](changes/archive/2026-09-11-fix-decision-request-id-correlation/proposal.md) |
| CAB04 | add-manual-cab-decision-mode | Ajouter le mode de décision manuelle CAB | Archivé | [2026-09-15-add-manual-cab-decision-mode](changes/archive/2026-09-15-add-manual-cab-decision-mode/) | [Titre principal](changes/archive/2026-09-15-add-manual-cab-decision-mode/proposal.md) |
| CAB05 | allow-generic-controller-workspace | Accepter un workspace générique pour le contrôleur CAB | Archivé | [2026-09-15-allow-generic-controller-workspace](changes/archive/2026-09-15-allow-generic-controller-workspace/) | [Titre principal](changes/archive/2026-09-15-allow-generic-controller-workspace/proposal.md) |
| CAB06 | fix-native-command-correlation | Corriger la corrélation des commandes natives CAB | Archivé | [2026-09-15-fix-native-command-correlation](changes/archive/2026-09-15-fix-native-command-correlation/) | [Titre principal](changes/archive/2026-09-15-fix-native-command-correlation/proposal.md) |
| CAB07 | add-pending-approval-controller-reminders | Proposition | Archivé | [2026-09-18-add-pending-approval-controller-reminders](changes/archive/2026-09-18-add-pending-approval-controller-reminders/) | [Titre principal](changes/archive/2026-09-18-add-pending-approval-controller-reminders/proposal.md) |
| EXT01 | release-tools-codex-v0-2 | Proposal | Archivé | [2026-09-19-release-tools-codex-v0-2](changes/archive/2026-09-19-release-tools-codex-v0-2/) | [Titre principal](changes/archive/2026-09-19-release-tools-codex-v0-2/proposal.md) |
| EXT02 | document-existing-extension-contracts | Proposition | Archivé | [2026-10-10-document-existing-extension-contracts](changes/archive/2026-10-10-document-existing-extension-contracts/) | [Titre principal](changes/archive/2026-10-10-document-existing-extension-contracts/proposal.md) |
| EXT03 | distribute-cm-plugin | Distribuer le catalogue CM comme plugin | Archivé | [2026-10-19-distribute-cm-plugin](changes/archive/2026-10-19-distribute-cm-plugin/) | [Titre principal](changes/archive/2026-10-19-distribute-cm-plugin/proposal.md) |
| EXT04 | migrate-cm-to-skill | Exposer le catalogue CM comme skill découvrable | Archivé | [2026-10-19-migrate-cm-to-skill](changes/archive/2026-10-19-migrate-cm-to-skill/) | [Titre principal](changes/archive/2026-10-19-migrate-cm-to-skill/proposal.md) |
| EXT05 | uppercase-tools-codex-commands | Commandes Tools Codex en majuscules | Archivé | [2026-10-27-uppercase-tools-codex-commands](changes/archive/2026-10-27-uppercase-tools-codex-commands/) | [Titre principal](changes/archive/2026-10-27-uppercase-tools-codex-commands/proposal.md) |
| LLM01 | fix-buffered-stream-throughput | Corriger le débit face aux flux reçus en rafale | Archivé | [2026-10-25-fix-buffered-stream-throughput](changes/archive/2026-10-25-fix-buffered-stream-throughput/) | [Titre principal](changes/archive/2026-10-25-fix-buffered-stream-throughput/proposal.md) |
| LLM02 | harmonize-free-model-performance | Harmoniser les tests gratuits et le raisonnement | Archivé | [2026-10-25-harmonize-free-model-performance](changes/archive/2026-10-25-harmonize-free-model-performance/) | [Titre principal](changes/archive/2026-10-25-harmonize-free-model-performance/proposal.md) |
| LLM03 | fix-tfl-pllm-model-evidence-and-shared-blacklist | Preuves des modèles et liste noire LM unique | Archivé | [2026-10-26-fix-tfl-pllm-model-evidence-and-shared-blacklist](changes/archive/2026-10-26-fix-tfl-pllm-model-evidence-and-shared-blacklist/) | [Titre principal](changes/archive/2026-10-26-fix-tfl-pllm-model-evidence-and-shared-blacklist/proposal.md) |
| LLM04 | modify-tfl-pllm-reasoning-and-openrouter-eur-filter | Filtrage strict HIGH/XHIGH et plafond OpenRouter en euros | Archivé | [2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter](changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/) | [Titre principal](changes/archive/2026-10-26-modify-tfl-pllm-reasoning-and-openrouter-eur-filter/proposal.md) |
| LLM05 | converge-current-medium-effort | Converger les états courants TFL/PLLM vers Medium | Archivé | [2026-10-27-converge-current-medium-effort](changes/archive/2026-10-27-converge-current-medium-effort/) | [Titre principal](changes/archive/2026-10-27-converge-current-medium-effort/proposal.md) |
| LLM06 | switch-tfl-pllm-reasoning-to-medium | Basculer TFL et PLLM vers le raisonnement Medium | Archivé | [2026-10-27-switch-tfl-pllm-reasoning-to-medium](changes/archive/2026-10-27-switch-tfl-pllm-reasoning-to-medium/) | [Titre principal](changes/archive/2026-10-27-switch-tfl-pllm-reasoning-to-medium/proposal.md) |
| LLM07 | qualify-pllm-catalog-evidence-0-7-20 | Qualifier les preuves TFL/PLLM et aligner Tools Codex 0.7.20 | Archivé | [2026-10-28-qualify-pllm-catalog-evidence-0-7-20](changes/archive/2026-10-28-qualify-pllm-catalog-evidence-0-7-20/) | [Titre principal](changes/archive/2026-10-28-qualify-pllm-catalog-evidence-0-7-20/proposal.md) |
| LM01 | add-lm-shared-model-blacklist | Ajouter LM et une liste noire partagée | Archivé | [2026-10-26-add-lm-shared-model-blacklist](changes/archive/2026-10-26-add-lm-shared-model-blacklist/) | [Titre principal](changes/archive/2026-10-26-add-lm-shared-model-blacklist/proposal.md) |
| LM02 | fix-lm-openrouter-tilde-identifiers | Accepter les préfixes OpenRouter marqués sans contourner LM | Archivé | [2026-10-26-fix-lm-openrouter-tilde-identifiers](changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/) | [Titre principal](changes/archive/2026-10-26-fix-lm-openrouter-tilde-identifiers/proposal.md) |
| PLL01 | add-pllm-free-fallback-auth-diagnostics | PLLM : repli gratuit et sélection par performances | Archivé | [2026-10-25-add-pllm-free-fallback-auth-diagnostics](changes/archive/2026-10-25-add-pllm-free-fallback-auth-diagnostics/) | [Titre principal](changes/archive/2026-10-25-add-pllm-free-fallback-auth-diagnostics/proposal.md) |
| PLL02 | fix-pllm-request-and-rate-limit-diagnostics | Corriger les requêtes Low et les diagnostics HTTP PLLM | Archivé | [2026-10-25-fix-pllm-request-and-rate-limit-diagnostics](changes/archive/2026-10-25-fix-pllm-request-and-rate-limit-diagnostics/) | [Titre principal](changes/archive/2026-10-25-fix-pllm-request-and-rate-limit-diagnostics/proposal.md) |
| PLL03 | split-pllm-free-modes | Séparer les politiques PLLM gratuites | Archivé | [2026-10-25-split-pllm-free-modes](changes/archive/2026-10-25-split-pllm-free-modes/) | [Titre principal](changes/archive/2026-10-25-split-pllm-free-modes/proposal.md) |
| PLL04 | optimize-pllm-first-valid-selection | Arrêter la sélection PLLM au premier candidat valide | Archivé | [2026-10-26-optimize-pllm-first-valid-selection](changes/archive/2026-10-26-optimize-pllm-first-valid-selection/) | [Titre principal](changes/archive/2026-10-26-optimize-pllm-first-valid-selection/proposal.md) |
| PLL05 | prioritize-paid-model-price | Classer les modèles payants PLLM par prix | Archivé | [2026-10-26-prioritize-paid-model-price](changes/archive/2026-10-26-prioritize-paid-model-price/) | [Titre principal](changes/archive/2026-10-26-prioritize-paid-model-price/proposal.md) |
| PLL06 | add-openrouter-catalog-and-free-policy | Étendre PLLM aux modèles OpenRouter payants et gratuits | Archivé | [2026-10-27-add-openrouter-catalog-and-free-policy](changes/archive/2026-10-27-add-openrouter-catalog-and-free-policy/) | [Titre principal](changes/archive/2026-10-27-add-openrouter-catalog-and-free-policy/proposal.md) |
| PLL07 | pllm-current-medium-and-openrouter-price-normalization | Proposal | Archivé | [2026-10-27-pllm-current-medium-and-openrouter-price-normalization](changes/archive/2026-10-27-pllm-current-medium-and-openrouter-price-normalization/) | [Titre principal](changes/archive/2026-10-27-pllm-current-medium-and-openrouter-price-normalization/proposal.md) |
| PLL08 | fix-pllm-catalog-provenance-and-auth-diagnostics | Provenance TFL et diagnostics d'authentification PLLM | Archivé | [2026-10-28-fix-pllm-catalog-provenance-and-auth-diagnostics](changes/archive/2026-10-28-fix-pllm-catalog-provenance-and-auth-diagnostics/) | [Titre principal](changes/archive/2026-10-28-fix-pllm-catalog-provenance-and-auth-diagnostics/proposal.md) |
| PLL09 | fix-pllm-performance-memory-schema | Corriger le schéma de la mémoire de performance PLLM | Archivé | [2026-10-28-fix-pllm-performance-memory-schema](changes/archive/2026-10-28-fix-pllm-performance-memory-schema/) | [Titre principal](changes/archive/2026-10-28-fix-pllm-performance-memory-schema/proposal.md) |
| PLL10 | restore-mode5-paid-benchmark | Rétablir le benchmark des payants OpenRouter en mode5 | Archivé | [2026-10-28-restore-mode5-paid-benchmark](changes/archive/2026-10-28-restore-mode5-paid-benchmark/) | [Titre principal](changes/archive/2026-10-28-restore-mode5-paid-benchmark/proposal.md) |
| PRM01 | add-prompt-dispatcher | Ajouter le résolveur et le lancement des prompts du projet | Archivé | [2026-10-19-add-prompt-dispatcher](changes/archive/2026-10-19-add-prompt-dispatcher/) | [Titre principal](changes/archive/2026-10-19-add-prompt-dispatcher/proposal.md) |
| PRM02 | unbound-prompt-runs | Lever la borne des RUN PROMPT et uniformiser leurs libellés | Archivé | [2026-10-28-unbound-prompt-runs](changes/archive/2026-10-28-unbound-prompt-runs/) | [Titre principal](changes/archive/2026-10-28-unbound-prompt-runs/proposal.md) |
| PRM03 | support-acl-prompt | Prise en charge d’ACL dans PROMPT | Archivé | [2026-10-28-support-acl-prompt](changes/archive/2026-10-28-support-acl-prompt/) | [Titre principal — annotation rétrospective du 28 octobre 2026](changes/archive/2026-10-28-support-acl-prompt/proposal.md) |
| SCH01 | add-user-llm-refresh-schedule | Planifier TFL puis PLLM dans la session utilisateur | Archivé | [2026-10-26-add-user-llm-refresh-schedule](changes/archive/2026-10-26-add-user-llm-refresh-schedule/) | [Titre principal](changes/archive/2026-10-26-add-user-llm-refresh-schedule/proposal.md) |
| TFL01 | add-general-opencode-catalog-to-tfl | Catalogue général OpenCode dans TFL | Archivé | [2026-10-25-add-general-opencode-catalog-to-tfl](changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/) | [Titre principal](changes/archive/2026-10-25-add-general-opencode-catalog-to-tfl/proposal.md) |
| TFL02 | add-tfl-live-provider-pricing | Actualisation automatique des tarifs TFL | Archivé | [2026-10-25-add-tfl-live-provider-pricing](changes/archive/2026-10-25-add-tfl-live-provider-pricing/) | [Titre principal](changes/archive/2026-10-25-add-tfl-live-provider-pricing/proposal.md) |
| TFL03 | collect-go-modalities-and-routing-dynamically | Métadonnées Go dynamiques dans TFL | Archivé | [2026-10-25-collect-go-modalities-and-routing-dynamically](changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/) | [Titre principal](changes/archive/2026-10-25-collect-go-modalities-and-routing-dynamically/proposal.md) |
| TFL04 | select-openrouter-models-by-live-filters | Sélection dynamique OpenRouter | Archivé | [2026-10-25-select-openrouter-models-by-live-filters](changes/archive/2026-10-25-select-openrouter-models-by-live-filters/) | [Titre principal](changes/archive/2026-10-25-select-openrouter-models-by-live-filters/proposal.md) |
| TFL05 | allow-empty-tfl-provider-selections | Publier les sélections TFL vides sans bloquer les autres catalogues | Archivé | [2026-10-26-allow-empty-tfl-provider-selections](changes/archive/2026-10-26-allow-empty-tfl-provider-selections/) | [Titre principal](changes/archive/2026-10-26-allow-empty-tfl-provider-selections/proposal.md) |
| TFL06 | remove-general-opencode-tfl | Retrait du catalogue général OpenCode de TFL | Archivé | [2026-10-26-remove-general-opencode-tfl](changes/archive/2026-10-26-remove-general-opencode-tfl/) | [Titre principal](changes/archive/2026-10-26-remove-general-opencode-tfl/proposal.md) |
| UPD01 | add-tcu-updater | Ajouter la mise à jour contrôlée des briques Tools Codex | Archivé | [2026-10-19-add-tcu-updater](changes/archive/2026-10-19-add-tcu-updater/) | [Titre principal](changes/archive/2026-10-19-add-tcu-updater/proposal.md) |
| UPD02 | manage-prompt-component | Gérer le composant PROMPT et les canaux indépendants dans TCU | Archivé | [2026-10-19-manage-prompt-component](changes/archive/2026-10-19-manage-prompt-component/) | [Titre principal](changes/archive/2026-10-19-manage-prompt-component/proposal.md) |
| UPD03 | tcu-plain-check | Accepter check comme argument de contrôle TCU | Archivé | [2026-10-19-tcu-plain-check](changes/archive/2026-10-19-tcu-plain-check/) | [Titre principal](changes/archive/2026-10-19-tcu-plain-check/proposal.md) |
| UPD04 | install-missing-tools-codex-components | Installation systématique des briques Tools Codex absentes | Archivé | [2026-10-28-install-missing-tools-codex-components](changes/archive/2026-10-28-install-missing-tools-codex-components/) | [Titre principal](changes/archive/2026-10-28-install-missing-tools-codex-components/proposal.md) |

## Entrées provisoires sans code

Aucune : les 45 attributions validées sont présentes dans leurs supports.
L’entrée provisoire SCM-ACL-R1 a été remplacée par PRM03 après validation d’ACL-PRM03-R1.
Cette section ne constitue ni une série ni une réservation.

## Limites et anomalies historiques

- CAB03 conserve la tâche 2.3 non cochée : test E2E historiquement empêché par une approbation antérieure pendante. Son état runtime actuel est NON VÉRIFIÉ ; aucune sonde n’a été lancée.
- CAB05 ne possède pas de design.md ; sa proposition et ses tâches permettent son identification.
- Neuf archives n’ont pas de STATISTICS.md : CAB01 à CAB07, EXT01 et LLM03. ACL ne crée ni ne régénère de statistiques historiques.
- CAB01 à CAB07 constituent un historique distinct du catalogue courant ; leur provenance reste non qualifiée selon PROJECT.md.
- Aucun BLOCKER.md ni BLOCKERS.md n’a été trouvé dans les changes examinés.

Ces constats ne rouvrent aucune archive et ne requalifient ni livraison, installation,
activation ou disponibilité actuelle. Voir la [cartographie](../DEVELOPMENT_MAP.md).
