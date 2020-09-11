from django.test import SimpleTestCase
from django.urls import resolve,reverse
from adra.views import PersonaListView,PersonaDetailView,PersonaCreateView
import  adra

class TestUrls(SimpleTestCase):

    def test_url_persona_home(self):
        url = reverse('adra:persona-home')
        self.assertEquals(resolve(url).func.view_class,PersonaListView)

    def test_url_persona_detail(self):
        url = reverse('adra:personas_detail',args=[3])
        self.assertEquals(resolve(url).func.view_class,PersonaDetailView)

    def test_url_persona_create(self):
        url = reverse('adra:persona-create')
        self.assertEquals(resolve(url).func.view_class,PersonaCreateView)