from django.test import TestCase
from blockchains.models import  BSCPair
from django.urls import reverse


class Exaples(TestCase):

    def setUp(self):
        BSCPair.objects.create(
            factory_address="factory_address1",
            pair_address = "pair_address1",
            pair_symbol = "pair_symbol1",
            token0 = "token01",
            token1 = "token11",
        )
    
    def tearDown(self):
        pairs = BSCPair.objects.all()
        for pair in pairs:
            pair.delete()


    def test_bscpair(self):
        pair1 = BSCPair.objects.get(pair_symbol='pair_symbol1')
        self.assertEqual(pair1.token0, 'token01')

    def test_bsc_list_view(self):
        response = self.client.get(reverse("blockchains:bsc-list"))
        self.assertEqual(response.status_code, 200)

        pairs_list = BSCPair.objects.all()
        pairs_in_context = response.context["pairs"]

        self.assertEqual(len(pairs_list), len(pairs_in_context))
        for a1, a2 in zip(pairs_list, pairs_in_context):
            self.assertEqual(a1.pk, a2.pk)