from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from events.models import Event, TakenEvent
from .forms import UploadEventFile


def index_page(request):
    return render(request, 'index.html')


def event_page(request):
    return render(request, 'events.html', {'events': Event.objects.all().order_by('data_limit')})


def plug_page(request):
    return render(request, 'plug.html')


def event_filter_parser(self, filter_string):

    filter_string = filter_string
    status = 2
    user_id = self.request.user

    if 'all' in filter_string:
        Status_Bool = False
        order_by = '-status'
    elif 'closed' in filter_string:
        Status_Bool = True
        order_by = '-data_limit'
        status = 2
    elif 'name=' in filter_string:
        Status_Bool = False
        order_by = '-data_limit'
        filter_string = filter_string.split('=')
        name = filter_string[1]
        return Event.objects.filter(user_id=user_id, name=name).order_by(order_by)
    elif 'sorting=' in filter_string:
        Status_Bool = True
        status = 1
        filter_string = filter_string.split('=')
        order_by = filter_string[1]
    else:
        Status_Bool = True
        order_by = 'data_limit'
        status = 1

    if Status_Bool:
        return Event.objects.filter(status_id=status, user_id=user_id).order_by(order_by)
    else:
        return Event.objects.filter(user_id=user_id).order_by(order_by)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = TakenEvent
    template_name = 'taken_events.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(LoanedBooksByUserListView, self).get_context_data(**kwargs)
        #some_data = TakenEvent.objects.select_related('event').filter(event__status_id=1,
        #                                                                    event__user_id=self.request.user)
        sort_type = self.kwargs.get('sort')
        some_data = event_filter_parser(self, str(sort_type)[:50])
        context.update({'something': some_data})
        return context

    def get_queryset(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Performers').exists():
            employee_query = TakenEvent.objects.filter(performer_id=self.request.user)
            event = Event.objects.filter(takenevent__in=employee_query).order_by('status')
            return event
        else:
            sort_type = self.kwargs.get('sort')
            event_query = event_filter_parser(self, str(sort_type)[:50])
            taken = TakenEvent.objects.filter(event__in=event_query)
            #event_query = TakenEvent.objects.select_related('event').filter(event__status_id=1, event__user_id=self.request.user)
            return taken


class EventView(LoginRequiredMixin, generic.DetailView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        event_query = Event.objects.filter(status_id=1, event_type_id=1)
        taken = TakenEvent.objects.filter(event__in=event_query, performer_id=self.request.user)
        context.update({'taken_event': taken})
        return context
    model = Event


def UploadRequestFileView(request, te):

    takenevent = get_object_or_404(TakenEvent, pk=te)

    if request.method == 'POST':
        form = UploadEventFile(request.POST, request.FILES)
        if form.is_valid():
            takenevent.response_file = form.cleaned_data['response_file']
            takenevent.save()
            return HttpResponseRedirect(reverse_lazy('my-event'))
    else:
        form = UploadEventFile()
    return render(request, 'upload_event_file.html', {'form': form, 'taken_event': takenevent})


class takeEventView(View):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('ct_event')
        event = Event.objects.get(id=event_id)
        event_connection = TakenEvent.objects.get_or_create(event=event, performer=request.user)

        # MAIL
        event_name = event.name
        requster = User.objects.get(username=request.user.username)
        requster_name = requster.username

        user_id = event.user
        USER = User.objects.get(username=user_id)
        user_email = USER.email
        user_name = USER.username

        if user_email is not None and user_email != '':
            subject = 'Уведомление: Новый отклик по событию \'{}\''.format(event_name)
            body = 'Приветствуем, @{}! На ваше событие \'{}\' откликнулся пользователь @{}.'.format(user_name, event_name, requster_name)
            send_mail(subject, body, 'andruy.savchovski@yandex.ru', [USER.email])
        return HttpResponseRedirect('/taken_events/')


class EventCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'events.create_event'
    model = Event
    fields = ['name', 'descriptions', 'event_type', 'data_limit']
    success_url = reverse_lazy('all-events')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)