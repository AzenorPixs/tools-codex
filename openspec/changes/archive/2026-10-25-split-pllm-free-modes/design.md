# Conception validée — six politiques PLLM

## Décision et périmètre

Le développeur a validé le périmètre SCM puis a fixé TTFT <30 s et débit
>20 tokens/s pour les seuls nouveaux modes 3/4. Les autres modes gardent
TTFT <90 s et débit >15 tokens/s. Le contexte minimal 1M et les filtres TFL,
Low, protocoles, diagnostics, paliers et classement sont préservés.

## Identité, authentification et sélection

Les six politiques ont des définitions explicites et des priorités 1 à 6.
Les références de trousseau restent historiques : mode1 pour 1/3, mode2 pour
2/4, ancien mode3 pour 5 et ancien mode4 pour 6. Aucun secret n'est déplacé,
créé, lu par l'agent ni ajouté aux sorties.

Les modes 3/4 sélectionnent exclusivement les gratuits vérifiés des sections
Go puis OpenCode général. Ils n'appellent jamais usage, credits ou balance,
même avant une reprise. Ils gardent une authentification et les limitations
HTTP réelles : aucun quota inventé, statut de quota non applicable explicite.
Les modes 1/2 s'arrêtent sur épuisement, y compris après un premier candidat
réussi. Le mode 5 conserve le repli gratuit OpenRouter après crédit épuisé.

Les forçages 1 à 6 ciblent le premier candidat admissible du mode. Les rangs
11–13, 21–23 restent des rangs Go bruts ; 31–33 et 41–43 ciblent les rangs de
la liste gratuite admissible Go puis général. Les anciens rangs OpenRouter
31–33 deviennent 51–53 ; 6 reste le modèle direct. Un rang incompatible ne
substitue aucun candidat. Ce changement de sens est documenté.

## Historique et mémoire

Le schéma courant passe à 2. Un historique à quatre politiques est validé
avant conversion en mémoire : 1/2 restent 1/2, 3 devient 5, 4 devient 6,
3/4 sont initialisés. Les lignes anciennes restent historiques et non
sélectionnées jusqu'à leur évaluation. Les historiques malformés ne sont pas
écrasés. Aucun fichier utilisateur n'est modifié pendant cette livraison.

La mémoire de schéma 1 est adaptée en mémoire vers le schéma 2, avec déplacement
des anciens 3/4 vers 5/6. Les nouveaux 3/4 commencent sans apprentissage ;
aucun succès ancien aux seuils plus faibles ne leur est attribué. Les paliers
restent des points de départ et ne valident jamais une nouvelle invocation.
Le remplacement atomique n'intervient qu'au moment normal de publication
ou d'une nouvelle réussite. Le retour à un ancien évaluateur nécessite une
copie préalable de ses données : le schéma 2 n'est pas lisible par celui-ci.

## Vérifications et limites

Tests hors ligne sur les deux distributions et Python 3.13/3.14 : absence
d'appels de quota en 3/4, comptes conservés, filtres, seuils stricts, erreurs,
classement, paliers, forçages, migration, publication et silence active.
Contrôles syntaxiques, format des skills, parité, versions, UTF-8/LF et
OpenSpec ciblé/global standard/strict. Ils ne prouvent ni les performances
fournisseur actuelles ni l'installation réelle dans une nouvelle session.
