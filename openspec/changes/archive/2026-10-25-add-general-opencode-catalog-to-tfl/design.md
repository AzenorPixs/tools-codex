# Conception

## Sources et séparation

Ajouter la source de disponibilité du catalogue général OpenCode, ses tableaux
tarifaires de https://opencode.ai/v2/docs/console/models/ et les métadonnées
models.dev du fournisseur opencode. Les lectures de catalogue sont distinctes
de toute génération. Le contrat d'accès public sera vérifié avant le code ;
aucune clé Go ne sera envoyée implicitement à un autre catalogue.

Sources vérifiées avant code : https://opencode.ai/zen/v1/models renvoie
publiquement 85 modèles, dont glm-5.3-flash-free et deepseek-v4.1-flash-free.
La page tarifaire générale fournit 84 références reconnues par l'extracteur
existant. La collecte générale utilise un GET public sans Authorization ;
elle n'emprunte pas le secret Go.

Les modèles identiques peuvent exister dans Go et dans le catalogue général,
avec des tarifs, contextes ou routes différents. Ils restent dans deux
sections ; aucun rapprochement entre fournisseurs ne complète une absence.
Réutiliser seulement les mécanismes communs de filtrage, extraction de tableaux,
modalités et contrats de transport, avec provenance correctement contextualisée.

## Contrat de sortie

Ordre : opencode_go, opencode, openrouter. Ajouter une section JSON opencode
avec sources, dates, prix, modalités, routage, modèles et exclusions. Les deux
sections existantes et leurs champs consommés par PLLM restent compatibles.
Les trois tableaux utilisent les huit mêmes colonnes et leur propre classement.
L'atomicité reste par fichier ; toutes les collectes indispensables et la
sérialisation stricte précèdent la publication.

## Filtres et garanties

Contexte vérifiable ≥ 1 000 000 tokens et moyenne entrée/sortie entre zéro et
0,50 USD/M inclus. Garder les exclusions de sortie audio/vidéo/speech/sound
et la blacklist permanente OpenCode muse-spark-1.2-contributor dans les deux
catalogues OpenCode. Conserver les variantes et prix de cache, les prix barrés
ignorés, les correspondances non ambiguës et les métadonnées datées. Une
variante gratuite 200K reste exclue malgré son coût nul.
Pour le catalogue général, le prix de référence est la moyenne maximale des
variantes publiées (paliers et périodes compris) ; Go conserve sa référence
hors pointe. Les prix de cache ne remplacent jamais les prix d'entrée/sortie.

Les transports documentés sont distincts des générations testées. Les SDK
inconnus restent signalés sans nouvelle prise en charge implicite. Une source
indispensable invalide, une contradiction ou une URL non sûre bloque la
publication. Aucun repli historique ni vers une autre section de fournisseur.

## Vérifications et documentation

Tests déterministes sur les deux distributions : nouveau catalogue, bornes,
variantes gratuites trop courtes, séparation d'un même ID, provenance, ordre,
colonnes, collecte invalide et rapports préservés. Adapter les fixtures des
tests de publication pour la troisième collecte. Vérifier que PLLM continue
de lire les sections existantes sans modifier sa politique. Mettre à jour les
deux SKILL.md TFL, le wrapper et la description TFL des deux CM, les documents
de cadrage/publics concernés et les cinq manifestes 0.5.6. La livraison locale
n'installe aucun profil, ne publie rien et ne crée aucune opération Git.
