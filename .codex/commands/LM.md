---
description: Gérer la liste noire commune des modèles exclus de TFL et PLLM
argument-hint: [LIST|ADD identifiant|REMOVE identifiant]
---

Utilise le skill `lm` pour cette demande `/LM` et exécute son script.
Sans argument ou avec LIST, affiche sans écriture. ADD et REMOVE modifient
la liste partagée selon l'identifiant demandé. Transmets les arguments sans
interprétation shell et rapporte les erreurs sans réinitialiser le fichier.
Ne lance pas TFL ni PLLM et ne modifie pas OpenCode.

Cette commande source n'enregistre pas automatiquement une slash native.
Le skill est directement invocable avec `$lm`.

LM est l'unique liste noire de TFL et PLLM ; aucune liste permanente ne
subsiste. muse-spark-1.2-contributor est une entrée ordinaire retirable.

Arguments reçus : `$ARGUMENTS`
