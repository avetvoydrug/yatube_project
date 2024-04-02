from django.test import TestCase

from django.contrib.auth import get_user_model

from posts.models import Post, Group

User = get_user_model()

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группаААА',
        )
    def test_models_have_correct_object_names(self):
        post = PostModelTest.post
        group = PostModelTest.group
        title = post.__str__()
        self.assertEqual(title, 'Тестовая группа')
        self.assertEqual(title, group.title)
