# OpenCode Go — contrat API utilisé par PLLM

Cette référence documente le comportement observé pour l’intégration PLLM. Les
routes et réponses peuvent évoluer ; les contrôles en temps réel restent
prioritaires.

## Routage par modèle

OpenCode Go expose plusieurs protocoles de génération. Le catalogue TFL publie
`api_endpoint`, `api_protocol` et `endpoint_source` pour chaque modèle retenu ;
PLLM utilise ces champs au lieu d’inférer une route depuis un nom commercial.

| Modèles | Protocole | Point d’accès | Corps de requête |
|---|---|---|---|
| Muse Spark 1.3/1.2, GPT 5.6 Luna, Grok 4.6 | `responses` | `/v1/responses` | `input`, `max_output_tokens`, `reasoning.effort` |
| MiniMax et Qwen déclarés par TFL | `messages` | `/v1/messages` | contrat Anthropic-compatible |
| autres modèles texte retenus | `chat_completions` | `/v1/chat/completions` | `messages`, `max_tokens` |

La source officielle du routage et des identifiants est la documentation
OpenCode Go : <https://opencode.ai/docs/fr/go/>.

## Point d’accès et session

Les points d’accès sont :

~~~
https://opencode.ai/zen/go/v1/responses
https://opencode.ai/zen/go/v1/messages
https://opencode.ai/zen/go/v1/chat/completions
~~~

OpenCode Go exige `x-opencode-session` sur les requêtes de complétion. PLLM
génère un identifiant stable par évaluation de politique et le réutilise pour
tous les paliers. La valeur ne doit jamais être publiée.

Sans cet en-tête, l’API répond observément `HTTP 400 MissingSessionID` avant
l’appel au modèle. Ce rejet concerne la compatibilité du client, pas le quota
ou la performance.

## Diagnostic Muse du 8 septembre 2026

Avec la clé du mode 2 :

- `GET /models` répond `200` et Muse est annoncé dans la liste ;
- `GET /usage` répond `200` et fournit les quotas rolling, weekly et monthly ;
- Muse sur `/chat/completions` répond `HTTP 500 Internal server error` ;
- DeepSeek V4 Flash sur la même route sert de contrôle et répond `200` ;
- Muse sur `/responses`, avec `input`, `max_output_tokens` et
  `reasoning.effort=low`, répond `200` ;
- Muse en streaming émet notamment `response.output_text.delta` puis
  `response.completed`.

La réponse `500` était donc un mauvais routage de protocole, et non une preuve
de quota épuisé ou de modèle indisponible. Le correctif PLLM sélectionne
`/responses` pour Muse et ne sélectionne plus `/chat/completions`.

Un `HTTP 429` sur `/responses` est un refus de limitation amont (`rate_limit_exceeded`) : il intervient avant la génération et ne constitue pas une mesure de latence, de débit ou de qualité de Muse. Les quotas exposés par `GET /usage` peuvent rester valides en parallèle. PLLM classe alors le mode `Invalide` faute de test de performance concluant et doit réévaluer le modèle ultérieurement ; elle ne le déclassera pas comme modèle défaillant. Pour les Modes 1 et 2, elle recherche alors le prochain modèle TFL OpenCode Go disponible et benchmarkable par coût croissant, sans basculer directement vers une autre politique PLLM.

## Données récupérables

| Route | Données utiles |
|---|---|
| `GET /models` | `data`, identifiants, `object`, `owned_by`, `created` |
| `GET /usage` | `usage.rolling`, `usage.weekly`, `usage.monthly`, avec `status`, `percent`, `resetsAt` |
| `POST /responses` | événements SSE, statut, sortie et coût |
| `POST /chat/completions` | `id`, `model`, `choices`, `cost`, `created`, `usage` |

Pour `responses`, PLLM lit le TTFT sur le premier
`response.output_text.delta`. Le comptage est lu dans
`response.completed.response.usage.output_tokens`, et le raisonnement dans
`output_tokens_details.reasoning_tokens` lorsqu’il est fourni. Un statut
incomplet, notamment pour `max_output_tokens`, est conservé comme test
tronqué et ne constitue pas une réussite.

Les routes de lecture testées mais non exposées sur ce préfixe ont répondu 404 :
`/models/{id}`, `/credits`, `/balance`, `/account`, `/me`, `/health`, `/status`,
`/rate_limits`, `/subscriptions` et `/billing`. Cette liste est un
relevé de diagnostic, pas une garantie d’exhaustivité des routes privées ou
futures.

## Règles de sécurité

Les clés sont injectées en mémoire depuis la base de secrets de l’hôte. La clé,
l’en-tête Authorization et la valeur `x-opencode-session` ne doivent apparaître
ni dans le catalogue, ni dans les rapports, ni dans les journaux.
