# Mise en ligne du site EM Visions (version 2)

Le site est prêt à être hébergé chez **Netlify** sous **emvisions.ca**. Ce qui est déjà fait, puis ce qu'il reste à régler (dans l'ordre).

## Déjà fait dans le code

- **Formulaire de devis** : Netlify Forms. Netlify reçoit la demande et la pièce jointe (7 Mo au plus), filtre le pourriel (Akismet et un champ piège invisible pour les robots) et envoie la demande par courriel. Aucun serveur à entretenir.
- **Sécurité** (`site/_headers`, généré par `outils/generateur/securite.py`) :
  - politique de sécurité du contenu (CSP) stricte : seuls les scripts du site s'exécutent (empreintes SHA-256), aucun cadre externe, formulaire limité au site ;
  - HTTPS imposé (HSTS), protection contre l'intégration du site dans une autre page, contre la détection de type de fichier et contre l'accès à la caméra, au micro ou à la position ;
  - aucun secret ni aucune clé dans le code du site.
- **Témoins (cookies) et Loi 25** : sans Google Analytics, le site ne dépose aucun témoin, il n'y a donc pas de bannière. Dès que l'identifiant Google Analytics est ajouté, une bannière apparaît : Google ne se charge qu'après « Accepter », « Refuser » est aussi visible qu'« Accepter », le choix est gardé 12 mois et peut être changé en tout temps (lien « Témoins (cookies) » du pied de page).
- **Politique de confidentialité** (FR et EN) à jour : hébergement Netlify, filtrage Akismet, témoins, Google Analytics, conservation, droits, personne responsable (Eduardo Mazzonna).
- **Référencement** : adresse canonique emvisions.ca, plan du site, robots.txt, données d'entreprise locale (schema.org), page 404.

## À régler pour la mise en ligne

1. **Relier le dépôt à Netlify** : Add new project > Import an existing project > GitHub > `DavidJ97/em-visions`, branche **`version-2`**. Le fichier `netlify.toml` indique déjà le dossier à publier (`site`). Chaque envoi sur cette branche met le site à jour.
2. **Activer les formulaires** : Forms > *Enable form detection*, puis redéployer une fois.
3. **Recevoir les demandes par courriel** : Forms > *Form notifications* > *Add notification* > *Email notification*, avec l'adresse d'Eduardo. Mettre aussi cette adresse dans `CONTACT_EMAIL` (`outils/generateur/config.py`) pour qu'elle s'affiche sur le site.
4. **Domaine emvisions.ca** : Domain management > *Add a domain*, puis appliquer chez le registraire du domaine les enregistrements DNS que Netlify affiche. Ne pas toucher aux enregistrements de courriel (MX). Le certificat HTTPS est créé automatiquement.
5. **Google Analytics** : créer une propriété GA4, copier l'identifiant `G-XXXXXXXXXX` dans `GA_ID` (`config.py`) et reconstruire. La bannière et la mise à jour de la politique se font toutes seules.

## Loi 25 : à garder en tête

- Avant de confier des renseignements personnels à des fournisseurs hors du Québec (Netlify, Google, Akismet aux États-Unis), la loi demande une **évaluation des facteurs relatifs à la vie privée**. C'est un court document à faire une fois et à garder au dossier.
- Exporter puis supprimer régulièrement les demandes de devis dans Netlify (Forms), selon la durée indiquée dans la politique (2 ans pour une demande sans suite).
- Ce document n'est pas un avis juridique.
