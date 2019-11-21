from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^shelf$' , views.index),
    url(r'^shelf/login$', views.login),
    url(r'^shelf/register$', views.register),
    url(r'^shelf/profile$', views.profile),
    url(r'^shelf/profile/edit', views.profile_edit_form),
    url(r'^shelf/edit$', views.edit_profile),    
    url(r'^shelf/item$', views.items),
    url(r'^shelf/item/search$', views.items_search),
    url(r'^shelf/locations$', views.locations),
    url(r'^shelf/locations/search$', views.location_search),
    url(r'^shelf/(?P<location_id>\d+)/items$', views.location_items),
    url(r'^shelf/(?P<location_id>\d+)/items/search$', views.location_items_search),
    url(r'^shelf/(?P<location_id>\d+)/create_item$', views.create_item_to_location),
    url(r'^shelf/(?P<location_id>\d+)/(?P<food_id>)/edit$', views.edit_item_at_location),
    url(r'^shelf/(?P<location_id>\d+)/(?P<food_id>)/update$', views.update_item_at_location),
    url(r'^shelf/(?P<aisle_id>\d+)/aisle$',views.view_aisle_items),
    url(r'^shelf/(?P<aisle_id>\d+)/aisle/search$',views.aisle_search),
    url(r'^shelf/(?P<item_id>\d+)/edit$', views.item_edit_form),
    url(r'^shelf/edit/(?P<item_id>\d+)$', views.edit_item),    
    url(r'^shelf/create/store$',views.create_store),
    url(r'^shelf/(?P<item_id>\d+)/add_favorite_item', views.add_favorite_item),
    url(r'^shelf/(?P<location_id>\d+)/add_favorite_location', views.add_favorite_location),
    url(r'^logout$', views.logout)
]
