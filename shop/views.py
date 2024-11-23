from django.shortcuts import render
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
        product = form.cleaned_data['product']
        person_name = form.cleaned_data['person']
        quantity = form.cleaned_data['quantity']
        address = form.cleaned_data['address']

        purchases = Purchase.objects.filter(
            person=person_name, product=product)

        if purchases.exists():
            purchase = purchases.first()
            total_quantity = purchase.quantity + quantity
            purchase.quantity += quantity  # Обновляем количество
        else:
            purchase = Purchase(product=product, person=person_name,
                                address=address, quantity=quantity)
            total_quantity = quantity

        discount = 0
        if total_quantity >= 10:
            discount = 20  # 20% скидка
        elif total_quantity >= 5:
            discount = 10  # 10% скидка

        total_price = product.price * total_quantity * (1 - discount / 100)

        purchase.save()

        message = f'Спасибо за покупку, {person_name}! '
        message += f'Теперь у вас {total_quantity} шт. товара {product.name}. '
        if discount > 0:
            message += f'Применена скидка {discount}%. '
        message += f'Итоговая цена: {total_price:.2f} руб. '

        context = {'message': message}
        return render(self.request, 'shop/purchase_success.html', context)
