# PROJECT.md — Tools Codex

## Objectif

Tools Codex rassemble des extensions internes destinées à enrichir Codex :

* des plugins maison ;
* des skills maison ;
* des commandes maison.

Le projet centralise ces ressources afin qu'elles puissent être versionnées,
maintenues et distribuées de manière cohérente.

## Version de release

La version de release de Tools Codex est déclarée dans `VERSION`. Les plugins
publiés par la marketplace doivent déclarer la même version de release dans
leur manifeste.

## Périmètre

Le projet contient uniquement les ressources d'extension propres à Codex et
leur documentation associée. Chaque ressource conserve un périmètre explicite
et indépendant afin de limiter les dépendances entre extensions.

Les archives OpenSpec relatives à CAB présentes dans ce dépôt constituent un
historique distinct du catalogue actuel ci-dessous. Leur provenance n'est pas
qualifiée par les cadrages actuels ; leur présence ne signifie pas que Tools
Codex distribue aujourd'hui CAB. Elles sont conservées inchangées et ne
constituent ni des changes actifs ni une liste de fonctionnalités à réimplémenter.

## Organisation

Les commandes sources CM/PLLM/TFL/TCU/LM/prompt sont conservées dans :

```text
.codex/commands/
```

Les plugins maison sont stockés dans des répertoires dédiés :

```text
plugins/<NOM_DU_PLUGIN>/
```

Les skills maison autonomes sont stockés dans des répertoires dédiés :

```text
skills/<NOM_DU_SKILL>/
```

Le skill `cm`, invocable avec `$cm`, fournit le catalogue des commandes maison.
Il est distribué sous forme autonome et dans le plugin `plugins/cm/` référencé
par la marketplace Tools Codex. Les deux copies restent identiques.
Il est découvert dans ce projet via le lien relatif `.agents/skills/cm` vers
`skills/cm/`. Les fichiers de `.codex/commands/` ne sont pas enregistrés
automatiquement comme commandes slash natives. L'installation autonome hors
du projet est décrite dans `BUILD.md`.

Un plugin peut également embarquer ses propres skills dans son répertoire
`skills/`, selon les conventions applicables de Codex.

## Catalogue actuel

| Type | Nom | Rôle |
|---|---|---|
| Plugin | `lm` | Gère la liste noire partagée, appliquée avant sélection et tests TFL/PLLM. |
| Plugin | `prompt` | Liste et lance les prompts du projet depuis son DEVOPS et son index. |
| Plugin | `tcu` | Met à jour les briques installées depuis marketplace et GitHub. |
| Plugin | `cm` | Distribue le catalogue des commandes maison, invocable avec `$cm`. |
| Plugin | `pllm` | Évalue une politique de modèles LLM et l'applique à une session OpenCode autorisée. |
| Plugin | `tfl` | Compare Go puis OpenRouter ; conserve le catalogue général dans le JSON. |
| Skill | `cgpt` | Affiche les quotas Codex disponibles. |
| Skill | `coding-session-statistics` | Produit un bilan auditable d'une session de codage ou de pilotage. |
| Skill | `pllm` | Expose la politique PLLM également en dehors du plugin. |
| Skill | `tfl` | Expose le rapport TFL également en dehors du plugin. |
| Skill | `cm` (`$cm`) | Affiche le catalogue des invocations `$cm`, `$pllm`, `$tfl`, `$tcu`, `$lm` et `$prompt`. |
| Skill | `prompt` (`$prompt`) | LIST et 38 actions en MAJUSCULE, dont les huit variantes à un change. |
| Skill | `lm` (`$lm`) | LIST, ADD et REMOVE ; mimo-v2.5 exclu par défaut. |
| Commande source | `/LM` | Délègue au skill LM sans enregistrer automatiquement une slash native. |
| Commande source | `/cm` | Délègue au catalogue CM, avec une seule entrée prompt et sans exécution. |
| Commande source | `/prompt` | Délègue au skill prompt avec LIST ou CODE ; ne crée pas une slash native. |
| Skill | `tcu` (`$tcu`) | Met à jour les briques présentes ; `check` contrôle sans écriture. |
| Commande source | `/TCU` | Délègue au skill TCU ; ne crée pas une slash native. |
| Commande source | `/pllm` | Instructions historiques de lancement de l'évaluation PLLM ; skill invocable avec `$pllm`. |
| Commande source | `/tfl` | Instructions historiques de lancement du rapport TFL ; skill invocable avec `$tfl`. |

