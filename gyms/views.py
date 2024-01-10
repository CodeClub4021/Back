from rest_framework import generics, status
from rest_framework.response import Response
from .models import Gym, Rating
from .serializers import GymSerializer, RatingSerializer, CoachCreateSerializer, UserRegisterSerializer, GymCommentSerializer, GymProgramSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .forms import GymForm, RatingForm
from django.shortcuts import get_object_or_404
from gyms.models import CustomUser, GymComment, GymProgram


class GetGymByManagerView(generics.RetrieveAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        id = self.request.query_params.get("manager_id")

        queryset = self.get_queryset()
        filter = {"manager_id": id}

        obj = get_object_or_404(queryset, **filter)
        return obj

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
    

class CoachCreateView(generics.CreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = CoachCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        gym_pk = self.kwargs.get('pk')
        gym = get_object_or_404(Gym, pk=gym_pk)

        if self.request.user != gym.manager:
            return Response({"detail": "You do not have permission to add coaches to this gym."}, status=status.HTTP_403_FORBIDDEN)

        coach_username = serializer.validated_data.get('coach_username')
        coach = get_object_or_404(CustomUser, username=coach_username)

        gym.coaches.add(coach)
        return Response({"detail": "Coach added successfully."}, status=status.HTTP_201_CREATED)

class GymRegisteration(generics.CreateAPIView):
    queryset = Gym.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        gym_pk = self.kwargs.get('pk')
        gym = get_object_or_404(Gym, pk=gym_pk)

        if self.request.user_type!= 'user':
            return Response({"detail": "You do not have permission to register to this gym."}, status=status.HTTP_403_FORBIDDEN)

        user_username = serializer.validated_data.get('user_username')
        user = get_object_or_404(CustomUser, username=user_username)

        gym.users.add(user)
        return Response({"detail": "You registered to this gym succesfully."}, status=status.HTTP_201_CREATED)
    

class GymCommentListCreateView(generics.ListCreateAPIView):
    queryset = GymComment.objects.all()
    serializer_class = GymCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GymProgramRecommendationView(generics.ListAPIView):
    serializer_class = GymProgramSerializer

    def get_queryset(self):
        weight = self.request.query_params.get('weight')
        height = self.request.query_params.get('height')

        # Example logic for gym program recommendations based on weight and height
        programs = []

        if weight and height:
            if int(weight) < 70 and int(height) < 170:
                programs = GymProgram.objects.filter(name__in=['Beginner Program', 'Weight Loss Program'])
            elif 70 <= int(weight) <= 90 and 170 <= int(height) <= 180:
                programs = GymProgram.objects.filter(name__in=['Intermediate Program', 'Strength Training Program'])
            elif int(weight) > 90 and int(height) > 180:
                programs = GymProgram.objects.filter(name__in=['Advanced Program', 'Muscle Building Program'])

        return programs


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
