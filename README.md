# Tools Codex

Version de release : `0.2.2`.

La source de vérité de cette version est le fichier [`VERSION`](VERSION).
La métadonnée Python du dépôt reprend cette release. Les branches Python
supportées sont 3.13 et 3.14 (`>=3.13,<3.15`), avec qualification hors ligne.

Utilisez **`$cm`** pour afficher le catalogue des commandes maison : `$cm`,
`$pllm` et `$tfl`, leurs syntaxes et descriptions. Ce skill remplace `/cm`.
Sa source est [`skills/cm/SKILL.md`](skills/cm/SKILL.md), exposée dans ce
projet via le lien relatif `.agents/skills/cm`. L'installation autonome hors
du projet et le contrôle de découverte sont décrits dans
[`BUILD.md`](BUILD.md#skill-catalogue-cm). Les plugins PLLM/TFL n'installent pas
ce catalogue à eux seuls.

PLLM accepte `--tfl-catalog CHEMIN` pour utiliser le catalogue TFL lorsque les
plugins sont installés séparément. Sans fichier courant initial, les quatre
politiques sont créées sans résultats historiques ; un fichier corrompu est
préservé. Les replis exigent les mesures du modèle effectivement sélectionné.
TFL exclut les prix non finis et publie un catalogue JSON strict.

Les prérequis et limites de qualification sont décrits dans
[`BUILD.md`](BUILD.md) et [`TECHNICAL.md`](TECHNICAL.md).
