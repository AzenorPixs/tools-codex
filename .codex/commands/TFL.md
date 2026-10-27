---
description: Générer le rapport LLM Go puis OpenRouter
---

Utilise obligatoirement la skill `tfl` installée par Tools Codex pour `/TFL`
(alias `/tfl`).

L’exécution de TFL DOIT toujours être effectuée hors sandbox pour permettre
l’accès réseau aux APIs OpenCode Go et OpenRouter. Dans Codex, demande une
exécution autorisée hors sandbox ; si cette autorisation est refusée, arrête la
commande et restitue l’erreur sans tenter de repli sandboxé.

À chaque invocation, exécute réellement le générateur autonome :

- sans argument : `python3 scripts/test_fournisseur_llm.py` ;
- avec `mode1`, `mode2` ou `auto` : transmet cet argument au générateur ;
- avec `--policy mode1`, `--policy mode2` ou `--policy auto` : transmet cette option au générateur.

Exécute la commande depuis le répertoire du skill TFL installé. Le tableau OpenCode Go
DOIT être produit et affiché en premier, puis OpenRouter. Les deux tableaux
DOIVENT conserver huit colonnes, Go en USD/M et OpenRouter en EUR/M.
OpenCode général n’est plus collecté, testé ou publié ; le JSON contient Go et OpenRouter.
Tester les gratuits des deux catalogues exclusivement en Medium, sans repli
vers un autre effort et sans contrôle de quota. Exiger contexte
≥1M, gratuité vérifiée, réponse complète, TTFT <30 s et débit >20 tokens/s.
Exclure les échecs de models, conserver leurs preuves et afficher le tableau
commun des essais gratuits après les deux tableaux fournisseurs.
Restitue intégralement la sortie produite par le générateur, sans masquer les
lignes de rapport ni les codes couleur. Les clés API ne doivent jamais être
affichées.

Argument reçu : `$ARGUMENTS`

Conserver les payants OpenRouter admissibles même sans preuve Medium. Exiger Medium et un benchmark réussi pour les gratuits ; garder les motifs JSON.
OpenRouter applique la moyenne de base ≤0,20 EUR/M au dernier taux BCE
publié vérifié ; aucune conversion historique implicite.

Pour Go et OpenRouter, un effort ou un contexte non
vérifiable impose l'analyse et la recherche du LLM suivant
`references/model-evidence.md` du skill. Compléter les preuves officielles
et relancer le générateur ; ne pas restituer un rapport provisoire comme
définitif sans investigation terminée ou blocage explicite. Un contexte
invérifiable après investigation exclut le modèle. Une capacité publiée
supplémentaire ne modifie pas l'effort demandé : tracer et respecter les
paramètres Medium du protocole publié.
LM est l'unique liste noire, avec toutes ses entrées retirables.
