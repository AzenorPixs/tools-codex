# Tools Codex

Version de release : `0.7.2`.

La source de vérité de cette version est le fichier [`VERSION`](VERSION).
La métadonnée Python du dépôt reprend cette release. Les branches Python
supportées sont 3.13 et 3.14 (`>=3.13,<3.15`), avec qualification hors ligne.

Utilisez **`$cm`** pour afficher le catalogue des commandes maison : `$cm`,
`$pllm`, `$tfl`, `$tcu` et `$prompt`, leurs syntaxes et descriptions. `/cm` délègue au même skill via sa commande source.
Sa source est [`skills/cm/SKILL.md`](skills/cm/SKILL.md), exposée dans ce
projet via le lien relatif `.agents/skills/cm`. Le plugin
[`cm`](plugins/cm/.codex-plugin/plugin.json) est également référencé dans la
marketplace Tools Codex et embarque le même skill. L'installation du plugin,
l'installation autonome hors du projet et le contrôle de découverte sont décrits dans
[`BUILD.md`](BUILD.md#skill-catalogue-cm). Les plugins PLLM/TFL n'installent pas
ce catalogue à eux seuls.

Choisissez le plugin CM ou la distribution autonome selon l'usage ; les deux
chargés simultanément peuvent produire deux entrées. Leur disponibilité dans
les sources ne démontre pas une installation dans un profil Codex.

PLLM accepte `--tfl-catalog CHEMIN` pour des plugins installés séparément.
Les six politiques sont évaluées par priorité :

| Modes | Candidats | Conditions spécifiques |
|---|---|---|
| 1/2 | Payants Go des comptes actuels | Quotas disponibles ; épuisement → rouge et invalide, sans gratuit |
| 3/4 | Gratuits vérifiés Go puis OpenCode général, comptes de 1/2 | Aucun contrôle de quota ; contexte ≥1M, réponse complète, TTFT <30 s et débit >20 tokens/s |
| 5 | Ancien mode 3 OpenRouter | Crédit pour payants ; repli gratuit après épuisement confirmé |
| 6 | Ancien mode 4 DeepSeek direct | Solde utilisable positif |

Les payants gardent TTFT <90 s et débit >15 tokens/s ; tous les gratuits,
y compris le repli OpenRouter de 5, exigent <30 s et >20 tokens/s. Les filtres TFL,
HIGH/XHIGH autorisé, transports et diagnostics s'appliquent partout. Un gratuit reste soumis
aux limitations fournisseur. Dans chaque mode, le débit maximal puis le TTFT
minimal désignent le gagnant sans changer les priorités 1 à 6.
Tous les benchmarks demandent HIGH ; XHIGH est le seul repli autorisé si
HIGH est indisponible et XHIGH pris en charge. Les références de secrets restent inchangées. Les historiques à quatre modes
sont adaptés au schéma 2 sans sélection actuelle héritée ; les nouveaux 3/4
commencent sans mesure ni apprentissage. Un fichier corrompu est préservé.
Le schéma 2 nécessite une copie des anciennes données pour revenir à l'ancien
évaluateur. Les forçages OpenRouter 31–33 deviennent 51–53 ; 31–33 et 41–43
ciblent désormais la liste gratuite admissible des nouveaux modes 3/4.
Pour Chat Completions OpenCode, HIGH est envoyé sans le paramètre thinking
spécifique à d'autres contrats. Hors le repli d'effort XHIGH autorisé, les refus HTTP 400 et les limitations 429
arrêtent les paliers du candidat ; le diagnostic filtré et le Retry-After
disponible restent visibles, sans répétition aux budgets supérieurs ni
promesse de disponibilité après l'échéance indiquée.
TFL exclut les prix non finis et publie un catalogue JSON strict.
À chaque génération, TFL récupère les tarifs OpenCode Go dans sa documentation
officielle et les tarifs OpenRouter dans son API. Le JSON conserve la source,
la date et les variantes tarifaires. Une collecte indispensable en échec
préserve les rapports précédents sans reprendre silencieusement leurs prix.
La sélection OpenRouter examine tout le catalogue API sans liste prédéfinie :
contexte ≥ 1M, coût moyen de base ≤ 0,50 USD/M, sorties admissibles et blacklist.
Les gratuits vérifiés doivent aussi réussir les tests HIGH/XHIGH : réponse
complète, TTFT <30 s et débit >20 tokens/s. Les échecs sont retirés de models
et leurs preuves sont conservées dans les exclusions JSON. Un nouveau modèle admissible apparaît sans modification du code.
Pour OpenCode Go, modalités et routage sont également collectés depuis les
déclarations API et models.dev, sans listes statiques de modèles. Le JSON
conserve les sources et dates ; une information absente reste non vérifiée,
une contradiction ou une URL de routage non sûre bloque la publication.
Une route documentée reste distincte d'un test réel de génération : les
gratuits TFL sont désormais testés, les payants restent un catalogue tarifaire.
Le rapport comprend trois tableaux fournisseurs : OpenCode Go, catalogue général OpenCode,
puis OpenRouter, suivis du tableau détaillé des tests gratuits. Le catalogue général est collecté publiquement et conserve
ses propres tarifs et métadonnées `opencode`, indépendants de `opencode-go`.
Les trois catalogues exigent contexte ≥ 1M et coût moyen ≤ 0,50 USD/M ; une
variante gratuite à 200K reste exclue. La section JSON supplémentaire
`opencode` fournit également les gratuits PLLM des modes 3/4 décrits plus haut.
TFL ne consulte aucun quota pour ses tests gratuits. Une section devenue vide
après qualification bloque la publication et préserve les rapports précédents.
Un échec dépend du compte TFL utilisé ; les exclus ne sont pas réintégrés par
PLLM. Le moteur scripts/performance.py est embarqué dans chaque paquet pour
préserver son autonomie, sans nouvelle dépendance Python.

Les prérequis et limites de qualification sont décrits dans
[`BUILD.md`](BUILD.md) et [`TECHNICAL.md`](TECHNICAL.md).

Utilisez **`$tcu check`** pour contrôler les mises à jour et **`$tcu`** pour
les appliquer aux briques déjà installées depuis la marketplace et GitHub.
TCU est aussi reconnu via `/TCU` ; le fichier de commande n'enregistre pas une
slash native. Le plugin [`tcu`](plugins/tcu/.codex-plugin/plugin.json) conserve
le [skill autonome](skills/tcu/SKILL.md) et son script identiques à la copie
embarquée. Sauvegardes, adoption et conflits sont décrits dans BUILD. TCU ne
modifie pas le checkout de développement. Seul `prompt` absent est installé
automatiquement, avec son skill embarqué vérifié et son wrapper de commande.
Les conflits locaux préservent leurs cibles sans bloquer les mises à jour
indépendantes ; le bilan reste partiel et le code de sortie non nul.

Le nouveau [skill prompt](skills/prompt/SKILL.md) utilise exclusivement le
référentiel indiqué dans le `DEVOPS.md` du projet courant :

```text
/prompt LIST
/prompt CISMP3
/prompt 1CISMP3
```

`LIST` affiche l'index. `CISMP3` lance le cycle du RUN CISMP3. `1CISMP3` borne
ce RUN à un change complet, archivage, statistiques puis arrêt de la session
de codage. Les codes sont en MAJUSCULE et les alias GCM/GCMP sélectionnent
GSCM.md/GSCMP.md. Le skill est directement invocable avec `$prompt CODE`.
Les sources de prompts restent externes ; les conditions du prompt choisi
continuent de s'appliquer. Les arguments et l'installation du plugin sont
décrits dans [BUILD](BUILD.md#utilisation-de-prompt).
