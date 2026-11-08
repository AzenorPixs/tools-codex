# Statistiques globales

**NCA — Nombre de changes analysés : 36**

## Périmètre et durée

| Indicateur | Nombre de changes | Valeur (jours décimaux ; NCMA en changes achevés/jour) |
|---|---|---|
| DGCT — Temps total de développement du projet via l’IA | 0 | N/A |
| DGCTSPA — Temps total de développement du projet via l’IA hors pauses et attentes | 0 | N/A |
| NJT — Ecart entre le premier change archivé à l’archivage du dernier | 36 | N/A |
| NCMA — Changes achevés par jour (NCA / NJT) | 36 | N/A |

| Indicateur | Nombre de changes | Valeur en heures décimales |
|---|---|---|
| DGCTM — Durée globale moyenne pour 0 changes | 0 | N/A |
| DGCTSPAM — Durée moyenne par change hors pauses et attentes pour 0 changes | 0 | N/A |

N/A : bornes complètes et durées de session compatibles indisponibles ; les durées partielles de tests ou de clôture ne les remplacent pas.

## Agents intervenants et LLM

Les agents de codage et les agents orchestrateurs ont utilisé les dernières versions disponibles au moment de chaque change, conformément au contexte déclaré par le développeur.

### LLM des agents de codage

| Nombre de changes réalisés ou partiellement réalisés | Modèle de LLM | Niveau de raisonnement | Pourcentage de NCA |
|---|---|---|---|
| 36 | N/A | N/A | 100,00 % |

Les rapports décrivent du codage direct. Le modèle exact et son niveau de raisonnement ne sont pas renseignés ; les modèles testés par le produit ne désignent pas les modèles des codeurs.

## Performances des LLM de codage OpenCode

N/A : aucune participation d’OpenCode comme codeur attestée. Aucune ligne de performance complète disponible.

| Indicateur | Valeur |
|---|---|
| TMTM total moyen (s) | N/A |
| Débit minimal total moyen (tokens/s) | N/A |
| Débit moyen total moyen (tokens/s) | N/A |
| Débit maximal total moyen (tokens/s) | N/A |

## Consommation de tokens, coûts et compactions des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Tokens d’entrée | N/A | N/A |
| Tokens de sortie | N/A | N/A |
| Tokens de raisonnement | N/A | N/A |
| Tokens de cache lus | N/A | N/A |
| Tokens de cache écrits | N/A | N/A |
| Total natif des tokens | N/A | N/A |
| Compactions achevées | N/A | N/A |

| Devise du coût de production déclaré | Total | Moyenne par change |
|---|---|---|
| N/A | N/A | N/A |

N/A : mesures de production non instrumentées ; les métriques des sondes et benchmarks fournisseur sont exclues.

## Messages et outils des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Messages | N/A | N/A |
| Appels d’outils | N/A | N/A |

| Rôle des messages | Nombre | Pourcentage |
|---|---|---|
| Utilisateur | N/A | N/A |
| Assistant | N/A | N/A |

Les messages « utilisateur » peuvent provenir de l’orchestrateur et ne représentent pas nécessairement des messages humains.

| Outil | Nombre d’appels | Pourcentage |
|---|---|---|
| N/A | N/A | N/A |

| Résultat technique des appels | Nombre | Pourcentage |
|---|---|---|
| Terminés | N/A | N/A |
| Erreurs techniques | N/A | N/A |
| En cours | N/A | N/A |

N/A : aucun comptage exhaustif et comparable des messages ou des appels natifs n’est disponible.

## Autorisations des opérations des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Demandes distinctes | N/A | N/A |

| Statut | Nombre de demandes | Pourcentage |
|---|---|---|
| Approuvées | N/A | N/A |
| Refusées | N/A | N/A |
| Expirées | N/A | N/A |
| Annulées | N/A | N/A |

N/A : les accords de périmètre sont documentés sans décompte exhaustif des demandes distinctes et de leurs statuts.

## Fichiers et volume du code actuel

| Mesure | Cumul | Moyenne par change |
|---|---|---|
| Écritures exécutées | N/A | N/A |
| Fichiers distincts touchés par change | 1133 | 34,333 |

