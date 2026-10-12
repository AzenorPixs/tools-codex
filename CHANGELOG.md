# Changelog

## Unreleased

- Déclarer le support Python 3.13/3.14 (`>=3.13,<3.15`) et aligner la métadonnée Python sur la release 0.2.1 de VERSION, sans packaging ou publication Python supplémentaire.

- Ajouter `--tfl-catalog CHEMIN` à PLLM en conservant le chemin voisin par défaut, et initialiser les quatre politiques lorsqu'aucun fichier courant n'existe ; préserver les fichiers corrompus.
- Recalculer les paliers après repli HTTP 429 et exiger les mesures du remplaçant avant toute sélection valide.
- Exclure les prix OpenRouter non finis et les débordements ; empêcher la publication d'un catalogue TFL non conforme au JSON strict.
- Qualifier ces comportements hors ligne dans les deux distributions ; l'installation réelle et les accès fournisseurs restent non vérifiés.

## 0.2.1 — 2026-10-10

- Porter le seuil strict de TTFT PLLM de 60 à 90 secondes, avec couleur et critères publiés cohérents.
- Aligner la release du projet et les manifestes PLLM/TFL sur 0.2.1.
