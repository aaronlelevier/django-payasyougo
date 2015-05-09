from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewTests(TestCase):

    def test_index(self):
        response = self.client.get(reverse('index'))
        assert response.status_code == 200
        assert response.context['headline']


class ErrorPageTests(TestCase):
    
    def test_404(self):
        response = self.client.get(reverse('404'))
        assert response.status_code == 404
        assert response.context['error_code']

    def test_500(self):
        response = self.client.get(reverse('500'))
        assert response.status_code == 500
        assert response.context['error_code']