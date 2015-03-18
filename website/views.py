import logging
from django.template import Context, loader
from django.db.models import Max
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext,loader
from website.models import *
from website.forms import *
from django.shortcuts import render_to_response
from django.forms.util import ErrorList
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404


logged_id=-1
	

def index(request):
	global logged_id
	logged_id=-1
	user_name="helo"
	context=RequestContext(request,{'user_name':user_name})
	return render(request,'index.html',context)

def login(request):
	if request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			account=Account.objects.get(user_name=form.cleaned_data['user_name'],pwd=form.cleaned_data['pwd'])
			global logged_id
			logged_id=account.user_id				
			if account.acc_type=="ME":
				return HttpResponseRedirect('/website/merchant_home/')				
			elif account.acc_type=="CU":
				return HttpResponseRedirect('/website/customer_home/') 
			return HttpResponseRedirect('/website/signup/')
	else:
		form=LoginForm()
	variables = RequestContext(request,{'form':form})
	return render_to_response ('login.html',variables)


def signup(request):
	if request.method=='POST':
		form=UserForm(request.POST)
		if form.is_valid():
			check=Account.objects.all().aggregate(Max('user_id'))
			if check['user_id__max']!=None:
                                id_count=check['user_id__max']+1
                        else:
                                id_count=0
			account = Account(user_id=id_count, user_name=form.cleaned_data['user_name'],pwd=form.cleaned_data		['pwd1'],email=form.cleaned_data['email'],acc_type=form.cleaned_data['type1'],address=form.cleaned_data['address'],phone=form.cleaned_data['phone'])
			account.save()
			if account.acc_type=="ME":
				merchant = Merchant(account=account,merchant_id=id_count,merchant_name=account.user_name)
				merchant.save()
			elif account.acc_type=="CU":
				customer = Customer(account=account,customer_id=id_count,customer_name=account.user_name)
				customer.save()	
			return HttpResponseRedirect('/website/login/') 
	else:
		form=UserForm()
	variables = RequestContext(request,{'form':form})
	return render_to_response ('signup.html',variables)

def about_us_cust(request):
	global logged_id
        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page</h1>')
                
	if account.acc_type=="CU":
		user_name="helo"
		context=RequestContext(request,{'user_name':user_name})
		return render(request,'about_us_cust.html',context)

def about_us_merch(request):
	global logged_id
	try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="CU":
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
	
	if account.acc_type=="ME":
		user_name="helo"
		context=RequestContext(request,{'user_name':user_name})
		return render(request,'about_us_merch.html',context)

