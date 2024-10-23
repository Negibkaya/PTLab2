from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address', 'quantity']

    def form_valid(self, form):
        purchase = form.save(commit=False)
        product = purchase.product.name
        person = purchase.person
        quantity = int(purchase.quantity)

        discount = 0
        if quantity >= 10:
            discount = 20  # 20% скидка
        elif quantity >= 5:
            discount = 10  # 10% скидка

        total_price = purchase.product.price * quantity * (1 - discount / 100)
        purchase.save()

        message = f'Спасибо за покупку, {person}! '
        message += f'Вы приобрели {quantity} шт. товара. '

        if discount > 0:
            message += f'Применена скидка {discount}%. '

        message += f'Итоговая цена: {total_price:.2f} руб. '
        message += f'Вы купили товар {product}. '

        context = {'message': message}

        return render(self.request, 'shop/purchase_success.html', context)
