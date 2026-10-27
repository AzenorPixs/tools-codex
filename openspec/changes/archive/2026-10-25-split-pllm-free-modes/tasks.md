## 1. Spécification validée
- [x] 1.1 Consigner le périmètre validé et les seuils renforcés 3/4.
- [x] 1.2 Valider le change et ses scénarios avant code et tests.

## 2. Implémentation
- [x] 2.1 Définir les six modes, comptes historiques, catégories et contrôles.
- [x] 2.2 Appliquer les seuils propres aux gratuits et adapter les forçages.
- [x] 2.3 Adapter historique et mémoire sans succès courant inventé.
- [x] 2.4 Adapter les rapports et synchroniser les deux distributions.

## 3. Qualification et documentation
- [x] 3.1 Couvrir les six modes et les régressions sur les deux distributions.
- [x] 3.2 Réussir les suites, syntaxe et imports sur Python 3.13/3.14.
- [x] 3.3 Mettre à jour TECHNICAL, BUILD, README, CHANGELOG et le wrapper.
- [x] 3.4 Aligner VERSION, pyproject.toml et les cinq manifestes sur 0.7.1.
- [x] 3.5 Contrôler les skills, la parité, UTF-8/LF et le périmètre des écritures.

## 4. Clôture
- [x] 4.1 Synchroniser pllm-evaluation et valider OpenSpec standard/strict.
- [x] 4.2 Revoir la matrice documentaire, consigner les preuves et préparer l'archive unique.
- [x] 4.3 Préparer les mesures et les six sections du rapport obligatoire après archive.

La checklist ci-dessus concerne les préconditions observées avant archive.
La clôture exige ensuite l'archive native unique, ses contrôles et le rapport
STATISTIQUES.md produit et vérifié dans cette archive, sans réarchivage.

## Preuves avant archive

- Le développeur a validé le périmètre SCM et imposé TTFT <30 s, débit >20
  pour les nouveaux gratuits 3/4. Les autres modes gardent <90 s et >15.
- Delta strict validé avant toute écriture de code ou test.
- Suites finales : 191 tests sous Python 3.13.5 et 191 sous Python 3.14.9,
  dont 13 nouveaux tests des six modes, avec sous-cas pour les deux distributions.
- Les tests existants qui représentaient les anciens modes et leur repli
  sont adaptés au comportement explicitement demandé, sans désactivation.
- 19 compilations et neuf imports de scripts par branche, Europe/Paris résolu.
- Deux SKILL.md validés par quick_validate.py ; scripts, skills et référence
  API identiques entre distributions. VERSION, pyproject.toml, README et cinq
  manifestes alignés sur 0.7.1.
- 24 fichiers livrables vérifiés en UTF-8/LF sans BOM avant archive.
- Onze exigences modifiées synchronisées, sans suppression ni renommage
  d'exigence ou abandon de scénario existant. Global standard et strict 9/9,
  sans avertissement après correction des paragraphes trop longs.
- Contrôle ciblé des empreintes initiales : aucune suppression ; seules
  modifications attendues. AGENTS, PROJECT, DEVOPS, CM et références inchangés.
- Essais intermédiaires : delta initial rejeté pour scénarios omis, puis corrigé ;
  attente incorrecte sur le gagnant d'un mode forcé corrigée et double découverte
  d'une classe importée supprimée. Ces essais ne sont pas des résultats finaux.
- Aucun accès fournisseur réel, aucune clé lue par l'agent, aucune installation,
  inspection Git, bascule OpenCode ou activation utilisateur.

## Matrice documentaire avant archive

| Élément | État et preuve |
|---|---|
| Projet réel | Six modes, catégories fixes, comptes et seuils couverts par les suites finales. |
| AGENTS.md | Inchangé ; règles de périmètre, secrets et OpenSpec appliquées ; empreinte conservée. |
| PROJECT.md | Inchangé ; Organisation, Catalogue actuel et Version de release restent exacts. |
| TECHNICAL.md | Mis à jour ; six modes, ressources, schéma 2, seuils et qualification. |
| BUILD.md | Mis à jour ; prérequis PLLM, migration et limites de retour de version. |
| DEVOPS.md | Inchangé ; chemins OpenSpec/Python et référentiel de prompts utilisés ; empreinte conservée. |
| README.md | Mis à jour ; tableau des six modes, version 0.7.1, migration et forçages. |
| CHANGELOG.md | Mis à jour dans Unreleased ; comportement livré, seuils, schéma et version locale. |
| openspec/specs | Onze exigences pllm-evaluation synchronisées et identiques au delta ; global 9/9 standard/strict. |

ORCHESTRATED_CODING.md est non applicable : SCM directe, sans pilotage.
L'installation réelle, la publication et les performances fournisseur actuelles
restent des preuves distinctes non réalisées dans ce périmètre.

## Clôture observée

Archive native unique réussie le 25 octobre 2026 :
2026-10-25-split-pllm-free-modes. specsUpdated=false car les onze exigences
étaient déjà synchronisées. Contrôles après archive : standard 8/8, strict
8/8, aucun avertissement ; onze blocs identiques au delta archivé et aucun
change actif. STATISTIQUES.md produit après archive et vérifié : six sections,
25 chemins uniques présents (19 modifiés + six nouveaux), quatorze tâches
préparatoires, parité, release 0.7.1 et UTF-8/LF sans BOM. Aucun réarchivage.
État : TERMINÉ pour le seul périmètre local validé.
