from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from posts.models import Post, Group

User = get_user_model()
    
class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.second_user = User.objects.create_user(username='who')
        cls.group = Group.objects.create(
            title = 'Test',
            slug = 'test-slug',
            description = 'test_desc'
        )
        cls.post = Post.objects.create(
            author = cls.user,
            text = 'something words should be here',
        )
    def setUp(self):
        #unauth
        self.guest_client = Client()
        #auth
        self.authorized_client = Client()
        self.authorized_client.force_login(URLTests.user)
        #auth guest
        self.second_authorized_user = Client()
        self.second_authorized_user.force_login(URLTests.second_user)

    def test_urls_get_correct_redirect_for_unauth_user(self):
        """"URL-adress have correct redirect for auth/unauth user"""
        correct_redirect = {
            '/auth/login/?next=/create/': '/create/'    
        }
        for red_url, adress in correct_redirect.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress, follow=True)
                self.assertRedirects(response, red_url)
    
    def test_urls_get_correct_redirect_for_guest_auth_user(self):
        """URL-adress have correct redirect for guest_auth user"""
        correct_redirect = {
            f'/posts/{URLTests.post.pk}/': f'/posts/{URLTests.post.pk}/edit/'
        }
        for red_url, adress in correct_redirect.items():
            with self.subTest(adress=adress):
                response = self.second_authorized_user.get(adress, follow=True)
                self.assertRedirects(
                    response, red_url
                )
    def test_urls_get_correct_redirect_for_author(self):
        """URL-response have status 200 for author"""
        correct_redirect = {
            f'/posts/{URLTests.post.pk}/edit/': 200
        }
        for adress, status in correct_redirect.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, status)
    
    def test_static_page(self):
        """URL-response have status 200 for unauth user"""
        correct = {
            '/': 200,
            '/about/author/': 200,
            '/about/tech/': 200,
            f'/posts/{URLTests.post.pk}/': 200,
            f'/profile/{URLTests.user.username}/': 200,
            f'/group/{URLTests.group.slug}/': 200,
            '/posts/924994129412/': 404
        }

        for adress, status in correct.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, status)

    def test_templates(self):
        """Check correct URL-Templates"""
        templates = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{URLTests.group.slug}/',
            'posts/profile.html': f'/profile/{URLTests.user.username}/',
            'posts/post_detail.html': f'/posts/{URLTests.post.pk}/',
            'posts/post_create.html': f'/posts/{URLTests.post.pk}/edit/',
            'posts/post_create.html': '/create/',
        }
        for template, adress in templates.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)