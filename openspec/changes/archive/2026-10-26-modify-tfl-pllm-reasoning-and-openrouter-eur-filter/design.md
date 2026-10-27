## Context

La collecte TFL et la sélection PLLM sont indépendantes et doivent toutes deux
filtrer avant les tests. Le moteur performance.py est distribué à quatre
emplacements identiques. Les modes 3/4 consomment aussi opencode dans le JSON.

## Goals / Non-Goals

Appliquer le périmètre approuvé : preuve HIGH/XHIGH, plafond OpenRouter EUR,
présentation à deux tableaux et release 0.7.9. Préserver les huit colonnes,
les prix natifs, le protocole 8, les six politiques, leurs catégories, seuils,
contrôles de ressources et forçages. Aucun benchmark fournisseur réel.

## Decisions

1. Centraliser l'admissibilité de l'effort dans performance.py. Une liste
   publiée contenant high ou xhigh est une preuve ; supported_efforts=null
   explicitement publié signifie tous les efforts de la passerelle. Une clé
   absente, une valeur invalide ou supports_max_tokens seul ne suffit pas.
   HIGH est préféré ; XHIGH est le seul repli. Aucune inférence par nom de
   modèle, famille, simple booléen reasoning ou requête historique réussie.
2. Filtrer dans les constructeurs TFL et dans ses rendus pour couvrir aussi
   des entrées anciennes. Les exclusions restent dans le JSON. PLLM valide
   chaque candidat, la frontière de génération, les résultats historiques et
   les rendus. Les lignes de politique sans candidat peuvent garder un
   diagnostic générique sans afficher l'identifiant d'un modèle exclu.
3. Embarquer le même traitement BCE/USD dans le moteur commun, sans dépendance
   d'un plugin sur un autre. TFL collecte une fois le dernier taux publié ;
   EUR = USD / USD_par_EUR. Date, source, récupération, taux positif fini sont
   vérifiés. Comparer les montants décimaux non arrondis au plafond inclusif.
   Le classement conserve l'ordre économique et les prix USD existants ;
   ajouter prix EUR et provenance. PLLM relit le taux actuel pour ses candidats
   OpenRouter et ne fait pas confiance à une moyenne EUR historique.
4. Le rapport TFL affiche Go puis OpenRouter, puis les essais gratuits
   admissibles à l'effort. La section opencode reste dans le JSON. Une section
   vide conserve la règle actuelle d'arrêt avant publication. Les prix Go et
   général gardent leur plafond 0,50 USD/M. Les colonnes OpenRouter sont en EUR.
5. Version unique 0.7.9 dans VERSION, pyproject.toml, README et les six
   manifestes. Documentation, commandes et catalogues CM sont synchronisés.

## Risks / Trade-offs

L'absence actuelle de capacités explicites Go peut rendre TFL non publiable ;
le développeur l'a acceptée. Une panne BCE est bloquante sans cours historique
de repli. Les anciennes qualifications ne satisfont pas la nouvelle preuve.
Les données utilisateur et rapports historiques ne sont pas réécrits. Retour
à une ancienne distribution possible par le développeur, sans migration
destructive, mais cette ancienne version n'applique pas les nouveaux filtres.

## Validation Strategy

Unité effort : fixtures absentes/invalides, null explicite, HIGH, XHIGH seul,
budget seul, gratuit/payant, forçage, historique, DeepSeek direct et absence
d'appels fournisseur pour les exclus. Unité EUR/rapport : seuil exact, valeur
supérieure avant arrondi, taux non unitaire/absent/invalide, récupération
échouée, préservation des fichiers, deux tableaux et JSON général conservé.
Puis suite hors ligne Python 3.13/3.14, compilation, parité des distributions,
UTF-8/LF, versions et validations OpenSpec ciblée, globale et stricte.


## Preuves finales avant archivage

- Périmètre approuvé par le développeur : strict HIGH/XHIGH, deux tableaux,
  plafond OpenRouter 0,20 EUR/M et release commune 0.7.9.
- Lot effort : 205 tests hors ligne réussis et compilation Python.
- Lot EUR/présentation : 113 tests ciblés réussis ; six tests EUR dédiés sur
  l'état final, dont la frontière décimale native et l'échec BCE sans écriture.
- Validation globale finale : 303 tests sous Python 3.14.10 et 303 sous
  Python 3.13.5, sans échec ni erreur, soit 606 exécutions pour 303 cas distincts.
- Compilation py_compile des 24 fichiers Python touchés sur chaque branche,
  soit 48 compilations. Temporaires sous tests, nettoyés après les contrôles.
- Quatre performance.py identiques ; scripts et skills TFL/PLLM et skills CM
  identiques dans les distributions autonome et embarquée.
- VERSION, pyproject.toml, README et six manifestes alignés sur 0.7.9.
  Contrôles UTF-8/LF et recherche de signatures de secrets réussis.
- OpenSpec avant archive : change ciblé strict valide ; global standard et
  strict 11/11. Aucun fournisseur réel ni installation utilisateur qualifié.
- Les 42 fichiers préexistants modifiés avant synchronisation sont identifiés
  par comparaison SHA-256 à l'instantané de lecture initial, sans inspection
  Git. Les nouveaux chemins sont explicitement recensés ; cette revue ciblée
  ne décrit pas les modifications antérieures ailleurs dans le dépôt.

## Matrice de cohérence documentaire

| Élément | État et preuve observée |
|---|---|
| Projet réel | Deux tableaux dans main TFL, admission commune et plafond dans catalog_candidate/evaluate_candidate ; 303 tests distincts réussis sur chaque branche. |
| AGENTS.md | Inchangé ; empreinte initiale préservée, aucune nouvelle dépendance ou règle d'environnement. |
| PROJECT.md | Mis à jour, catalogue TFL : Go/OpenRouter affichés et général conservé dans le JSON. |
| TECHNICAL.md | Mis à jour, admission stricte et contrat 0.7.9/BCE ; budget seul retiré. |
| BUILD.md | Mis à jour, présentation, admission et conversion ; installation/activation distinctes de la livraison locale. |
| DEVOPS.md | Inchangé ; empreinte initiale préservée, interprètes /usr/bin/python3 et /home/devops/python/current/bin/python3 utilisés. |
| README.md | Mis à jour, version 0.7.9, deux tableaux et plafond OpenRouter EUR/HIGH vérifiable. |
| CHANGELOG.md | Entrée Unreleased ajoutée sur le comportement, compatibilité et limites ; historique existant préservé. |
| openspec/specs/ | Deltas tfl-catalog/pllm-evaluation validés avant code ; synchronisation native prévue à l'archivage. Les autres capacités restent inchangées. |
| Skills/commandes/CM | Sources et distributions synchronisées ; descriptions et commandes reflètent le nouveau contrat. |

## Limites et reprise

Aucun TFL/PLLM fournisseur réel, TCU, profil utilisateur, planning, commit,
push, tag ou publication distante exécuté. Les tests isolent fournisseurs et
trousseau. Les profils installés restent distincts des sources 0.7.9. Les
capacités d'effort absentes peuvent exclure tout Go et DeepSeek direct ;
aucune réussite historique ne rétablit leur admissibilité. L'absence de taux
BCE vérifiable bloque la nouvelle publication sans cours de repli.
