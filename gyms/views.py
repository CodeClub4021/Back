from django.shortcuts import render, get_object_or_404, redirect
from .models import Gym, Rating
from .forms import GymForm, RatingForm

def gym_list(request):
    gyms = Gym.objects.all()
    return render(request, 'myapp/gym_list.html', {'gyms': gyms})

def gym_detail(request, pk):
    gym = get_object_or_404(Gym, pk=pk)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.gym = gym
            rating.save()

    form = RatingForm()

    return render(request, 'myapp/gym_detail.html', {'gym': gym, 'form': form})

def gym_create(request):
    if request.method == 'POST':
        form = GymForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gym_list')
    else:
        form = GymForm()
    return render(request, 'myapp/gym_form.html', {'form': form})

def gym_update(request, pk):
    gym = get_object_or_404(Gym, pk=pk)
    if request.method == 'POST':
        form = GymForm(request.POST, instance=gym)
        if form.is_valid():
            form.save()
            return redirect('gym_list')
    else:
        form = GymForm(instance=gym)
    return render(request, 'myapp/gym_form.html', {'form': form})

def gym_delete(request, pk):
    gym = get_object_or_404(Gym, pk=pk)
    gym.delete()
    return redirect('gym_list')
