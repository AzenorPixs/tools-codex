# Conception

## Collecte et correspondances

Utiliser la bibliothèque standard Python (HTMLParser, urllib, Decimal) pour
extraire les tableaux contenant Model/Input/Output de la documentation Go.
Ignorer les anciens montants barrés. Rapprocher les noms et les ID par une
normalisation limitée à la casse et aux séparateurs ; toute collision ou
valeur ambiguë provoque un diagnostic, jamais un choix arbitraire.

Les tableaux Go et Go Plus répètent les prix : les variantes identiques sont
dédupliquées, les contradictions sont bloquantes. Les limites d'abonnement
ne servent pas au classement. Les estimations de requêtes restent non
vérifiées (N/A) lorsqu'elles ne sont pas collectées ; aucune estimation
historique n'est recyclée.

## Variantes et preuve

Conserver dans le JSON les variantes standard, pointe/hors pointe et paliers
de contexte, ainsi que les prix de cache disponibles. Utiliser les tarifs
hors pointe lorsqu'ils existent. Pour plusieurs paliers, retenir le coût
moyen maximal hors pointe, afin de ne pas classer un modèle 1M selon un prix
réservé à un contexte plus court. Indiquer cette règle dans les métadonnées.
Un prix gratuit explicitement publié vaut zéro ; un prix absent reste inconnu.

Pour OpenRouter, continuer à utiliser pricing.prompt/completion par token,
convertis en USD par million, et conserver séparément les champs de cache
disponibles. Les prix négatifs, non finis ou débordants ne sont pas exploitables.
Chaque fournisseur expose la source et la date de récupération tarifaire ;
les champs déjà consommés par PLLM conservent leur structure.

## Échecs et limites

Une source indispensable inaccessible, un tableau tarifaire non reconnu,
une contradiction ou une réponse invalide fait échouer la génération avant
toute publication. Un modèle sans tarif correspondant est explicitement
exclu. Aucun repli statique ni réemploi silencieux d'un rapport précédent.
Les deux fichiers restent préparés avant leur remplacement atomique individuel.
Le classement ne qualifie ni la qualité du modèle ni sa route de génération ;
les routes inconnues restent signalées, sans protocole inventé.

## Vérifications

Tests déterministes sans réseau ni secrets sur les deux distributions :
nouveaux modèles, deux collectes aux prix différents, prix barrés, variantes,
doublons, ambiguïtés, données absentes, prix invalides, provenance et échecs.
Régression complète, compilation Python, parité, release et OpenSpec.
Une collecte HTTPS réelle utilise un répertoire temporaire dans tests et
ne modifie ni les catalogues publiés dans les sources ni le profil utilisateur.
