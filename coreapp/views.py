from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.views.generic.detail import DetailView
from coreapp.cart import Cart
from .models import Category, Product, ProductImage
from django.core.mail import EmailMultiAlternatives

def commonData():
    context = {}
    parentCatData = Category.objects.filter(status=1,parent__isnull=True).order_by('id')
    for cat in parentCatData:
        cat.subcatData = ""
        subCategoryData = Category.objects.filter(status=1,parent=cat.id)
        if subCategoryData:
            cat.subcatData = subCategoryData

    context['globalCategory'] = parentCatData
    return context

def handleSignin(request):
    if request.user.is_authenticated:
        redirect('/blog')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == '':
            messages.error(request,'Please enter username!')
            return render(request, 'login.html', {'commonData': commonData()})
        if password == '':
            messages.error(request,'Please enter password!')
            return render(request, 'login.html', {'commonData': commonData()})
        else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request,'Incorrect username or password!')
                return render(request, 'coreapp/authentication/login.html', {'commonData': commonData()})
    else:
        return render(request, 'coreapp/authentication/login.html', {'commonData': commonData()})

def handleLogout(request):
    auth.logout(request)
    return redirect('/')

def handleSignup(request):
    if request.method=='POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(email)<10:
            messages.error(request, " Your email is not valid")
            return render(request, 'coreapp/authentication/register.html', {'commonData': commonData()})

        if len(fname)<2  or len(lname)<2:
            messages.error(request, " First,Last Name Should be proper")
            return render(request, 'coreapp/authentication/register.html', {'commonData': commonData()})

        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return render(request, 'coreapp/authentication/register.html', {'commonData': commonData()})

        if not User.objects.filter(username=email, email=email ).exists():
            myuser = User.objects.create_user(first_name=fname, last_name=lname, username=email, email=email, password=pass1)
            #########SEND EMAIL CODE#########
            plaintext = get_template('email_register.html')
            htmly     = get_template('email_register.html')
            baseurl = request.build_absolute_uri()
            d = { 
                'first_name': fname,
                'last_name': lname,
                'username': email,
                'password': pass1,
                'baseurl': baseurl,
            }
            subject, from_email, to = 'Your Registration is successful', 'admin@webblogapp.com', email
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            myuser.save()
            messages.success(request, "You are Registered successfully !")
            return redirect('/login')
        else:
            messages.error(request, "Whoops .! Username/Email Already in use .!")
            return render(request, 'coreapp/authentication/register.html', {'commonData': commonData()})
    else:
        return render(request, 'coreapp/authentication/register.html', {'commonData': commonData()})

def index(request):
    product = Product.objects.filter(is_published=1).order_by('-id')
    for singleblog in product:
        proImage = ProductImage.objects.filter(product=singleblog.id).first()
        singleblog.image = ""
        if proImage:
            singleblog.image = proImage

    params = {
        'productData': product,
        'commonData': commonData()
    }
    
    return render(request, 'coreapp/index.html', params)

class productDetail(DetailView):
    model = Product
    template_name = "coreapp/product-details.html"
    context_object_name = "productData"

    def get_context_data(self, *args, **kwargs):
        product  = Product.objects.get(slug=self.kwargs.get("slug"))
        context = super().get_context_data(*args, **kwargs)
        context['productImg'] = ProductImage.objects.filter(product=product)
        context['commonData'] = commonData()
        return context

def categoryView(request, slug):
    catDetail = Category.objects.get(slug=slug)
    if catDetail.status is "0":
        raise Http404

    subcatData = ""
    if catDetail.parent is not None:
        catDetail = Category.objects.get(id=catDetail.parent.id)
        subcatData = Category.objects.filter(slug=slug)
    d = {"category":catDetail.id,"is_published":1}
    
    if subcatData:
        d.update({
            "subcategory":subcatData[0].id
        })
    product = Product.objects.filter(**d).order_by('-id')

    for singleblog in product:
        proImage = ProductImage.objects.filter(product=singleblog.id).first()
        singleblog.image = ""
        if proImage:
            singleblog.image = proImage

    params = {
        'productData': product,
        'categoryData': catDetail,
        'subCategoryData': subcatData,
        'commonData': commonData()
    }
    
    return render(request, 'coreapp/category-view.html', params)

def checkoutView(request):
    params = {'commonData': commonData()}
    return render(request, 'coreapp/checkout.html', params)

def contactView(request):
    params = {'commonData': commonData()}
    return render(request, 'coreapp/contact.html', params)
"""
    CART FUNCTIONS
"""
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def cartDetail(request):
    params = {'commonData': commonData()}
    return render(request, 'coreapp/cart.html', params)

@csrf_exempt
def cartAdd(request, id):
    cartQty = int(request.POST.get('cartQty', 0))
    cart = Cart(request)
    product = Product.objects.get(id=id)
    if cartQty > 0:
        for i in range(cartQty):
            cart.add(product=product)
    return JsonResponse({
        "success":True
    })

@csrf_exempt
def cartDeleteProduct(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return JsonResponse({"success":True})

@csrf_exempt
def cartItemclear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return JsonResponse({"success":True})

@csrf_exempt
def cartClear(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({"success":True})
