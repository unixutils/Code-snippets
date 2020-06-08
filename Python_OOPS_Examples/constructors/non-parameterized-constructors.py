#!/usr/bin/env python

class Topup_wallet:
    # non-parameterized constructor
    def __init__(self):
        self.topup_amount = 10

    def topup(self):
        print('{} Points added up to wallet!'.format(self.topup_amount))


wallet = Topup_wallet()
wallet.topup()
