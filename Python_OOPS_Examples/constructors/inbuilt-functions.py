#!/usr/bin/env python

class Topup_wallet:
    # non-parameterized constructor
    def __init__(self, my_topup_amount):
        self.topup_amount = my_topup_amount

    def topup(self):
        print('{} Points added up to wallet!'.format(self.topup_amount))

wallet = Topup_wallet('20')
wallet.topup()
print('')

print('Check if "topup_amount" attribute exists')
print(hasattr(wallet, "topup_amount"))
print('')

print('display the value assigned to attribute "topup_amount" during object creation')
print(getattr(wallet, "topup_amount"))
print('')

print('Change the value that was assigned  to attribute "topup_amount" during object creation, to 30')
setattr(wallet, "topup_amount", "30")
print('')

print('display the changed value')
print(getattr(wallet, "topup_amount"))
print('')

print('delete attribute "topup_amount"')
delattr(wallet, 'topup_amount')
print('')

print('Check if "topup_amount" attribute exists')
print(hasattr(wallet, "topup_amount"))
print('')
