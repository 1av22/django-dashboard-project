from django.shortcuts import render
from rest_framework import generics
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


from .models import WorldBankData
from .serializers import WorldBankDataSerializer


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = 'dashboard/dashboard.html'
    login_url = '/login/'


class DataListAPIView(generics.ListAPIView):

    serializer_class = WorldBankDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        queryset = WorldBankData.objects.all()

        country = self.request.query_params.get('country')
        series = self.request.query_params.get('series')
        start_year = self.request.query_params.get('start_year')
        end_year = self.request.query_params.get('end_year')

        if country:
            queryset = queryset.filter(country__iexact=country)

        if series:
            queryset = queryset.filter(series__icontains=series)

        if start_year:
            queryset = queryset.filter(year__gte=start_year)

        if end_year:
            queryset = queryset.filter(year__lte=end_year)

        return queryset.order_by('year')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
