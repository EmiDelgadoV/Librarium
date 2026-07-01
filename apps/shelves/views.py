from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shelf
from .serializers import ShelfSerializer
from apps.books.models import Book

class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer

    # POST /api/shelves/{id}/books/ -> Agregar libro a un estante específico
    @action(detail=True, methods=['post'], url_path='books')
    def add_book(self, request, pk=None):
        shelf = self.get_object()  
        book_id = request.data.get('book_id')

        if not book_id:
            return Response({'error': 'Se requiere el campo book_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
            shelf.books.add(book) 
            return Response({'status': f'Libro "{book.title}" agregado al estante "{shelf.name}"'}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error': 'El libro especificado no existe'}, status=status.HTTP_404_NOT_FOUND)