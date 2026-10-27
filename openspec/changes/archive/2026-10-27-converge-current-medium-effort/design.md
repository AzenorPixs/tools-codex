## Contexte

Les scripts `performance.py` exigent déjà une capacité Medium et émettent les
paramètres propres à chaque transport. En revanche, `effort_allowed` traite
uniquement les capacités déclarées : un ancien résultat avec effort enregistré
différent peut rester visible si les métadonnées du fournisseur incluent aussi
Medium. Les commandes `/TFL` et `/PLLM` décrivent encore l'ancien contrat et
les fichiers de résultat PLLM distribués ont été produits avec cet ancien
effort.

## Décisions

1. Conserver les transports API et exiger la valeur effective `medium` dans
   chaque requête ; aucune valeur d'effort différente n'est demandée ou reprise.
2. Valider les champs d'effort effectivement demandés dans les anciens rapports
   et leurs tentatives. La présence d'une capacité Medium dans la source ne
   rend pas admissible un rapport exécuté autrement.
3. Lorsqu'un résultat antérieur est rejeté, préserver son motif dans les
   exclusions, vider sa sélection et ses mesures, puis continuer avec les
   candidats admissibles. Ne pas reprendre de palier mémorisé pour l'ancien
   effort.
4. Fournir aux deux distributions PLLM des rapports initiaux non évalués et
   une mémoire vide ; synchroniser les fichiers embarqués depuis les sources
   autonomes.
5. Reformuler les documents courants sans modifier les archives, les preuves
   publiées ni les tests négatifs. Ces sources historiques restent lisibles,
   mais ne fondent aucune demande ou sélection actuelle.
6. Passer `VERSION`, `pyproject.toml`, les six manifestes et la documentation
   publique à 0.7.15 après correction.

## Risques

Des résultats antérieurs peuvent disparaître des tableaux PLLM, même si la
capacité fournisseur couvre Medium, lorsque la requête historique n'était pas
Medium. Cela force une nouvelle évaluation et évite de présenter une mesure
incomparable comme actuelle. Les archives et preuves source restent inchangées.

## Validation

Ajouter une régression où un rapport indique une capacité Medium mais une
requête ou une tentative avec un effort différent ; vérifier qu'il est rendu
invalide et exclu. Couvrir les quatre copies du moteur partagé, l'absence de
repli, les rapports initiaux, la parité autonome/embarqué, les versions et
l'alignement des spécifications et documents.
