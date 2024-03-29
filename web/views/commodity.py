from django.urls import reverse_lazy
from django_filters import (CharFilter, DateFilter,
                            BooleanFilter, ModelChoiceFilter)
from web.base.forms import ModelForm
from web.base.forms.fields import DisplayField
from web.base.forms import FilterSet, widgets
from web.base.views import (SecureFilteredListView, SecureUpdateView,
                            SecureCreateView)
from web.models import Commodity, CommodityType
from .filters import _filter_config


class CommodityEditForm(ModelForm):
    commodity_code = DisplayField(label='Commodity Code')

    class Meta:
        model = Commodity
        fields = [
            'commodity_code', 'validity_start_date', 'validity_end_date',
            'sigl_product_type'
        ]
        labels = {
            'validity_start_date': 'First day of validity',
            'validity_end_date': 'Last day of validity',
            'sigl_product_type': 'SIGL Product Type'
        }
        help_texts = {
            'validity_start_date':
            'The commodity code will be available for applications to choose \
            on applications forms, starting on this date',
            'validity_end_date':
            'After this date, the commodity will no \
            longer be available for applications to choose on application \
            forms. Leave blank for indefinitely continuing validity',
            'sigl_product_type':
            'Mandatory for Iron, Steel, Aluminium and \
            Textile commodities'
        }
        config = {
            'label': {
                'cols': 'three'
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
                    'href': 'commodity-list'
                },
                'submit': {
                    'label': 'Save'
                }
            }
        }


class CommodityCreateForm(ModelForm):
    commodity_code = CharFilter(label='Commodity Code')

    class Meta(CommodityEditForm.Meta):
        config = {
            'label': {
                'cols': 'three'
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
                    'href': 'commodity-list'
                },
                'submit': {
                    'label': 'Create'
                }
            }
        }


class CommodityFilter(FilterSet):
    commodity_code = CharFilter(field_name='commodity_code',
                                lookup_expr='icontains',
                                widget=widgets.TextInput,
                                label='Commodity Code')

    commodity_type = ModelChoiceFilter(queryset=CommodityType.objects.all(),
                                       lookup_expr='icontains',
                                       label='Commodity Type')

    valid_start = DateFilter(field_name='validity_start_date',
                             widget=widgets.DateInput,
                             lookup_expr='gte',
                             label='Valid between')

    valid_end = DateFilter(field_name='validity_end_date',
                           widget=widgets.DateInput,
                           lookup_expr='lte',
                           label='and')

    is_archived = BooleanFilter(field_name='is_active',
                                widget=widgets.CheckboxInput,
                                lookup_expr='exact',
                                exclude=True,
                                label='Search Archived')

    class Meta:
        model = Commodity
        fields = []
        config = _filter_config


class CommodityListView(SecureFilteredListView):
    template_name = 'web/commodity/list.html'
    filterset_class = CommodityFilter
    model = Commodity
    paginate_by = 100


class CommodityEditView(SecureUpdateView):
    template_name = 'web/commodity/edit.html'
    form_class = CommodityEditForm
    success_url = reverse_lazy('commodity-list')
    model = Commodity


class CommodityCreateView(SecureCreateView):
    template_name = 'web/commodity/create.html'
    form_class = CommodityCreateForm
    success_url = reverse_lazy('commodity-list')
