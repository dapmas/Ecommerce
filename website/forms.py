from django import forms
from website.models import *
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList

class UserForm(forms.Form):
	user_name = forms.CharField()
	name = forms.CharField()
	pwd1 = forms.CharField(widget=forms.PasswordInput(),required=False)
	pwd2 = forms.CharField(widget=forms.PasswordInput(),required=False)
	email = forms.EmailField()
	address = forms.CharField()
	phone = forms.CharField()
	type1 = forms.ChoiceField(choices=(('CU','Customer'),('ME','Merchant')),required=True)
	

		
	def clean_email(self):
		email=self.cleaned_data['email']
		try:
			Account.objects.get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('An account is already registered under this email.')

	def clean_user_name(self):
		user_name=self.cleaned_data['user_name']
		try:
			Account.objects.get(user_name=user_name)
		except Account.DoesNotExist:
			return user_name
		raise forms.ValidationError("A user with that username already exists.")

	def clean(self):
		
                pwd1 = self.cleaned_data['pwd1']
                pwd2 = self.cleaned_data['pwd2']
	
		if pwd2 == '' or pwd1 == '':
                    self._errors['pwd2'] = self.error_class(['Password field cannot be blank'])		

                if pwd1 != pwd2:
                    # raise forms.ValidationError("Your passwords did not match.")
                    # instead of raising exceptions you should put an error on the form itself.
                    self._errors['pwd2'] = self.error_class(['Your passwords did not match'])
                return self.cleaned_data # return that cleaned data

                '''#if 'pwd1' in self.cleaned_data and 'pwd2' in self.cleaned_data:
                if self.cleaned_data['pwd1'] != self.cleaned_data['pwd2']:
                        raise forms.ValidationError("The two password fields didn't match.")
                else:
                        return self.cleaned_data
		pwd1=self.cleaned_data['username']
		
		try:
			Account.objects.get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError("A user with that username already exists.")'''


class LoginForm(forms.Form):
	user_name = forms.CharField()
	pwd = forms.CharField(widget=forms.PasswordInput())
	def clean(self):
		user_name=self.cleaned_data['user_name']
		pwd = self.cleaned_data['pwd']
		try:
                        Account.objects.get(user_name=user_name,pwd=pwd)
                        return self.cleaned_data
		except Account.DoesNotExist:
                        self._errors['pwd'] = self.error_class(['Username or password is incorrect.'])
                                
                #raise forms.ValidationError("Username or password is incorrect.")
                '''else:
                        return self.cleaned_data'''


class NewProductForm(forms.Form):
	prod_name = forms.CharField()
	price = forms.CharField()
	discount = forms.CharField()
	no = forms.CharField()
	
class DeleteProd(forms.Form):
	prod_id = forms.CharField()

class OrderProd(forms.Form):
	prod_id = forms.CharField()
	quantity = forms.CharField()

class ChoiceForm(forms.Form):
    company = forms.ModelChoiceField(queryset=Shipping_Company.objects.all().order_by('ship'),required=True)
