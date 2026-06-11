from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Content
from django.urls import reverse
# Create your tests here.
class PostModelTestCase(TestCase):

    def create_author(self, username='testuser'):
        return User.objects.create_user(username=username)

    def create_post(self, title='Test Title', author=None):
        return Post.objects.create(title=title, author=author)

    def test_custom_slugify(self):
        post = Post()
        slug = post.custom_slugify("Test Post Title")
        self.assertEqual(slug, "test-post-title")

    def test_save_method_with_existing_slug(self):
        author = self.create_author()
        post1 = self.create_post(title='Test Post', author=author)
        post2 = self.create_post(title='Test Post', author=author)
        self.assertNotEqual(post1.slug, post2.slug)

    def test_save_method_without_slug(self):
        author = self.create_author()
        post = self.create_post(title='Test Post', author=author)
        self.assertIsNotNone(post.slug)

    def test_str_method(self):
        author = self.create_author()
        post = self.create_post(title='Test Post', author=author)
        self.assertEqual(str(post), 'Test Post')

class ContentTestCase(TestCase):

    def test_content_ordering(self):
        post = Post.objects.create(title="Test Post")
        Content.objects.create(post=post, content_type='text', text='This is a test text content', order=2)
        Content.objects.create(post=post, content_type='image', image='test_image.jpg', order=1)

        contents = Content.objects.filter(post=post)
        ordered_contents = Content.objects.filter(post=post).order_by('order')

        self.assertEqual(list(contents), list(ordered_contents))

    def test_content_str_method(self):
        post = Post.objects.create(title="Test Post")
        content = Content.objects.create(post=post, content_type='text', text='This is a test text content', order=1)

        self.assertEqual(str(content), f"text - {post.title}")

class TestPostListView(TestCase):

    def test_post_list_view(self):
        response = self.client.get(reverse('blog_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog_app/post_list.html')
        self.assertContains(response, 'Post List')

    def test_pagination_is_ten(self):
        for i in range(15):
            Post.objects.create(title=f'Test Post {i}')

        response = self.client.get(reverse('blog_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 10)

class PostDetailViewTests(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='test', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            author=test_user,
        )
        self.content1 = Content.objects.create(
            post=self.post,
            text='Test Content 1',
            order=1,
        )
        self.content2 = Content.objects.create(
            post=self.post,
            text='Test Content 2',
            order=2,
        )
    
    def test_post_detail_view(self):
        response = self.client.get(reverse('blog_app:read_post', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post)
        self.assertQuerysetEqual(response.context['contents'], [repr(self.content1), repr(self.content2)])

class TestCreatePostView(TestCase):

    def test_create_post_view(self):
        # Create a test user
        test_user = User.objects.create_user(username='test', password='12345')

        # Log in the test user
        self.client.login(username='test', password='12345')

        # Prepare POST data
        post_data = {
            'title': 'Test Title',
            'content_type': ['text', 'image'],
            'text': ['Text content', ''],
            'image': [None, self.get_temporary_image()],
            'order': ['1', '2']
        }

        response = self.client.post(reverse('blog_app:create_post'), post_data)

        # Check if the post is created
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Post.objects.filter(title='Test Title').exists())

        post = Post.objects.get(title='Test Title')

        # Check if contents are created
        self.assertEqual(Content.objects.filter(post=post).count(), 2)
        self.assertEqual(Content.objects.filter(post=post, content_type='text').count(), 1)
        self.assertEqual(Content.objects.filter(post=post, content_type='image').count(), 1)

        # Check if the redirection is correct
        self.assertRedirects(response, reverse('blog_app:read_post', kwargs={'slug': post.slug}))

    def get_temporary_image(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        from io import BytesIO
        from PIL import Image
    
        # Create a temporary image file
        image = Image.new('RGB', (100, 100))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_file = SimpleUploadedFile('test.jpg', image_io.getvalue())
    
        return image_file


class PostDeleteViewTestCase(TestCase):

    def test_post_delete_view(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        post = Post.objects.create(title='Test Post', author=user)

        response = self.client.post(reverse('blog_app:delete_post', kwargs={'pk': post.pk}))

        self.assertEqual(response.status_code, 302)  # Check if deletion was successful
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())  # Check if post was deleted

    def test_post_delete_view_redirect(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        post = Post.objects.create(title='Test Post', author=user)

        response = self.client.post(reverse('blog_app:delete_post', kwargs={'pk': post.pk}))

        self.assertRedirects(response, '/')  # Check if redirect to success_url occurs

class TestEditPostView(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post', author=self.user)
    
    def test_edit_post_unauthorized_user(self):
        unauthorized_user = User.objects.create_user(username='unauthorized', password='12345')
        self.client.force_login(unauthorized_user)
    
        response = self.client.get(reverse('blog_app:update_post', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 403)
    
    def test_edit_post_get_request(self):
        self.client.force_login(self.user)
    
        response = self.client.get(reverse('blog_app:update_post', kwargs={'slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_edit_post_valid_post_request(self):
        self.client.force_login(self.user)
        updated_title = 'Updated Post Title'
    
        response = self.client.post(reverse('blog_app:update_post', kwargs={'slug': self.post.slug}), data={'title': updated_title})
        self.assertEqual(response.status_code, 302)
    
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, updated_title)
