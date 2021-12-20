from django.test import TestCase
import datetime

from django.utils import timezone

from .models import Input

class InputModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now()+datetime.timedelta(days=30)
        future_Input = Input(date=time)
        self.assertIs(future_Input.was_published_recently(),False)
# Create your tests here.
