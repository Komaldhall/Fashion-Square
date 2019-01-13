from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
now = datetime.datetime.today().strftime("%Y-%m-%d")


def index(request):
    request.session['current_page']=''
    if not 'amount' in request.session:
        request.session['amount']={}
    if not 'cart' in request.session:
        request.session['cart'] = 0
    if not 'user_id' in request.session:
        user = ''
        first_user = '' 
        last_user = ''
    else:
        user = User.objects.get(id=request.session['user_id'])
        first_user = user.first_name.split()
        first_user = first_user[0][0]
        last_user = user.last_name.split()
        last_user = last_user[0][0]
    length=request.session['cart'] 
    context = {
        'user': user,   
        'first':first_user,
        'last':last_user,
        'length':length,
    }
        
    return render(request, 'its_eCommerce/fashionfront.html', context)
    
def register(request):
    display='1'
    if request.method == 'POST':
        form=request.POST
        errors = []
        
        if len(form['first_name']) < 2:
            errors.append('First name must be at least 2 characters.')
        if len(form['last_name']) < 2:
            errors.append('Last name must be at least 2 characters.')
        if len(form['password']) < 8:
            errors.append('Password must be at least 8 characters.')
        if not form['password'] == form['cpassword']:
            errors.append('Password/Confirmation do not match.')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('Please provide a valid email') 
        
        if errors:
            for e in errors:
                messages.error(request, e)
        else:        
            try:
                User.objects.get(email=form['email'])
                messages.error(request, 'Your email already exists. Please Login.')
                
            except User.DoesNotExist:
                hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
                c_hashed_pw = hashed_pw.decode('utf-8')
                User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=c_hashed_pw)
                messages.success(request,"You successfully registered. Please login!")
            context={
            'displayl':display,
            }  
            return render(request, 'its_eCommerce/fashionfront.html', context)   
    context={   
        'displayr':display,
    }             
    return render(request, 'its_eCommerce/fashionfront.html', context)


def login(request):
    confirm = ''
    display='1'
    if not 'current_page' in request.session:
        current_page = ''
    if request.method == 'POST':
        errors = []
        form=request.POST 
        if not EMAIL_REGEX.match(form['emaill']):
            errors.append('Please provide a valid email') 
        else:
            try:
                user=User.objects.get(email=form['emaill'])
                result = bcrypt.checkpw(request.POST['passwordl'].encode(), user.password.encode())
                if result:
                    request.session['user_id'] = user.id
                    
                    confirm = 'yes'
                    location = request.session['current_page']
                    print('location is ',location)
                    if location=='':
                        return redirect("/")
                    else:
                        return redirect("/"+location)
                    # use confirm for signin function in logpay

                    # if 'prod_id' in request.session: 
                          
                    #     return redirect('/cart')
                    # return redirect('/')    
                else:
                    messages.error(request, 'Password does not match.')    
            except User.DoesNotExist:
                messages.error(request, 'Your email does not exists. Please register.')
                return redirect('/register')
        
        if errors:
            for e in errors:
                messages.error(request, e)  
             
    context={
        'displayl':display,
    }  
    return render(request, 'its_eCommerce/fashionfront.html', context)   

def logout(request):
    location = request.session['current_page']
    request.session.clear()
    print('location is ',location)
    if location=='':
        return redirect("/")
    else:
        return redirect("/"+location)

def search(request):
    if request.method == 'POST':
        form=request.POST
        cate = form['category']
        cat=int(cate)
        if cat >0 and cat < 13:
            return redirect('/men?cat='+cate)
        elif cat>12 and cat<25:
            return redirect('/women?cat='+cate) 
        else:
            return redirect('/kid?cat='+cate)
    return redirect("/")

def cart(request):
    if not 'cart' in request.session:
        request.session['cart'] = 0
    productinfo = ''
    user_d = ''
    amount = 0
    length=0
    request.session['current_page']='cart'
    
    if not 'user_id' in request.session:
        user = ''
        first_user = '' 
        last_user = ''
        if 'id' in request.GET:
            id = request.GET['id']
            if not 'prod_id' in request.session:
                request.session['prod_id'] = id    
                # return redirect('/register') 
    else:
        user = request.session['user_id']
        user_d = User.objects.get(id=user)
        first_user = user_d.first_name.split()
        first_user = first_user[0][0]
        last_user = user_d.last_name.split()
        last_user = last_user[0][0]
        
    if 'prod' in request.session:
        productlist = request.session['prod']
        if (productlist != {}):
            if 'amount' in request.session:
                amount = request.session['amount']
                print(amount)  
            productinfo = {}
                    
            for key, val in productlist.items():
                productinfo[Product.objects.get(id = key)] = val
            length=len(productinfo)    
    request.session['cart']=length
    context={
        'user':user_d,
        'prodlist':productinfo,
        'amount':amount, 
        'length':length, 
        'first':first_user,
        'last':last_user,          
    }
    
    
    return render(request, 'its_eCommerce/cart.html', context)

