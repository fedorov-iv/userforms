# -*- coding: utf8 -*-
from django.contrib import admin
from userforms.models import UserForm


class UserFormListFilter(admin.SimpleListFilter):

    # USAGE
    # In your admin class, pass the filter class as tuple for the list_filter attribute:
    #
    # list_filter = (CategoryListFilter,)

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Form'

    #template = "admin/select_filter.html"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'userform'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        list_tuple = []
        for user_form in UserForm.objects.all():
            #print category
            list_tuple.append((user_form.id, user_form.title))
        return list_tuple

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or 'other')
        # to decide how to filter the queryset.
        if self.value():
            return queryset.filter(user_form__id=self.value())
        else:
            return queryset
