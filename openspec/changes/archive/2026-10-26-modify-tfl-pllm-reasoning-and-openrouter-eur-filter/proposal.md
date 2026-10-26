# Filtrage strict HIGH/XHIGH et plafond OpenRouter en euros

## Why

TFL publie actuellement des payants sans preuve de prise en charge de HIGH ou
XHIGH, et ses consommateurs PLLM peuvent reprendre ces candidats. Le rapport
affiche aussi un tableau général OpenCode devenu indésirable et applique à
OpenRouter un plafond de 0,50 USD/M au lieu du plafond demandé de 0,20 EUR/M.

## What Changes

- Exiger une capacité HIGH ou XHIGH vérifiable pour chaque candidat gratuit ou
  payant TFL/PLLM, avant génération, sélection et affichage. Les capacités
  absentes, invalides ou limitées à un budget de tokens sont exclues.
- Conserver les causes dans les audits JSON, sans afficher ces modèles dans
  aucun tableau ni réutiliser un historique pour contourner ce contrôle.
- Retirer le tableau général OpenCode du rapport TFL ; conserver sa collecte
  indépendante et sa section JSON pour les modes gratuits PLLM 3/4.
- Convertir les prix OpenRouter USD en EUR au dernier taux BCE publié et
  appliquer moyenne <= 0,20 EUR/M ; tracer taux, date et source, conserver les
  prix USD et publier les colonnes tarifaires OpenRouter en EUR.
- Réappliquer les critères dans PLLM, y compris aux anciens catalogues et aux
  forçages ; préserver seuils de performance, catégories et priorités.
- Aligner la release locale commune et les six plugins sur 0.7.9.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `tfl-catalog`: admissibilité HIGH/XHIGH, plafond EUR, deux tableaux fournisseurs.
- `pllm-evaluation`: contrôle indépendant de l'effort et du plafond OpenRouter,
  publication sans modèles dont l'effort est invérifiable.

## Impact

Distributions autonomes et embarquées TFL/PLLM, moteur commun performance.py,
tests hors ligne, commandes, descriptions CM, documentation et manifestes.
Les fournisseurs sans métadonnées d'effort peuvent perdre tous leurs candidats.
Une sélection vide ou une conversion invalide empêche la nouvelle publication
TFL et préserve les rapports existants. Aucun effet utilisateur, Git, réseau
de qualification, installation, activation du planning ou publication distante.

## Validation du développeur

Périmètre SCM approuvé le 26 octobre 2026, y compris l'exclusion lorsque
HIGH/XHIGH n'est pas vérifiable, le cycle OpenSpec jusqu'à l'archivage et la
release commune 0.7.9.
