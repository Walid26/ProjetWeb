from django.contrib import admin
from .models import *
from django.utils.text import Truncator
from .forms import UtilisateurCreationForm, UtilisateurChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

class RequeteAdmin(admin.ModelAdmin):
	list_display   = ('titreRequete', 'demandeurRequete', 'dateRequete', 'remunerationRequete','apercu_texte')
	list_filter    = ('demandeurRequete','categorieRequete','statutRequete')
	date_hierarchy = 'dateRequete'
	ordering       = ('dateRequete',)
	search_fields  = ('titreRequete', 'texteRequete')
	
	def apercu_texte(self, requete):
		return Truncator(requete.texteRequete).chars(50, truncate='...')

	apercu_texte.short_description = ('Aperçu de la requête')

class UtilisateurAdmin(UserAdmin):
	add_form = UtilisateurCreationForm
	form = UtilisateurChangeForm
	model = Utilisateur
	list_display = ['email', 'username', 'zoneUtilisateur']

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Requete, RequeteAdmin)
admin.site.register(ZoneGeographique)
admin.site.register(CategorieRequete)
admin.site.register(SuiviRequete)
