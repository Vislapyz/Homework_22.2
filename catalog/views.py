from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(name, phone, message)
        return super().get(request, *args, **kwargs)


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        products = self.get_queryset()
        for product in products:
            product.version = product.versions.filter(is_current=True).first()

        context["object_list"] = products

        return context


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )

        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(self.request.POST)

        else:
            context_data["formset"] = VersionFormset()

        return context_data

    def form_valid(self, form):

        context_data = self.get_context_data()
        formset = context_data["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object

            formset.save()

            self.object = form.save()
            self.object.author = self.request.user
            self.object.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product

    form_class = ProductForm

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.get_object().pk])

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )

        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(
                self.request.POST, instance=self.object
            )

        else:
            context_data["formset"] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):

        context_data = self.get_context_data()
        formset = context_data["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            #
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:products_list")
