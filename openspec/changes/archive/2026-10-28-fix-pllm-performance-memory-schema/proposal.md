# Why
PLLM 0.7.20 refuse la mémoire installée contenant uniquement policies.mode7 sans schema_version. L'écriture d'un succès sérialise son argument sans garantir sa version.

# What Changes
- Récupérer en mémoire le cas sans version identifiable avec certitude : mémoire vide ou seul mode7 DeepSeek Medium avec identité du protocole 8 et succès cohérents.
- Refuser et préserver tout format ambigu, schéma inconnu ou donnée corrompue.
- Garantir une écriture atomique au schéma 3 après un succès, avec relecture possible.
- Livrer 0.7.21, qualifier les deux distributions, archiver et appliquer la clôture SCM.

# Impact
Deux évaluateurs PLLM, tests, documentation, métadonnées et six manifestes. Aucun changement des fournisseurs, seuils, secrets, quotas ou de TFL. Après qualification : mise à jour installée et PLLM réel autorisés.
