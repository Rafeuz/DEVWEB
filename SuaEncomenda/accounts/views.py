from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, PerfilUpdateForm


def registrar(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Seja bem vindo(a) {username}, sua conta foi criada com sucesso, agora você pode entrar no sistema!')
			return redirect('login')
	else:
		form = UserRegisterForm()

	return render(request, 'accounts/registrar.html', {'form':form})

@login_required
def perfil(request):
	if request.method == 'POST':
		uForm = UserUpdateForm(request.POST, instance=request.user)
		pForm = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

		if uForm.is_valid() and pForm.is_valid():
			uForm.save()
			pForm.save()
			messages.success(request, f'Sua conta foi atualizada.')
			return redirect('perfil')

	else:
		uForm = UserUpdateForm(instance=request.user)
		pForm = PerfilUpdateForm(instance=request.user.perfil)

	context = {'uForm':uForm, 'pForm':pForm}

	return render(request, 'accounts/perfil.html', context)