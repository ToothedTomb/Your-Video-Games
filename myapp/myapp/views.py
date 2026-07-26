from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
import json
from django.contrib import messages
from django.http import JsonResponse
from .models import Game
from .forms import GameForm
from django.db.models import Q
def index(request):
    return render(request,'index.html')
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('information')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request,'login.html', {'form':form})
    
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('information')  # Redirect to information after signup
    
    def form_valid(self, form):
        # Save the user
        user = form.save()
        # Log the user in automatically
        auth_login(self.request, user)
        # Redirect to information page
        return HttpResponseRedirect(self.success_url)
@login_required
def information(request):  # Changed from dashboard to information
    user_games = Game.objects.filter(user=request.user).order_by('order')
    
    search_query = request.GET.get('search', '')  # Get the search term from URL
    if search_query:
        # Search in name, about, platform, genre, and comment
        user_games = user_games.filter(
            Q(name__icontains=search_query)        )
    
    return render(request, 'information.html', {
        'user_games': user_games,
        'search_query': search_query,  # Pass search term back to template
    })
def logout_view(request):
    auth_logout(request)
    return redirect('index')

def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.user = request.user
            game.save()
            return redirect('information')
    else:
        form = GameForm()
    return render(request, 'add_game.html', {'form': form})

def delete_game(request,game_id):
    game = get_object_or_404(Game, id=game_id)
    if game.user != request.user:
        return redirect('information')
    game.delete()
    return redirect('information')

def edit_game(request, game_id):
    # Get the game or return 404 if not found
    game = get_object_or_404(Game, id=game_id)
    
    # Check if the current user owns this game
    if game.user != request.user:
        return redirect('information')
    
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('information')
    else:
        form = GameForm(instance=game)
    
    return render(request, 'edit_game.html', {'form': form, 'game': game})

def save_game_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_order = data.get('order', [])
            
            # Update the order for each game
            for index, game_id in enumerate(game_order):
                game = Game.objects.get(id=game_id, user=request.user)
                game.order = index
                game.save()
            
            return JsonResponse({'status': 'success', 'message': 'Order updated'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Log the user out first
        auth_logout(request)
        # Delete the user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('index')
    
    return render(request, 'delete_account.html', {'user': request.user})