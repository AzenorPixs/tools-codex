# Conception

## Preuves et cause

Diagnostic réel préalable, 25 octobre 2026 : trois sondes reproduisent les
erreurs originales, une sonde Go modifie uniquement le corps en retirant
thinking et une dernière sonde générale extrait le délai de reprise. Les
clés restent confinées au processus local, les erreurs sont filtrées avant
restitution ; aucun fichier ou résultat PLLM publié n'est modifié.

Beam Free Go : Chat Completions avec reasoning_effort=low et thinking activé
reçoit HTTP 400, invalid_request_error, paramètre thinking non pris en charge.
Sans thinking et avec Low inchangé : réponse complète, 505 tokens, budget
1024, TTFT 1,6694 s et débit global 388,52 tokens/s. Cela établit un correctif
du contrat de requête, sans réduire le raisonnement.

Beam Free général et Nemotron gratuit général : HTTP 429 avec Retry-After.
La sonde détaillée de Beam indique une limite d'usage gratuit par modèle et
56249 secondes, soit un réessai estimé le 26 octobre à 01:00 Europe/Paris.
Le détail de reprise de Nemotron n'a pas été extrait. Le compteur exact,
sa clé compte/IP et la réussite après échéance restent inconnus. Aucun
contournement de limite ou d'identité de client n'est proposé.

## Paramètres

OpenCode Go et général, chat_completions : reasoning_effort=low uniquement.
Responses garde reasoning.effort=low ; Messages garde le budget thinking
déjà défini. DeepSeek direct conserve thinking activé et reasoning_effort=low.
OpenRouter conserve sa résolution Low depuis ses métadonnées. Aucun nom
de modèle ne détermine le corps ni n'est ajouté à une liste de compatibilité.

## Extraction sûre

Lire au plus 64 Kio du corps d'une erreur HTTP, une seule fois, en mémoire.
Ne garder que des codes et noms de paramètres connus et un diagnostic issu
de catégories explicites. Tout texte non reconnu devient une erreur générique.
Ne publier ni message brut, compte, clé, URL d'erreur ou valeur de session.
Fermer la réponse HTTP même si elle est vide, invalide ou déjà fermée.
Mémoriser seulement l'extraction filtrée sur l'objet erreur pour les couches
qui le consultent plusieurs fois ; ne pas conserver le corps brut.

Retry-After accepte secondes entières non négatives ou date HTTP avec fuseau.
Résoudre une échéance ISO avec fuseau ; une date passée vaut délai nul. Une
valeur absente, malformée, négative ou hors plage reste indisponible, sans
inventer de date. La disponibilité après cette échéance n'est pas garantie.
Le JSON conserve le diagnostic dans les tentatives et le candidat concerné ;
la cellule État présente le paramètre refusé ou la limitation et la reprise.

## Reprises

HTTP 400 et HTTP 429 terminent les paliers de ce candidat pour cette invocation.
Ne pas augmenter max_tokens ni dormir jusqu'à un quota journalier. Poursuivre
les autres candidats de la catégorie autorisée, avec leurs propres contrôles.
La reprise annoncée n'autorise aucune exécution planifiée ni changement de
catégorie. Les troncatures et seuils mesurés continuent d'utiliser les quatre
paliers. 401/403 gardent leurs règles ; les autres erreurs sont inchangées.

## Qualification et livraison

Tests des corps envoyés par les quatre contrats, HTTP 400/429 et une seule
tentative, 401/403 préservés, délais numériques/dates HTTP, erreurs vides ou
non JSON, double lecture, filtrage de contenus sensibles et fermeture des flux.
Préserver le classement et la mémoire par configuration. Aucune nouvelle
dépendance ni migration destructive. Les sources restent réversibles ; les
champs JSON sont additifs et les historiques existants restent lisibles.

Sources documentaires consultées pendant le diagnostic : documentation Go et
catalogue général OpenCode, RFC 6585 section 4. Un Retry-After est une
indication d'attente, pas une preuve de succès futur. Les suites finales sont
hors réseau/trousseau, distinctes de ces sondes préalables. Les profils et
la marketplace installés restent inchangés pendant ce SCM.
