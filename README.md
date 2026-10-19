# Tools Codex

Version de release : `0.3.0`.

La source de vérité de cette version est le fichier [`VERSION`](VERSION).
La métadonnée Python du dépôt reprend cette release. Les branches Python
supportées sont 3.13 et 3.14 (`>=3.13,<3.15`), avec qualification hors ligne.

Utilisez **`$cm`** pour afficher le catalogue des commandes maison : `$cm`,
`$pllm`, `$tfl` et `$tcu`, leurs syntaxes et descriptions. Ce skill remplace `/cm`.
Sa source est [`skills/cm/SKILL.md`](skills/cm/SKILL.md), exposée dans ce
projet via le lien relatif `.agents/skills/cm`. Le plugin
[`cm`](plugins/cm/.codex-plugin/plugin.json) est également référencé dans la
marketplace Tools Codex et embarque le même skill. L'installation du plugin,
l'installation autonome hors du projet et le contrôle de découverte sont décrits dans
[`BUILD.md`](BUILD.md#skill-catalogue-cm). Les plugins PLLM/TFL n'installent pas
ce catalogue à eux seuls.

Choisissez le plugin CM ou la distribution autonome selon l'usage ; les deux
chargés simultanément peuvent produire deux entrées. Leur disponibilité dans
les sources ne démontre pas une installation dans un profil Codex.

PLLM accepte `--tfl-catalog CHEMIN` pour utiliser le catalogue TFL lorsque les
plugins sont installés séparément. Sans fichier courant initial, les quatre
politiques sont créées sans résultats historiques ; un fichier corrompu est
préservé. Les replis exigent les mesures du modèle effectivement sélectionné.
TFL exclut les prix non finis et publie un catalogue JSON strict.

Les prérequis et limites de qualification sont décrits dans
[`BUILD.md`](BUILD.md) et [`TECHNICAL.md`](TECHNICAL.md).

Utilisez **`$tcu check`** pour contrôler les mises à jour et **`$tcu`** pour
les appliquer aux briques déjà installées depuis la marketplace et GitHub.
TCU est aussi reconnu via `/TCU` ; le fichier de commande n'enregistre pas une
slash native. Le plugin [`tcu`](plugins/tcu/.codex-plugin/plugin.json) conserve
le [skill autonome](skills/tcu/SKILL.md) et son script identiques à la copie
embarquée. Sauvegardes, adoption et conflits sont décrits dans BUILD. TCU ne
modifie pas le checkout de développement et n'installe pas les briques absentes.
