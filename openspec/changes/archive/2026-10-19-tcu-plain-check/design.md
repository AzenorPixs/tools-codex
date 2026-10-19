## Context

Le script vérifie déjà sans écriture par défaut et possède --check/--apply.
Le skill traduit l'invocation explicite sans argument en application. La forme
sans tirets doit donc être reconnue explicitement avant cette traduction.

## Decisions

Ajouter un positionnel optionnel check et interdire son association à --apply.
Conserver tous les indicateurs existants. Afficher check dans les exemples et
le catalogue, garder --check comme alias compatible. Synchroniser les copies.

## Validation

Étendre les tests de modes et vérifier que check + --apply sort en erreur sans
appeler le moteur. Exécuter la suite sur Python 3.13/3.14, py_compile, parité,
UTF-8/LF et OpenSpec strict. Archiver et produire le rapport à six sections.
Le contrôle réel ne modifie aucun profil ; un conflit reste un résultat valide
et explicite du contrôle, pas une mise à jour réussie.

## Preuves

Les suites Python 3.13.5 et 3.14.8 réussissent chacune avec 44 tests, soit 88
exécutions finales réussies. Les trois py_compile, la parité CM/TCU et la
release locale inchangée à 0.3.0 sont vérifiés. Les deux exigences restent
sous 500 caractères. Le cas check --apply sort avec code 2 avant le moteur.

Le contrôle réel a été exécuté avant et après correction, avec --check puis
check. Les deux appels observent la release GitHub 0.2.2 au SHA
ef51e8f07279e99dfeebe6be5b53e0fc23f26af0, PLLM et TFL installés 0.2.2,
le skill global coding-session-statistics courant et les autres copies
recherchées absentes. Le dossier global de prompts est un lien : conflit
signalé, code 1, aucun remplacement et aucune sauvegarde. Cette règle est
préservée ; aucun forçage ni rafraîchissement de marketplace n'est lancé.

PROJECT (catalogue), TECHNICAL (mode de contrôle), BUILD (exemples), README
(usage) et CHANGELOG (Unreleased) sont actualisés. AGENTS et DEVOPS restent
inchangés : aucune nouvelle règle ni dépendance. VERSION, TOML et catalogue
marketplace sont inchangés. Les deux spécifications sont adaptées à la syntaxe
check en conservant la compatibilité --check. Les archives précédentes ne
sont pas reprises. La publication et l'application restent hors périmètre.
