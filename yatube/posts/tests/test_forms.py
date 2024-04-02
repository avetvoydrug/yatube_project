from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Post
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()

class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author = cls.user,
            text = 'suckkkk'
        )
        cls.form = PostForm()
    
    def setUp(self):
        self.guest_client = Client()
        self.guest_client.force_login(PostFormTests.user)

    def test_create_post(self):
        posts_count = Post.objects.count()

        form_data = {
            'text': 'wtf'
        }

        response = self.guest_client.post(
            reverse('posts:post_create'),
            data = form_data,
            follow= True
        )
        #self.assertRedirects(response, (reverse('posts:profile'), kwargs={'username': 'auth'}))
        self.assertEqual(Post.objects.count(), posts_count+1)

    def test_post_edit(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'after',
        }

        response = self.guest_client.post(
            reverse('posts:post_edit', args=(f'{PostFormTests.post.pk}',)),
            data = form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                id=f'{PostFormTests.post.pk}',
                text='after'
            ).exists()
        )