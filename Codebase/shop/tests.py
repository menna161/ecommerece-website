# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Product, Category

# tests.py
# tests.py
class UserRegistrationTests(TestCase):
    def test_registration_form_fields(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'name="confirm_password"')

    def test_email_validation(self):
        response = self.client.post(reverse('register'), {
            'email': 'invalid-email',
            'password': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_password_validation(self):
        response = self.client.post(reverse('register'), {
            'email': 'user@example.com',
            'password': 'short',
            'confirm_password': 'short'
        })
        self.assertFormError(response, 'form', 'password', 'Ensure this value has at least 8 characters (it has 5).')

    def test_successful_registration(self):
        response = self.client.post(reverse('register'), {
            'email': 'user@example.com',
            'password': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(email='user@example.com')
        self.assertIsNotNone(user)

class UserLoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@example.com', password='ValidPass123!')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'user@example.com',  # Use email as username
            'password': 'ValidPass123!'
        })
        self.assertRedirects(response, reverse('home'))

    def test_logout(self):
        self.client.login(username='user@example.com', password='ValidPass123!')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login') + '?next=/logout/')

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'user@example.com',  # Use email as username
            'password': 'WrongPass123!'
        })
        self.assertContains(response, 'Invalid email or password')

# class UserLoginLogoutTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='user', email='user@example.com', password='ValidPass123!')

#     def test_login(self):
#         response = self.client.post(reverse('login'), {
#             'username': 'user@example.com',  # Use email as username
#             'password': 'ValidPass123!'
#         })
#         self.assertRedirects(response, reverse('home'))

#     def test_logout(self):
#         self.client.login(username='user@example.com', password='ValidPass123!')
#         response = self.client.get(reverse('logout'))
#         self.assertRedirects(response, reverse('login') + '?next=/logout/')  # Redirect to login page with next parameter

#     def test_invalid_login(self):
#         response = self.client.post(reverse('login'), {
#             'username': 'user@example.com',  # Use email as username
#             'password': 'WrongPass123!'
#         })
#         self.assertContains(response, 'Invalid email or password')


class HomeViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=999.99,
            stock_quantity=10,
            image='static/shop/images/laptop.jpg',
            category=self.category
        )

    def test_home_display(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.product.image)

    def test_search_products(self):
        response = self.client.get(reverse('home') + '?q=Laptop')
        self.assertContains(response, self.product.name)

    def test_category_navigation(self):
        response = self.client.get(reverse('home') + '?category=' + str(self.category.id))
        self.assertContains(response, self.product.name)

class ProductDetailTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=999.99,
            stock_quantity=10,
            image='static/shop/images/laptop.jpg',
            category=self.category
        )

    def test_product_detail_display(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, self.product.price)
        self.assertContains(response, self.product.image)
        self.assertContains(response, 'Add to Cart')

    def test_multiple_images(self):
        # Assuming the product has multiple images
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertContains(response, 'laptop.jpg')