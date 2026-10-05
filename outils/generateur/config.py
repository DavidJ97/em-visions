"""Réglages du site EM Visions. Tout ce qui risque de changer est ici."""
import os
# Adresse du site : à remplacer par le vrai domaine au lancement.
SITE_URL=os.environ.get('SITE_URL','https://davidj97.github.io/em-visions/site').rstrip('/')
# Courriel qui reçoit les demandes de devis. None tant que la nouvelle adresse n'existe pas
# (info@emvisions.ca rebondit). Dès qu'il est rempli : il apparaît dans le pied de page et la
# politique de confidentialité, et le formulaire envoie les demandes à cette adresse.
CONTACT_EMAIL=os.environ.get('CONTACT_EMAIL') or None
INSTAGRAM='https://instagram.com/visionsem'
# Heures d'ouverture — À CONFIRMER avec EM (sûr à 90 %). Le samedi est soit midi–14 h, soit
# 10 h–14 h : on affiche midi–14 h, la plage commune aux deux. Mettre HOURS=None pour les masquer.
HOURS=[(['Monday','Tuesday','Wednesday','Thursday','Friday'],'09:00','17:00'),(['Saturday'],'12:00','14:00')]
HOURS_FR=['Lun–ven : 9 h à 17 h','Sam : 12 h à 14 h']
HOURS_EN=['Mon–Fri: 9 am to 5 pm','Sat: 12 pm to 2 pm']
# Texte de présentation de la section À propos (remplace le bouton « Découvrir notre équipe »).
ABOUT_FR='Ouvert depuis la pandémie, EM Visions est un atelier de Saint-Léonard qui s’occupe de design graphique, d’impression et de vêtements personnalisés. Vous arrivez avec une idée, on la mène jusqu’au produit fini. Passez nous voir, rue Jean-Talon Est.'
ABOUT_EN='Open since the pandemic, EM Visions is a Saint-Léonard workshop handling graphic design, printing and custom apparel. You come in with an idea, we take it all the way to the finished product. Come see us on Jean-Talon Street East.'
