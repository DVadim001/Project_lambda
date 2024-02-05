from django.shortcuts import render, redirect
from . import forms
from .models import Product, Category, Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .handlers import bot


# Create your views here.


# отображение главной статраницы
def home(request):
    # Поисковая строка
    search_bar = forms.SearchForm()
    # Собираем все продукты
    product_info = Product.objects.all()
    # Собираем все категории товаров
    category_info = Category.objects.all()
    # отправить элементы на фронт
    context = {'form': search_bar,
               'product': product_info,
               'category': category_info}
    return render(request, 'index.html', context)


# Вывод товаров по определённой категории
def get_full_category(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category_name=category)
    # Отправляем данные на фронт
    context = {'products': products}
    return render(request, 'exact_category.html', context)


# Вывод информации о конкретном продукте
def get_full_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'exact_product.html', context)


# отображение страницы о нас
def about(request):
    return render(request, 'about.html')


# отображение страницы с контактами
def contact(request):
    return render(request, 'contact.html')


# поиск продукта
def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        try:
            exat_product = Product.objects.get(pr_name__icontains=get_product)

            return redirect(f"product/{exat_product.id}")
        except:
            return redirect('/product-not-found')


# Если продукт не был найден
def pr_not_found(request):
    return render(request, 'not_found.html')


# Добавление товара в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        cheker = Product.objects.get(id=pk)
        if cheker.pr_count >= int(request.POST.get('pr_amount')):
            Cart.objects.create(user_id=request.user.id,
                                user_product=cheker,
                                user_product_quantity=int(request.POST.get('pr_amount'))).save()
            # Сделать, чтобы удалялось количество товара из базы при оформлении заказа

            return redirect('/')


# Отображение корзина пользователя
def get_user_cart(request):
    # Вся информация о корзине пользователя
    cart = Cart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        text = 'Новый заказ!\n\n'

        for i in cart:
            text += f'Название товара: {i.user_product}\n' \
                    f'Количество: {i.user_product_quantity}\n\n'
        bot.send_message(82836904, text)
        cart.delete()
        return redirect('/')

    # Отправить данные на фронт
    context = {'cart': cart}
    return render(request, 'user_cart.html', context)


# Удаление товара из корзины
def del_from_cart(request, pk):
    product_to_delete = Product.objects.get(id=pk)
    Cart.objects.filter(user_id=request.user.id,
                        user_product=product_to_delete).delete()
    return redirect('/cart')


# Регистрация
class Register(View):
    template_name = 'registration/register.html'

    # Отправка формы регистрации
    def get(self, request):
        context = {'form': UserCreationForm}
        return render(request, self.template_name, context)

    # Добавление пользователя в БД
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        context = {'form': UserCreationForm}
        return render(request, self.template_name, context)


# Функция выхода
def logout_view(request):
    logout(request)
    return redirect('/')
