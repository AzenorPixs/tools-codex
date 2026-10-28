# Tools Codex

Version de release : `0.7.25`.

La source de vérité de cette version est le fichier [`VERSION`](VERSION).
La métadonnée Python du dépôt reprend cette release. Les branches Python
supportées sont 3.13 et 3.14 (`>=3.13,<3.15`), avec qualification hors ligne.

Utilisez **`$cm`** pour afficher le catalogue des commandes maison : `$cm`,
`$pllm`, `$tfl`, `$tcu`, `$lm` et `$prompt`, leurs syntaxes et descriptions. `/CM` délègue au même skill via sa commande source.
Les six commandes sources sont **CM, PLLM, TFL, TCU, LM et PROMPT**, avec
fichiers et déclencheurs en majuscules. Les anciennes graphies restent des
alias ; les noms techniques des skills et invocations $… restent inchangés.
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
Vérifiez la date de la collecte TFL réellement produite : une copie autonome
et une copie du plugin peuvent diverger. Passez explicitement le catalogue
voulu ; PLLM ne relance pas TFL et ne recherche pas dans les configurations
privées. Le JSON trace son chemin, sa date, son âge et les compteurs de
candidats. Une absence de gratuit concerne ce catalogue. Une date non
vérifiable ou future est signalée sans seuil arbitraire de péremption.
Un HTTP 401 au contrôle des quotas est identifié avec sa phase et son endpoint,
sans conclure à un épuisement ou modifier les secrets. Le mode4 continue
indépendamment d'un refus mode2, sans consulter de quota.
Les sept politiques sont évaluées par priorité :

| Modes | Candidats | Conditions spécifiques |
|---|---|---|
| 1/2 | Payants Go des comptes actuels | Quotas disponibles ; épuisement → rouge et invalide, sans gratuit |
| 3/4 | Gratuits vérifiés Go exclusivement, comptes de 1/2 | Aucun contrôle de quota ; contexte ≥1M, Medium, TTFT <30 s et débit >20 tokens/s |
| 5 | Payants OpenRouter | Solde positif, contexte ≥1M et coût moyen ≤0,10 €/M ; benchmark Medium, TTFT <90 s et débit >15 tokens/s |
| 6 | Gratuits OpenRouter | Aucun contrôle de solde ; contexte ≥1M, Medium, TTFT <30 s et débit >20 tokens/s |
| 7 | Ancien mode 4 DeepSeek direct | Solde utilisable positif et benchmark payant Medium |

Les payants benchmarkés 1/2/5/7 gardent TTFT <90 s et débit >15 tokens/s ; les gratuits
3/4/6 exigent <30 s et >20 tokens/s. Le mode5 s'appuie sur les prix vérifiés,
le contexte et le crédit avec benchmark Medium concluant. Les filtres TFL, transports et
diagnostics s'appliquent selon le mode. Essayer les payants Go 1/2 par coût
moyen croissant ; essayer les gratuits 3/4/6 dans l'ordre TFL et retenir le
premier succès. Les priorités 1 à 7 sont fixes. En invocation normale, poursuivre les politiques ;
active s'arrête à la première valide. Le contexte ≥1M est une capacité
d'entrée vérifiée, sans envoi d'un million de tokens pendant le benchmark.
Tous les benchmarks demandent exclusivement Medium ; aucun repli vers un autre effort n'est
autorisé. Les tokens/s représentent désormais une moyenne sur la requête complète,
attente et TTFT inclus, sans extrapolation entre fragments reçus. Le protocole
8 conserve la portée de comptage Go ou OpenRouter/DeepSeek, trace la
durée non arrondie et sépare les anciens succès en mémoire. Une réponse
complète en un bloc reste mesurable. Les anciens débits ne sont pas directement
comparables ; les seuils numériques conservés peuvent modifier le classement
et la qualification. Les références de secrets restent inchangées. Les historiques des schémas 1/2 sont adaptés au schéma 3 sans sélection actuelle héritée ; l'ancien mode5 est réinitialisé, DeepSeek est déplacé au mode7 et le mode6 OpenRouter gratuit commence sans mesure ni apprentissage. Un fichier corrompu est préservé. Le schéma3 nécessite une copie des anciennes données pour revenir à l'ancien évaluateur. Les forçages OpenRouter payants restent 51–53 et les gratuits utilisent 61–63.

PLLM récupère une mémoire sans `schema_version` uniquement si elle contient
`policies` vide ou le seul `mode7` DeepSeek Medium avec identité, profil de
débit du protocole 8 et succès cohérents. Le chargement conserve le fichier
intact ; le prochain succès publie atomiquement le schéma 3. Les mémoires
ambiguës ou corrompues restent refusées et préservées. L'écriture valide et
normalise sa mémoire avant publication pour garantir sa relecture.

