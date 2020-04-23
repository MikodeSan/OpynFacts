import pytest

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

# from .models import Album, Artist, Contact, Booking


# Front Anomymous
class TestFrontAnomymous(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.USER_EMAIL = 'user@dummy.com'
        cls.USER_NAME = cls.USER_EMAIL
        cls.USER_PWD = 'dummy_pwd'
        
        cls.KNOWN_EMAIL = 'known_user@dummy.com'
        cls.KNOWN_NAME = cls.KNOWN_EMAIL
        cls.KNOWN_PWD = 'dummy_known_pwd'
        user = get_user_model().objects.create_user(cls.KNOWN_NAME, cls.KNOWN_EMAIL, cls.KNOWN_PWD)
        print('Dummy known user {} is created for test: {}'.format(user, user != None))

    def tearDown(self):
        self.client.logout()

    def test_front_signup_get_page(self):
        """
        test that signup page returns a 200
        """
        response = self.client.get(reverse('account:signup'))
        self.assertEqual(response.status_code, 200)

    def test_front_signup_post_new_user(self):
        """
        test that signup page redirects to profil
        """
        data = {
            'user_mail': self.USER_NAME,
        }
        response = self.client.post(reverse('account:signup'), data)

        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, reverse('account:signup'))
        self.assertNotIn('errors', response.context)

    def test_front_signup_post_known_user(self):
        """
        test that signup page redirects to profil
        """
        data = {
            'user_mail': self.KNOWN_NAME,
        }
        response = self.client.post(reverse('account:signup'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('account:signup'))
        self.assertIn('errors', response.context)

    def test_front_signup_password_new_user(self):
        """
        test that signup-password page redirects to Home
        """
        data = {
            'user_mail': self.USER_EMAIL,
            'user_password': self.USER_PWD,
            'user_password_confirm': self.USER_PWD,
            }
        response = self.client.post(reverse('account:signup-pwd'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('product:home'))

    def test_front_signin_page(self):
        """
        test that signin page returns a 200
        """
        response = self.client.get(reverse('account:signin'))
        self.assertEqual(response.status_code, 200)

    def test_front_signin_post_id(self):
        """
        test that signin page redirects to profile
        """
        data = {
            'username': self.KNOWN_NAME,
            'password': self.KNOWN_PWD,
        }
        response = self.client.post(reverse('account:signin'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, reverse('account:profile', kwargs={'user_id':1}))
        self.assertContains(response, reverse('account:profile'))
        self.assertNotIn('error', response.context)

    def test_front_profile_page(self):
        """
        [TODO] Test that profile page redirects to sign-in page
        """
        # response = self.client.get(reverse('account:profile', kwargs={'user_id': 1}), follow=True)
        # self.assertEqual(response.status_code, 200)
        # self.assertContains(response, reverse('account:signin'))
        pass

    def test_front_signout_request_page(self):
        """
        [TODO] Test that sign-out request page redirects to sign-in page
        """
        # response = self.client.get(reverse('account:profile', kwargs={'user_id': 1}), follow=True)
        # self.assertEqual(response.status_code, 200)
        # self.assertContains(response, reverse('account:signin'))
        pass

    def test_front_signout_page(self):
        """
        test that sign-out page redirects to home
        """
        response = self.client.get(reverse('account:signout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('product:home'))

# Front Authenticated
class TestFrontAuthenticated(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.USER_PWD = 'dummy_pwd'
        email = 'user@dummy.com'
        username = email
        cls.USER = get_user_model().objects.create_user(username, email, cls.USER_PWD)
        print('Dummy user {} is created for test: {}'.format(cls.USER, cls.USER != None))

    def setUp(self):
        # self.client = Client()
        self.client.login(username=self.USER.username, password=self.USER_PWD)

    def tearDown(self):
        self.client.logout()

    def test_front_signup_page(self):
        """
        [TODO] Test that sign-up page redirects to sign-out request page
        """
        pass

    def test_front_signup_password_page(self):
        """
        [TODO] Test that sign-up password page redirects to sign-out request page
        """
        pass

    def test_front_signin_page(self):
        """
        [TODO] Test that sign-in page redirects to sign-out request page
        """
        pass

    def test_front_profile_page(self):
        """
        Test that profile page returns a 200
        """
        response = self.client.get(reverse('account:profile', kwargs={'user_id': 1}))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_front_signout_request_page(self):
        """
        Test that signout request page returns a 200
        """
        response = self.client.get(reverse('account:signout_request'))
        self.assertEqual(response.status_code, 200)

    def test_front_signout_page(self):
        """
        Test that signout page redirects to home
        """
        response = self.client.get(reverse('account:signout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('product:home'))

