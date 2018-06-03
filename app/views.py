from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import UtilisateurCreationForm

class ListeRequete(ListView):
	model = Requete
	context_object_name = "requetes"
	template_name = "app/liste_requete.html"
	paginate_by = 10

class DetailRequete(DetailView):
	model = Requete
	context_object_name = "requete"
	template_name = "app/detail_requete.html"

class RequeteUpdate(UpdateView):
	model = Requete
	form_class = RequeteForm
	template_name = "app/requete_update_form.html"
	success_url = reverse_lazy('mes_requetes')

	def get_object(self, queryset=None):
		pk = self.kwargs.get('pk', None)
		return get_object_or_404(Requete, pk=pk)

	def form_valid(self, form):
		self.object = form.save()
		messages.success(self.request, "Votre requête a été mise à jour avec succès.")
		return HttpResponseRedirect(self.get_success_url())

class RequeteDelete(DeleteView):
	model = Requete
	context_object_name = "requete"
	success_url = reverse_lazy('mes_requetes')

	def get_object(self, queryset=None):
		pk = self.kwargs.get('pk', None)
		return get_object_or_404(Requete, pk=pk)

	def form_valid(self, form):
		self.object = form.save()
		messages.success(self.request, "Votre requête a été supprimée avec succès.")
		return HttpResponseRedirect(self.get_success_url())

class SuiviRequeteUpdate(UpdateView):
	model = SuiviRequete
	form_class = SuiviRequeteForm
	template_name = "app/suivirequete_update_form.html"
	success_url = reverse_lazy('mes_requetes')

	def get_object(self, queryset=None):
		pk = self.kwargs.get('pk', None)
		return get_object_or_404(SuiviRequete, pk=pk)

	def form_valid(self, form):
		suivi = form.save(commit=False)
		requete = suivi.requeteSuiviRequete
		repondeur = requete.repondeurRequete
		user = Utilisateur.objects.filter(pk=repondeur.pk)
		if suivi.satisfactionSuiviRequete == "Satisfait" :
			user.update(fiabiliteUtilisateur=user.fiabiliteUtilisateur+1)
		elif suivi.satisfactionSuiviRequete == "Insatisfait" :
			user.update(fiabiliteUtilisateur=user.fiabiliteUtilisateur-1)
		user.save()
		self.object = form.save()
		messages.success(self.request, "Votre suivi a été mis à jour avec succès.")
		return HttpResponseRedirect(self.get_success_url())

class SignUp(CreateView):
	form_class = UtilisateurCreationForm
	success_url = reverse_lazy('login')
	template_name = 'app/inscription.html'

@login_required
def mes_requetes(request):
	user = request.user
	mes_requetes = Requete.objects.filter(demandeurRequete=user.pk)
	return render(request, 'app/mes_requetes.html', {'mes_requetes':mes_requetes})

@login_required
def mon_profil(request):
	profil = request.user
	return render(request, 'app/mon_profil.html', {'profil':profil})

@login_required
def suivi(request, idRequete):
	requete = get_object_or_404(Requete, idRequete=idRequete)
	suivi = SuiviRequete.objects.filter(requeteSuiviRequete=requete)
	if not suivi :
		if request.method == 'POST' :
			form = SuiviRequeteForm(request.POST)
			if requete.repondeurRequete == None :
				return HttpResponse("Veuillez renseigner le répondeur de la requête avant de réaliser le suivi")
			else :
				if form.is_valid():
					suivi = form.save(commit=False)
					repondeur = requete.repondeurRequete
					setattr(suivi, 'requeteSuiviRequete', requete)
					suivi.save()
					user = Utilisateur.objects.filter(pk=repondeur.pk)[0]
					fiabilite = user.fiabiliteUtilisateur
					if suivi.satisfactionSuiviRequete == "Satisfait" :
						user.update(fiabiliteUtilisateur=fiabilite+1)
					elif suivi.satisfactionSuiviRequete == "Insatisfait" :
						user.update(fiabiliteUtilisateur=fiabilite-1)
					user.save()
					return redirect('mes_requetes')
		else :
			form = SuiviRequeteForm()
		return render(request, 'app/suivirequete_create_form.html', {'form': form, 'idRequete': idRequete})
	else :
		return render(request, 'app/detail_suivi.html', {'suivi': suivi,'requete': requete})

@login_required
def mes_suivis(request):
	user = request.user
	mes_suivis = SuiviRequete.objects.filter()
	return render(request, 'app/mes_suivis.html', {'mes_suivis':mes_suivis})

@login_required
def profil(request, username):
	profil = get_object_or_404(Utilisateur, username=username)
	return render(request, 'app/profil.html', {'profil':profil})

@login_required
def creer_requete(request):
	user = request.user
	if request.method == 'POST':
		form = RequeteForm(request.POST)
		if form.is_valid():
			requete = form.save(commit=False)
			requete.demandeurRequete = user
			requete.save()
			return redirect('liste_requete')
	else :
		form = RequeteForm()
	return render(request, 'app/creer_requete.html', {'form': form})

def inscription(request):
	if request.method == 'POST':
		form = UtilisateurCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activation de votre compte AppLance'
			message = render_to_string('app/acc_active_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': account_activation_token.make_token(user),})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return HttpResponse('Veuillez confirmer votre adresse mail pour rejoindre AppLance')
	else:
		form = UtilisateurCreationForm()
	return render(request, 'app/inscription.html', {'form': form})

def activation(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = Utilisateur.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('home')
	else:
		return HttpResponse("Le lien d'activation de votre compte est invalide")
