#!/usr/bin/env python

class Topup_wallet:
    # non-parameterized constructor
    def __init__(self, my_topup_amount):
        self.topup_amount = my_topup_amount

    def topup(self):
        print('{} Points added up to wallet!'.format(self.topup_amount))

wallet = Topup_wallet('20')
wallet.topup()
