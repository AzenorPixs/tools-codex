# Conception

Réutiliser evaluate_candidate et le moteur performance existants pour mode5 au lieu du raccourci de validation tarifaire. La boucle commune garantit le contrôle de ressources séquentiel avant chaque palier et le passage au candidat suivant après échec non bloquant. Le tri tarifaire et la collecte actuelle de prix sont conservés.

Le raisonnement Medium, les critères payants, les mesures et la mémoire par identité deviennent obligatoires en mode5. Le nettoyage des historiques applique les mêmes règles Medium aux sept modes ; un ancien résultat non benchmarké reste historique et ne peut être sélectionné. Les fichiers utilisateur ne sont pas migrés pendant la livraison source.

TFL conserve les payants sans preuve Medium : le benchmark PLLM vérifie l'acceptation courante du paramètre. L'absence de métadonnées seule ne prouve pas un refus. Aucun effort alternatif n'est essayé.

Le retour à une ancienne release restaure l'ancien comportement sans benchmark ; conserver les rapports utilisateur avant un retour de version. Les tests contrôlent les seuils stricts, paliers, ordre des contrôles, replis, erreurs HTTP, rangs, mémoire et publication.