Pour Chat Completions OpenCode, Medium est envoyé sans le paramètre thinking
spécifique à d'autres contrats. Un refus HTTP 400 ou une limitation 429
arrêtent les paliers du candidat ; le diagnostic filtré et le Retry-After
disponible restent visibles, sans répétition aux budgets supérieurs ni
promesse de disponibilité après l'échéance indiquée.
Medium désigne l'effort effectivement appliqué ; un alias fournisseur mappé à
High ne valide pas un benchmark Medium.
TFL exclut les prix non finis et publie un catalogue JSON strict.
À chaque génération, TFL récupère les tarifs OpenCode Go dans sa documentation
officielle et les tarifs OpenRouter dans son API. Le JSON conserve la source,
la date et les variantes tarifaires. Une collecte indispensable en échec
préserve les rapports précédents sans reprendre silencieusement leurs prix.
La sélection OpenRouter examine tout le catalogue API sans liste prédéfinie :
contexte ≥ 1M, coût moyen de base ≤0,10 EUR/M au taux BCE vérifié, sorties admissibles et blacklist. TFL conserve les payants sans benchmark ; PLLM mode5 vérifie Medium et ses performances.
Les gratuits vérifiés doivent aussi réussir les tests Medium : réponse
complète, TTFT <30 s et débit >20 tokens/s. Les échecs sont retirés de models
et leurs preuves sont conservées dans les exclusions JSON. Un nouveau modèle admissible apparaît sans modification du code.
Pour OpenCode Go, modalités et routage sont également collectés depuis les
déclarations API et models.dev, sans listes statiques de modèles. Le JSON
conserve les sources et dates ; une information absente reste non vérifiée,
une contradiction ou une URL de routage non sûre bloque la publication.
Une route documentée reste distincte d'un test réel de génération : les
gratuits TFL sont désormais testés, les payants restent un catalogue tarifaire.
Le rapport comprend deux tableaux fournisseurs : OpenCode Go puis OpenRouter,
suivis du tableau détaillé des tests gratuits admissibles à Medium.
OpenCode général n'est plus collecté, testé ou publié. Le JSON contient
seulement opencode_go et openrouter. Les deux catalogues exigent contexte ≥1M ; Medium est requis pour tous les benchmarks PLLM, y compris mode5 ; TFL conserve les payants sans benchmark. Go conserve ≤0,50 USD/M et OpenRouter ≤0,10 EUR/M au dernier taux BCE publié. Les modes PLLM 1/2 utilisent exclusivement les payants Go, 3/4 les gratuits Go, 5 les payants OpenRouter benchmarkés, 6 les gratuits OpenRouter benchmarkés et 7 DeepSeek direct.
TFL ne consulte aucun quota pour ses tests gratuits. Une sélection vide après
filtrage ou qualification ne bloque pas les autres catalogues : les deux
tableaux sont publiés, avec « Aucun modèle admissible » et une synthèse des
exclusions pour un tableau vide. Le JSON conserve les sources, motifs détaillés,
compteurs, selection_status (available ou empty) et exclusion_summary. Même
deux sélections vides issues de collectes valides produisent un rapport frais
et un code zéro. Les erreurs de collecte ou de données indispensables restent
bloquantes et préservent les rapports précédents. Le planning reste inchangé :
son contrôle exige les deux listes models Go/OpenRouter non vides avant PLLM.
Un échec dépend du compte TFL utilisé ; les exclus ne sont pas réintégrés par
PLLM. Le moteur scripts/performance.py est embarqué dans chaque paquet pour
préserver son autonomie, sans nouvelle dépendance Python.

Les prérequis et limites de qualification sont décrits dans
[`BUILD.md`](BUILD.md) et [`TECHNICAL.md`](TECHNICAL.md).

Utilisez **`$tcu check`** pour contrôler les mises à jour et **`$tcu`** pour
actualiser les briques présentes et installer les absentes depuis la marketplace et GitHub.
TCU est aussi reconnu via `/TCU` ; le fichier de commande n'enregistre pas une
slash native. Le plugin [`tcu`](plugins/tcu/.codex-plugin/plugin.json) conserve
le [skill autonome](skills/tcu/SKILL.md) et son script identiques à la copie
embarquée. Sauvegardes, adoption et conflits sont décrits dans BUILD. TCU ne
modifie pas le checkout de développement. Tous les plugins du catalogue officiel,
skills autonomes et commandes sources absents sont installés dans chaque racine
configurée. PROMPT conserve la vérification de son skill embarqué et de son
résolveur avant le wrapper. Plusieurs distributions peuvent afficher plusieurs
entrées d’un même skill. `check` annonce ces installations sans les réaliser.
Les conflits locaux préservent leurs cibles sans bloquer les mises à jour
indépendantes ; le bilan reste partiel et le code de sortie non nul.
TCU crée le nouveau wrapper sous PROMPT.md ; une copie historique en
minuscules reste mise à jour sous son nom actuel, sans doublon. Les liens
personnels vers les anciens chemins sources doivent être réorientés lors
d'une migration explicite, selon BUILD.

