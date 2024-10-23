from django.urls import reverse
from django.test import TestCase, Client
from shop.models import Product, Purchase


class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="book", price=740)

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_purchase_creation_without_discount(self):
        response = self.client.post(reverse('buy', args=[self.product.id]), {
            'product': self.product.id,
            'person': 'Ivanov',
            'address': 'Svetlaya St.',
            'quantity': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Спасибо за покупку, Ivanov! Вы приобрели 2 шт. товара. Итоговая цена: 1480.00 руб. Вы купили товар book.')

    def test_purchase_creation_with_10_discount(self):
        response = self.client.post(reverse('buy', args=[self.product.id]), {
            'product': self.product.id,
            'person': 'Ivanov',
            'address': 'Svetlaya St.',
            'quantity': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Спасибо за покупку, Ivanov! Вы приобрели 5 шт. товара. Применена скидка 10%. Итоговая цена: 3330.00 руб. Вы купили товар book.')

    def test_purchase_creation_with_20_discount(self):
        response = self.client.post(reverse('buy', args=[self.product.id]), {
            'product': self.product.id,
            'person': 'Ivanov',
            'address': 'Svetlaya St.',
            'quantity': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Спасибо за покупку, Ivanov! Вы приобрели 10 шт. товара. Применена скидка 20%. Итоговая цена: 5920.00 руб. Вы купили товар book.')
