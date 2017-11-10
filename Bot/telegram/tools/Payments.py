import json


class LabeledPrice:
    def __init__(self):
        self._labeled_price = []

    def add(self, label, amount):
        self._labeled_price.append({'label': label,  'amount': amount})

    def __getattr__(self, attr):
        return json.dumps(self._labeled_price) if attr == 'json' else None
