# Harmoniser les tests gratuits et le raisonnement

## Why
Le développeur a validé le cycle SCM jusqu'à l'archive et STATISTIQUES.md,
release 0.7.2, puis imposé l'exclusion TFL des gratuits échoués et HIGH avec
repli XHIGH lorsque disponible. Ces décisions remplacent la proposition de
conserver les gratuits échoués dans models et le défaut Low.

## What Changes
- Tous les gratuits MUST exiger contexte ≥1M, prix nuls vérifiés, réponse
  complète, TTFT <30 s et débit >20 tokens/s, y compris le repli gratuit de 5.
- TFL MUST tester les gratuits des trois catalogues et exclure les échecs
  de models, en gardant les tentatives et causes dans excluded_models.
- Tous les benchmarks PLLM et les gratuits TFL MUST demander HIGH, puis XHIGH
  seulement si HIGH est indisponible et XHIGH pris en charge. Aucun repli Low.
- Un moteur local commun MUST être embarqué dans chaque paquet pour conserver
  leur autonomie. Les clés et données privées MUST rester hors des sorties.
- VERSION, pyproject.toml, README et cinq manifestes MUST déclarer 0.7.2.

## Capabilities
### Modified Capabilities
- pllm-evaluation : seuils gratuits, HIGH/XHIGH et mémoire par configuration.
- tfl-catalog : mesures gratuites, exclusions, authentification et restitution.

## Impact
Scripts et skills PLLM/TFL autonomes/embarqués, moteur performance.py dans
chacun, wrappers PLLM/TFL, CM autonome/embarqué, tests, TECHNICAL, BUILD,
README, CHANGELOG, VERSION, pyproject.toml et cinq manifestes. Les six modes,
comptes partagés 1/3 et 2/4, quotas des payants et leurs seuils restent préservés.
Aucun accès aux clés par l'agent, aucune installation, activation ni opération
Git. Qualification hors ligne ; documentation officielle consultée en lecture.
