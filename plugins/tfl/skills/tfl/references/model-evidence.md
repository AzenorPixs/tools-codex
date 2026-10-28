# Investigation des modèles

Ce workflow s'applique à OpenCode Go et OpenRouter.
Le module partagé accepte également `deepseek` pour le registre direct PLLM ;
TFL ne collecte pas et n'utilise pas ce fournisseur.
`model_investigations` dans le JSON TFL donne les champs encore inconnus.
Le statut `required` exige une analyse et une recherche du LLM avant sa
restitution finale ; une collecte CLI seule ne réalise pas cette recherche.
Si l'investigation est empêchée, restituer précisément le blocage et conserver
le rapport provisoire. Ne pas présenter une absence de preuve comme la preuve
d'une incapacité.

## Recherche et conclusion

1. Relever fournisseur, ID exact, route publiée et champ manquant. Vérifier
   d'abord le catalogue actuel et `reasoning_options` de models.dev, puis la
   documentation officielle du fournisseur ou du créateur du modèle. Vérifier
   l'applicabilité au service et au protocole réellement utilisés.
2. Pour l'effort, conserver les sources officielles applicables au modèle et au
   transport. Lorsqu'un benchmark TFL ou PLLM est prévu, une requête réelle
   exclusivement en Medium peut établir l'acceptation du paramètre : seule une
   réponse complète la prouve. Un mapping documenté peut être tracé, mais ne
   mesure pas l'effort interne.
3. Pour le contexte, chercher une capacité chiffrée applicable au fournisseur.
   Ne pas déduire sa taille d'un prix, du nom du modèle ou d'un autre service.
   Le seuil reste 1 000 000 tokens. Aucune requête de cette taille n'est nécessaire.
4. Conclure `verified` avec une valeur et ses preuves ; `unsupported` seulement
   si une source établit explicitement l'absence de prise en charge ; sinon
   `unverifiable` avec le périmètre de recherche et les sources examinées.
   Si le contexte reste invérifiable après cette investigation, exclure le modèle.
5. Enregistrer la conclusion dans `model-evidence.json` dans le répertoire
   du rapport TFL, puis relancer TFL. Reprendre les champs éventuellement révélés
   par cette résolution. Ne jamais modifier manuellement models, rangs ou performances.

## Registre et vérification

Le fichier déclare `schema_version: 1` et `records`. Chaque entrée contient :

| Champ | Valeur |
|---|---|
| provider | opencode_go ou openrouter ; opencode et deepseek sont réservés aux registres PLLM/historiques |
| model_id | Identifiant exact dans ce catalogue |
| field | context ou reasoning |
| protocol | null pour context ; chat_completions, responses ou messages pour reasoning |
| status | verified, unsupported ou unverifiable |
| investigated_at | Date ISO 8601 avec fuseau |
| conclusion | Synthèse de la recherche et de son applicabilité |
| sources | URL HTTPS officielle, authority=official, fingerprint_method, sha256 et retrieved_at avec fuseau |
| value | Pour verified : entier de contexte, ou objet supported_efforts contenant medium, ou null explicitement publié pour tous les efforts |

L'objet d'effort peut préciser `effort_equivalence: accepted_alias` pour
des niveaux acceptés équivalents. `thinking_enabled` décrit l'équivalence
Medium vers thinking.type=enabled, uniquement pour Chat Completions
OpenCode sur preuve applicable. Il n'invente aucune route ni ne transpose une
preuve vers un autre fournisseur. Un budget ou un booléen seul reste insuffisant.

Le registre de référence livré dans `references/model-evidence.json` conserve
des preuves de capacité historiques. Elles déclenchent une nouvelle recherche
pour établir Medium lorsqu'elles ne couvrent pas cet effort ; elles ne
permettent pas seules l'admission.
Le registre du
répertoire de rapport peut le compléter ou réviser une entrée exacte.
L'agent rédige les conclusions après recherche ; pour HTML, `html_visible_text_v1`
empreinte le texte visible normalisé en UTF-8 NFC avec espaces consécutifs
réduits, sans scripts, styles, navigation ou balisage volatil. Pour les autres
formats, `raw_bytes_v1` empreinte les octets reçus. Le contrôle SHA-256 prouve
seulement que le contenu retenu n'a pas changé, pas l'interprétation sémantique du LLM.
TFL relit les sources avant admission. Un contenu changé ou inaccessible
réactive l'investigation sans réutiliser l'ancienne preuve. PLLM recontrôle
ces sources avant génération et conserve les résultats d'investigation TFL.

Les preuves ne qualifient ni accès au compte, ni génération, ni performance.
Conserver tous les autres filtres et tests applicables. Ne lancer aucune
génération payante simplement pour compléter une preuve documentaire.

Le contrôle du téléchargement accepte une redirection HTTPS uniquement vers
le même hôte public ; les paramètres de cache ajoutés par ce même hôte ne
modifient pas l'URL enregistrée. Toute redirection vers un autre hôte, HTTP,
un port non standard, des identifiants ou un fragment reste bloquée.
