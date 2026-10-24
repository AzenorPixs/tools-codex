# Conception

## Collecte

Utiliser directement https://openrouter.ai/api/v1/models, sans paramètres
de catégorie, modalités, prix ou limit issus de l'ancienne sélection.
Le tri et tous les filtres sont appliqués localement sur la réponse complète.
La source et la date tarifaires continuent d'être conservées dans le JSON.

## Sélection

Supprimer OPENROUTER_FIXED_IDS et la vérification de leur présence. Pour
chaque modèle, appliquer la blacklist permanente puis les contrôles de
contexte, sorties et prix existants. Le contexte vérifiable minimal reste
1 000 000 tokens. Les prix API de base par token sont convertis en USD/M ;
leur moyenne doit être comprise entre zéro et 0,50 inclus. Cache et paliers
restent séparés et ne changent pas la politique de classement de base.
Les overrides peuvent être conditionnés par min_prompt_tokens ou par
utc_days/utc_start/utc_end, comme observé dans le catalogue intégral. Conserver
ces conditions sans inventer un seuil de contexte pour les variantes horaires ;
vérifier leurs types, jours et heures UTC. Les heures restent au format HHMM
publié par l'API, sans sélection d'un tarif selon l'horloge locale.
Une entrée multimodale reste admissible ; les quatre sorties audio, vidéo,
speech et sound sont exclues comme auparavant.

Le JSON désigne explicitement la sélection dynamique et conserve les motifs
d'exclusion pour les modèles examinés. Le tri reste coût moyen, prix d'entrée,
prix de sortie puis identifiant. L'absence d'un ancien modèle n'est plus une
erreur. Une collecte invalide ou l'absence de tout résultat admissible restent
bloquantes avant publication ; aucun ancien catalogue n'est repris.

## Compatibilité et limites

Les champs utilisés par PLLM, les deux tableaux et les CLI sont conservés.
PLLM peut désormais lire des modèles OpenRouter autres que les trois anciens
identifiants : c'est le changement fonctionnel demandé. La disponibilité,
les prix gratuits et les limites fournisseurs peuvent évoluer ; le classement
n'est pas une qualification de génération ou de débit. Le moteur Go et ses
routes ne changent pas. Les sources sont livrées en 0.5.3 sans installation
dans le profil ni modification de l'archive précédente.

## Vérifications

Fixtures locales indépendantes d'une constante de production, contenant
des modèles inédits et divers motifs d'exclusion. Vérifier la sélection de
nouveaux IDs, les bornes zéro/0,50, le contexte 1M, les modalités, blacklist,
prix non finis, ordre stable, évolution/disparition entre collectes et requête
sans restriction ni limite artificielle. Vérifier aussi conservation des
rapports lors d'un échec, JSON strict, provenance et parité des distributions.
