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
- **Interface d'administration** : `emvisions.ca/admin/`, aux couleurs du site (Sveltia CMS, logiciel libre, successeur de Netlify/Decap CMS ; fonctionne aussi sur téléphone). On y modifie les coordonnées, les heures, les textes de l'accueil, de l'À propos et des services, et les réalisations (avec photos). Chaque « Enregistrer » enregistre la modification dans le dossier `contenu/` du dépôt GitHub ; Netlify reconstruit alors le site en une minute environ. Les photos (JPG, PNG, HEIC d'iPhone) sont réduites et converties en WebP dans le navigateur avant l'envoi, puis déclinées en miniature à la construction. Le contrôle de qualité GitHub reconstruit et vérifie aussi le site à chaque modification. Une valeur invalide ne casse jamais le site : elle est ignorée et la valeur d'origine est gardée.

## À régler pour la mise en ligne

1. **Relier le dépôt à Netlify** : Add new project > Import an existing project > GitHub > `DavidJ97/em-visions`, branche **`version-2`**. Le fichier `netlify.toml` indique déjà la commande de construction et le dossier à publier (`site`). Chaque envoi sur cette branche, y compris depuis /admin, met le site à jour.
2. **Activer les formulaires** : Forms > *Enable form detection*, puis redéployer une fois.
3. **Recevoir les demandes par courriel** : Forms > *Form notifications* > *Add notification* > *Email notification*, avec l'adresse d'Eduardo. Pour l'afficher aussi sur le site : /admin > Coordonnées > Courriel public.
4. **Domaine emvisions.ca** : Domain management > *Add a domain*, puis appliquer chez le registraire du domaine les enregistrements DNS que Netlify affiche. Ne pas toucher aux enregistrements de courriel (MX). Le certificat HTTPS est créé automatiquement.
5. **Ouvrir /admin** (une seule fois) :
   - GitHub > Settings > Developer settings > OAuth Apps > *New OAuth App* : Homepage URL `https://emvisions.ca`, Authorization callback URL `https://api.netlify.com/auth/done`. Copier le *Client ID* et créer un *Client secret*.
   - Netlify > Project configuration > Access & security > OAuth > *Install provider* > GitHub : coller l'ID et le secret.
   - Eduardo se crée un compte GitHub ; dans le dépôt, Settings > Collaborators > *Add people*, avec le droit d'écriture.
   - Se connecter sur `https://emvisions.ca/admin/` avec *Se connecter avec GitHub*.
   - Solution de rechange, sans l'étape OAuth : *Se connecter avec un jeton d'accès* (GitHub > Settings > Developer settings > Personal access tokens > *Fine-grained*, accès au seul dépôt `em-visions`, permission *Contents: Read and write*).
6. **Google Analytics** : créer une propriété GA4, copier l'identifiant `G-XXXXXXXXXX` dans `GA_ID` (`config.py`) et reconstruire. La bannière et la mise à jour de la politique se font toutes seules.

## Utiliser /admin

- **Coordonnées** : téléphone, courriel public, lien Instagram. Un champ vide n'apparaît pas sur le site.
- **Heures d'ouverture** : pour chaque jour, *Ouvert* puis l'heure d'ouverture et de fermeture (format 24 h, ex. `09:00`). Décocher *Afficher les heures sur le site* pour les masquer partout.
- **Accueil**, **À propos**, **Services** : texte en français et en anglais. Si l'anglais est laissé vide, le français s'affiche sur la page anglaise.
- **Réalisations** : *Ajouter projet* (il s'ajoute en haut), le nom du client, le type de travail, puis *Ajouter photo* > *Parcourir* > *Téléverser* (JPG, PNG ou HEIC) avec une courte description de ce qu'on voit. La première photo sert de vignette. Les flèches changent l'ordre des projets.
- Cliquer **Enregistrer**. Le site est à jour environ une minute plus tard.

## Loi 25 : à garder en tête

- Avant de confier des renseignements personnels à des fournisseurs hors du Québec (Netlify, Google, Akismet aux États-Unis), la loi demande une **évaluation des facteurs relatifs à la vie privée**. C'est un court document à faire une fois et à garder au dossier.
- Exporter puis supprimer régulièrement les demandes de devis dans Netlify (Forms), selon la durée indiquée dans la politique (2 ans pour une demande sans suite).
- Ce document n'est pas un avis juridique.
