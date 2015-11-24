from django.test import TestCase


class VisualizationsMethodTests(TestCase):
    def test_dummy(self):
        test_var = 30
        self.assertEqual(test_var > 20, True, "The number is not bigger")
