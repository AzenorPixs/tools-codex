# Qualifier les preuves TFL/PLLM et aligner Tools Codex 0.7.18

## Pourquoi

La collecte TFL courante contient des modèles OpenCode Go sous le plafond de
prix, mais PLLM les exclut faute de preuve d'acceptation du paramètre Medium
rattachée à leur fournisseur, identifiant et transport exacts. Le diagnostic
final masque ces exclusions derrière « aucun candidat admissible ». Le mode7
utilise directement DeepSeek ; sa documentation officielle indique que
`medium` est accepté comme alias de `high`.

Le développeur valide le périmètre SCM le 27 octobre 2026, puis précise le
28 octobre 2026 que l'acceptation API du paramètre `medium` suffit, même si le
fournisseur le convertit ou l'ignore. Les seuils de performance, les quotas et
les soldes restent inchangés.

## Changements

- Conserver une preuve d'acceptation Medium liée à l'identifiant et au transport OpenCode Go
  exacts : employer les niveaux courants publiés par models.dev quand ils sont
  présents, et compléter par des sources officielles lorsqu'ils manquent.
  Muse Spark 1.3 Contributor et Qwen3.8 Flash doivent apparaître admissibles
  dans la collecte TFL fraîche sans modification manuelle du catalogue.
- Tracer dans PLLM que l'API DeepSeek accepte le paramètre Medium comme alias
  de High ; considérer le critère d'acceptation satisfait sans prétendre à un
  effort interne Medium, puis effectuer le benchmark payant normal.
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

Tous les modes sont évalués avec des contrôles et mesures réels. Un mode est
Valide uniquement si ses ressources, sa réponse, ses seuils et l'acceptation
du paramètre demandé sont observés. Une API qui accepte `medium` valide ce
critère même si elle le convertit, l'ignore ou ne l'applique pas en interne ;
le rapport n'affirme pas que l'effort interne est Medium. Un refus API de
`medium` ou l'échec d'un autre critère laisse le mode invalide avec sa cause
précise. Aucune mesure n'est simulée.

La qualification de la version locale ne prouve ni son installation dans un
profil Codex ni une publication distante. La livraison de rapports réels
dépend des comptes, des services et de leurs disponibilités au moment de
l'exécution.
