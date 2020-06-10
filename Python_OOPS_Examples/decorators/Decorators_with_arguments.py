#!/usr/bin/env python

# Decorator method, modifies behavior of an existing method, when called.
# Here, since we wanted to pass an attribute to decorator, 
# we wrap the decorator method 'round_off_decor' inside a wrapper function 'round_off'.

def round_off(round_off_by):
    def round_off_decor(method):
        def inner(fun):
            fun.amount = round(fun.amount, round_off_by)
            method(fun)
        return inner
    return round_off_decor

class Wallet:
    def __init__(self):
        self.amount = 81.5687

    def show_amount(self):
        print self.amount

# Child class inheriting method 'show_amount' without Decorator 'round_off'
class Wallet_Old(Wallet, object):
    def show_amount(self):
        super(Wallet_Old, self).show_amount()

# Child class inheriting method 'show_amount' with Decorator 'round_off'
class Wallet_New(Wallet, object):
    @round_off(round_off_by=2)
    def show_amount(self):
        super(Wallet_New, self).show_amount()

      

W = Wallet_Old()
W.show_amount() 

W = Wallet_New()
W.show_amount()
