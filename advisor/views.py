from .forms import FinancialAdviceForm
from .logic import FinancialAdvisor
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import AdviceHistory
from django.utils import timezone

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required(login_url='/')
def dashboard(request):
    form = FinancialAdviceForm()
    recent_history = AdviceHistory.objects.filter(user=request.user).order_by('-created_at')[:5]

    return render(request, 'home.html', {'form': form, 'recent_history': recent_history})

@login_required(login_url='/')
def results(request):
    if request.method == 'POST':
        form = FinancialAdviceForm(request.POST)
        if form.is_valid():
            advisor = FinancialAdvisor()
            result = advisor.get_financial_advice(
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                objective=form.cleaned_data['objective'],
                factor=form.cleaned_data['factor'],
                duration=form.cleaned_data['duration'],
                expect=form.cleaned_data['expect'],
                avenue=form.cleaned_data['avenue']
            )

            similar_profiles_json = result['similar_profiles']

            # Save to DB
            AdviceHistory.objects.create(
                user=request.user,
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                objective=form.cleaned_data['objective'],
                factor=form.cleaned_data['factor'],
                duration=form.cleaned_data['duration'],
                expect=form.cleaned_data['expect'],
                avenue=form.cleaned_data['avenue'],
                advice_html=result['advice'],
                similar_profiles_percentage=result['similar_profiles_percentage'],
                created_at=timezone.now()
            )
            
           
            
            return render(request, 'results.html', {
                'form_data': form.cleaned_data,
                'advice': result['advice'],
                'similar_profiles': similar_profiles_json,
                'similar_profiles_percentage': result['similar_profiles_percentage'],
            })
    else:
        form = FinancialAdviceForm()
    
    return render(request, 'index.html', {'form': form})

@login_required
def history(request):
    histories = AdviceHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'histories': histories})

@redirect_authenticated_user
def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html', {'form': form})

@redirect_authenticated_user
def user_signup(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    # Customize the email subject and template
    email_template_name = 'password_reset_email.html'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    # already authenticated users should be redirected to the dashboard
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('login')

    # already authenticated users should be redirected to the dashboard
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    

def history_detail(request, pk):
    history = get_object_or_404(AdviceHistory, pk=pk, user=request.user)

    return render(request, 'history_detail.html', {
        'form_data': {
            'Age': history.age,
            'Gender': history.gender,
            'Objective': history.objective,
            'Factor': history.factor,
            'Duration': history.duration,
            'Expect': history.expect,
            'Avenue': history.avenue,
        },
        'advice': history.advice_html,
        'similar_profiles_percentage': history.similar_profiles_percentage,
    })