Le nombre de fichiers touchés cumule les destinations distinctes renseignées par change, sans recompter leur déplacement d’archive. Le nombre d’écritures reste N/A faute de comptage exhaustif.

| Périmètre | Lignes de code | Lignes de commentaires |
|---|---|---|
| Global | 15972 | 225 |
| cgpt | 86 | 1 |
| cm | 0 | 0 |
| coding-session-statistics | 0 | 0 |
| lm | 732 | 16 |
| pllm | 2372 | 24 |
| prompt | 356 | 6 |
| tcu | 1436 | 8 |
| tfl | 2270 | 22 |
| Moteur commun TFL/PLLM | 3056 | 52 |
| Ordonnancement TFL/PLLM | 5664 | 96 |

Les lignes physiques non vides sont comptées lexicalement ; les docstrings sont des commentaires et une ligne mixte contribue aux deux compteurs. Les sources maintenues des distributions autonome et embarquée sont incluses ; liens, tests, données, documentation, dépendances et artefacts générés sont exclus. Les modules partagés sont rattachés à leur responsabilité documentée, sans sous-total parent redondant.

## Commandes des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Commandes exécutées | N/A | N/A |

| Résultat des commandes exécutées | Nombre | Pourcentage |
|---|---|---|
| Code de sortie nul | N/A | N/A |
| Code de sortie non nul | N/A | N/A |

| Famille de commandes | Nombre | Pourcentage |
|---|---|---|
| N/A | N/A | N/A |

N/A : les sous-ensembles de qualification consignés ne constituent pas des totaux exhaustifs de commandes de production.

## Accès web des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Appels aux outils web | 3 | 0,120 |

| Résultat | Nombre | Pourcentage |
|---|---|---|
| Appels web réussis | 2 | N/A |

| Type d’appel web | Nombre | Pourcentage |
|---|---|---|
| Recherche | 1 | 33,33 % |
| Consultation | 2 | 66,67 % |

| Type d’appel web | Outil | URL consultée ou requête de recherche | Résultat |
|---|---|---|---|
| Consultation | N/A | https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28 ; https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28 | Réussie ; deux pages dans un seul appel |
| Recherche | N/A | N/A — requête technique non consignée | N/A |
| Consultation | N/A | https://openrouter.ai/docs/guides/best-practices/reasoning-tokens | Réussie |

Le pourcentage de réussite est N/A : le résultat de la recherche n’est pas individualisé. Les autres consultations et recherches décrites sans appels dénombrables ou sans détail individuel restent N/A. Les lectures API sans outil web et les connexions fournisseur sont exclues.

## Validation et livraison des codeurs

| Mesure | Total | Moyenne par change |
|---|---|---|
| Tests exécutés dans les bilans finaux | 14698 | 408,278 |
| Fichiers ayant passé un contrôle syntaxique | 436 | 12,824 |
| Tâches OpenSpec prouvées et terminées | 276 | 11,500 |

| Résultat des tests finaux | Nombre | Pourcentage |
|---|---|---|
| Tests finaux réussis | 14698 | 100,00 % |
| Tests finaux échoués | 0 | 0,00 % |

| Catégorie de tests | Nombre |
|---|---|
| Suites Python unittest — répartition unitaire/intégration non ventilée | 14698 |

| Validations OpenSpec | Réussies | Échouées | Réussite | Échec |
|---|---|---|---|---|
| Standard | 26 | 0 | 100,00 % | 0,00 % |
| Strict | 101 | 12 | 89,38 % | 10,62 % |

Les suites ciblées recouvrant les suites globales ne sont pas additionnées. Les exécutions finales sur des interpréteurs différents restent distinctes. Les fichiers contrôlés syntaxiquement sont dédupliqués par change. Une validation OpenSpec groupée compte pour une exécution, indépendamment du nombre d’éléments ; les reprises documentées en échec puis réussies restent distinctes. Les mesures non établies dans un rapport sont exclues des sommes et des dénominateurs.

## Synthèse transversale des codeurs

| Domaine | Nombre d’appels | Pourcentage des appels |
|---|---|---|
| Écritures de fichiers | N/A | N/A |
| Commandes | N/A | N/A |
| Web | N/A | N/A |
| Autres outils | N/A | N/A |
| Total | N/A | N/A |
