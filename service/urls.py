"""service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf.urls.static import static
from django.conf import settings

from events.views import event_page, plug_page, index_page, LoanedBooksByUserListView, EventView, EventCreate
from events.views import takeEventView, UploadRequestFileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='home-page'),
    path('events/', event_page, name='all-events'),
    path('events/?<pk>', EventView.as_view(), name='detail-event'),
    path('taken_events/<sort>', LoanedBooksByUserListView.as_view(), name='my-event-sorting'),
    path('taken_events/', LoanedBooksByUserListView.as_view(), name='my-event'),
    path('plug/', plug_page,  name='plug-page'),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('events/create/', EventCreate.as_view(), name='event_create'),
    path('events/file-upload/<te>', UploadRequestFileView, name='request_upload'),
    path('take-event/<str:ct_event>/', takeEventView.as_view(), name='add-event')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

