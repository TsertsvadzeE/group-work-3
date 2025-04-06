from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Dish, Order, Review
from .forms import DishForm, OrderForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dish_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('dish_list')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class HomeRedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dish_list')
        return redirect('login')


class DishListView(ListView):
    model = Dish
    template_name = 'dish_list.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        queryset = Dish.objects.all()

        name = self.request.GET.get('name', '')
        category = self.request.GET.get('category', '')
        price_min = self.request.GET.get('price_min', '')
        price_max = self.request.GET.get('price_max', '')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = dict(Dish.category_choices)
        return context


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish
    template_name = 'dish_detail.html'
    context_object_name = 'dish'

class DishCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'dish_create.html'
    success_url = reverse_lazy('dish_list')

    def test_func(self):
        return self.request.user.is_staff

class DishUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'dish_create.html'
    success_url = reverse_lazy('dish_list')

    def test_func(self):
        return self.request.user.is_staff

class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dish
    template_name = 'dish_confirm_delete.html'
    success_url = reverse_lazy('dish_list')

    def test_func(self):
        return self.request.user.is_staff


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_form.html'

    def form_valid(self, form):
        dish = get_object_or_404(Dish, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.dish = dish
        messages.success(self.request, f"{dish.name} add to your orders!")
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('order_list')

class OrderDeleteView (LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Order
    template_name = 'order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

    def test_func(self):
        return self.request.user == self.get_object().user


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)



class ReviewCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_create.html'

    def form_valid(self, form):
        dish = get_object_or_404(Dish, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.dish = dish
        messages.success(self.request, "Added successfully!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated

    def get_success_url(self):
        return reverse_lazy('review_list')


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

    def test_func(self):
        return self.request.user == self.get_object().user


