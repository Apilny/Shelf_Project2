from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            messages.error(request, 'E-Mail or Password is incorrect')
            return redirect('/shelf')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/shelf/profile')
        else:
            messages.error(request, 'E-Mail or Password is incorrect')
            return redirect('/shelf')

    return redirect('/shelf')


def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/shelf')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                password=pw_hash
            )
            request.session['user_id'] = User.objects.last().id

    return redirect('/shelf')


def profile(request):
    if not 'id' in request.session:
        messages.error(request, "must log in")
        return redirect('/shelf')
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)


def logout(request):
    request.session.clear()
    return redirect('/shelf')


def items(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'view_items.html', context)

def items_search(request):
    if request.method == 'GET':
        context={
            'items': Item.objects.filter(name__icontains=request.GET['search_field'])
        }
    return render (request, 'view_items.html',context)

def locations(request):
    context = {
        'stores': Store.objects.all()
    }
    return render(request, 'view_locations.html', context)


def location_items(request, location_id):
    location = Location.objects.get(id=location_id)
    context = {
        'items': location.items.all(),
        'location': location
    }
    return render(request, 'view_location_items.html', context)

def location_items_search(request, location_id):
    if request.method == 'GET':
        location=Location.objects.get(id=location_id)
        context={
            'items': location.items.filter(name__icontains=request.GET['search_field']),
            'location': location
        }
    return render(request, 'view_location_items.html',context)

def create_item_to_location(request, location_id):
    if request.method == "POST":
        location = Location.objects.get(id=location_id)
        try:
            Aisle.objects.get(id=request.POST['aisle_id'])
            aisle = Aistle.objects.get(id=request.POST['aisle_id'])
            Item.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                aisle=aisle,
                location=location
            )
            return redirect(f'shelf/{location_id}/items')
        except:
            aisle = Aisle.objects.create(
                description=request.POST['description'],
                location=Location.objects.get(id=location_id)
            )
            Item.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                aisle=aisle,
                location=location
            )
            return redirect(f'shelf/{location_id}/items')


def edit_item_at_location(request, item_id, location_id):
    item = Item.objects.get(id=item_id)
    context = {
        'item': item,
        'location': Location.objects.get(id=location_id)
    }
    return render(request, 'edit_item.html', context)


def update_item_at_location(request, item_id, location_id):
    if request.method == 'POST':
        item = Item.objects.get(id=item_id)
        item.name = request.POST['name']
        item.price = request.POST['price']
        try:
            Aisle.objects.get(id=request.POST['aistle_id'])
            aistle = Aistle.objects.get(id=request.POST['aistle_id'])
            item.aistle = aistle
            return redirect(f'shelf/{location_id}/items')
        except:
            aistle = aistle.objects.create(
                description=request.POST['location'],
                location=Location.objects.get(id=location_id),
                aistle=aistle
            )
            return redirect(f'shelf/{location_id}/items')


def view_aisle_items(request, aisle_id):
    context = {
        'aisle': Aisle.objects.get(id=aisle_id)
    }
    return render(request, 'view_aisle.html', context)


def create_store(request):
    if request.method == "POST":
        errors = Store.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/shelf/locations')
        else:
            try:
                store = Store.objects.get(name=request.POST['store_name'])
            except:
                store = Store.objects.create(
                    name=request.POST['store_name']
                )
            finally:
                Location.objects.create(
                    address=request.POST['address'],
                    city=request.POST['city'],
                    state=request.POST['state'],
                    zip_code=request.POST['zip_code'],
                    store=store
                )
    return redirect('/shelf/locations')

def show_map(request):
    mapbox_access_token = 'pk.eyJ1IjoiY29keW1hbGRvbmFkbzI4IiwiYSI6ImNrMzYzdjRyeDA3ZXUzYmt4MXE3ajI4encifQ.OpwaNlWkZIOU5W1rzfUI4w'
    return render(request, 'maps.html',
        {'mapbox_access_token':'pk.eyJ1IjoiY29keW1hbGRvbmFkbzI4IiwiYSI6ImNrMzYzdjRyeDA3ZXUzYmt4MXE3ajI4encifQ.OpwaNlWkZIOU5W1rzfUI4w' })
