from rest_framework import generics
from rest_framework.response import Response
from .models import Gym, Rating
from .serializers import GymSerializer, RatingSerializer
from .forms import GymForm, RatingForm

class GymListCreateView(generics.ListCreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

class GymDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        gym_pk = self.kwargs.get('pk')
        gym = get_object_or_404(Gym, pk=gym_pk)
        serializer.save(gym=gym)

class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    

# # from rest_framework import generics, permissions, status
# # from rest_framework.response import Response
# # from rest_framework.authtoken.models import Token
# # from django.contrib.auth import authenticate
# # from .models import CustomUser, Gym, GymRating
# # from .serializers import GymSerializer, GymRatingSerializer



# # class GymView(generics.ListCreateAPIView):
# #     queryset = Gym.objects.all()
# #     serializer_class = GymSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def perform_create(self, serializer):
# #         serializer.save(manager=self.request.user)

# # class GymDetailView(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Gym.objects.all()
# #     serializer_class = GymSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def perform_update(self, serializer):
# #         if self.request.user != serializer.instance.manager and self.request.user not in serializer.instance.coaches.all():
# #             raise PermissionDenied("You do not have permission to perform this action.")
# #         serializer.save()

# #     def perform_destroy(self, instance):
# #         if self.request.user != instance.manager:
# #             raise PermissionDenied("You do not have permission to perform this action.")
# #         instance.delete()

# # class GymRatingView(generics.CreateAPIView):
# #     queryset = GymRating.objects.all()
# #     serializer_class = GymRatingSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)

# # class GymRatingView(generics.CreateAPIView):
# #     queryset = GymRating.objects.all()
# #     serializer_class = GymRatingSerializer
# #     permission_classes = [permissions.IsAuthenticated]

# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)



# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Gym, Rating
# from .forms import GymForm, RatingForm

# def gym_list(request):
#     gyms = Gym.objects.all()
#     return render(request, 'myapp/gym_list.html', {'gyms': gyms})

# def gym_detail(request, pk):
#     gym = get_object_or_404(Gym, pk=pk)

#     if request.method == 'POST':
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating = form.save(commit=False)
#             rating.gym = gym
#             rating.save()

#     form = RatingForm()

#     return render(request, 'myapp/gym_detail.html', {'gym': gym, 'form': form})

# def gym_create(request):
#     if request.method == 'POST':
#         form = GymForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('gym_list')
#     else:
#         form = GymForm()
#     return render(request, 'myapp/gym_form.html', {'form': form})

# def gym_update(request, pk):
#     gym = get_object_or_404(Gym, pk=pk)
#     if request.method == 'POST':
#         form = GymForm(request.POST, instance=gym)
#         if form.is_valid():
#             form.save()
#             return redirect('gym_list')
#     else:
#         form = GymForm(instance=gym)
#     return render(request, 'myapp/gym_form.html', {'form': form})

# def gym_delete(request, pk):
#     gym = get_object_or_404(Gym, pk=pk)
#     gym.delete()
#     return redirect('gym_list')
