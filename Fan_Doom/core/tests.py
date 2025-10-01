from django.test import TestCase
from .models import Post, Author, Fandom, WikiPage

class PostModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.fandom = Fandom.objects.create(name="Test Fandom")
        self.post = Post.objects.create(title="Test Post", content="This is a test post.", author=self.author, fandom=self.fandom)

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post.")
        self.assertEqual(self.post.author.name, "Test Author")
        self.assertEqual(self.post.fandom.name, "Test Fandom")

class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")

    def test_author_creation(self):
        self.assertEqual(self.author.name, "Test Author")

class FandomModelTest(TestCase):
    def setUp(self):
        self.fandom = Fandom.objects.create(name="Test Fandom")

    def test_fandom_creation(self):
        self.assertEqual(self.fandom.name, "Test Fandom")

class WikiPageModelTest(TestCase):
    def setUp(self):
        self.wiki_page = WikiPage.objects.create(title="Test Wiki", content="This is a test wiki page.")

    def test_wiki_page_creation(self):
        self.assertEqual(self.wiki_page.title, "Test Wiki")
        self.assertEqual(self.wiki_page.content, "This is a test wiki page.")