def ship(request):
    if not 'user_id' in request.session:
        return redirect('/login')
    else:
        user = request.session['user_id']
        user_d = User.objects.get(id=user)
        first_user = user_d.first_name.split()
        first_user = first_user[0][0]
        last_user = user_d.last_name.split()
        last_user = last_user[0][0]
        length=request.session['cart']
        context={
            'user':user,
            'length':length, 
            'first':first_user,
            'last':last_user, 
        }
        return render(request, 'its_eCommerce/ship.html', context) 
        
def order(request):
    user = request.session['user_id']
    user_d = User.objects.get(id=user)
    first_user = user_d.first_name.split()
    first_user = first_user[0][0]
    last_user = user_d.last_name.split()
    last_user = last_user[0][0]
    length=request.session['cart']
    if request.method == 'POST':
        form=request.POST
        errors = []
        
        if len(form['name']) < 5:
            errors.append('Name must be at least 5 characters.')
        if errors:
            for e in errors:
                messages.error(request, e)
                return redirect('/buy')
        else:
            return redirect('/success')
    context={
            'user':user,
            'length':length, 
            'first':first_user,
            'last':last_user, 
    }        
    return render(request, 'its_eCommerce/buy.html', context) 

def success(request):
    if 'cart' in request.session:
        del request.session['cart']
    if 'prod' in request.session:
        del request.session['prod']
    user = request.session['user_id']
    user_d = User.objects.get(id=user)
    first_user = user_d.first_name.split()
    first_user = first_user[0][0]
    last_user = user_d.last_name.split()
    last_user = last_user[0][0]
    context={
        'user':user,
        'first':first_user,
        'last':last_user, 
    }  
    return render(request, 'its_eCommerce/success.html', context)

def buy(request):
    length=request.session['cart']
    user = request.session['user_id']
    user_d = User.objects.get(id=user)
    first_user = user_d.first_name.split()
    first_user = first_user[0][0]
    last_user = user_d.last_name.split()
    last_user = last_user[0][0]
    if request.method == 'POST':
        form=request.POST
        errors = []
        
        if len(form['full_name']) < 5:
            errors.append('Full name must be at least 5 characters.')
        if len(form['state']) < 5:
            errors.append('State must be at least 5 characters.')
        if len(form['address']) < 8:
            errors.append('Address must be at least 8 characters.')
        if errors:
            for e in errors:
                messages.error(request, e)
                return redirect('/ship')
    context={
        'length':length, 
        'first':first_user,
        'last':last_user, 
    }            
    return render(request, 'its_eCommerce/buy.html', context)

       

def add(request):
    if not 'prod' in request.session:
        request.session['prod'] = {}
    if 'id' in request.GET:
        id = request.GET['id']
        if not 'prev_cat' in request.session:
            request.session['prev_cat'] = ''
        if'loc' in request.GET:
            loc=request.GET['loc']
        if'cat' in request.GET:
            cat=request.GET['cat']
            request.session['prev_cat'] = cat

        if not 'id' in request.session:
            request.session['id'] = ''
        request.session['id'] = id    
        prod = Product.objects.get(id=id)
        productlist = request.session['prod']
        
        if (productlist == {}):
            productlist[prod.id] = 1
            
            request.session['prod'] = productlist 
        else:     
            found = ''
            for key, val in productlist.items():
                if (key == prod.id):
                    found = 'yes'
            if (found == ''):
                productlist[prod.id] = 1
            request.session['prod'] = productlist
        request.session['cart']=len(productlist)    
        amount = Product.objects.get(id = id).price
        print(amount)
        amountlist = request.session['amount']
        if (amountlist == {}):
            amountlist[prod.id] = amount
            
            request.session['amount'] = amountlist 
        else:     
            found = ''
            for key, val in amountlist.items():
                if (key == prod.id) :
                    found = 'yes'
            if (found == '') :
                amountlist[id] = amount 
            request.session['amount'] = amountlist    
    return redirect('/'+loc) 

def remove(request):
    if 'id' in request.GET:
        id = request.GET['id']
        productlist = request.session['prod']
        print('id', id)
        for key, val in productlist.items():
            if (key == id):
                print('came here')
                productlist.pop(key)
                break
        request.session['prod'] = productlist
        print('productlist', productlist)
        amountlist = request.session['amount']

        for key, val in amountlist.items():
            if (key == id):
                amountlist.pop(key)
                break
        request.session['amount'] = amountlist
        print('amountlist', amountlist)
        
    return redirect('/cart')    


def quantity(request):
    if request.method == 'POST':
        if 'id' in request.GET:
            id = request.GET['id']       
        quantity = int(request.POST['quantity'])
        
        if request.POST['button'] == 'left':
            if quantity > 1:
                quantity -= 1
        elif request.POST['button'] == 'right':   
            quantity += 1
        if quantity < 1 :
            quantity = 1
        
        amount = quantity * Product.objects.get(id = id).price
        
        amountlist = request.session['amount']
        
        for key, val in amountlist.items():
            if (key == id) :
                amountlist[key] = amount      
        request.session['amount'] = amountlist
        
        
        productlist = request.session['prod']
        for key, val in productlist.items():
            if key == id :
                productlist[key] = quantity

        request.session['prod'] = productlist

    return redirect('/cart') 

