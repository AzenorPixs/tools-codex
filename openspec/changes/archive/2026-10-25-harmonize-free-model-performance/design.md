# Décisions validées

## Qualification
Les gratuits utilisent contexte ≥1M, prix d'entrée/sortie nuls vérifiés avec
variantes compatibles, réponse complète et comptage fiable, TTFT <30 s et
débit >20 tokens/s. Les payants PLLM gardent <90 s et >15 tokens/s. Les tests
TFL concernent seulement les gratuits et n'appellent aucun quota ou solde.
TFL conserve les payants structuraux, retire les gratuits échoués de models,
conserve exclusions et un tableau commun des essais gratuits. Les trois
tableaux fournisseurs gardent leurs huit colonnes. Le résultat est lié au
compte TFL sélectionné : un échec peut supprimer un candidat utilisable par
un autre compte jusqu'à une nouvelle collecte/qualification TFL. Cette limite
résulte du filtrage explicitement demandé ; PLLM ne récupère pas les exclus.
Si une section devient vide, la publication est arrêtée et les anciens
rapports sont préservés, conformément au contrat existant.

## Raisonnement
HIGH est le défaut pour les six modes PLLM et les gratuits TFL. Une annonce
explicite sans HIGH mais avec XHIGH permet XHIGH avant requête. Un refus
HTTP 400 précisément lié au paramètre d'effort permet au plus un passage à
XHIGH, seulement si annoncé. Aucun repli sur 401/403/429, seuil, troncature ou
paramètre autre que l'effort ; aucun niveau inférieur. La préférence et le
niveau effectif sont tracés. Les paliers restent 1024, 2048, 4096, 8192 et
120 secondes par requête. La mémoire inclut le niveau effectif : Low ne
valide ni n'amorce un succès HIGH ou XHIGH. Les futures évaluations
repartent de HIGH même après un succès XHIGH historique.

OpenCode Chat Completions utilise reasoning_effort, Responses reasoning.effort,
Messages thinking adaptive et output_config.effort. DeepSeek garde thinking
activé et reasoning_effort=high. OpenRouter utilise les supported_efforts
publiés, ou le budget documenté de 80 % pour HIGH lorsque seul max_tokens
est exposé. XHIGH par budget est 95 % si le contrat le permet. Les paramètres
réellement envoyés sont conservés ; accepter une requête ne prouve pas la
profondeur interne du raisonnement. Aucun nom de modèle n'invente un support.

## Architecture et accès
performance.py embarque les constantes, les seuils et la mesure streaming
commune, avec dépendances réseau/horloge injectées pour préserver les tests.
Les quatre copies sont identiques ; chaque plugin fonctionne isolément.
TFL utilise la clé Go déjà sélectionnée pour Go/général et la clé OpenRouter
existante (environnement, sinon référence historique du mode 5 dans le
trousseau), toujours injectée en mémoire, jamais en argument ou rapport.
Le catalogue expose les capacités de raisonnement publiées sans donnée privée.
Un accès manquant produit une exclusion gratuite explicite, sans clé créée.
Les erreurs restent filtrées et les routes HTTPS validées.

## Validation et retour
Suites hors ligne Python 3.13/3.14, syntaxe/imports, fuseau Europe/Paris,
seuils stricts, HIGH/XHIGH, corps HTTP/SSE, filtrage TFL, absence de quota,
comptes, secrets, mémoire et paquets isolés ; parité, release, UTF-8/LF et
OpenSpec standard/strict. Aucun benchmark fournisseur réel ni installation.
Les champs JSON consommés restent présents ; ajout de détails de performance.
Les historiques corrompus restent préservés. Le filtre TFL est recalculé à
chaque invocation, sans migration système ni modification d'un secret.

## Sources de contrats consultées le 25 octobre 2026
- https://openrouter.ai/docs/guides/best-practices/reasoning-tokens
- https://platform.claude.com/docs/en/build-with-claude/effort
- https://api-docs.deepseek.com/guides/thinking_mode/