Le nouveau [skill PROMPT](skills/prompt/SKILL.md) utilise exclusivement le
référentiel indiqué dans le `DEVOPS.md` du projet courant :

```text
/PROMPT LIST
/PROMPT CISMP3
/PROMPT 1CISMP3
```

`CISMPx` et `1CISMPx` acceptent tout entier décimal ASCII positif sans zéro
initial, sans borne supérieure (par exemple `1CISMP9` ou `CISMP12345`).
`LIST` affiche l'index. `CISMP3` lance le cycle du RUN CISMP3. `1CISMP3` borne
ce RUN à un change complet, archivage, statistiques puis arrêt de la session
de codage. Les codes sont en MAJUSCULE et les alias GCM/GCMP sélectionnent
GSCM.md/GSCMP.md. Le skill est directement invocable avec `$prompt CODE`.
Les sources de prompts restent externes ; les conditions du prompt choisi
continuent de s'appliquer. Les arguments et l'installation du plugin sont
décrits dans [BUILD](BUILD.md#utilisation-de-prompt).

## LM — Liste noire des modèles

`/LM` ou `$lm` affiche la liste sans écriture ; `/LM ADD identifiant` ajoute
une exclusion et `/LM REMOVE identifiant` la retire. `mimo-v2.5` et
`muse-spark-1.2-contributor` sont exclus par défaut et tous deux retirables,
y compris avec préfixe fournisseur ou suffixe gratuit.
Les préfixes OpenRouter marqués, comme `~vendor/model`, sont acceptés sans
changer l'identité LM : `~xiaomi/mimo-v2.5:free` reste exclu.
LM figure dans le catalogue CM. Les plugins et skills TFL/PLLM appliquent la
même liste avant classement, sélection et tests, même avec un ancien catalogue
ou une cible forcée. LM est l'unique liste noire ; aucune liste permanente
interne TFL/PLLM ne subsiste.

Pour les deux catalogues, un effort ou un contexte inconnu impose une
analyse et une recherche du LLM dans les sources officielles. Un contexte
encore invérifiable après investigation exclut le modèle. Les valeurs
Medium doit être explicitement déclaré ou couvert par un `null` explicite ;
une ancienne preuve qui ne couvre pas Medium ne suffit pas. Les sources, dates et
paramètres effectifs sont tracés.
Le générateur marque les investigations en attente et son rapport provisoire.
Le [guide des preuves](skills/tfl/references/model-evidence.md) décrit le registre
complémentaire et ses contrôles. Les seuils existants restent inchangés.

Le stockage commun CODEX_HOME/lm/blacklist.json (repli ~/.codex) reste hors
des caches et est conservé par TCU. Une liste invalide bloque sans écrasement.
LM ne réécrit pas les anciens rapports ; les prochaines invocations appliquent
les modifications. Le [skill LM](skills/lm/SKILL.md), son
[plugin](plugins/lm/.codex-plugin/plugin.json) et la commande source /LM sont
livrés localement ; une slash native n'est pas automatiquement enregistrée.
La publication et l'installation dans le profil sont des étapes distinctes.

## TFL puis PLLM à 00 h et 12 h

Les plugins proposent un hook de démarrage à approuver dans Codex ; TCU
installe aussi le planning lors d'une application réussie. Un unique timer
systemd utilisateur déclenche TFL puis PLLM normal à 00 h et 12 h Paris,
uniquement si l'application ou un CLI interactif Codex est ouvert et si les
quotas Codex sont vérifiables et non épuisés. Le quota est relu avant PLLM.
Quota nul/inconnu, Codex fermé ou échec TFL : PLLM ne démarre pas. Aucun
rattrapage ni changement des seuils ou exclusions LM n'est ajouté.
TFL et PLLM doivent déjà être installés ; leur absence ne les installe pas.
Voir [installation et contrôle](BUILD.md#planning-utilisateur-tfl-puis-pllm).

Les anciennes validations du mode5 sans benchmark ne prouvent plus sa validité ni un palier de performance ; une nouvelle évaluation Medium concluante est requise. La livraison source 0.7.25 ne modifie pas les profils installés et ne qualifie pas les performances réelles.
