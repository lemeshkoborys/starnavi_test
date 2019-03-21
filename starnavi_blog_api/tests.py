from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.request import Request
from .models import Post, PostLikes
from starnavi_blog_api import serializers


FACTORY = APIRequestFactory()


class PostCreateTestCase(APITestCase):

    """
    Checks post create
    """

    def setUp(self):
        """
        Set ups test case with user and authentication
        """
        self.user = User.objects.create_user(
            'test_case_user',
            'test_case_email@example.com',
            'test_case_password'
        )
        login_url = '/sign-in/'
        login_response = self.client.post(
            login_url,
            data={
                'username': self.user.username,
                'password': 'test_case_password'
            },
            format='json'
        )
        self.auth_token = login_response.data['access']
        self.url = '/api/v1/posts/'
        self.request = Request(FACTORY.get(self.url))

    def test_post_can_create(self):
        """
        Checks post create option
        """
        post_data_to_create = {
            'title': 'Test Case Post Title',
            'content': 'Test Case Post Content'
        }
        response = self.client.post(
            self.url,
            data=post_data_to_create,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.auth_token}'
        )
        serialized_post = serializers.PostModelSerializer(
            Post.objects.first(),
            context={'request': self.request}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serialized_post.data)
        self.assertEqual(
            Post.objects.first().title,
            post_data_to_create['title']
        )

    def test_post_cant_create_not_authorized(self):

        """
        Checks that unauthorized user has no rights to create post object
        """

        post_data_to_create = {
            'title': 'Test Case Post Title',
            'content': 'Test Case Post Content'
        }
        response = self.client.post(
            self.url,
            data=post_data_to_create,
            format='json'
            # HTTP_AUTHORIZATION=f'Bearer {self.auth_token}' authentication is not provided
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_cant_create_bad_request(self):
        """
        Checks that user can't create post with bad input
        """

        post_bad_data_to_create = {
            'title': True,
            'content': 276
        }

        response = self.client.post(
            self.url,
            data=post_bad_data_to_create,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.auth_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostCanGetListAPITestCase(APITestCase):

    """
    Checks post list retrieve option
    """

    def setUp(self):
        """
        Set ups test case with user, authentication and Post object
        """
        self.user = User.objects.create_user(
            'test_case_user',
            'test_case_email@example.com',
            'test_case_password'
        )
        login_url = '/sign-in/'
        login_response = self.client.post(
            login_url,
            data={
                'username': self.user.username,
                'password': 'test_case_password'
            },
            format='json'
        )
        self.auth_token = login_response.data['access']
        self.url = '/api/v1/posts/'
        self.request = Request(FACTORY.get(self.url))
        self.post = Post.objects.create(
            title='Test Case Post Title',
            content='Test Case Post Content'
        )

    def test_post_can_get_list(self):
        """
        Checks post list retrieve options
        """
        response = self.client.get(
            self.url,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.auth_token}'
        )

        serialized_post = serializers.PostModelSerializer(
            Post.objects.all(),
            many=True,
            context={'request': self.request}
        )
        self.assertEqual(response.data, serialized_post.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_cant_get_not_authorized(self):
        """
        Check that unauthorized user can't retrieve post objects
        """

        response = self.client.get(
            self.url,
            format='json'
            # HTTP_AUTHORIZATION=f'Bearer {self.auth_token}' authentication is not provided
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCanSignUpAPITestCase(APITestCase):
    """
    Checks that user can sign up
    """

    def setUp(self):
        self.existing_username_user = User.objects.create_user(
            username='test_case_existing_username',
            email='email1@example.com',
            password='test_case_password'
        )

        self.existing_email_user = User.objects.create_user(
            username='test_case_user',
            email='lemeshkob@gmail.com',
            password='test_case_password'
        )

        self.url = '/sign-up/'

    def test_user_can_sign_up(self):
        """
        Checks that user can sign up
        """
        user_sign_up_data = {
            'username': 'lemes',
            'email': 'lemeshko.borys@gmail.com',
            'password': '1234qwer'
        }

        response = self.client.post(
            self.url,
            data=user_sign_up_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.get(username=user_sign_up_data['username']).username,
            user_sign_up_data['username']
        )

    def test_user_cant_sign_up_username_already_taken(self):

        """
        Checks that username is unique
        """

        user_sign_up_bad_data = {
            'username': 'test_case_existing_username',
            'email': 'lemeshkob@gmail.com',
            'password': '1234qwer'
        }
        response = self.client.post(
            self.url,
            data=user_sign_up_bad_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_sign_up_email_already_taken(self):
        """
        Checks that username is unique
        """

        user_sign_up_bad_data = {
            'username': 'lemes',
            'email': 'lemeshkob@gmail.com',
            'password': '1234qwer'
        }
        response = self.client.post(
            self.url,
            data=user_sign_up_bad_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_sign_up_email_is_bad(self):
        user_sign_up_bad_data = {
            'username': 'lemes',
            'email': 'qwe123wewwsdasdawdwdx@gmail.com',
            'password': '1234qwer'
        }
        response = self.client.post(
            self.url,
            data=user_sign_up_bad_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserCanSignInAPITestCase(APITestCase):

    """
    Checks if user can sign in
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_case_user',
            email='test@case.email',
            password='test_case_password'
        )
        self.url = '/sign-in/'
        self.request = Request(FACTORY.get(self.url))

    def test_user_can_sign_in(self):

        """
        Checks if user can sign in and server returned JWT
        """

        response = self.client.post(
            self.url,
            data={
                'username': self.user.username,
                'password': 'test_case_password'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['access'])

    def test_user_cant_login_user_does_not_exist(self):

        """
        Checks if unregistred user can't login
        """

        response = self.client.post(
            self.url,
            data={
                'username': 'bat_user_username',
                'password': 'test_case_password'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'])

    def test_user_cant_login_invalid_password(self):
        """
        Checks if user can't login with bad password
        """

        response = self.client.post(
            self.url,
            data={
                'username': self.user.username,
                'password': 'bad_password'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'])


class PostLikesAPITestCase(APITestCase):
    """
    Checks if user can like some posts
    """

    def setUp(self):
        """
        Set ups user, authentication and post object
        """
        self.user = User.objects.create_user(
            username='test_case_user',
            email='test@case.email',
            password='test_case_password'
        )

        self.url = '/api/v1/posts/like/'
        login_response = self.client.post(
            '/sign-in/',
            data={
                'username': self.user.username,
                'password': 'test_case_password'
            },
            format='json'
        )
        self.auth_token = login_response.data['access']
        self.request = Request(FACTORY.get(self.url))
        self.post = Post.objects.create(
            title='Test Case Post Title',
            content='Test Case Post Content'
        )

    def test_user_can_like(self):
        """
        Checks if authorized user can like post
        """

        post_to_like = {
            'post': self.post.id
        }

        response = self.client.post(
            self.url,
            data=post_to_like,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.auth_token}'
        )

        serialized_post = serializers.PostModelSerializer(
            Post.objects.first(),
            context={'request': self.request}
        )
        self.assertEqual(1, serialized_post.data['likes'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_unlike(self):
        """
        Checks if authorized user can unlike post
        """

        PostLikes.objects.create(
            post=self.post,
            user=self.user
        )

        post_to_like = {
            'post': self.post.id
        }

        response = self.client.post(
            self.url,
            data=post_to_like,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.auth_token}'
        )

        serialized_post = serializers.PostModelSerializer(
            Post.objects.first(),
            context={'request': self.request}
        )
        self.assertEqual(0, serialized_post.data['likes'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cant_like_unauthorized(self):
        """
        Checks if unauthorized user can't like post
        """

        post_to_like = {
            'post': self.post.id
        }

        response = self.client.post(
            self.url,
            data=post_to_like,
            format='json'
            # HTTP_AUTHORIZATION=f'Bearer {self.auth_token}' authorization is not providet
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cant_like_post_not_found(self):
        """
        Checks if authorized user can't like nonexistent post
        """

        post_to_like = {
            'post': 12
        }

        response = self.client.post(
            self.url,
            data=post_to_like,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.auth_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cant_like_bad_request(self):
        """
        Checks if authorized user can't make bad request
        """

        post_to_like = {
            'post': 'hell_yeah'
        }

        response = self.client.post(
            self.url,
            data=post_to_like,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.auth_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

