from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_list_url_exists_at_desired_location(self):
        """Страница group/<slug:slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url_exists_at_desired_location(self):
        """Страница profile/<str:username>/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/test_user/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_exists_at_desired_location(self):
        """Страница posts/<int:post_id>/ доступна любому пользователю."""
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_exists_at_desired_location(self):
        """Страница posts/<post_id>/edit/ доступна автору поста."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_exists_at_desired_location(self):
        """Страница create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_page_url_exists_at_desired_location(self):
        """Страница unexisting_page/ доступна любому пользователю."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/test_user/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create.html',
            '/posts/1/edit/': 'posts/create.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
