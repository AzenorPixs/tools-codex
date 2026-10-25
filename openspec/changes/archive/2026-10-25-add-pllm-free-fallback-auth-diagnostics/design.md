# Conception

## Séparation des ressources et retour au payant

L'identité du compte est déterminée par le mode, jamais par le fournisseur
historique du gagnant. Chaque invocation repart du contrôle Go pour modes 1/2,
OpenRouter pour mode 3, DeepSeek pour mode 4. Un épuisement n'est reconnu que
sur des données complètes, finies et cohérentes reçues avec authentification.
Un refus HTTP 401, un secret inaccessible, un refus d'accès 403, une panne ou
une donnée manquante ne constituent jamais un épuisement confirmé.

Quand les ressources sont disponibles, filtrer les gratuits avant le classement.
Après épuisement confirmé, filtrer tous les payants. Pour Go, examiner les
gratuits de opencode_go puis opencode avec leur fournisseur et leur route
propres. Pour OpenRouter, examiner les gratuits de openrouter. Seuls les tarifs
d'entrée/sortie publiés, finis et nuls prouvent la gratuité ; un suffixe free
ne suffit pas. Préserver les filtres TFL : contexte 1M, coût maximal, modalités,
blacklist et transport. Ne jamais construire un identifiant ni inventer une route.

Les contrôles précèdent chaque tentative. Si la catégorie disponible change
pendant l'évaluation, recommencer la sélection dans la nouvelle catégorie et
écarter les gagnants de la précédente ; borner ces transitions pour éviter une
boucle en cas d'oscillation du quota. L'absence de candidat ou un refus du
fournisseur laisse la politique invalide. Aucun repli gratuit après simple
échec de performance ou erreur d'authentification.

## Mesures et classement

Évaluer chaque candidat autorisé avec les paliers mémorisés 1024/2048/4096/8192,
120 s/requête, Low, TTFT visible <90 s et débit >15. Arrêter ses paliers à la
première réussite ; continuer les autres candidats. Comparer les réussites
par débit décroissant, TTFT croissant puis ordre TFL stable (Go avant général).
Go et OpenCode général emploient le débit raisonnement+réponse ; OpenRouter
et DeepSeek le débit réponse seule. Ne pas comparer les débits entre modes.
Les priorités 1 à 4 priment toujours sur ce classement interne.

Tracer candidats, tentatives, catégorie, source de quota et gagnant dans le
JSON. La mémoire garde les succès par configuration sans transformer un échec
en apprentissage. Afficher seulement un palier correspondant au candidat courant.
Les forçages conservent le rang TFL exact et interdisent toute substitution.

## Routage et secrets

Pour les deux catalogues OpenCode, utiliser l'endpoint/protocole TFL et une
session stable par évaluation. Le compte Go du mode authentifie le contrôle
et ses appels OpenCode sur la même origine HTTPS autorisée ; aucune recherche
de configuration privée ni de nouveau secret. Conserver le véritable provider
opencode pour le catalogue général. Une clé refusée par ce service reste un
échec explicite, sans changer les agents ni copier de secret.

Sources documentaires consultées le 25 octobre 2026 :
https://opencode.ai/v2/docs/console/go/ (Beam Free, client propre et session),
https://opencode.ai/v2/docs/console/models/ (routes et restriction de certains
gratuits au client natif), https://openrouter.ai/docs/guides/routing/model-variants/free
(gratuit distinct, limites et disponibilité propres). Le développeur confirme
l'inclusion du catalogue général pour son agent de codage natif OpenCode.
PLLM inclut ces candidats sans fabriquer un en-tête d'identité du client natif.
Ces sources ne prouvent ni accès actuel ni performance de génération.

## Diagnostics et compatibilité

Conserver state Valide/Invalide dans le JSON ; ajouter un diagnostic sûr dans
la cellule État : authentification refusée (401), accès refusé (403), clé
inaccessible, épuisement sans gratuit ou échec de mesure. Décoder les codes
d'erreur HTTP/SSE sans publier le corps brut, message privé, compte ou clé.
Le tableau conserve huit colonnes et les mesures indisponibles restent '-'.
Un gagnant gratuit affiche Valide — repli gratuit avec les quotas réellement
épuisés conservés. active garde son silence et s'arrête après le classement
complet du premier mode valide. JSON additif de version 1, lecture des états
historiques autorisant le provider opencode dans modes 1/2 seulement.

## Livraison et repli

Release commune 0.6.0. Pas de migration destructive ni nouvelle dépendance.
La livraison locale reste réversible par restauration des seules sources ;
les nouvelles données gardent des champs historiques compatibles. Tests hors
ligne : aucune clé réelle ni appel fournisseur. Installation, publication et
adoption par une session OpenCode restent des opérations distinctes.
