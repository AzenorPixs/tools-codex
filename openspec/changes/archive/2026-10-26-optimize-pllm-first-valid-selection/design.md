## Context

Les six politiques et les tests actuels sont conservés. Le changement porte
sur l'ordre des candidats et la fin de leur parcours, ainsi que sur la
suppression du repli gratuit OpenRouter du mode5. Le périmètre SCM a été
explicitement validé par le développeur le 26 octobre 2026.

## Goals / Non-Goals

Retenir le premier succès sans tester les candidats suivants. Préserver la
distinction payants (<90 s et >15 tokens/s avec ressources) et gratuits
(<30 s et >20 tokens/s sans contrôle de ressources), les paliers
1024/2048/4096/8192 et le délai de 120 s. Contexte TFL ≥1M désigne une capacité
d'entrée vérifiée, sans envoi d'un million de tokens pendant le benchmark.

Les benchmarks réels, l'installation dans les profils, les opérations Git,
les modifications OpenCode et les changements TFL sont hors périmètre.

## Decisions

1. Trier les payants 1/2/5 par leur moyenne vérifiée des prix TFL (hors pointe
   Go, base OpenRouter). Le tri stable conserve l'ordre TFL à prix égal.
   Les rangs explicitement forcés ne sont pas réinterprétés.
2. Conserver l'ordre gratuit actuel : Go puis général, ordre des lignes TFL
   dans chaque section. Aucun classement par mesure historique.
3. Après une réussite, conserver ses contrôles et preuves et quitter le
   parcours du mode. Sinon, continuer les paliers puis le candidat suivant
   conformément aux règles HTTP existantes. Les erreurs d'authentification
   ou de ressources bloquantes arrêtent toujours le mode.
4. Un crédit épuisé invalide le mode5 avant génération. Sa catégorie reste
   payante, sans transition gratuite ; une invocation ultérieure relit le
   crédit. Les historiques gratuits restent lisibles mais ne valent pas
   sélection actuelle.
5. En invocation normale, poursuivre les politiques suivantes ; en active,
   conserver l'arrêt silencieux à la première politique valide. Tracer
   uniquement les candidats effectivement évalués, sans inventer de mesures
   pour les candidats non visités.

## Risks / Trade-offs

Le premier succès à prix égal ou gratuit peut être moins performant qu'un
candidat non testé : ce compromis de durée est explicitement demandé.
Le mode5 n'offre plus de service gratuit après épuisement. Les seuils et
contrôles restent inchangés, sans modification de secret ni migration.

## Validation

Tests déterministes des deux distributions : ordre de coût malgré un
catalogue désordonné, prix égaux stables, arrêt au premier succès, reprise
après échec, gratuit Go avant général, absence de génération après crédit
épuisé, forçages, active, seuils stricts et contrôles de ressources. Compléter
par syntaxe Python, suite hors ligne, parité, cohérence documentaire,
alignement de release et validations OpenSpec ciblée et globale.

## Preuves de qualification et cohérence

- Suite de référence avant modification : 71 tests PLLM réussis.
- Suite finale : 234 tests réussis sous Python 3.14.10 et 234 sous Python
  3.13.5, avec `unittest discover -s tests`, réseau et trousseau réels isolés
  dans les fixtures. Les répertoires temporaires sont créés dans le dépôt
  et nettoyés. Les échecs intermédiaires d'attentes exhaustives et de fixture
  ont été corrigés ; les deux suites finales sont sans échec.
- Syntaxe des huit fichiers Python modifiés vérifiée par `py_compile` sous
  Python 3.14.10, avec cache temporaire dans le dépôt puis nettoyé.
- Parité exacte des scripts et SKILL.md PLLM autonome/embarqué, UTF-8/LF.
- `quick_validate.py` : deux skills valides sous Python 3.13.5. PyYAML est
  absent du Python DevOps ; le validateur a utilisé le Python système déjà
  équipé, sans installation de dépendance. Le code projet est testé avec les
  deux runtimes ci-dessus.
- OpenSpec ciblé strict : valide avant code/tests ; un premier delta
  omettait des scénarios et a été corrigé avant implémentation.
- OpenSpec global standard et strict avant archivage : 9/9, zéro échec.
- Après qualification, release 0.7.5 alignée dans VERSION, pyproject.toml,
  cinq manifestes, README et référence courante BUILD.

| Élément | État et preuve de revue |
|---|---|
| Projet réel | Sélection vérifiée par tests des deux distributions ; mode6 inchangé, aucune qualification fournisseur réelle déduite. |
| AGENTS.md | Inchangé : règles de sécurité, OpenSpec, Git et statistiques d'archive conservées ; aucune règle générale n'est modifiée. |
| PROJECT.md | Inchangé : objectif, catalogue d'extensions, distributions et source VERSION restent exacts. |
| TECHNICAL.md | Mis à jour : sélection au premier succès, catégories fixes, contexte d'entrée, active et forçages dans Prérequis d'exécution. |
| BUILD.md | Mis à jour : comportement PLLM et référence à la release courante ; processus d'installation conservé. |
| DEVOPS.md | Inchangé : inventaire d'environnement et chemins d'outils, sans nouvelle dépendance. |
| README.md | Mis à jour : tableau des modes, ordre de sélection, tests actuels et release courante. |
| CHANGELOG.md | Mis à jour : entrée Unreleased sur la sélection, l'incompatibilité du mode5 gratuit et la release 0.7.5, sans date de publication inventée. |
| openspec/specs/ | Spécification pllm-evaluation synchronisée et change archivé le 26 octobre 2026. release-versioning reste applicable sans modification de ses exigences. |

La suppression du repli gratuit du mode5 et le départage stable à prix égal
sont des changements demandés. Les tests de troncature, HTTP 400/401/403/429,
seuils stricts, HIGH/XHIGH, ressources avant requête, mémoire, rangs forcés et
publication demeurent actifs. Aucun benchmark réel, profil utilisateur,
opération Git ou effet OpenCode n'est inclus dans cette qualification.

Après archivage, le contrôle standard a réussi à 8/8 avec un nouvel
avertissement de longueur, et le strict a échoué sur cet avertissement. Le
paragraphe concerné a été resserré à 441 caractères sans changer les
exigences, dans la spécification courante et son delta archivé. Les contrôles
finaux standard et strict réussissent à 8/8 sans avertissement. Aucun second
archivage n'a été réalisé. Le rapport STATISTIQUES.md atteste la clôture.
