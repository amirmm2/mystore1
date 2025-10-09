from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm ,UpdateUserForm,UpdatePasswordForm,UpdateUserInfo
from django.utils.text import slugify
from django.contrib.auth.models import User
from  django.db.models import Q
import  json
from cart.cart import Cart
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect



def order_details(request, pk):
    if request.user.is_authenticated:
        order=Order.objects.get(id=pk)
        items=OrderItem.objects.filter(order=pk)


        context = {
            'order':order,
            'items':items,

        }
        return render(request, 'order_details.html', context)



    else:
        messages.success(request, 'دسترسی به این صفحه امکان پذیر نمی باشد')
        return redirect('/')


def search(request):
    query = request.GET.get("q")  # چون توی فرم اسم input = "q" هست
    if query:
        searched = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        if not searched.exists():
            messages.warning(request, 'چنین محصولی وجود ندارد')
            return redirect('search')
        return render(request, 'search.html', {'searched': searched})

    # وقتی چیزی وارد نشده
    return render(request, 'search.html', {})


def user_orders(request):
    if request.user.is_authenticated:
        delivered_orders=Order.objects.filter(user=request.user,status='Delivered')
        other_orders=Order.objects.filter(user=request.user).exclude(status='Delivered')
        context = {
            'delivered':delivered_orders,
            'other':other_orders,
        }
        return render(request, 'orders.html',context)
    else:
        messages.success(request,'دسترسی به این صفحه امکان پذیر نمی باشد')
        return redirect('/')

def search(request):
    query = request.GET.get("q")  # چون توی فرم اسم input = "q" هست
    if query:
        searched = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        if not searched.exists():
            messages.warning(request, 'چنین محصولی وجود ندارد')
            return redirect('search')
        return render(request, 'search.html', {'searched': searched})

    # وقتی چیزی وارد نشده
    return render(request, 'search.html', {})




def category_summery(request):
    all_cat=Category.objects.all()
    return render(request, 'category_summery.html',{'category':all_cat})




def home(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()  # برای نمایش دسته‌ها در منو یا صفحه اصلی
    return render(request, 'index.html', {
        'Products': all_products,
        'categories': categories
    })


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user=request.user)  # 🔧 اصلاح شد
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart.cart)
                cart = Cart(request)
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, "با موفقیت وارد شدید ✅")
            return redirect('/')
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است ❌")
            return redirect('login')
    return render(request, 'login.html')



def logout_user(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید ✅')
    return redirect('/')


def signup_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # کاربر جدید رو لاگین کن
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'اکانت شما ساخته شد ✅')
            return redirect('/')
        else:
            messages.error(request, 'مشکلی در ثبت‌نام وجود دارد ❌')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request, 'پروفایل شما ویرایش شد')
            return redirect('/')
        return render(request, 'update_user.html',{'user_form': user_form})
    else:
        messages.success(request, 'ابتدا باید ثبت نام کنید یا وارد شوید')
        return redirect('/')






def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

        form = UpdateUserInfo(request.POST or None, instance=current_user)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'اطلاعات کاربری شما با موفقیت ویرایش شد')
            return redirect('/')

        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'ابتدا باید ثبت نام کنید یا وارد شوید')
        return redirect('/')





def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == "POST":
            form = PasswordChangeForm(current_user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "پسورد با موفقیت تغییر کرد")
                return redirect('/')  # مقصد رو خودت مشخص کن
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = PasswordChangeForm(current_user)

        # همیشه فرم رو برگردون (چه معتبر باشه چه نباشه)
        return render(request, 'update_password.html', {'form': form})

    else:
        messages.success(request, 'باید اول ثبت نام کنید')
        return redirect('/')







def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product.html', {'product': product})


def category(request, cat):
    # جایگزینی - با فاصله (در صورت استفاده در URL)
    cat_name = cat.replace('-', ' ').strip()
    category = get_object_or_404(Category, name=cat_name)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {
        'products': products,
        'category': category
    })



