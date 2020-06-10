#!/usr/bin/env python

# Decorator method, modifies behavior of an existing method, when called.
def round_off(method):
    def inner(fun):
        fun.amount = round(fun.amount)
        method(fun)
    return inner

class Wallet:
    def __init__(self):
        self.amount = 81.9987

    def show_amount(self):
        print self.amount

# Child class inheriting method 'show_amount' without Decorator 'round_off'
class Wallet_Old(Wallet, object):
    def show_amount(self):
        super(Wallet_Old, self).show_amount()

# Child class inheriting method 'show_amount' with Decorator 'round_off'
class Wallet_New(Wallet, object):
    @round_off
    def show_amount(self):
        super(Wallet_New, self).show_amount()

      

W = Wallet_Old()
W.show_amount() 

W = Wallet_New()
W.show_amount()
