from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
# from rest_framework.decorators import api_view #for function based views
from rest_framework.views import APIView #for class based views
from rest_framework import status, mixins, generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, 
                                           ReviewSerializer)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.all()
        if review_queryset.filter(watchlist=watchlist, review_user=review_user).exists():
            raise ValidationError('You have already reviewed this movie')
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2    
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(review_user=review_user, watchlist=watchlist)
        
    

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated] 
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
    
# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    
    
    
    
    
        
# class StreamPlatformVS(viewsets.ViewSet):
    # queryset = StreamPlatform.objects.all()
    # def list(self, request):
    #     serializer = StreamPlatformSerializer(self.queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    # def retrieve(self, request, pk=None):
    #     watchList = get_object_or_404(self.queryset, pk=pk)
    #     serializer = StreamPlatformSerializer(watchList, context={'request': request})
    #     return Response(serializer.data)
    # def create(self, request):
    #     serializer = StreamPlatformSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def update(self, request, pk=None):
    #     platform = self.queryset.get(pk=pk)
    #     serializer = StreamPlatformSerializer(platform, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def destroy(self, request, pk=None):
    #     platform = self.queryset.get(pk=pk)
    #     platform.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

class StreamPlatformAV(APIView):
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        # serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)
class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'Platform not found'}, status=status.HTTP_404_NOT_FOUND)            
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'Platform not found'}, status=status.HTTP_404_NOT_FOUND)    
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'Platform not found'}, status=status.HTTP_404_NOT_FOUND)    
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    

class WatchListAV(APIView):
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)
    
class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)            
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)    
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)    
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    

# Create your views here.
# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies = WatchList.objects.all()
#         serializer = WatchListSerializer(movies, many=True) # Add many=True to serialize multiple objects
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)            
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)    
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)    
#         WatchList.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    