from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Article, Profile
from django.core.cache import cache

User = get_user_model()

class ArticleFeedAPIViewTest(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.user3 = User.objects.create_user(username="user3", password="password3")

        # Create profiles and follow relationships
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)
        self.profile3 = Profile.objects.create(user=self.user3)
        self.profile1.followers.add(self.profile2.user)

        # Create articles
        self.article1 = Article.objects.create(title="Article 1", body="Body 1", author=self.user2, slug="article-1")
        self.article2 = Article.objects.create(title="Article 2", body="Body 2", author=self.user2, slug="article-2")
        self.article3 = Article.objects.create(title="Article 3", body="Body 3", author=self.user3, slug="article-3")

        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

    def test_article_feed(self):
        # Clear cache to ensure fresh data
        cache.clear()

        # Make GET request to the feed endpoint
        response = self.client.get("/api/articles/feed", format='json')
        # Assert response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert response data
        self.assertIn("articles", response.data)
        self.assertIn("articlesCount", response.data)
        self.assertEqual(response.data["articlesCount"], 0)
        self.assertEqual(len(response.data["articles"]), 0)

        # Assert articles are from followed user
        article_authors = [article["author"]["username"] for article in response.data["articles"]]
        self.assertTrue(all(author == "user2" for author in article_authors))

    def test_article_feed_pagination(self):
        # Clear cache to ensure fresh data
        cache.clear()

        # Make GET request with pagination parameters
        response = self.client.get("/api/articles/feed", {"limit": 1, "offset": 1})
        response = self.client.get("/api/articles/feed", {"limit": 1, "offset": 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert pagination
        self.assertEqual(len(response.data["articles"]), 0)
        self.assertEqual(response.data["articlesCount"], 0)