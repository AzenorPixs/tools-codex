# Accepter les préfixes OpenRouter marqués sans contourner LM

## Why
Le catalogue réel OpenRouter contient des identifiants tels que
`~unbiased/pareto-latest`. Le validateur LM rejette leur préfixe et arrête
TFL avant publication. La liste noire par défaut reste pourtant valide.

## What Changes
- Accepter un unique `~` initial dans un préfixe fournisseur complet.
- Préserver l'identité canonique, les exclusions LM et permanentes, les
  validations strictes et le stockage utilisateur sans migration.
- Synchroniser les six modules LM/TFL/PLLM et qualifier leurs intégrations.
- Aligner la release locale et les six plugins sur 0.7.7, documenter,
  synchroniser et archiver ce seul change avec ses statistiques.
- Relancer TFL depuis la source corrigée vers les rapports usuels du profil.

## Capabilities
### New Capabilities
Aucune nouvelle capacité indépendante.
### Modified Capabilities
- `lm-blacklist`: préfixe marqué et invariants de canonicalisation.
- `tfl-catalog`: collecte complète contenant ces identifiants.

## Impact
Les six copies de scripts/model_blacklist.py, tests/test_lm_blacklist.py,
et l'attente de release du test d'instantané réel dans tests/test_tcu_update.py,
TECHNICAL.md, README.md, CHANGELOG.md, VERSION, pyproject.toml et les six
manifestes. Aucun changement de seuil, transport, dépendance ou secret.
AGENTS, PROJECT, BUILD et DEVOPS restent applicables sans modification.
La relance TFL est autorisée ; aucune publication Git ni installation de
sources dans le profil n'est incluse. Les anciens rapports restent préservés
en cas d'échec de la collecte ou de la qualification gratuite.

## Autorisation
Le développeur a validé explicitement le périmètre autonome SCM le
26 octobre 2026 : correction sans affaiblissement LM, tests, 0.7.7,
archivage OpenSpec avec statistiques, puis relance réelle TFL.
