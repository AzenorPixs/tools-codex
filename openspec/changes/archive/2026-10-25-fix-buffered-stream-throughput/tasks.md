## 1. Contrat
- [x] 1.1 Consigner le diagnostic et la méthode validée, release 0.7.3.
- [x] 1.2 Valider les deltas avant toute écriture de code ou test.

## 2. Réalisation
- [x] 2.1 Corriger la mesure dans le moteur commun et ses quatre copies.
- [x] 2.2 Tracer durée non arrondie, formule, portée et nouveau protocole.
- [x] 2.3 Isoler la mémoire par profil sans supprimer les succès historiques.
- [x] 2.4 Adapter publication et documentation PLLM/TFL.

## 3. Qualification et release
- [x] 3.1 Reproduire la rafale Mercury et couvrir les cas de mesure.
- [x] 3.2 Vérifier mémoire, classement, seuils et qualification gratuite.
- [x] 3.3 Réussir les suites, syntaxe et imports sur Python 3.13/3.14.
- [x] 3.4 Vérifier skills, parité, UTF-8/LF et périmètre des écritures.
- [x] 3.5 Aligner VERSION, pyproject.toml, README et cinq plugins sur 0.7.3.

## 4. Préparation de clôture
- [x] 4.1 Synchroniser les spécifications et valider OpenSpec standard/strict.
- [x] 4.2 Consigner les preuves et la matrice documentaire ; préparer l'archive.
- [x] 4.3 Préparer les mesures du rapport obligatoire à six sections.

La clôture exige ensuite l'archive unique, ses contrôles puis la production
et vérification de STATISTIQUES.md, sans réarchivage.

## Preuves avant archive

- Méthode et périmètre validés explicitement par le développeur : durée totale,
  portées de comptage conservées, aucun écrêtage, release 0.7.3 et clôture SCM.
- Delta strict validé avant code et tests.
- Suites finales : 222 tests sous Python 3.13.5 et 222 sous Python 3.14.9,
  dont 14 nouveaux tests avec sous-cas sur les distributions et transports.
- Cas Mercury simulé : 715 - 462 = 253 tokens de réponse sur 1,7751 s,
  soit 142,527 tokens/s malgré une fenêtre de fragments arrondie à 0,0001 s.
  Ce cas utilise les compteurs historiques comme fixture, pas un appel réel.
- Invariance au regroupement, bloc unique, trois transports, durée non arrondie,
  durées/compteurs invalides, absence de mesure périmée, classement et TFL
  gratuits, mémoire ancienne préservée et nouveau profil réutilisable couverts.
- 25 compilations et 13 imports de scripts par branche ; Europe/Paris résolu.
- Quatre SKILL.md validés ; scripts et skills autonomes/embarqués identiques,
  quatre moteurs identiques. Pas d'ancienne formule dans les sources ciblées.
- VERSION, pyproject.toml, README et cinq manifestes alignés sur 0.7.3.
- 33 livrables UTF-8/LF sans BOM avant archive ; quatre exigences synchronisées
  (trois PLLM, une TFL), global standard et strict 9/9 sans avertissement.
- Contrôle ciblé : 58 empreintes initiales, 27 modifications prévues,
  31 fichiers inchangés et aucune suppression initiale. Un nouveau test et
  cinq artefacts de change sont comptés séparément avant le rapport.
- Aucun échec dans les suites exécutées ; aucune dépendance ajoutée, aucun
  accès web, appel fournisseur, secret lu, installation, TCU ou opération Git.

## Matrice documentaire avant archive

| Élément | État et preuve |
|---|---|
| Projet réel | Mesure et intégrations couvertes par 222 tests sur deux branches Python. |
| AGENTS.md | Inchangé, empreinte conservée ; sécurité, périmètre et cycle OpenSpec appliqués. |
| PROJECT.md | Inchangé, empreinte conservée ; architecture, catalogue et version commune restent exacts. |
| TECHNICAL.md | Mis à jour ; durée totale, compteurs, protocole et mémoire distincte. |
| BUILD.md | Mis à jour ; distribution cohérente 0.7.3 et relance distincte après installation. |
| DEVOPS.md | Inchangé, empreinte conservée ; chemins Python/OpenSpec et référentiel utilisés. |
| README.md | Mis à jour ; 0.7.3, portée du débit et limite de comparaison historique. |
| CHANGELOG.md | Mis à jour dans Unreleased ; correction, protocole et release locale. |
| openspec/specs | Quatre exigences ciblées synchronisées ; global standard/strict 9/9. |

La cohérence vérifiée concerne le périmètre du débit corrigé. Une mention
préexistante dans « Classement interne par performances » dit encore
« Go avant général pour le repli modes 1/2 », alors que les gratuits autonomes
sont en 3/4 et 1/2 restent payants. Ce libellé historique est signalé hors
périmètre et laissé intact ; il ne change pas le calcul ni l'ordre exécuté.
ORCHESTRATED_CODING.md est non applicable à cette SCM directe.
La clôture exige encore l'archive unique et le rapport post-archive vérifié.

## Clôture observée

Archive native unique réussie le 25 octobre 2026 :
2026-10-25-fix-buffered-stream-throughput. specsUpdated=false car les quatre
exigences étaient déjà synchronisées. Après archive : standard 8/8, strict
8/8, aucun avertissement, quatre blocs identiques aux deltas et aucun change
actif. STATISTIQUES.md produit puis vérifié : six sections, 34 chemins uniques
présents (27 modifiés + sept nouveaux), quatorze tâches préparatoires,
UTF-8/LF sans BOM, release 0.7.3 et distributions identiques.
Les 58 empreintes initiales donnent 27 modifications attendues et 31 fichiers
inchangés, aucune suppression initiale. L'écart de libellé préexistant décrit
dans la matrice reste signalé et inchangé. Aucun réarchivage, installation ou
benchmark fournisseur réel. État : TERMINÉ pour le périmètre local validé.
