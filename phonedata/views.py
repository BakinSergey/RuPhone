from django.views.generic.base import TemplateView
from django.contrib import messages
from phonedata.models import PhoneRange


class PhoneView(TemplateView):
    http_method_names = ['get']
    template_name = 'phone_info.html'
    search_query = ''
    phone_numb = ''

    def find_numberdata(self):
        code = self.phone_numb[:3]
        body = self.phone_numb[3:]
        try:
            phone = PhoneRange.objects.get(code=code, start__lte=body, finish__gte=body)
        except PhoneRange.MultipleObjectsReturned:
            return 'wrong_reestr'

        except PhoneRange.DoesNotExist:
            return 'not found'

        return self.search_query, phone.provider, phone.region

    def validate_number(self):

        self.search_query = self.search_query.replace(' ', '')

        if False in [i.isdigit() for i in self.search_query]:
            return 'not digit'

        if len(self.search_query) > 11:
            return 'len exceed'

        if len(self.search_query) < 5:
            return 'len too few'

        self.phone_numb = self.search_query

        if len(self.search_query) == 11:
            self.phone_numb = self.search_query[1:]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        self.search_query = self.request.GET.get('q')

        if not self.search_query:
            messages.add_message(self.request, messages.INFO, 'Введите номер')
            return context
        else:

            if self.validate_number() == 'not digit':
                messages.add_message(self.request, messages.ERROR, 'в номере допустимы только цифры')
            elif self.validate_number() == 'len exceed':
                messages.add_message(self.request, messages.ERROR, 'номер не может быть длиннее 11 цифр')

            elif self.validate_number() == 'len too few':
                messages.add_message(self.request, messages.ERROR, 'слишком короткий номер(менее 5 цифр)')

            else:
                search_result = self.find_numberdata()
                if search_result == 'wrong_reestr':
                    messages.add_message(self.request, messages.ERROR,
                                         'номер найден в более чем одном диапазоне - реестр кривой')
                    return context

                if search_result == 'not found':
                    messages.add_message(self.request, messages.INFO, 'номер не найден')
                    return context
                # success case
                for field in search_result:
                    messages.add_message(self.request, messages.SUCCESS, field)

        return context
