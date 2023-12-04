from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm
from mailing.models import Client, Mailing, Logs
from mailing.services import time_task


class ChecksUser:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        if form.is_valid:
            new_client = form.save()
            new_client.owner = self.request.user
            new_client.save()

        return super().form_valid(form)


class ClientListView(ChecksUser, ListView):
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        client = super().get_queryset()
        return client.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'

    def test_func(self):
        objects = self.get_object()
        return self.request.user == objects.owner or self.request.user.is_superuser


class ClientDeleteView(LoginRequiredMixin, ChecksUser, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(LoginRequiredMixin, ChecksUser, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            new_client = form.save()
            new_client.owner = self.request.user
            new_client.save()
        return super().form_valid(form)

    def get_queryset(self):
        return time_task()

    def get_form_kwargs(self):
        user_request = super().get_form_kwargs()
        user_request['user'] = self.request.user
        return user_request


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        if self.request.user.has_perm('mailing.deactivate_mailing') or self.request.user.is_superuser:
            mailing = super().get_queryset()
            return mailing
        else:
            mailing = super().get_queryset()
            return mailing.filter(owner=self.request.user)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'


class MailingDeleteView(LoginRequiredMixin, ChecksUser, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(LoginRequiredMixin, ChecksUser, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        user_request = super().get_form_kwargs()
        user_request['user'] = self.request.user
        return user_request


class LogsListView(ListView):
    model = Logs
    template_name = 'mailing/mailing_report.html'


def contacts(request):
    return render(request, 'mailing/contacts.html')


class HomePageView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        blog = Blog.objects.all()[:3]  # выборка из базы данных 3 случайных записи Blog
        clients_count = len(Client.objects.all())  # подсчёт кол-во клиентов
        mailing_count = len(Mailing.objects.all())  # подсчёт кол-во рассылок
        mailing_active = len(Mailing.objects.filter(status='started'))  # подсчёт кол-во активных рассылок
        context = super().get_context_data()
        context['mailing_count'] = mailing_count
        context['mailing_active'] = mailing_active
        context['clients_count'] = clients_count
        context['blogs'] = blog

        return context


@permission_required('mailing.deactivate_mailing')
def off(request, pk):
    """Контролер для отключения рассылок"""

    obj = Mailing.objects.get(pk=pk)

    if obj.status == 'created' or 'started':
        obj.status = 'done'
        obj.save()

    return redirect(reverse('mailing:mailing_list'))