Les skills `cm`, `pllm`, `tfl`, `tcu`, `lm` et `prompt` sont volontairement fournis sous forme autonome et
embarquée afin de couvrir les deux modes de distribution. Le skill
`coding-session-statistics` s'appuie sur `cgpt` pour les relevés de quota
hebdomadaires lorsqu'ils sont demandés.

TCU est le nom final de l'outil proposé initialement comme TFU. Il distingue
les plugins de la marketplace et les copies autonomes issues de GitHub. Il
actualise les briques présentes et peut installer le seul composant prompt
absent : plugin, skill embarqué vérifié et wrapper. Les conflits locaux ne
bloquent pas les opérations indépendantes ; ils restent visibles dans le
bilan partiel. Les checkouts de développement ne sont pas modifiés.
Le lien `.agents/skills/tcu` expose le skill autonome dans ce projet. Les modes
de contrôle, sauvegardes et conflits sont décrits dans BUILD et TECHNICAL.

## Principes

Les extensions doivent privilégier :

* une responsabilité claire ;
* la compatibilité avec Codex ;
* la documentation des comportements et prérequis ;
* l'absence de secrets dans les sources ;
* une évolution indépendante et traçable de chaque plugin, skill ou commande.

Les évolutions fonctionnelles du projet sont décrites et validées dans
OpenSpec avant leur implémentation, conformément aux règles du dépôt.

## Lancement de prompts

`/prompt LIST` affiche l'index déclaré par le DEVOPS.md du projet courant.
`/prompt CODE` ou `$prompt CODE` charge le prompt correspondant et exécute
son processus jusqu'à ses conditions terminales ou une condition imposant
une décision. Aucun prompt n'est embarqué dans Tools Codex.

GCM et GCMP sont les alias validés de GSCM.md et GSCMP.md. CISMP1 à CISMP8
conservent le RUN demandé et le cycle normal de CISMP.md. Les variantes
1CISMP1 à 1CISMP8 bornent le même RUN à un change complet, suivi de
l'archivage, des statistiques puis de l'arrêt de la session de codage.

## Liste noire des modèles

LM partage CODEX_HOME/lm/blacklist.json entre toutes les installations TFL/PLLM,
avec ~/.codex par défaut. La valeur initiale mimo-v2.5 est appliquée sans
création de fichier ; une liste vide explicite permet son retrait. TFL et
PLLM filtrent avant classement, sélection et génération, indépendamment des
anciens catalogues ou succès mémorisés. Le stockage hors cache est conservé
par TCU. Les exclusions permanentes historiques restent distinctes.

## Rafraîchissement utilisateur planifié

Les six plugins embarquent un bootstrap SessionStart soumis à la confiance
native de Codex. TCU applique le même bootstrap après vérification des sources ;
les copies autonomes fournissent aussi l'installateur. Une seule installation
utilisateur déclenche TFL puis PLLM normal à 00 h et 12 h Europe/Paris.
L'application ou un CLI interactif Codex doit être ouvert pour cet utilisateur.
Un quota Codex épuisé ou inconnu empêche TFL et PLLM ; le quota est relu avant
PLLM. Les passages manqués ne sont pas rattrapés. L'installation n'exécute
aucun LLM ; un échec TFL empêche PLLM et la réutilisation d'un ancien catalogue.
La qualification des sources reste distincte de l'activation du timer réel.