def add_product(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="CU":
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
        
	if account.acc_type=="ME":
		if request.method=='POST':
			form=NewProductForm(request.POST)
			if form.is_valid():
				check=Product.objects.all().aggregate(Max('prod_id'))
				#id_count=check['prod_id__max']+1
				if check['prod_id__max']!=None:
                                        id_count=check['prod_id__max']+1
                                else:
                                        id_count=0
				merchant=Merchant.objects.get(merchant_id=logged_id)
				product = Product(merchant=merchant,prod_id=id_count,prod_name=form.cleaned_data['prod_name'],price=form.cleaned_data['price'],discount=form.cleaned_data['discount'],number=form.cleaned_data['no'])
				product.save()
				return HttpResponseRedirect('/website/my_products/') 
		else:
			form=NewProductForm()
		variables = RequestContext(request,{'form':form})
		return render_to_response ('add_product.html',variables)

def delete_order(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
	
	if account.acc_type=="CU":
		if request.method=='POST':
			form=DeleteProd(request.POST)
			if form.is_valid():
                                try:
                                        product=Product.objects.get(prod_id=form.cleaned_data['prod_id'])
                                        order=Order.objects.get(customer__customer_id=logged_id)
                                        Product_Order.objects.filter(order=order,product=product).delete()
                                except Product_Order.DoesNotExist:
                                        return HttpResponseNotFound('<h1>Invalid Product ID</h1>')
                                
				return HttpResponseRedirect('/website/order/') 
		else:
			form=DeleteProd()
		variables = RequestContext(request,{'form':form})
		return render_to_response ('delete_order.html',variables)


def add_order(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
	
	if account.acc_type=="CU":
		if request.method=='POST':
			form=OrderProd(request.POST)
			if form.is_valid():
				try:
					Order.objects.get(customer__customer_id=logged_id)
				except Order.DoesNotExist:
					check=Order.objects.all().aggregate(Max('order_id'))
					if check['order_id__max']!=None:
                                                id_count=check['order_id__max']+1
                                        else:
                                                id_count=0	
					customer=Customer.objects.get(customer_id=logged_id)	
					new_order=Order(order_id=id_count,customer=customer)
					new_order.save()
				order=Order.objects.get(customer__customer_id=logged_id)
				product=Product.objects.get(prod_id=form.cleaned_data['prod_id'])
				prod=Product_Order(order=order,product=product,quantity=form.cleaned_data['quantity'])
				prod.save()
				return HttpResponseRedirect('/website/order/') 
		else:
			form=OrderProd()
		variables = RequestContext(request,{'form':form})
		return render_to_response ('add_order.html',variables)


def delete_product(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="CU":
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
	
	if account.acc_type=="ME":

		if request.method=='POST':
			form=DeleteProd(request.POST)
			if form.is_valid():
                                try:
                                        product1=Product.objects.get(prod_id=form.cleaned_data['prod_id'])
                                        product2=Product.objects.filter(merchant__merchant_id=logged_id)
                                        if product1 in product2:
                                                Product.objects.get(prod_id=form.cleaned_data['prod_id']).delete()
                                except Product.DoesNotExist:
                                        return HttpResponseNotFound('<h1>Invalid Product ID</h1>')
                                
				return HttpResponseRedirect('/website/my_products/') 
		else:
			form=DeleteProd()
		variables = RequestContext(request,{'form':form})
		return render_to_response ('delete_product.html',variables)


def customer_home(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')

	
	if account.acc_type=="CU":
		user_name="helo"
		context=RequestContext(request,{'user_name':user_name})
		return render(request,'customer_home.html',context)

def merchant_home(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="CU":
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
	
	if account.acc_type=="ME":
		user_name="helo"
		context=RequestContext(request,{'merchant_home':user_name})
		return render(request,'merchant_home.html',context)

def finalise_order(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')

	
	if account.acc_type=="CU":

		if request.method=='POST':
			form=ChoiceForm(request.POST)
			if form.is_valid():
				order=Order.objects.get(customer__customer_id=logged_id)
				ship=Shipping_Company.objects.get(ship_name=form.cleaned_data['company'])
				try:
					orderShip.objects.get(order=order)
				except orderShip.DoesNotExist:
					order_ship=orderShip(order=order,ship=ship)
					order_ship.save()
				order_ship=orderShip.objects.get(order=order)
				order_ship.ship.no_sold+=order.shipping		
				order_ship.ship.save()
				product_order=Product_Order.objects.filter(order=order)
				for prod in product_order:
					prod.product.number-=prod.quantity
					prod.product.merchant.no_prod+=prod.quantity*prod.product.price
					prod.product.merchant.no_prod-=prod.quantity*prod.product.discount
					prod.product.merchant.save()
					prod.product.save()
				customer=Customer.objects.get(customer_id=logged_id)	
				customer.balance-=order.final_cost
				customer.save()
				Order.objects.get(customer__customer_id=logged_id).delete()		
				return HttpResponseRedirect('/website/order/') 
		else:
			form=ChoiceForm()
		variables = RequestContext(request,{'form':form})
		return render_to_response ('finalise_order.html',variables)


def my_products(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="CU":
                return HttpResponseNotFound('<h1>Page not found: Login as Merchant to access this page</h1>')
	
	if account.acc_type=="ME":
		produc=Product.objects.filter(merchant__merchant_id=logged_id)
		t=loader.get_template('my_products.html')	
		c=Context({'produc':produc,})
		return HttpResponse(t.render(c))

def order(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
	
	if account.acc_type=="CU":
		try:
			Order.objects.get(customer__customer_id=logged_id)
		except Order.DoesNotExist:
			check=Order.objects.all().aggregate(Max('order_id'))
			#id_count=check['order_id__max']+1
			if check['order_id__max']!=None:
                                id_count=check['order_id__max']+1
                        else:
                                id_count=0
			customer=Customer.objects.get(customer_id=logged_id)	
			new_order=Order(order_id=id_count,customer=customer)
			new_order.save()
		order=Order.objects.get(customer__customer_id=logged_id)
		produc=Product_Order.objects.filter(order=order)
		total=0
		discount=0
		qty=0
		for prod in produc:
			total=total+(prod.product.price*prod.quantity)
			discount=discount+(prod.product.discount*prod.quantity)
			qty=qty+prod.quantity
		order.total=total
		order.discount=discount
		order.taxes=(0.04)*order.total
		order.shipping=5*qty
		order.final_cost=order.total-order.discount+order.taxes+order.shipping
		order.save()
		t=loader.get_template('order.html')
		shipping=Shipping_Company.objects.all()	
		c=Context({'produc':produc,'order':order,'shipping':shipping})
		return HttpResponse(t.render(c))

def products(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

        try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')

	
	if account.acc_type=="CU":
		produc=Product.objects.all()
		t=loader.get_template('products.html')	
		c=Context({'produc':produc,})
		return HttpResponse(t.render(c))

def shipping_details(request):
	global logged_id
	#account=Account.objects.get(user_id=logged_id)

	try:
                account=Account.objects.get(user_id=logged_id)
        except Account.DoesNotExist:
                #404
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')
        #account=Account.objects.get(user_id=logged_id)

        if account.acc_type=="ME":
                return HttpResponseNotFound('<h1>Page not found: Login as Customer to access this page.</h1>')

        
	if account.acc_type=="CU":
		produc=Shipping_Company.objects.all()
		t=loader.get_template('shipping_details.html')	
		c=Context({'produc':produc,})
		return HttpResponse(t.render(c))


