from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime


class ProductTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name="book", price=740)
        self.product2 = Product.objects.create(name="pencil", price=50)

    def test_correctness_types(self):
        self.assertIsInstance(self.product1.name, str)
        self.assertIsInstance(self.product1.price, int)
        self.assertIsInstance(self.product2.name, str)
        self.assertIsInstance(self.product2.price, int)

    def test_correctness_data(self):
        self.assertEqual(self.product1.price, 740)
        self.assertEqual(self.product2.price, 50)
        self.assertEqual(self.product1.name, "book")
        self.assertEqual(self.product2.name, "pencil")

    def test_str_method(self):
        self.assertEqual(str(self.product1), "book")
        self.assertEqual(str(self.product2), "pencil")


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_book = Product.objects.create(name="book", price=740)
        self.datetime = datetime.now()
        self.purchase = Purchase.objects.create(
            product=self.product_book,
            person="Ivanov",
            address="Svetlaya St.",
            quantity=3
        )

    def test_purchase_quantity(self):
        self.assertEqual(self.purchase.quantity, 3)

    def test_correctness_types(self):
        self.assertIsInstance(self.purchase.person, str)
        self.assertIsInstance(self.purchase.address, str)
        self.assertIsInstance(self.purchase.date, datetime)
        self.assertIsInstance(self.purchase.quantity, int)

    def test_correctness_data(self):
        self.assertEqual(self.purchase.person, "Ivanov")
        self.assertEqual(self.purchase.address, "Svetlaya St.")
        self.assertEqual(self.purchase.quantity, 3)
        self.assertTrue(
            self.purchase.date.replace(microsecond=0) ==
            self.datetime.replace(microsecond=0)
        )

    def test_str_method(self):
        expected_str = "Ivanov - book (3 шт.)"
        self.assertEqual(str(self.purchase), expected_str)

    def test_foreign_key_relationship(self):
        self.assertEqual(self.purchase.product, self.product_book)
        self.assertEqual(self.purchase.product.price, 740)
        self.assertEqual(self.purchase.product.name, "book")
