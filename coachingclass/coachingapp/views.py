from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from django.views import View 
from .models import *  
from .forms import CustomerRegistrationForm, CustomerProfileForm  
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here. 
@login_required
def home(request): 

    students = Customer.objects.all() 
    nearest_birthdays = []
    min_days = float('inf')

    for student in students:
        days_until_bday = student.days_until_birthday()
        if days_until_bday < min_days:
            min_days = days_until_bday
            nearest_birthdays = [student]
        elif days_until_bday == min_days:
            nearest_birthdays.append(student)

    # Prepare notification message
    notification = None
    if nearest_birthdays:
        if min_days == 0:
            notification = f"Happy Birthday {' and '.join([student.name for student in nearest_birthdays])}!"
        #else:
            #notification = f"Upcoming birthdays: {' and '.join([student.name for student in nearest_birthdays])} in {min_days} days."

    if notification is not None:
        return render(request, 'home.html', {'notification': notification})
    else:
        return render(request, 'home.html')
@login_required
def contact(request): 
    return render(request,"contact.html")  

@login_required
def services(request): 
    return render(request,"services.html")   

@login_required
def about(request): 
    return render(request,"about.html")  

@login_required
def gallery(request): 
    images=Image.objects.all()  
    cats=Category.objects.all() 
    data={'images':images,'cats':cats}  
    return render(request,"gallery.html",data) 

@login_required
def show_category_page(request,cid):     
    cats=Category.objects.all()  
    catg=Category.objects.get(pk=cid)   
    images=Image.objects.filter(cat=catg)
    data={'images':images,'cats':cats}  
    return render(request,"gallery.html",data)     

class CustomerRegistrationView(View):  
    def get(self,request):      
        form=CustomerRegistrationForm()      
        return render(request,'customerregistration.html',locals())   
    def post(self,request): 
        form=CustomerRegistrationForm(request.POST)   
        if form.is_valid():   
            form.save()   
            messages.success(request,"Congratulations! User created successfully.")   
        else: 
            messages.warning(request,"Invalid user data.")    
        return render(request,'customerregistration.html',locals())      

   
 
@method_decorator(login_required,name='dispatch')
class ProfileView(View):   
    def get(self, request):   
        form=CustomerProfileForm()   
        return render(request,'profile.html',locals())  
    def post(self, request):  
        form=CustomerProfileForm(request.POST) 
        if form.is_valid():  
            user=request.user 
            name=form.cleaned_data['name'] 
            mobile=form.cleaned_data['mobile']  
            email=form.cleaned_data['email']  
            bday=form.cleaned_data['bday']
            reg=Customer(user=user, name=name, mobile=mobile, email=email, bday=bday) 
            reg.save()  
            messages.success(request,"Congratulations! Profile saved successfully")   
            return redirect('profile')  # Adjust the URL name as needed
        else:
            messages.warning(request, "Invalid data provided.")
            
        # Render the profile page again with the form and validation errors
        return render(request, 'profile.html', {'form': form})  
    
@login_required    
def data(request):  
    dat=Customer.objects.filter(user=request.user)   
    return render(request,"data.html",locals())   

@method_decorator(login_required,name='dispatch') 
class updateData(View):                       
    def get(self,request,pk):   
        dat=Customer.objects.get(pk=pk) 
        form=CustomerProfileForm(instance=dat)  
        return render(request,"updateData.html",locals())     
    def post(self,request,pk):  
        form=CustomerProfileForm(request.POST)  
        if form.is_valid():  
            dat=Customer.objects.get(pk=pk) 
            dat.name=form.cleaned_data['name'] 
            dat.mobile=form.cleaned_data['mobile'] 
            dat.email=form.cleaned_data['email']  
            dat.bday=form.cleaned_data['bday']
            dat.save()    
            messages.success(request,"Congratulations! Profile updated successfully")   
        else: 
            messages.warning("Invalid input data!")    
        return redirect("data")       
    
