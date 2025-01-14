from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from Owner.models import Owner
from Manager.models import Manager
from CustomerHome.models import Customer
from Vehicles.models import Vehicle
from RentVehicle.models import RentVehicle
from django.core.paginator import Paginator
from datetime import datetime
from datetime import date

# Create your views here.
def index(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    print(request.session.get('user_email'),"Manager Search section part")
    manager_email = request.session.get('user_email')

    vehicle_queryset = Vehicle.objects.all()
    if request.method == 'POST':

        vehicle_type = request.POST.get('vehicle_type')
        companies = request.POST.getlist('company')
        fuel_types = request.POST.getlist('fuel')
        price_range = request.POST.get('price_range')
        
        if vehicle_type:
            vehicle_queryset = vehicle_queryset.filter(Vehicle_type=vehicle_type)
        
       
        if companies:
            vehicle_queryset = vehicle_queryset.filter(Vehicle_company__in=companies)
        

        if fuel_types:
            vehicle_queryset = vehicle_queryset.filter(Vehicle_fuel__in=fuel_types)
        

        if price_range:
            if price_range == "Under 1000":
                vehicle_queryset = vehicle_queryset.filter(Vehicle_price__lt=1000)
            elif price_range == "1000-2000":
                vehicle_queryset = vehicle_queryset.filter(Vehicle_price__gte=1000, Vehicle_price__lte=2000)
            elif price_range == "Above 2000":
                vehicle_queryset = vehicle_queryset.filter(Vehicle_price__gt=2000)

    manager = Manager.objects.get(Manager_email=manager_email)
    vehicle = Vehicle.objects.all()
    Message=f"Welcome {manager.Manager_firstname}"

    paginator = Paginator(vehicle_queryset, 4)  
    page_number = request.GET.get('page')
    vehicle_page = paginator.get_page(page_number)

    no_of_pending_request=count_pending_rent_request()

    context = {
        'vehicle': vehicle_page,
        'Message': Message,
        'manager': manager,
        'no_of_pending_request': no_of_pending_request,
        "vehicle_types": ["Car", "Bike", "Bus", "Scooter", "Bicycle", "Tourist Van", "Truck"],
        "companies": [
            "Maruti", "Audi", "Mercedes", "Toyota", "Tata", "Kia", "Tesla", "Hyundai", "Land Rover", "MG", "Volkswagen", "BMW", "Jaguar", "Jeep", "Porsche", "Volvo",
            "Mahindra", "Honda", "Ford", "Renault", "Nissan", "Skoda", "Peugeot", "Fiat", "Mitsubishi", "Isuzu", "Suzuki", "Changan", "BYD", "SAIC", "Great Wall Motors", "Fisker"
            "Skoda", "Isuzu", "Datsun", "Bajaj", "Hero", "TVS", "Royal Enfield", 
            "Yamaha", "Suzuki", "Piaggio", "Ashok Leyland", "Force Motors", "Eicher"
        ],
        "fuel_types": ["Petrol", "Diesel", "CNG", "Electric"],
        "price_ranges": ["Under 1000", "1000-2000", "Above 2000"],
    }
    
    # return render(request, 'Owner_index.html', context)
    # return render(request,'Manager_index.html',{'vehicle':vehicle,'Message':Message,'manager':manager,'no_of_pending_request':no_of_pending_request})
    return render(request,'Manager_index.html',context)

def Profile(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)

    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_Profile.html',{'manager':manager,'no_of_pending_request':no_of_pending_request})

def AllCustomers(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    customer = Customer.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Manager_All_Customers.html",{'customer':customer,'manager':manager,'no_of_pending_request':no_of_pending_request})

def Customer_Profile(request,customer_email):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    customer = Customer.objects.get(customer_email=customer_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_Customer_Profile.html',{'manager':manager,'customer':customer,'no_of_pending_request':no_of_pending_request})

def upload_Vehicle(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Manager_Upload_Vehicle.html",{'manager':manager,'no_of_pending_request':no_of_pending_request})

def AllVehicles(request):
    if('user_email' not in request.session):
        return redirect('/signin/')
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    vehicle = Vehicle.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,"Manager_all_vehicles.html",{'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})

def showdetails(request,Vehicle_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)
    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_showdetails.html',{'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})

def CheckAvailability(request,Vehicle_license_plate):
    if('user_email' not in request.session):
        return redirect('/signin/')

    RentVehicle_Date_of_Booking=request.POST.get('RentVehicle_Date_of_Booking','')
    RentVehicle_Date_of_Return=request.POST.get('RentVehicle_Date_of_Return','')

    RentVehicle_Date_of_Booking = datetime.strptime(RentVehicle_Date_of_Booking, '%Y-%m-%d').date()
    RentVehicle_Date_of_Return = datetime.strptime(RentVehicle_Date_of_Return, '%Y-%m-%d').date()

    rentvehicle = RentVehicle.objects.filter(Vehicle_license_plate=Vehicle_license_plate)
    vehicle = Vehicle.objects.get(Vehicle_license_plate=Vehicle_license_plate)

    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)
    
    no_of_pending_request=count_pending_rent_request()

    if RentVehicle_Date_of_Booking < date.today():
        Incorrect_dates = "Please give proper dates"
        return render(request,'Owner_showdetails.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})

    if RentVehicle_Date_of_Return < RentVehicle_Date_of_Booking:
        Incorrect_dates = "Please give proper dates"
        return render(request,'Manager_showdetails.html',{'Incorrect_dates':Incorrect_dates,'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})
    
    days=(RentVehicle_Date_of_Return-RentVehicle_Date_of_Booking).days+1
    total=days*vehicle.Vehicle_price
    
    rent_data = {"RentVehicle_Date_of_Booking":RentVehicle_Date_of_Booking, "RentVehicle_Date_of_Return":RentVehicle_Date_of_Return,"days":days, "total":total}

    for rv in rentvehicle:

        # if (RentVehicle_Date_of_Booking < rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return < rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking > rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return > rv.RentVehicle_Date_of_Return):
        #     Available = True
        #     return render(request,'Manager_showdetails.html',{'Available':Available,'vehicle':vehicle,'manager':manager,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

        if (rv.RentVehicle_Date_of_Booking >= RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Booking) or (RentVehicle_Date_of_Booking >= rv.RentVehicle_Date_of_Booking and RentVehicle_Date_of_Return <= rv.RentVehicle_Date_of_Return) or (RentVehicle_Date_of_Booking <= rv.RentVehicle_Date_of_Return and RentVehicle_Date_of_Return >= rv.RentVehicle_Date_of_Return):
            if rv.isAvailable:
                Available = True
                Message = "Note that somebody has also requested for this vehicle from " + str(rv.RentVehicle_Date_of_Booking) + " to " + str(rv.RentVehicle_Date_of_Return)
                return render(request,'Manager_showdetails.html',{'Message':Message,'Available':Available,'vehicle':vehicle,'manager':manager,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

            NotAvailable = True
            return render(request,'Manager_showdetails.html',{'NotAvailable':NotAvailable,'dates':rv,'vehicle':vehicle,'manager':manager,'no_of_pending_request':no_of_pending_request})
    
    Available = True
    return render(request,'Manager_showdetails.html',{'Available':Available,'vehicle':vehicle,'manager':manager,'rent_data':rent_data,'no_of_pending_request':no_of_pending_request})

def RentRequest(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)

    rentvehicle = RentVehicle.objects.all()
    no_of_pending_request=count_pending_rent_request()
    return render(request,'Manager_RentRequest.html',{'manager':manager,'rentvehicle':rentvehicle,'no_of_pending_request':no_of_pending_request})

def SentRequests(request):
    if('user_email' not in request.session):
        return redirect('/signin/')

    manager_email = request.session.get('user_email')
    manager = Manager.objects.get(Manager_email=manager_email)

    no_of_pending_request=count_pending_rent_request()
    
    rentvehicle = RentVehicle.objects.filter(customer_email=manager_email)
    if rentvehicle.exists():
        vehicle = Vehicle.objects.all()
        return render(request,'Manager_SentRequests.html',{'manager':manager,'rentvehicle':rentvehicle,'vehicle':vehicle,'no_of_pending_request':no_of_pending_request})
    else:
        Message = "You haven't rented any vehicle yet!!"
        return render(request,'Manager_SentRequests.html',{'manager':manager,'rentvehicle':rentvehicle,'Message':Message,'no_of_pending_request':no_of_pending_request})

def count_pending_rent_request():
    no_of_pending_request=0
    rentvehicle = RentVehicle.objects.all()
    for rv in rentvehicle:
        if rv.request_status == "Pending":
            no_of_pending_request+=1
    return no_of_pending_request