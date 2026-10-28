# Conception

Ajouter ACL à DIRECT dans les deux copies identiques. Le chemin reste choisi par l’entrée ACL de l’index déclaré dans DEVOPS.md ; le nom attendu est ACL.md. Aucun nouveau mode, paramètre, dépendance ou mécanisme de repli.

Les tests couvrent API et CLI des deux distributions, source absente, rejet de acl avant configuration, conservation du texte et du système de fichiers, et absence de RUN/actions. Les suites existantes couvrent les alias et CISMP.

La release patch passe de 0.7.25 à 0.7.26, avec VERSION, pyproject.toml, six manifestes et README alignés. Le test LM portant une attente littérale de release est ajusté uniquement à cette version.

AGENTS.md, PROJECT.md et DEVOPS.md restent exacts et inchangés. TECHNICAL.md, BUILD.md, README.md et CHANGELOG.md décrivent ACL. Les registres existants suivent ce seul change sans attribution de code. Archivage après validations ; STATISTICS.md à six sections à partir des preuves accessibles. Aucun retour automatique de version ni installation ; le correctif est limité à des sources locales réversibles.
