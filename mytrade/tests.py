from django.test import TestCase
import datetime

from django.utils import timezone
from django.urls import reverse

from .models import Input


class InputModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now()+datetime.timedelta(days=30)
        future_Input = Input(date=time)
        self.assertIs(future_Input.was_published_recently(), False)
# Create your tests here.


class views_test(TestCase):
    def test_sma(self):
        request_data = {'short': 5, 'long': 14, 'val': 30, 'jpy': 100000, 'term_from_year': 2019,
                        'term_from_month': 1,  'term_from_day': 1, 'term_to_year': 2020, 'term_to_month': 1, 'term_to_day': 1, 'candlestick': 'BTC1D'}
        response = self.client.get(reverse('sma'))

        self.assetEqual(response.status_code, 200)
