# Conception

## Sources et priorités

Conserver la collecte models.dev et exposer les métadonnées complètes du
fournisseur opencode-go à la résolution, en plus des limites de contexte.
Lire les modalités explicites de l'API lorsqu'elles sont présentes et les
compléter depuis modalities.input/output de models.dev. Les données connues
contradictoires sont un échec explicite ; une donnée absente reste inconnue.
La provenance et la date de collecte sont conservées dans le catalogue.

## Résolution des transports

Utiliser les métadonnées de routage explicites si disponibles, puis le SDK,
le protocole et la base API publiés par le fournisseur ou sa surcharge modèle.
Un SDK/protocole constitue un contrat de transport générique, pas une liste
de modèles. Ne pas déduire le protocole d'un nom MiniMax/Qwen/OpenAI ni d'un
préfixe de modèle. Les suffixes de route des trois protocoles supportés sont
les opérations documentées responses, chat/completions et messages.

Les contrats génériques vérifiés dans les sources officielles AI SDK sont :
@ai-sdk/openai-compatible → chat_completions ; @ai-sdk/openai → responses
(fabrique de modèle par défaut) ; @ai-sdk/anthropic → messages. Les SDK
non reconnus restent non résolus. models.dev publie npm/api au niveau du
fournisseur et peut les surcharger par modèle. MiniMax-M3.1-Flash hérite du
SDK openai-compatible et publie la base /inference/go/openai/v1 ; MiniMax-M3
surcharge le SDK anthropic et la base /inference/go/anthropic/v1. Ces exemples
sont des observations de sources et ne deviennent aucune table dans le code.

Références consultées :
- https://models.dev/api.json
- https://ai-sdk.dev/providers/openai-compatible-providers
- https://ai-sdk.dev/providers/ai-sdk-providers/anthropic
- https://raw.githubusercontent.com/vercel/ai/main/packages/openai/src/openai-provider.ts
- https://raw.githubusercontent.com/vercel/ai/main/packages/openai/src/responses/openai-responses-language-model.ts
- https://raw.githubusercontent.com/vercel/ai/main/packages/openai-compatible/src/chat/openai-compatible-chat-language-model.ts
- https://raw.githubusercontent.com/vercel/ai/main/packages/anthropic/src/anthropic-language-model.ts

Valider HTTPS, l'absence d'identifiants utilisateur, de query et fragment, et
l'origine OpenCode avant publication d'un endpoint susceptible de recevoir
une clé chez un consommateur. Un protocole inconnu ou une base manquante
produit une route non vérifiée et un motif explicite, sans substitution.
La résolution utilise les métadonnées de chaque collecte et ne conserve aucun
repli par nom de modèle, catalogue historique ou fichier de profil.

## Contrat et vérification

Les champs api_endpoint, api_protocol et endpoint_source restent présents ;
les valeurs de protocole supportées restent celles de PLLM. Les provenances
de modalités et de transport sont ajoutées au JSON. Le routage publié est
une résolution documentaire, distincte d'une qualification de génération.
Les filtres, les tarifs, les blacklists et la sélection OpenRouter restent
inchangés. Le rapport affiche l'inconnu et les avertissements résiduels.

Les tests simulent les deux fournisseurs et les schémas de transport, sans
réseau ni trousseau. Une lecture réelle des sources publiques et une collecte
TFL dans un temporaire du projet vérifient MiniMax-M3.1-Flash et les sources,
sans appeler une route de génération. La documentation publique et les cinq
plugins partagent la release 0.5.5 ; aucune copie installée n'est remplacée.
