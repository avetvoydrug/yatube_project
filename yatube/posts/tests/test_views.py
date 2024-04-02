import tempfile
import shutil
import time

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

from posts.models import Post, Group

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

small_gif = (            
             b'\x47\x49\x46\x38\x39\x61\x02\x00'
             b'\x01\x00\x80\x00\x00\x00\x00\x00'
             b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
             b'\x00\x00\x00\x2C\x00\x00\x00\x00'
             b'\x02\x00\x01\x00\x00\x02\x02\x0C'
             b'\x0A\x00\x3B'
        )

@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title = 'test title',
            slug = 'test-slug',
            description = 'test desc'
        )
        cls.post = Post.objects.create(
            author = cls.user,
            text = 'teststsetest',
            image = SimpleUploadedFile(
                name='small.gif',
                content= small_gif,
                content_type='image/gif'
            ),
            group = cls.group
        )
    
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
    
    def setUp(self):
        self.autorized_client = Client()
        self.autorized_client.force_login(PostsPagesTests.user)

    def test_pages_uses_correct_template(self):
        """URL-adress uses correct template"""
        templates_pages_names = {
            'posts/index.html': reverse('posts:main_page'),
            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': 'test-slug'})
            ),
            'posts/profile.html': (
                reverse('posts:profile', kwargs={'username': 'auth'})
            ),
            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': PostsPagesTests.post.pk})
            ),
            'posts/post_create.html': (
                reverse('posts:post_edit', kwargs={'post_id': PostsPagesTests.post.pk})
            ),
            'posts/post_create.html': reverse('posts:post_create'),
        }
        # Проверяем, что при обращении к name вызывается соответствующий html-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.autorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
                
    
    def test_context_have_correct_post(self):
        response = self.autorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': PostsPagesTests.post.pk}))
        self.assertEqual(
            response.context.get('post').pk, PostsPagesTests.post.pk
        )
        self.assertEqual(
            response.context.get('post').image, PostsPagesTests.post.image
        )
    def test_context_form_post_edit(self):
        response = self.autorized_client.get(reverse(
            'posts:post_edit', 
            kwargs={'post_id': PostsPagesTests.post.pk}
            )
        )
        self.assertEqual(
            response.context.get('is_edit').pk,
            PostsPagesTests.post.pk
        )
    
    def test_context_form_post_create(self):
        response = self.autorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
    

class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.second_user = User.objects.create_user(username='test')
        cls.group = Group.objects.create(
            title = 'test',
            slug = 'test-slug',
            description = 'test desc',
        )
        for i in range(13):
            cls.post = Post.objects.create(
                author = cls.user,
                text = f'test text {i}'
            )
        cls.post = Post.objects.create(
            author = cls.second_user,
            text = 'something in the way',
            group = cls.group,
        )
    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:main_page'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        response = self.authorized_client.get(reverse('posts:main_page') + '?page=2')

        self.assertEqual(len(response.context['page_obj']), 4)

    def test_group_contains_one_record(self):
        response = self.authorized_client.get(reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        self.assertEqual(len(response.context['page_obj']), 1)
    
    def test_profile_of_second_user_contains_from_one_record(self):
        response = self.authorized_client.get(reverse('posts:profile', kwargs={'username': 'test'}))

        self.assertEqual(len(response.context['page_obj']), 1)


        