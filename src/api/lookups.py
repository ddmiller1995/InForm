from ajax_select import register, LookupChannel
from .models import Youth

@register('youth')
class YouthLookup(LookupChannel):

    model = Youth

    def get_query(self, q, request):
        return self.model.objects.filter(youth_name__icontains=q).order_by('youth_name')[:50]

    def format_item_display(self, item):
        return u"<span class='youth'>%s</span>" % item.youth_name