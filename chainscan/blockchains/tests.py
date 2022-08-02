from django.test import TestCase
from blockchains.models import  BSCPair


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

    

