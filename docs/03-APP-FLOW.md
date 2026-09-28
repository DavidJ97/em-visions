# 3. App Flow — EM Visions

> Objectif : chaque écran, chaque parcours et le résultat de chaque clic.

## Points d'entrée
- Lien direct `emvisions.ca` → Accueil (FR ou EN selon URL).
- Liens profonds partagés : `#services`, `#realisations`, `#catalogue`, `#a-propos`, `#contact`, et `#en/home`, `#en/services`, `#en/work`, `#en/catalog`, `#en/about`, `#en/contact`.
- Instagram (@visionsem), Google Maps, bouche-à-oreille.

## Inventaire des écrans (sections)
| Section | Rôle | Données requises |
| --- | --- | --- |
| Accueil | Promesse + devis + carrousel | 5 médias (devanture, Ricova, Buono, Elevate, MA) |
| Services | 6 prestations | Titres, descriptions, 2 médias (Elevate, MA vidéo) |
| Réalisations | Preuves | 5 projets + vidéos |
| Catalogue | Choisir un support | 6 fournisseurs + URL |
| À propos | L'équipe | Eduardo Mazzonna (design), Vince Mariani (gestion de projets) |
| Contact | Devis + boutique | Formulaire, adresse, carte |
| Menu mobile (plein écran) | Navigation < 1024 px | 6 liens, FR/EN, thème |
| Visionneuse projet | Agrandir un projet | Image + nom |
| Confirmation « Merci » | Après envoi | Référence de demande |

## Parcours principal
Accueil → « Demander un devis » → défilement doux vers Contact → remplir → « Demander un devis » → état « Envoi en cours… » → écran **MERCI.** (référence).

## Parcours alternatifs
- Accueil → défilement → Réalisations → « Voir le projet » → visionneuse → Échap → retour.
- Catalogue → survol/clic fournisseur → lien externe (nouvel onglet) → retour.
- N'importe où → EN → même section en anglais.
- Contact → « Itinéraire » → Google Maps (nouvel onglet).
- Merci → « Nouvelle demande » → formulaire vidé.

## Détail des actions
| Action | Déclencheur | Validation | Chargement | Succès | Erreur | Suite |
| --- | --- | --- | --- | --- | --- | --- |
| Lien menu | Clic | — | Défilement doux | Section active soulignée, URL mise à jour | — | Section |
| FR / EN | Clic | — | — | Textes traduits, titres réajustés | Traduction manquante → texte FR | Même section |
| Thème | Clic sur la lune | — | — | Calques clairs/sombres, choix mémorisé | — | — |
| Flèches carrousel | Clic, ← →, balayage | — | Fondu 0,55 s | Compteur 0X / 05, barre active | Vidéo indisponible → photo | — |
| Voir le projet | Clic | — | — | Visionneuse ouverte, focus sur Fermer | — | Échap = retour focus |
| Champ | Sortie du champ | Nom non vide, courriel valide, projet non vide, quantité entier ≥ 1 | — | Bordure normale | Bordure rouge + message | — |
| Fichier | Sélection | JPG/PNG/PDF, ≤ 10 Mo | — | Nom + poids affichés | Message format/poids | — |
| Envoyer | Clic | Tous les champs | « Envoi en cours… », bouton désactivé | Écran MERCI + référence | Réseau/serveur : message + saisie conservée | Merci |

## Règles de navigation
- Ordinateur : en-tête fixe, trait bleu qui glisse sous la section active.
- Mobile : en-tête collant, bouton ☰ → menu plein écran, Échap ou lien → fermeture.
- Retour navigateur : revient à la section précédente (historique des ancres).
- Défilement : l'URL suit la section visible (`history.replaceState`).

## États vides et bloqués
- Vidéo non chargée → image d'attente (poster).
- Réseau coupé à l'envoi → message + bouton réessayer, saisie conservée.
- Mouvement réduit → aucune vidéo, aucune animation.
- JavaScript désactivé → contenu lisible, liens d'ancre fonctionnels.

## Première visite
Pas de compte. Thème selon la préférence système, langue selon l'URL.
