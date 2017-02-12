from django.conf.urls import include, url
from .views import McBotView

urlpatterns = [
                  url(r'^688a4b82f1be392a232d017eb0d9197ef2515edf5175b88722/?$', McBotView.as_view()) 
               ]