# Conception

## Décision
Étendre uniquement la grammaire de canonical_id : un `~` optionnel au début
est accepté s'il précède un segment fournisseur valide suivi de `/`.
La grammaire existante des segments, du modèle et du suffixe reste inchangée.
La canonicalisation retire déjà le préfixe par le dernier `/` ; le marqueur
ne doit donc jamais entrer dans l'identité canonique.

`~vendor/model`, `vendor/model` et `model` partagent ainsi la même identité.
`~xiaomi/mimo-v2.5:free` reste exclu par le défaut mimo-v2.5 ; une entrée
personnalisée ou permanente conserve le même effet. Les noms voisins restent
distincts. `~model`, `~~vendor/model`, `vendor/~model`, espaces, contrôles,
Unicode et longueurs supérieures à 256 caractères restent invalides.

## Unités et preuves
1. Spécification préalable : valider les deux deltas strictement avant code.
2. Module et tests indissociables : la même grammaire dans les six paquets,
   tests de canonicalisation, bornes, CRUD canonique, corruption, TFL et
   gardes de génération PLLM sans accès réel. Cette unité partage un seul
   invariant : aucun préfixe marqué ne contourne l'identité LM.
3. Release et documentation : 0.7.7 dans neuf supports, descriptions dans
   TECHNICAL/README/CHANGELOG, suite globale Python 3.13 et 3.14, parité,
   syntaxe, UTF-8/LF et OpenSpec strict. Le test préexistant inspectant Git
   reste non exécuté, conformément à SCM, et n'est jamais compté réussi.
4. Synchroniser et archiver une seule fois après les contrôles, produire le
   rapport à six sections, puis relancer TFL depuis skills/tfl avec
   --output-dir /home/ade/.codex/skills/tfl/data. Les trois tableaux et les
   essais gratuits sont restitués, ou l'erreur réelle sans résultat inventé.

## Risques et limites
Le `~` n'est pas autorisé dans le modèle final ni ailleurs dans l'identifiant.
Une alias fournisseur dont le nom final est différent reste une identité
distincte : aucune résolution approximative ou distante n'est introduite.
La limite de 256 porte sur l'identifiant complet, marqueur compris.
Le stockage et le schéma ne changent pas. Aucun mécanisme de migration n'est
nécessaire ; les sources antérieures ne reconnaissent pas ces préfixes mais
leur stockage canonique reste compatible. Le profil installé reste en 0.7.6
jusqu'à une mise à jour distincte ; seul le rapport TFL y sera actualisé si
la relance réussit. Les erreurs réseau, d'accès ou de performance des gratuits
restent possibles et ne justifient aucun assouplissement des seuils.
