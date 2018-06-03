from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

typeStatutRequete = (('Disponible','Disponible'),('Suspendue','Suspendue'),('Clôturée','Clôturée'))
satisfactionSuiviRequete = (('0','Satisfait'),('1','Insatisfait'))
sexeUtilisateur = (('0','Masculin'),('1','Feminin'))

class Utilisateur(AbstractUser):
	sexeUtilisateur = models.CharField(max_length=1, default="Masculin", choices=sexeUtilisateur, verbose_name="Sexe")
	fiabiliteUtilisateur = models.IntegerField(default = 0, verbose_name="Fiabilité")
	zoneUtilisateur = models.ForeignKey('ZoneGeographique', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Région")

	def __str__(self):
		return self.username

	class Meta:
		unique_together = ('email',)
		verbose_name = "Utilisateur"

class ZoneGeographique(models.Model):
	idZoneGeographique = models.AutoField(primary_key=True)
	nomZoneGeographique = models.CharField(max_length=100, verbose_name="Nom de la région")

	def __str__(self):
		return self.nomZoneGeographique

	class Meta:
		verbose_name = "Zone"

class Requete(models.Model):
	idRequete = models.AutoField(primary_key=True)
	dateRequete = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Date")
	titreRequete = models.CharField(max_length=100, verbose_name="Titre")
	texteRequete = models.TextField(verbose_name="Texte")
	remunerationRequete = models.IntegerField(verbose_name="Rémunération")
	statutRequete = models.CharField(max_length=42, choices=typeStatutRequete,default="Disponible", verbose_name="Statut")
	categorieRequete = models.ForeignKey('CategorieRequete', on_delete=models.CASCADE, verbose_name="Catégorie")
	demandeurRequete = models.ForeignKey('Utilisateur', null=True, blank=True, on_delete=models.CASCADE, related_name='idDemandeurRequete', verbose_name="Pseudo demandeur")
	repondeurRequete = models.ForeignKey('Utilisateur', null=True, blank=True, on_delete=models.CASCADE, related_name='idRepondeurRequete', verbose_name="Pseudo Répondeur")

	def __str__(self):
		return self.titreRequete

	class Meta:
		verbose_name = "Requête"
		ordering = ['-dateRequete']

class CategorieRequete(models.Model):
	idCategorieRequete = models.AutoField(primary_key=True)
	nomCategorieRequete = models.CharField(max_length=100, verbose_name="Nom de la catégorie")

	def __str__(self):
		return self.nomCategorieRequete

	class Meta:
		verbose_name = "Catégorie"

class SuiviRequete(models.Model):
	idSuiviRequete = models.AutoField(primary_key=True)
	requeteSuiviRequete = models.ForeignKey('Requete', on_delete=models.CASCADE, verbose_name="Titre de la requête")
	satisfactionSuiviRequete = models.CharField(max_length=1, choices=satisfactionSuiviRequete, verbose_name="Satisfaction")
	commentaireSuiviRequete = models.TextField(verbose_name="Commentaires")

	class Meta:
		verbose_name = "Suivi"
