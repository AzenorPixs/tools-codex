# Conception

## Déclarations canoniques
Les six commandes sources portent les noms CM.md, PLLM.md, TFL.md, TCU.md,
LM.md et PROMPT.md. Les déclencheurs /CM, /PLLM, /TFL, /TCU, /LM et /PROMPT
sont documentés comme formes canoniques. Les noms techniques et les chemins
de skills restent en minuscules ; agents/openai.yaml déclare le libellé
en majuscules dans chacune des deux distributions.

## Compatibilité TCU
La source PROMPT.md est canonique ; une ancienne source prompt.md reste
lisible pour permettre le contrôle d'une release antérieure, sans retour de
version forcé. Pour chaque commande canonique, TCU sélectionne les copies
canoniques ou historiques effectivement présentes ; aucune autre commande
absente n'est créée. Le wrapper PROMPT absent est la seule création autorisée.
Si prompt.md existe seul, sa mise à jour reste sur ce nom avec sa provenance.
Si les deux noms existent, les deux sont vérifiés dans le même plan et le
même reçu de composant. Les reçus génériques ignorent les deux graphies de
PROMPT lorsque le composant dédié les gère. Les gardes sur liens, modifications
locales, adoption, sauvegarde et retour de version restent applicables.

## Validation et repli
Les tests isolent GitHub, le CLI et les profils. Ils couvrent les noms
canoniques, les copies historiques avec reçus, les collisions des deux
graphies, les liens et modifications locales, l'absence de doublon et check
sans écriture. La qualification vérifie aussi les six commandes, libellés,
manifestes, la release et la parité autonome/embarquée, sous Python 3.13/3.14.
Les sauvegardes TCU et son repli atomique restent inchangés. La livraison
des sources ne modifie pas les profils installés ni les liens externes.
