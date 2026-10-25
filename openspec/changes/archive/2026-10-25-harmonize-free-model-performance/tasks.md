## 1. Spécification
- [x] 1.1 Consigner le périmètre validé et ses deux corrections explicites.
- [x] 1.2 Valider les deltas avant code et tests.

## 2. Réalisation
- [x] 2.1 Embarquer le moteur commun et préserver les contrats de mesure.
- [x] 2.2 Appliquer les seuils gratuits à PLLM et HIGH/XHIGH à ses six modes.
- [x] 2.3 Tester les gratuits TFL sans quotas et exclure leurs échecs.
- [x] 2.4 Tracer critères, raisonnement, essais, causes et exclusions.
- [x] 2.5 Synchroniser les distributions et adapter les paquets isolés.

## 3. Qualification et documentation
- [x] 3.1 Couvrir seuils, raisonnements, transports, comptes et publication.
- [x] 3.2 Réussir suites, syntaxe et imports sur Python 3.13/3.14.
- [x] 3.3 Actualiser skills, wrappers, CM, TECHNICAL, BUILD, README et CHANGELOG.
- [x] 3.4 Aligner VERSION, pyproject.toml et cinq manifestes sur 0.7.2.
- [x] 3.5 Vérifier parité, UTF-8/LF, secrets simulés et périmètre des écritures.

## 4. Préparation de clôture
- [x] 4.1 Synchroniser les spécifications et valider OpenSpec standard/strict.
- [x] 4.2 Consigner les preuves et la matrice documentaire ; préparer l'archive.
- [x] 4.3 Préparer les mesures du rapport obligatoire à six sections.

La clôture exige ensuite l'archive unique, ses contrôles puis la production
et vérification de STATISTIQUES.md, sans réarchivage.

## Preuves avant archive

- Le développeur a validé le périmètre SCM en 0.7.2, puis imposé l'exclusion
  des gratuits échoués dans TFL et HIGH avec le seul repli XHIGH pris en charge.
- Deltas stricts validés avant toute écriture de code ou test.
- Suites finales : 208 tests sous Python 3.13.5 et 208 sous Python 3.14.9,
  dont 17 nouveaux tests communs, avec sous-cas pour les distributions.
- 24 fichiers compilés et 13 scripts importés par branche ; Europe/Paris résolu.
- Six SKILL.md validés par quick_validate.py ; parité autonome/embarqué de
  PLLM, TFL et CM, et quatre moteurs performance.py identiques.
- VERSION, pyproject.toml, README et cinq manifestes alignés sur 0.7.2.
- 39 livrables vérifiés UTF-8/LF sans BOM ; neuf exigences synchronisées :
  cinq PLLM et quatre TFL. Global standard et strict 9/9 sans avertissement final.
- Contrôle ciblé de 50 empreintes initiales : 29 modifications prévues,
  21 fichiers inchangés, aucune suppression initiale ; cinq nouveaux fichiers
  source/tests et cinq artefacts de change avant le rapport post-archive.
- Les cas incluent seuils stricts, HIGH/XHIGH, mémoire Low non réutilisée,
  corps et parseurs, gratuité/variantes, métadonnées invalides, HTTP filtré,
  absence de quota gratuit TFL, clés distinctes par fournisseur, retrait de
  models, exclusions auditables, paquets isolés et rapports préservés si vide.
- Essais intermédiaires : deux erreurs dues au même fixture de sérialisation
  sans id, corrigé en conservant sa valeur NaN pour vérifier le rejet JSON ;
  quatre avertissements de longueur normative corrigés avant qualification finale.
- Seule la documentation officielle a été consultée sur le web. Aucun appel
  de génération réel, accès aux valeurs de clés par l'agent, inspection Git,
  installation, mise à jour TCU ou changement OpenCode.

## Matrice documentaire avant archive

| Élément | État et preuve |
|---|---|
| Projet réel | Qualification gratuite TFL et HIGH/XHIGH couverts par 208 tests sur deux branches. |
| AGENTS.md | Inchangé, empreinte conservée ; sécurité, périmètre et OpenSpec appliqués. |
| PROJECT.md | Inchangé, empreinte conservée ; organisation, catalogue et rôles de comparaison/évaluation restent exacts. |
| TECHNICAL.md | Mis à jour ; moteur embarqué, filtres, HIGH/XHIGH, authentification et preuves. |
| BUILD.md | Mis à jour ; empaquetage performance.py, génération gratuite et limites par compte. |
| DEVOPS.md | Inchangé, empreinte conservée ; chemins Python/OpenSpec et référentiel de prompts utilisés. |
| README.md | Mis à jour ; 0.7.2, seuils communs, filtres TFL et raisonnement. |
| CHANGELOG.md | Mis à jour dans Unreleased ; comportement, exclusions, raisonnement et release locale. |
| openspec/specs | Neuf exigences synchronisées et identiques aux deltas ; standard et strict 9/9. |

ORCHESTRATED_CODING.md est non applicable : SCM directe, sans pilotage.
L'archive unique et le rapport post-archive restent obligatoires pour clore.

## Clôture observée

Archive native unique réussie le 25 octobre 2026 :
2026-10-25-harmonize-free-model-performance. specsUpdated=false parce que les
neuf exigences étaient déjà synchronisées. Après archive : standard 8/8,
strict 8/8, aucun avertissement, neuf blocs identiques aux deltas et aucun
change actif. STATISTIQUES.md est produit puis vérifié : six sections,
40 chemins uniques présents (29 modifiés + onze nouveaux), quinze tâches
préparatoires, UTF-8/LF sans BOM, release 0.7.2 et parité des distributions.
Les 50 empreintes initiales donnent 29 modifications attendues et 21 fichiers
inchangés, aucune suppression initiale. Aucun réarchivage, installation ou
benchmark fournisseur réel. État : TERMINÉ pour le périmètre local validé.
