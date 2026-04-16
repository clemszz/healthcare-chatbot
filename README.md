# 🩺 Assistant Santé Travail

Ce projet est un assistant conversationnel conçu pour aider les collaborateurs à s’orienter rapidement en cas de question liée à leur santé au travail.

L’idée est simple : proposer un point d’entrée unique, accessible via une interface de chat, qui permet d’identifier une situation (douleur, stress, besoin de rendez-vous, problématique de poste…) et de guider l’utilisateur vers les bons interlocuteurs dans l’entreprise.

L’application ne cherche pas à remplacer un professionnel de santé. Elle sert avant tout à **clarifier les démarches à suivre** et à éviter les situations où l’on ne sait pas vers qui se tourner.

---

## Fonctionnement

L’utilisateur décrit sa situation librement dans le chat.  
Le système analyse le message pour détecter le besoin principal, puis génère une réponse adaptée en s’appuyant sur un modèle de langage.

Les réponses restent volontairement simples et orientées action, par exemple :
- se rapprocher de la médecine du travail
- contacter les ressources humaines
- envisager un aménagement de poste

---

## Aperçu du projet :

<img width="934" height="601" alt="Capture d’écran 2026-04-15 à 21 39 26" src="https://github.com/user-attachments/assets/fe5e744b-bcd7-4191-8abb-07f53b670bf7" />


<img width="934" height="650" alt="Capture d’écran 2026-04-15 à 21 39 44" src="https://github.com/user-attachments/assets/786d40ef-88f0-43e4-aab2-483e5d806a4f" />



## Stack technique

- Python
- Streamlit (interface)
- API Mistral (génération de texte)
- python-dotenv (gestion des variables d’environnement)

*Le choix de Mistral s’explique par son positionnement européen et ses garanties en matière de conformité RGPD. Cependant,  l’utilisation de données potentiellement sensibles impose néanmoins une vigilance particulière et un encadrement adapté.*

Ce projet m’a permis de travailler sur un cas d’usage concret : intégrer un modèle de langage dans un outil simple, utile et directement compréhensible en contexte professionnel.
L’objectif était de rester pragmatique :
une interface légère
des réponses utiles
une logique métier simple mais pertinente

Limites :
pas de diagnostic médical
dépendance au modèle de langage
logique d’intention encore basique

Améliorations possibles :
intégration avec des outils internes (RH, planning)
gestion d’un historique utilisateur
amélioration de la détection d’intention
personnalisation selon l’entreprise
