## 1. Contrat
- [x] 1.1 Consigner le diagnostic réel préalable, le périmètre validé et 0.6.1.
- [x] 1.2 Valider le delta strict avant code et tests.

## 2. Implémentation
- [x] 2.1 Séparer les paramètres Low par fournisseur et protocole.
- [x] 2.2 Extraire des diagnostics HTTP bornés, filtrés et réutilisables.
- [x] 2.3 Publier Retry-After sans rejouer les paliers HTTP 400/429.
- [x] 2.4 Synchroniser les scripts et les consignes des deux distributions.

## 3. Qualification et release
- [x] 3.1 Couvrir requêtes, erreurs, délais et absence de fuite par tests ciblés.
- [x] 3.2 Exécuter suites, syntaxe et imports sur Python 3.13/3.14.
- [x] 3.3 Vérifier skills, parité, encodage et périmètre ciblé.
- [x] 3.4 Aligner VERSION, pyproject.toml, README et cinq plugins en 0.6.1.
- [x] 3.5 Réviser les cadrages et documents concernés avec matrice de cohérence.

## 4. Clôture
- [x] 4.1 Valider OpenSpec ciblé, global standard et strict.
- [x] 4.2 Préparer l'archivage natif et les mesures du rapport post-archive.

La clôture requiert ensuite l'archive unique, les contrôles après fusion et
STATISTIQUES.md à six sections, sans réarchivage.

## Preuves avant archive

- Delta strict validé avant le code et les tests, puis revalidé.
- Suites finales : 178 tests sous Python 3.13.5 et 178 sous Python 3.14.9.
- 22 nouveaux tests HTTP, couvrant les deux distributions ; aucun test existant modifié ou désactivé.
- Trois fichiers Python compilés et deux scripts importés par branche ; Europe/Paris résolu.
- Deux skills validés par quick_validate.py ; scripts et SKILL.md identiques.
- VERSION, pyproject.toml, README et cinq manifestes alignés sur 0.6.1.
- 20 fichiers contrôlés avant archive : parité, encodage UTF-8/LF sans BOM et versions.
- OpenSpec ciblé strict, global standard 9/9 et global strict 9/9, sans avertissement.
- Contrôle ciblé de 44 empreintes : 15 modifications SCM prévues, un changement
  externe de DEVOPS.md et 28 fichiers inchangés avant synchronisation.
- Pour DEVOPS.md, remplacer localement le nouvel horodatage du relevé par
  l'initial retrouve exactement l'empreinte initiale : seul ce champ a changé.
  Le changement externe du 25 octobre 08:34:09 UTC est conservé sans écriture.
- Les preuves réelles de diagnostic précèdent l'implémentation ; aucune
  nouvelle requête fournisseur ni installation pendant cette qualification.
- Aucun échec ni avertissement dans les validations exécutées.

## Matrice documentaire avant archive

| Élément | État et preuve |
|---|---|
| Projet réel | Corps Low, erreurs et délais couverts par 178 tests ; contrat de génération préservé. |
| AGENTS.md | Inchangé ; périmètre, secrets et cycle OpenSpec appliqués. |
| PROJECT.md | Inchangé ; Catalogue actuel et organisation restent exacts. |
| TECHNICAL.md | Mis à jour ; contrats Low, extraction filtrée, Retry-After et tests. |
| BUILD.md | Mis à jour ; erreurs publiées, champs additifs et absence de migration. |
| DEVOPS.md | Aucun changement SCM ; seul horodatage externe du relevé préservé et vérifié par empreinte. |
| README.md | Mis à jour ; 0.6.1 et comportement HTTP 400/429. |
| CHANGELOG.md | Mis à jour ; quatre entrées Unreleased pour le correctif et sa release. |
| openspec/specs | Deux exigences modifiées et deux ajoutées, synchronisation native prévue. |

La clôture reste conditionnée à l'archive native unique, aux contrôles après
fusion et au rapport STATISTIQUES.md produit ensuite, sans réarchivage.

## Clôture observée

Archivage natif unique réussi avec specsUpdated=true : deux exigences ajoutées
et deux modifiées. Après fusion, global standard et strict 8/8 sans avertissement,
quatre blocs identiques au delta archivé et aucun change actif. Rapport
STATISTIQUES.md produit après l'archive, six sections, totaux SCM 16 fichiers
initiaux modifiés + six nouveaux chemins = 22, écart DEVOPS externe séparé.
Aucun échec de validation ni réarchivage.
