# llm-refresh-scheduling Specification

## Purpose
Définir l'installation utilisateur et la séquence TFL puis PLLM conditionnée à l'activité Codex et à ses quotas disponibles.

## Requirements

### Requirement: Installation utilisateur idempotente
Le planning SHALL utiliser un timer systemd utilisateur à 00 h et 12 h
Europe/Paris, sans rattrapage. Les hooks approuvés et TCU SHALL partager une
seule installation. Le bootstrap SHALL NOT lancer de LLM, modifier les
planifications étrangères ou approuver lui-même la confiance des hooks.

#### Scenario: Réinstallation et horaires
- **WHEN** plusieurs paquets ou mises à jour enregistrent le planning
- **THEN** un seul timer déclenche aux deux horaires Paris, changements d'heure compris
- **AND** une échéance manquée n'est pas rejouée

### Requirement: Activité utilisateur réelle
Le runner SHALL exiger l'application Codex ou un CLI interactif ouvert du
même UID. Il SHALL NOT démarrer Codex ou assimiler un daemon, une exécution
non interactive ou un autre utilisateur à cette présence.

#### Scenario: Codex absent
- **WHEN** aucune application ou session CLI interactive du même utilisateur n'est ouverte
- **THEN** TFL et PLLM ne sont pas lancés et le passage est signalé ignoré

### Requirement: Quotas Codex frais avant chaque étape
Le runner SHALL lire en direct les quotas du bucket codex avant TFL puis
avant PLLM. Une fenêtre épuisée SHALL empêcher l'étape et sa suite. Un quota
absent, illisible ou non vérifiable SHALL produire un passage ignoré, jamais
un zéro inventé. Spark et les observations historiques SHALL NOT le remplacer.

#### Scenario: Quota épuisé au départ
- **WHEN** une fenêtre Codex indique un restant nul avant TFL
- **THEN** ni TFL ni PLLM ne sont exécutés

#### Scenario: Quota épuisé pendant TFL
- **WHEN** TFL réussit mais le nouveau contrôle Codex constate un restant nul
- **THEN** PLLM n'est pas exécuté et la cause est enregistrée

#### Scenario: Quota inconnu
- **WHEN** l'accès en lecture seule ou une fenêtre publiée n'est pas exploitable
- **THEN** aucun appel fournisseur de l'étape n'est lancé et la cause reste explicite

### Requirement: Séquence fraîche et exclusive
Le runner SHALL lancer TFL puis PLLM normal uniquement après succès et
publication fraîche TFL, avec --tfl-catalog explicite. Il SHALL empêcher les
chevauchements et la mise à jour TCU concurrente. Les invocations manuelles
SHALL conserver leurs comportements, seuils et exclusions existants.

#### Scenario: Échec ou ancien catalogue
- **WHEN** TFL échoue ou ne publie pas un nouveau catalogue valide
- **THEN** PLLM n'est pas exécuté et aucun ancien catalogue ne remplace cette étape

#### Scenario: Séquence déjà occupée
- **WHEN** une autre séquence ou une application TCU détient le verrou requis
- **THEN** le passage est ignoré sans attente ni seconde séquence

### Requirement: Installation préservée et diagnostic sûr
Les fichiers gérés SHALL être identifiés par reçu et empreintes, réguliers
et propres à l'utilisateur. Les conflits SHALL rester inchangés. Le retrait
SHALL être borné aux fichiers reconnus. État, erreurs et rapports SHALL NOT
exposer de secret, compte, transcription ou réponse brute d'authentification.

#### Scenario: Fichier étranger ou modifié
- **WHEN** une unité ou un runner cible n'est pas reconnu conforme au reçu
- **THEN** l'installation refuse de l'écraser et conserve les autres données

#### Scenario: Préservation après erreur
- **WHEN** l'installation ou une étape échoue
- **THEN** les effets réels sont décrits et les fichiers précédents sont préservés ou restaurés selon le repli borné
