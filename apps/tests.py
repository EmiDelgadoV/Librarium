from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User
from apps.books.models import Book
from apps.shelves.models import Shelf
from apps.reviews.models import Review


def create_user(email="test@test.com", username="testuser", password="testpass123"):
    return User.objects.create_user(
        email=email,
        username=username,
        password=password
    )


def get_token(client, email="test@test.com", password="testpass123"):
    response = client.post(reverse("token_obtain_pair"), {
        "email": email,
        "password": password
    }, format="json")
    return response.data["access"]


def auth_client(client, token):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


# ── AUTH ─────────────────────────────────────────────────

class AuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        response = self.client.post(reverse("auth_register"), {
            "email": "nuevo@test.com",
            "username": "nuevo",
            "password": "testpass123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_email(self):
        create_user()
        response = self.client.post(reverse("auth_register"), {
            "email": "test@test.com",
            "username": "otro",
            "password": "testpass123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        create_user()
        response = self.client.post(reverse("token_obtain_pair"), {
            "email": "test@test.com",
            "password": "testpass123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_wrong_password(self):
        create_user()
        response = self.client.post(reverse("token_obtain_pair"), {
            "email": "test@test.com",
            "password": "wrongpass"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_without_token(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ── BOOKS ────────────────────────────────────────────────

class BookTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        token = get_token(self.client)
        self.client = auth_client(self.client, token)

    def test_create_book(self):
        response = self.client.post(reverse("book-list"), {
            "title": "El Principito",
            "author": "Antoine de Saint-Exupéry",
            "category": "Ficción",
            "status": "quiero_leer"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "El Principito")

    def test_list_books_only_own(self):
        Book.objects.create(
            user=self.user,
            title="Mi libro",
            author="Autor",
            category="Cat"
        )
        other_user = create_user(email="otro@test.com", username="otro")
        Book.objects.create(
            user=other_user,
            title="Libro ajeno",
            author="Autor",
            category="Cat"
        )
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_book(self):
        book = Book.objects.create(
            user=self.user,
            title="Para borrar",
            author="Autor",
            category="Cat"
        )
        response = self.client.delete(reverse("book-detail", args=[book.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_users_book(self):
        other_user = create_user(email="otro@test.com", username="otro")
        book = Book.objects.create(
            user=other_user,
            title="Ajeno",
            author="Autor",
            category="Cat"
        )
        response = self.client.delete(reverse("book-detail", args=[book.id]))
        self.assertIn(response.status_code, [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ])


# ── SHELVES ──────────────────────────────────────────────

class ShelfTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        token = get_token(self.client)
        self.client = auth_client(self.client, token)

    def test_create_shelf(self):
        response = self.client.post(reverse("shelf-list"), {
            "name": "Favoritos"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_book_to_shelf(self):
        shelf = Shelf.objects.create(user=self.user, name="Mi estante")
        book = Book.objects.create(
            user=self.user,
            title="Libro",
            author="Autor",
            category="Cat"
        )
        response = self.client.post(
            reverse("shelf-add-book", args=[shelf.id]),
            {"book_id": book.id},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(book, shelf.books.all())

    def test_add_nonexistent_book_to_shelf(self):
        shelf = Shelf.objects.create(user=self.user, name="Mi estante")
        response = self.client.post(
            reverse("shelf-add-book", args=[shelf.id]),
            {"book_id": 9999},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ── REVIEWS ──────────────────────────────────────────────

class ReviewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        token = get_token(self.client)
        self.client = auth_client(self.client, token)
        self.book = Book.objects.create(
            user=self.user,
            title="Libro para reseñar",
            author="Autor",
            category="Cat"
        )

    def test_create_review(self):
        response = self.client.post(reverse("review-list"), {
            "book": self.book.id,
            "rating": 5,
            "comment": "Excelente libro"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_rating(self):
        response = self.client.post(reverse("review-list"), {
            "book": self.book.id,
            "rating": 6,
            "comment": "Rating inválido"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_review(self):
        review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=4,
            comment="Bueno"
        )
        response = self.client.delete(reverse("review-detail", args=[review.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_reviews_public(self):
        Review.objects.create(
            user=self.user,
            book=self.book,
            rating=3,
            comment="Regular"
        )
        response = self.client.get(reverse("review-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)