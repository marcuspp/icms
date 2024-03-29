from django_filters import CharFilter, ChoiceFilter
from web.base.forms import FilterSet, ModelForm
from web.base.forms.widgets import Select, TextInput
from web.base.views import (SecureCreateView, SecureFilteredListView,
                            SecureUpdateView)
from web.models import Constabulary

from .contacts import ContactsManagementMixin
from .filters import _filter_config


class ConstabularyEditForm(ModelForm):
    class Meta:
        model = Constabulary
        fields = ['name', 'region', 'email']
        labels = {
            'name': 'Constabulary Name',
            'region': 'Constabulary Region',
            'email': 'Email Address'
        }
        widgets = {'region': Select(choices=Constabulary.REGIONS)}
        config = {
            'label': {
                'cols': 'three',
                'prompt': 'west'
            },
            'input': {
                'cols': 'six'
            },
            'padding': {
                'right': 'three'
            },
            'actions': {
                'padding': {
                    'left': None
                },
                'link': {
                    'label': 'Cancel',
                    'href': 'constabulary-list'
                }
            }
        }


class ConstabularyCreateForm(ConstabularyEditForm):
    class Meta(ConstabularyEditForm.Meta):
        config = {
            'label': {
                'cols': 'three',
                'prompt': 'west'
            },
            'input': {
                'cols': 'six'
            },
            'padding': {
                'right': 'three'
            },
            'actions': {
                'padding': {
                    'left': None
                },
                'link': {
                    'label': 'Cancel',
                    'href': 'constabulary-list'
                },
                'submit': {
                    'label': 'Create'
                }
            }
        }


class ConstabulariesFilter(FilterSet):
    name = CharFilter(field_name='name',
                      lookup_expr='icontains',
                      widget=TextInput,
                      label='Constabulary Name')

    region = ChoiceFilter(field_name='region',
                          choices=Constabulary.REGIONS,
                          lookup_expr='icontains',
                          widget=Select,
                          label='Constabulary Region')

    email = CharFilter(field_name='email',
                       lookup_expr='icontains',
                       widget=TextInput,
                       label='Email Address')

    class Meta:
        model = Constabulary
        fields = []
        config = _filter_config


class ConstabularyListView(SecureFilteredListView):
    template_name = 'web/constabulary/list.html'
    model = Constabulary
    filterset_class = ConstabulariesFilter


class ConstabularyEditView(ContactsManagementMixin, SecureUpdateView):
    template_name = 'web/constabulary/edit.html'
    form_class = ConstabularyEditForm
    model = Constabulary


class ConstabularyCreateView(ContactsManagementMixin, SecureCreateView):
    template_name = 'web/constabulary/create.html'
    form_class = ConstabularyCreateForm
    model = Constabulary
