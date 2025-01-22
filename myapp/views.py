from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from myapp.models import Product
from django.http import JsonResponse
import datetime

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'registration/signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'registration/signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'registration/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request,'registrartion/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'registrartion/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('home')



def add(request):
    user = request.user
    if request.method == "POST":
            expense = request.POST['expense']
            category = request.POST['category']

            name,price = expense.strip().split(' ')

            product = Product(category=category, name=name, price=price, user=user)
            product.save()
           
            return redirect ('home')
       

def chart(request):
    labels = []
    data = []
    month = datetime.date.today().month

    queryset = Product.objects.filter(user = request.user,current_date__month = month).values()

    final_dict = {}
    unset = set()
    for product in queryset:
        category = product.get('category').title()
        price = product.get('price')
        if category in unset:
            temp = {
                category: int(final_dict.get(category) + price)
            }
        else:
            temp ={
                category: int(price)
            }
            unset.add(category) 
        final_dict.update(temp)

    labels = list(final_dict.keys())
    data = list(final_dict.values())
    total = sum(data)

    return JsonResponse(data= {
        'labels': labels,
        'data': data,
        'total': total,
    })


def yearly(request):

    today = datetime.date.today()

    year = today.year

    labels = []
    data = []

    queryset = Product.objects.filter(user = request.user,current_date__year = year ).values()

    month_dict = {'January': 0, 'February': 0, 'March': 0, 'April': 0, 'May': 0, 'June': 0, 
              'July': 0, 'August': 0, 'September': 0, 'October': 0, 'November': 0, 'December': 0}

    for product in queryset:
        month = product.get('current_date').strftime("%B")
        price = product.get('price')
        month_dict[month] = int(month_dict[month]+ price)
    
    labels = list(month_dict.keys())
    label_data = list(month_dict.values())

    data= {
        'labels': labels,
        'label_data': label_data,
    }
    return render(request,'yearly.html',data)


def view_more(request):
    month = datetime.date.today().month

    queryset = Product.objects.filter(user = request.user,current_date__month = month).values('category','name','price','current_date','id').order_by("-id")

    return render(request,'home.html',{'comp_data':queryset})

def delete_product(request):

    id1 = request.GET.get('id')
    Product.objects.get(id=id1).delete()
    return redirect('view_more')