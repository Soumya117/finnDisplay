class JsonUtil:
    def __init__(self, result, data):
        self.result = result
        self.data = data
        self.result['link'] = self.data['link']

    def prepare_json(self, data=None, output=None, price=None):
        if data is None:
            data = self.data
        if output is None:
            output = self.result
        if price is not None:
            self.result['price'] = price

        output['text'] = data['text']
        output['address'] = data['address']
        output['geocode'] = data['geocode']
        output['area'] = data['area']

