# Qualifier les preuves TFL/PLLM et aligner Tools Codex 0.7.18

## Pourquoi

La collecte TFL courante contient des modèles OpenCode Go sous le plafond de
prix, mais PLLM les exclut faute de preuve Medium rattachée à leur fournisseur,
identifiant et transport exacts. Le diagnostic final masque ces exclusions
derrière « aucun candidat admissible ». Le mode7 utilise directement DeepSeek ;
sa documentation officielle indique que `medium` est accepté comme alias de
`high`, ce qui ne démontre pas un effort Medium effectif.

Le développeur valide le périmètre SCM le 27 octobre 2026 : améliorer la
traçabilité des preuves, produire une collecte TFL fraîche, évaluer les sept
politiques sans modifier leurs seuils, justifier chaque mode invalide et
incrémenter toutes les versions des composants Tools Codex.

## Changements

- Conserver une preuve Medium liée à l'identifiant et au transport OpenCode Go
  exacts : employer les niveaux courants publiés par models.dev quand ils sont
  présents, et compléter par des sources officielles lorsqu'ils manquent.
  Muse Spark 1.3 Contributor et Qwen3.8 Flash doivent apparaître admissibles
  dans la collecte TFL fraîche sans modification manuelle du catalogue.
- Tracer dans PLLM le motif exact d'exclusion du mode7 lorsque DeepSeek mappe
  Medium vers High ; ne pas qualifier cette équivalence de succès Medium.
- Lancer TFL, puis PLLM avec le catalogue tout juste produit et conserver les
  sept politiques, seuils, catégories, quotas, soldes et tests existants.
- Publier les rapports dans un emplacement local non versionné, sans inclure
  les quotas et soldes dans les artefacts distribués.
- Incrémenter de 0.7.17 à 0.7.18 `VERSION`, `pyproject.toml`, `README.md`,
  `CHANGELOG.md` et les six manifestes de plugins.

## Impact

Delta `tfl-catalog`, `pllm-evaluation` et `release-versioning` ; preuves
TFL/PLLM ; validation des deux distributions autonomes et embarquées ; tests
de preuves, d'admission des efforts et des sept politiques ; documentation et
versions des six plugins. Aucun seuil, secret, configuration d'agent, liste
noire ou politique fournisseur n'est modifié.

## Acceptation et limites

Les critères de chaque mode restent ceux de la spécification validée. Tous les
modes sont évalués avec des contrôles et mesures réels. Un mode est Valide
uniquement si tous ses critères sont observés ; sinon le rapport donne le
blocage précis, les preuves disponibles et les contrôles non exécutés. La
demande de résultat valide pour les sept modes ne permet pas de simuler une
mesure ni de traiter Medium mappé à High comme Medium.

La qualification de la version locale ne prouve ni son installation dans un
profil Codex ni une publication distante. La livraison de rapports réels
dépend des comptes, des services et de leurs disponibilités au moment de
l'exécution.
