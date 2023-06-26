from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse
from django.conf import settings
#from django.http import JsonResponse
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib import messages
from accounts.models import Client, Domain
from django_tenants.utils import schema_context
#from podsprint.views import AboutTemplateView
# Create your views here.

def users_root(request):
    return HttpResponseRedirect(reverse(settings.LOGIN_URL))

def login_view(request):
    return render(request, 'registration/login.html')


def check_username(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        data = User.objects.filter(email=email).exists()
        if data:
            error_message = "<div id='email-error' class='error-message'>That email is already taken.  Please enter another email.</div>"
            return HttpResponse(error_message)
        else:
            return HttpResponse("<div id='email-error' class='error-message hidden'>That email is already taken.  Please enter another email.</div>")

def register_view(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                username_ = request.POST.get('username').lower()
                email = request.POST.get('email').lower()

                with schema_context('public'):
                    public_client = Client.objects.filter(schema_name='public').first()
                    public_domain = Domain.objects.filter(tenant=public_client).values('domain').first()
                    #domain_ = username_ + '.' + str(public_domain['domain'])
                    domain_ = username_

                
                    tenant = Client(schema_name=username_, name=email)
                    tenant.save()

                    domain = Domain()
                    domain.domain = domain_
                    domain.tenant = tenant
                    domain.is_primary = True
                    domain.save()

                    user = form.save(commit=False)
                    user.username = username_
                    user.schema = tenant
                    user.save()

                    tenant.user = user
                    tenant.save()

                # Resto del código

                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('index')
            except Exception as e:
                error_message = str(e)
                return HttpResponseServerError(f"Error: {error_message}")
        else:
            required_field = None
            for field in form:
                if field.errors:
                    required_field = field.label
                    break
            return render(request, 'registration/register.html', {'form': form, 'required_field': required_field})
    else:
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})



class CustomLoginView(LoginView):
    
    def get(self, request):
        return render(request, 'users/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')        
        else:
            return render(request, 'user/login.html', {'error': 'Invalid login'})
        
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

        # user_schema = request.user.CustomUser.schema
        # # Obtén el dominio del usuario desde el objeto de solicitud
        # user_domain = f"{user_schema.schema_name}.localhost"
        # # Construye la URL de redirección completa con el dominio del usuario
        # redirect_url = f"http://{user_domain}/"
        # # Redirige al usuario a la URL con su dominio personalizado
        # return redirect('index')