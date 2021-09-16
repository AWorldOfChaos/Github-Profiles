from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from accounts.models import Account, Profile, Repository
import requests
from requests.exceptions import HTTPError
from django.utils import timezone


# Create your views here.
def home(request):
    name = "Github Profiles"
    args = {'name': name}
    return render(request, 'registration/home.html', args)


def signup(request):
    name = "Sign-Up Page"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = authenticate(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            profile = Profile(account=user, num_of_followers=0, name=username, last_updated=timezone.now())
            profile.save()
            return redirect('/site/')
    else:
        form = SignUpForm()
    return render(request, 'registration/Signup.html', {'name': name, 'form': form})


def login_view(request):
    name = "Login Page"
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/site/')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'name': name, 'form': form})


@login_required(login_url="/login/")
def site_view(request):
    return render(request, 'site/siteview.html')


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url="/login/")
def profile_view(request):
    data = request.user
    profile = data.profile_set.all()
    time = profile[0].last_updated
    numfolls = profile[0].num_of_followers
    repos_name, repos_stars = [], []
    for reps in profile[0].repository_set.all():
        repos_name.append(reps.name)
        repos_stars.append(reps.stars)
    repos = sorted(zip(repos_stars, repos_name))
    repos.reverse()
    return render(request, 'site/profile.html', {'data': data, 'numfolls': numfolls, 'repos': repos, 'time': time})


@login_required(login_url="/login/")
def update_view(request):
    data = request.user

    link = 'https://api.github.com/users/'
    username = data.username
    link += username

    profile = data.profile_set.all()[0]
    profile.delete()
    profile = Profile(account=data, num_of_followers=0, name=username, last_updated=timezone.now())
    try:
        response = requests.get(link)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        repos_link = response.json()['repos_url']
        profile.num_of_followers = response.json()['followers']
        profile.save()
        response3 = requests.get(repos_link)

        for repo in response3.json():
            stars = repo['stargazers_count']
            name = repo['name']
            temp = Repository(stars=stars, name=name, profile=profile)
            temp.save()
    return redirect('/profile/')


@login_required(login_url="/login/")
def explore(request):
    all_users = Account.objects.values()
    all_accounts = []
    for account in all_users:
        all_accounts.append(account['username'])
    return render(request, 'site/explore.html', {'all_accounts': all_accounts})


@login_required(login_url="/login/")
def explore_view(request, account):
    data = Account.objects.get(username=account)
    profile = data.profile_set.all()
    numfolls = profile[0].num_of_followers
    repos_name, repos_stars = [], []
    for reps in profile[0].repository_set.all():
        repos_name.append(reps.name)
        repos_stars.append(reps.stars)
    repos = sorted(zip(repos_stars, repos_name))
    repos.reverse()
    return render(request, 'site/explore_view.html', {'data': data, 'numfolls': numfolls, 'repos': repos})
