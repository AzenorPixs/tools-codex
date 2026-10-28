# Conception

Le chemin explicite --tfl-catalog reste prioritaire ; sans option, le chemin voisin reste inchangé. Aucun parcours des configurations privées ou choix automatique du catalogue le plus récent n'est ajouté. Le skill demande de résoudre le catalogue réellement produit avant l'évaluation et de signaler les divergences connues.

Chaque politique consommatrice conserve catalog_source avec chemin absolu, sélection explicit/default, generated_at validé, âge calculé et avertissements structurés. Une date absente, invalide, sans fuseau ou future reste visible sans invalider arbitrairement les modèles. Les compteurs par catégorie et la synthèse d'exclusions sont distincts des preuves de performance.

La cellule État d'une sélection vide désigne ce catalogue et sa date ; les huit colonnes restent inchangées. Le chemin complet reste au JSON. Les contrôles de ressources tracent resource_control : phase, endpoint constant public, date, statut et diagnostic HTTP filtré. Une erreur d'authentification au quota est nommée comme telle sans conclure sur sa cause privée ou sur la génération.

Les secrets restent injectés uniquement en mémoire. Les gratuits ne consultent aucune ressource. Le refus mode2 n'empêche ni mode4 ni les autres politiques. Les données de provenance/contrôle sont réinitialisées à chaque politique visitée, et les historiques non visités en active restent datés.

Le retour de version consiste à réinstaller la release précédente en conservant les données existantes ; les nouveaux champs sont additifs au schéma3. Aucun changement du trousseau n'est prévu.
