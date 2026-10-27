# Conception

## Stockage et API
Chaque distribution LM/TFL/PLLM embarque le même scripts/model_blacklist.py,
sans dépendre d'un plugin voisin. La source canonique est celle de LM.
Le chemin unique est CODEX_HOME/lm/blacklist.json, avec ~/.codex en repli
si CODEX_HOME est absent. TFL/PLLM chargent sans écrire ; fichier absent :
schéma 1 et models=[mimo-v2.5] en mémoire. LM LIST est aussi sans écriture.
ADD/REMOVE réalisent un verrou local, valident, puis remplacent atomiquement
le fichier. Une liste vide explicite permet le retrait de la valeur initiale.
Les exclusions permanentes historiques restent indépendantes et non retirables
par LM. Le fichier utilisateur hors cache est préservé par TCU sans migration.
Les tests utilisent exclusivement des profils temporaires sous tests/.

## Identité des modèles
Comparer des identifiants ASCII validés, sans espaces ni caractères de contrôle.
Normaliser la casse, retirer le préfixe fournisseur (dernier segment /),
puis les seuls suffixes :free et -free. Pas de sous-chaîne approximative :
mimo-v2.5-pro et mimo-v2.50 restent distincts. Les paramètres ADD/REMOVE
stockent les identités canoniques triées et uniques ; une opération répétée
est idempotente. Un JSON invalide, dupliqué ou illisible bloque les consommateurs
avant appel fournisseur et préserve le fichier, sans réinitialisation silencieuse.

## Frontières de filtrage
TFL applique LM aux trois collecteurs, puis vérifie encore avant qualification
gratuite ; les exclus restent dans excluded_models avec cause, jamais parmi
models ni les tests gratuits. Le JSON conserve la politique LM appliquée.
PLLM recharge la liste à l'invocation et vérifie aussi les sélecteurs/rangs,
le candidat direct du mode6 et la frontière evaluate_candidate. Les rangs
forcés gardent leur cible : une cible interdite est refusée sans substitution.
Les modèles historiques interdits sont invalidés et retirés des listes de
candidats ; aucune mémoire ne rend valide un candidat interdit. Les rapports
historiques sur disque ne sont pas réécrits par LM lui-même.
Les priorités, quotas, prix, seuils, HIGH/XHIGH et protocole 8 restent inchangés.

## Distribution et repli
LM fournit SKILL.md, agents/openai.yaml (LM), scripts/lm.py et le module commun,
un manifeste de release 0.7.6, .codex/commands/LM.md et le lien relatif
.agents/skills/lm. La marketplace et CM décrivent les six invocations.
TCU découvre les composants depuis le catalogue ; les tests prouvent la mise
à jour des copies LM déjà présentes et la conservation des absents/données.
Une slash source ne promet pas un enregistrement natif automatique ; $lm
est l'invocation de skill. Aucun profil installé n'est changé ici.
Retour de sources possible vers 0.7.5 ; l'ancien code ignore LM, donc ne
constitue pas un retour conservant les exclusions utilisateur.

## Matrice documentaire
PROJECT : catalogue LM. TECHNICAL : stockage, normalisation, filtrage.
BUILD : distribution et utilisation. README : 0.7.6 et syntaxes.
CHANGELOG : ajout et limites dans Unreleased. AGENTS : inchangé, règles suffisantes.
DEVOPS : inchangé, outils et branches Python existants. Specs : nouvelle
capacité et deltas TFL/PLLM/distribution ; release-versioning conservée.

## Validation prévue
Tests LM CRUD/atomicité/erreurs/concurrence ; intégration Go/général/OpenRouter,
forçages, historique et mode6 ; preuve d'absence de génération pour les exclus.
Tests hors ligne Python 3.13 et 3.14 ; compilation py_compile isolée, validateurs
skills, parité, paquets isolés, versions JSON/TOML, TCU simulé, UTF-8/LF,
OpenSpec ciblé et global strict avant/après archivage. Aucun benchmark réel.
