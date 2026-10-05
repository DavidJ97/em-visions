"""Réglages du site EM Visions. Tout ce qui risque de changer est ici."""
import os
# Adresse du site : à remplacer par le vrai domaine au lancement.
SITE_URL=os.environ.get('SITE_URL','https://davidj97.github.io/em-visions/site').rstrip('/')
# Courriel qui reçoit les demandes de devis. None tant que la nouvelle adresse n'existe pas
# (info@emvisions.ca rebondit). Dès qu'il est rempli : il apparaît dans le pied de page et la
# politique de confidentialité, et le formulaire envoie les demandes à cette adresse.
CONTACT_EMAIL=os.environ.get('CONTACT_EMAIL') or None
INSTAGRAM='https://instagram.com/visionsem'
