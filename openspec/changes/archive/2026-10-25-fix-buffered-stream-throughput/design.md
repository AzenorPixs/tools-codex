# Débit moyen sur la requête complète

## Décision validée
Le débit est une moyenne observée côté client sur la durée complète de la
requête : avant l'ouverture HTTP jusqu'à la fin du flux et la libération de
la réponse. Il inclut TTFT, attente, réseau et raisonnement. Il ne prétend pas
mesurer la vitesse intrinsèque de génération du fournisseur.
Go/général : completion_tokens / request_seconds.
OpenRouter/DeepSeek : (completion_tokens - reasoning_tokens) / request_seconds,
avec les mêmes règles de comptage fiable que le protocole précédent.
Le premier token n'est plus soustrait puisque toute la durée est prise en compte.

Le calcul MUST utiliser la durée monotone non arrondie. Les valeurs arrondies
restent des affichages, jamais des dénominateurs. La fenêtre entre fragments
MAY rester un diagnostic ; elle SHALL NOT déterminer les tokens/s. Aucun
écrêtage ou plancher artificiel n'est introduit. Une réponse complète en un
bloc est admissible si compteurs et durée sont fiables. Une durée nulle,
négative ou non finie, un compteur incohérent ou un flux incomplet produit
une mesure indisponible et une cause explicite, sans ancienne valeur reprise.

## Protocole et mémoire
Le protocole devient 8, avec throughput_metric=request_average_v1,
throughput_window=request_total et measurement_protocol_version=8. Ces
champs sont additifs dans les rapports ; les compteurs, durées et formule
restent auditables. duration_seconds conserve son rôle d'affichage arrondi,
request_seconds porte le dénominateur non arrondi. Le TTFT reste défini sur
le premier contenu visible. Les portées de comptage restent distinctes.

La mémoire ajoute le profil de débit à l'identité de configuration. Les
anciens succès et leurs paliers sont conservés comme historique, mais ne sont
pas réutilisés pour le nouveau protocole. Une configuration sans succès de
même profil commence à 1024 ; un succès du nouveau profil reste réutilisable.
Les niveaux HIGH et XHIGH restent distincts. Les anciennes évaluations ne
sont pas réécrites ou présentées comme des contrôles actuels.

## Compatibilité et limites
Les quatre moteurs sont identiques et les paquets restent autonomes. Les
seuils numériques 15/20 tokens/s et TTFT 90/30 s sont conservés, mais le sens
du débit change : classement et éligibilité peuvent donc changer. Les valeurs
historiques ne sont pas directement comparables au nouveau débit.
Les interfaces CLI, colonnes, prix, filtres, HIGH/XHIGH et contrôles de quota
restent préservés. Aucun changement de modèle, secret ou compte.
Aucune migration destructive ; le retour à un ancien évaluateur reste une
action distincte, sans transformer les nouvelles mesures en preuves anciennes.

## Validation
Cas Mercury simulé, réception coalescée ou répartie, bloc unique, trois
transports, comptages global/réponse, précision non arrondie, durées invalides,
compteurs invalides, troncature/erreurs et absence de mesure périmée.
Tests d'intégration : classement, seuils stricts, filtres gratuits, mémoire
ancienne/nouvelle et parité des paquets. Suites Python 3.13/3.14, syntaxe,
imports, skills, JSON/release, UTF-8/LF et OpenSpec standard/strict.
Le recalcul 253/1,7751≈142,5 est une illustration des compteurs historiques,
pas un nouveau benchmark ni une validation fournisseur actuelle.
