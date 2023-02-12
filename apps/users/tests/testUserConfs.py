from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

from apps.users.forms.userConfigsForms import UserChangePasswordForm

#utils
def create_user(email='prueba@mail.com', password='elpepe!', username='elpepe', **kwargs):
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password=password,
        **kwargs
    )

class TestUserConfs(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = create_user(bio='biography1')
        
        self.client.force_login(self.user)
        
    def test_change_user_biography(self):
        change_bio_url = reverse_lazy('core:users:change_bio')
        
        old_bio = self.user.bio
        
        data = {
            'biography': 'newBiography',
        }
        
        self.client.post(change_bio_url, data)
        self.user.refresh_from_db()
        
        self.assertNotEqual(old_bio, self.user.bio)
        self.assertEqual(self.user.bio, data['biography'])
    
    def test_change_password(self):
        change_password_url = reverse_lazy('core:users:change_password')
        
        old_password = 'elpepe!'
        old_password_encrypted = self.user.password
        
        new_password = 'sanjuan12!'
        
        data = {
            'old_password': old_password,
            'password1': new_password,
            'password2': new_password,
        }
        
        self.client.post(change_password_url, data)
        self.user.refresh_from_db()
        
        self.assertTrue(self.user.check_password(new_password))
        self.assertNotEqual(old_password_encrypted, self.user.password)
        self.assertFalse(self.user.check_password(old_password))
    
    def test_change_invalid_password(self):
        change_password_url = reverse_lazy('core:users:change_password')
        
        old_password = 'invalidpassword'
        new_password = 'sanjuan'
        
        data = {
            'old_password': old_password,
            'password1': new_password,
            'password2': 'sanjuan12',
        }

        form = UserChangePasswordForm(data=data, user=self.user)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"], ["Passwords don't match"])
        self.assertEqual(form.errors["old_password"], ["You have entered your old password incorrectly!"])
    