def showmen(request):
    if 'cart' in request.session:
        length=request.session['cart'] 
    else:
        length=0   
    request.session['current_page']='men'
    if not 'user_id' in request.session:
        user = ''
        first_user = '' 
        last_user = ''
    else:
        user = User.objects.get(id=request.session['user_id'])
        first_user = user.first_name.split()
        first_user = first_user[0][0]
        last_user = user.last_name.split()
        last_user = last_user[0][0]
    if 'prev_cat' in request.session:
        selected = request.session['prev_cat']
        products=Product.objects.filter(category_id=selected)
        del request.session['prev_cat']
    elif 'cat' in request.GET:
        selected = request.GET['cat']
        products=Product.objects.filter(category_id=selected)
    else:
        cat=Category.objects.filter(catType='men')
        products=Product.objects.filter(category__in = cat)
    categories=Category.objects.filter(catType='men')
    if 'prod' in request.session:
        productlist = request.session['prod']
    else:
        productlist=''    
        print(productlist)
    context={
        'categories': categories,
        'products': products,
        'prodlist':productlist,
        'user': user,   
        'first':first_user,
        'last':last_user,
        'length':length,
    }
    return render(request, 'its_eCommerce/men.html', context)

def showwomen(request):
    if 'cart' in request.session:
        length=request.session['cart'] 
    else:
        length=0    
    request.session['current_page']='women'
    if not 'user_id' in request.session:
        user = ''
        first_user = '' 
        last_user = ''
    else:
        user = User.objects.get(id=request.session['user_id'])
        first_user = user.first_name.split()
        first_user = first_user[0][0]
        last_user = user.last_name.split()
        last_user = last_user[0][0]
    if 'prev_cat' in request.session:
        selected = request.session['prev_cat']
        products=Product.objects.filter(category_id=selected)
        del request.session['prev_cat']
    elif 'cat' in request.GET:
        selected = request.GET['cat']
        products=Product.objects.filter(category_id=selected)
    else:
        cat=Category.objects.filter(catType='women')
        products=Product.objects.filter(category__in = cat)
    categories=Category.objects.filter(catType='women')
    context={
        'categories': categories,
        'products': products,
        'user': user,   
        'first':first_user,
        'last':last_user,
        'length':length,
    }
    return render(request, 'its_eCommerce/women.html', context)

def showkid(request):
    if 'cart' in request.session:
        length=request.session['cart'] 
    else:
        length=0  
    request.session['current_page']='kid'
    if not 'user_id' in request.session:
        user = ''
        first_user = '' 
        last_user = ''
    else:
        user = User.objects.get(id=request.session['user_id'])
        first_user = user.first_name.split()
        first_user = first_user[0][0]
        last_user = user.last_name.split()
        last_user = last_user[0][0]
   
    if 'prev_cat' in request.session:
        selected = request.session['prev_cat']
        products=Product.objects.filter(category_id=selected)
        del request.session['prev_cat']
    elif 'cat' in request.GET:
        selected = request.GET['cat']
        products=Product.objects.filter(category_id=selected)
    else:
        cat=Category.objects.filter(catType='boy')|Category.objects.filter(catType='girl')
        products=Product.objects.filter(category__in = cat)
    categoriesb=Category.objects.filter(catType='boy')
    categoriesg=Category.objects.filter(catType='girl')
    context={
        'categoriesb': categoriesb,
        'categoriesg': categoriesg,
        'products': products,
        'user': user,   
        'first':first_user,
        'last':last_user,
        'length':length,
    }
    return render(request, 'its_eCommerce/kid.html', context)    

def showProd(request):
    if 'cart' in request.session:
        length=request.session['cart'] 
    else:
        length=0  
    
    request.session['current_page']='showProduct'
    if not 'user_id' in request.session:
        user = ''
        first_user = '' 
        last_user = ''
    else:
        user = User.objects.get(id=request.session['user_id'])
        first_user = user.first_name.split()
        first_user = first_user[0][0]
        last_user = user.last_name.split()
        last_user = last_user[0][0]
    if 'id' in request.GET:
        id = request.GET['id']
        product=Product.objects.get(id=id)
        category=Category.objects.get(id=product.category_id)
        allProduct=Product.objects.filter(category_id=product.category_id)    
    else:
        product=''
        category=''
        allProduct=''
    context={
        'product':product,
        'category':category,
        'allProduct':allProduct,
        'user': user,   
        'first':first_user,
        'last':last_user,
        'length':length
    }
    return render(request, 'its_eCommerce/showProduct.html', context)











 
        

        


       



