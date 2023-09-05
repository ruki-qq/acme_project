from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context


class BirthdayCreateView(BirthdayMixin, CreateView):
    form_class = BirthdayForm


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    form_class = BirthdayForm


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'pk'
    paginate_by = 10


def birthday(request, pk=None):
    instance = get_object_or_404(Birthday, pk=pk) if pk else None
    form = BirthdayForm(
        request.POST or None, files=request.FILES or None, instance=instance
    )
    context = {'form': form}
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})

    return render(request, 'birthday/birthday_form.html', context)


def birthday_list(request):
    birthdays = Birthday.objects.order_by('pk')
    paginator = Paginator(birthdays, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    context = {'page': page}
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('birthday:list')
    return render(request, 'birthday/birthday_form.html', context)
