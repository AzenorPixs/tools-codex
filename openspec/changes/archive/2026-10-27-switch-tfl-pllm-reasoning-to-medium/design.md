## Contexte

TFL et PLLM ont chacun une distribution autonome et une copie embarquée. Le
moteur de performance est partagé au sein de chacune des distributions, et
les candidats sont filtrés avant la génération. Les métadonnées `null`
explicitement publiées signifient que la passerelle accepte tous les efforts ;
elles permettent donc l'admission en Medium, mais le test doit envoyer Medium.

## Objectifs et hors périmètre

Exiger, tracer et demander Medium partout dans TFL et PLLM. Préserver les
transports, seuils, paliers, priorités, contrôles de ressources et protocoles
de mesure. Hors périmètre : qualification fournisseur réelle, actualisation
des profils utilisateurs et requalification manuelle de rapports existants.

## Décisions

1. `verified_effort` renvoie `medium` lorsque `supported_efforts` contient
   `medium` ou vaut explicitement `null`. Une liste qui ne contient que
   `high`/`xhigh`, une clé absente, une valeur invalide ou un budget seul
   n'est pas une preuve admissible.
2. `choose_effort` demande `medium` par défaut et refuse tout niveau différent.
   Tous les transports conservent leur encodage, en envoyant la valeur
   `medium`. Aucun refus d'effort ne déclenche un repli vers HIGH ou XHIGH.
3. Les identités de mémoire restent distinguées par effort. Les succès
   HIGH/XHIGH existants ne correspondent donc pas à Medium et ne réduisent pas
   le premier palier Medium, qui commence à 1024 sans réussite correspondante.
4. Les rapports et preuves historiques ne sont ni édités ni réinterprétés.
   Les sources et descriptions sont synchronisées entre les deux modes de
   distribution.
5. La release commune devient 0.7.14 dans `VERSION`, `pyproject.toml`, les six
   manifestes et la documentation publique.

## Risques

Des candidats jusqu'ici valides peuvent être exclus s'ils ne déclarent pas
Medium. Les refus de paramètre Medium arrêtent le candidat selon le protocole
HTTP existant ; aucun repli d'effort n'est permis. Les rapports déjà publiés
restent datés et peuvent décrire l'ancien contrat jusqu'à leur prochaine
exécution.

## Stratégie de validation

Les tests hors ligne vérifient les preuves Medium et null, l'exclusion des
listes High/XHigh seules, l'envoi Medium pour chaque transport, l'absence de
repli après HTTP 400, la séparation des mémoires et la synchronisation des
copies. Exécuter ensuite la suite Python du dépôt, la compilation des fichiers
modifiés, les contrôles de versions, d'encodage, de parité et OpenSpec.
