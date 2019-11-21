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
            request.session['first_name'] = user.first_name
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
            request.session['id'] = User.objects.last().id
            request.session['first_name'] = User.objects.last().first_name
            return redirect('/shelf/profile')
    return redirect('/shelf')


def profile(request):
    if not 'id' in request.session:
        messages.error(request, "must log in")
        return redirect('/shelf')
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user,
        'locations': user.locations.all(),
        'items': user.items.all()
    }
    return render(request, 'profile.html', context)


def profile_edit_form(request):
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, "edit_user.html", context)


def edit_profile(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/shelf/profile/edit')
        else:
            change = User.objects.get(id=request.session['id'])
            change.email = request.POST['email']
            change.first_name = request.POST['first_name']
            change.last_name = request.POST['last_name']
            change.password = request.POST['password']
            change.save()
            return redirect('/shelf/profile')
    return redirect('/shelf')


def logout(request):
    request.session.clear()
    return redirect('/shelf')


def items(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'items': Item.objects.all().order_by('name'),
        'user': user
    }
    return render(request, 'view_items.html', context)


def item_edit_form(request, item_id):
    context = {
        "item": Item.objects.get(id=item_id)
    }
    return render(request, 'edit_item.html', context)


def edit_item(request, item_id):
    if request.method == 'POST':
        changes = Item.objects.get(id=item_id)
        changes.name = request.POST['name']
        changes.price = request.POST['price']
        changes.aisle.description = request.POST['description']
        changes.save()
        return redirect('/shelf/{item_id}/edit')
    else:
        return redirect('view_items.html')


def items_search(request):
    if request.method == 'GET':
        context = {
            'items': Item.objects.filter(name__icontains=request.GET['search_field'])
        }
    return render(request, 'view_items.html', context)


def locations(request):
    context = {
        'stores': Store.objects.all().order_by('name')
    }
    return render(request, 'view_locations.html', context)


def location_search(request):
    if request.method == 'GET':
        context = {
            'stores': Store.objects.filter(name__icontains=request.GET['search_field'])
        }
    return render(request, 'view_locations.html', context)


def location_items(request, location_id):
    location = Location.objects.get(id=location_id)
    context = {
        'items': location.items.all().order_by('name'),
        'location': location
    }
    return render(request, 'view_location_items.html', context)


def location_items_search(request, location_id):
    if request.method == 'GET':
        location = Location.objects.get(id=location_id)
        context = {
            'items': location.items.filter(name__icontains=request.GET['search_field']),
            'location': location
        }
    return render(request, 'view_location_items.html', context)


def create_item_to_location(request, location_id):
    if request.method == "POST":
        errors = Item.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect(f'/shelf/{location_id}/items')
            else:
                location = Location.objects.get(id=location_id)
                print(request.POST['aisle_id'])
                try:
                    aisle=Aisle.objects.get(id=request.POST['aisle_id'])
                    print(request.POST['aisle_id'])
                    print('this did work')
                except:
                    print('did not work')
                    aisle = Aisle.objects.create(
                        description=request.POST['aisle_id'],
                        location=Location.objects.get(id=location_id)
                    )
                finally:
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
    aisle = Aisle.objects.get(id=aisle_id)
    context = {
        'items': aisle.items.all().order_by('name'),
        'aisle': aisle
    }
    return render(request, 'view_aisle.html', context)


def aisle_search(request, aisle_id):
    if request.method == 'GET':
        aisle = Aisle.objects.get(id=aisle_id)
        context = {
            'items': aisle.items.filter(name__icontains=request.GET['search_field']),
            'aisle': aisle
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
                print(request.POST['store_name'])
                store = Store.objects.get(id=request.POST['store_name'])
            except:
                print('did not work')
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

def add_favorite_item(request, item_id):
    user=User.objects.get(id=request.session['id'])
    item=Item.objects.get(id=item_id)
    user.items.add(item)
    print('item worked')
    return redirect('/shelf/profile')

def add_favorite_location(request, location_id):
    user=User.objects.get(id=request.session['id'])
    location=Location.objects.get(id=location_id)
    user.locations.add(location)
    print('location worked')
    return redirect('/shelf/profile')
