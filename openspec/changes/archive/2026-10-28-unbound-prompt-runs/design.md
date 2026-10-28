# Décisions
Le suffixe est reconnu par [1-9][0-9]* et conservé comme chaîne : ni liste finie ni limite de conversion numérique. Les arguments invalides restent rejetés avant lecture de configuration, par CLI et par API Python.
Les noms techniques prompt et $prompt restent compatibles. Les métadonnées affichent déjà PROMPT ; le bilan JSON TCU ajoute libelle: PROMPT aux trois ressources, et son skill utilise ce libellé pour la restitution. Les clés brique/composant et les chemins restent inchangés.
Les deux distributions sont synchronisées. Les tests couvrent les bornes historiques, des numéros multichiffres et un suffixe de plus de 4300 chiffres, les erreurs et les ressources isolées. La release commune passe de 0.7.21 à 0.7.22.
# Repli
Le retour à la release précédente rétablit la limite historique ; aucune donnée utilisateur n'est migrée.
