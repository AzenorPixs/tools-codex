# Matrice de cohérence documentaire

| Élément | État et preuve observée |
|---|---|
| Projet réel | TFL à deux sections ; PLLM 1/2 payants Go et 3/4 gratuits Go, anciens catalogues inclus. 323 tests globaux réussis sur chacune des deux branches Python. |
| AGENTS.md | Inchangé ; empreinte baseline.json conservée. Règles de sécurité et d'autorisation appliquées. |
| PROJECT.md | Mis à jour : Catalogue actuel et investigation des deux catalogues. |
| TECHNICAL.md | Mis à jour : prérequis, modes 1 à 4, contrat producteur/consommateurs, deux sections et planning, contrat 0.7.12. Helpers historiques isolés explicités. |
| BUILD.md | Mis à jour : catalogue distribué, usage PLLM et contrat 0.7.12 ; installation/activation distinctes. |
| DEVOPS.md | Inchangé depuis le début SCM ; empreinte conservée. Python DevOps et binaire OpenSpec déclarés utilisés. |
| README.md | Mis à jour : release 0.7.12, Go exclusif pour 1 à 4, deux catalogues et garde du planning. |
| CHANGELOG.md | Entrées Unreleased ajoutées pour retrait, Go exclusif, exclusion LM utilisateur et release ; historique préservé. |
| OpenSpec | tfl-catalog, pllm-evaluation et llm-refresh-scheduling synchronisés par archive native ; standard et strict globaux 10/10 après archive. |
| Commandes et skills | Instructions TFL/PLLM/CM et guides de preuve mis à jour ; parité des six paquets et douze schedulers vérifiée. |
| VERSION / pyproject / manifestes | Release 0.7.12 alignée dans la source de vérité, métadonnée Python, README et six manifestes. |
| LM utilisateur | ADD explicites des familles inkling et inkling-small, conservation des deux exclusions précédentes et idempotence prouvées ; défauts distribués inchangés. |

Aucun nouveau langage, dépendance, lint, frontend ou mécanisme de migration
n'est introduit. La compilation py_compile et les tests hors ligne couvrent
Python 3.13.5 et 3.14.10. L'anomalie tarifaire OpenRouter observée avant SCM
reste signalée et hors périmètre. Les résultats fournisseur, anciens rapports,
profils installés et timer réel ne sont pas requalifiés ou actualisés par ces preuves.
