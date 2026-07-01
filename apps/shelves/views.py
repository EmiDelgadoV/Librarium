from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.users.permissions import IsOwnerOrReadOnly
from .models import Shelf
from .serializers import ShelfSerializer
from apps.books.models import Book

class ShelfViewSet(viewsets.ModelViewSet):
    serializer_class = ShelfSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='books')
    def add_book(self, request, pk=None):
        shelf = self.get_object()
        if shelf.user != request.user:
            return Response({'error': 'No tienes permiso para modificar este estante'}, status=status.HTTP_403_FORBIDDEN)
            
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Se requiere el campo book_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
            shelf.books.add(book)
            return Response({'status': f'Libro "{book.title}" agregado al estante "{shelf.name}"'}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error': 'El libro especificado no existe'}, status=status.HTTP_404_NOT_FOUND)