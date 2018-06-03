from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UtilisateurCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = Utilisateur
		fields = ('username', 'email', 'first_name', 'last_name', 'sexeUtilisateur', 'zoneUtilisateur')

class UtilisateurChangeForm(UserChangeForm):
	class Meta:
		model = Utilisateur
		fields = UserChangeForm.Meta.fields

class RequeteForm(forms.ModelForm):
	class Meta:
		model = Requete
		fields = ['titreRequete', 'categorieRequete', 'remunerationRequete', 'statutRequete', 'texteRequete', 'repondeurRequete']

class SuiviRequeteForm(forms.ModelForm):
	class Meta:
		model = SuiviRequete
		fields = ['satisfactionSuiviRequete', 'commentaireSuiviRequete']

class CategorieRequeteForm(forms.ModelForm):
	class Meta:
		model = CategorieRequete
		fields = ['nomCategorieRequete']
