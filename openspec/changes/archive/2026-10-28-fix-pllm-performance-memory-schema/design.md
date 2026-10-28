# Diagnostic et décision
La mémoire installée n'a que la clé policies, avec mode7 pour deepseek-v4-flash, medium, réponse seule, Chat Completions et profil request_average_v1/request_total/protocole 8. Le test test_mode7_accepts_documented_medium_alias_after_a_complete_response redirigeait ROOT mais pas MEMORY_PATH et écrivait cette mémoire dans les sources. Son isolation est corrigée : MEMORY_PATH pointe désormais dans le dossier temporaire et la persistance au schéma 3 y est vérifiée. Les deux données source touchées par la qualification ont été restaurées depuis le snapshot marketplace après vérification de leur empreinte Git contre celle de l'index (2c1db3c1dbaaa721386ff6b3a56d330b581e2669).

Une récupération limitée évite d'attribuer arbitrairement le schéma 3 à un ancien mode4 ou mode6. Sans version, seul un objet policies vide ou limité à mode7 avec identité DeepSeek courante et enregistrements cohérents est admis. Les configurations doivent correspondre à leur clé d'identité et à cette identité. Le chargement ne modifie jamais le fichier. L'ajout de schema_version=3 se fait en mémoire et est persisté uniquement par l'écriture atomique du prochain succès. Les schémas explicites 1/2 gardent leur migration et les invalides sont préservés.

L'écrivain valide et normalise son argument avant toute mutation ou écriture ; il refuse les formats ambigus. Les tests utilisent des dossiers isolés, sans secret ni réseau. Une évaluation réelle peut échouer aux critères fournisseur sans remettre en cause la correction du chargement.

# Repli
Les données installées sont sauvegardées avant mise à jour. Aucun effacement ni réparation manuelle de l'historique. Revenir au code antérieur ne restaure pas sa capacité à lire le fichier sans version ; conserver la sauvegarde.
