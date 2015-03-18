from django.contrib import admin
from website.models import Account, Customer, Merchant, Product, Shipping_Company, Order, Transaction, Product_Order, orderShip#, Account_view


admin.site.register(Account)
admin.site.register(Product_Order)
admin.site.register(Customer)
admin.site.register(Merchant)
admin.site.register(Product)
admin.site.register(Shipping_Company)
admin.site.register(Order)
admin.site.register(orderShip)
admin.site.register(Transaction)
#admin.site.register(Account_view)
# Register your models here.
