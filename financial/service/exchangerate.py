class MoneyRate:
    def __init__(self, from_currency: str, to_currency: str, summa: float, rate: float):
        self.to = to_currency
        self.from_ = from_currency
        self.rate = rate
        self.summa = summa
        self.__valuta_dict = None

    @property
    def changed_summa(self):
        self.__valuta_dict = {
            'USD': {
                'EUR': self.summa * (1 / self.rate),
                'UAH': self.summa * self.rate,
                'PLN': self.summa * self.rate,
            },
            'EUR': {
                'USD': self.summa * self.rate,
                'UAH': self.summa * self.rate,
                'PLN': self.summa * self.rate
            },
            'UAH': {
                'USD': self.summa * (1 / self.rate),
                'EUR': self.summa * (1 / self.rate),
                'PLN': self.summa * (1 / self.rate)
            },
            'PLN': {
                'USD': self.summa * (1 / self.rate),
                'EUR': self.summa * (1 / self.rate),
                'UAH': self.summa * self.rate
            }

        }
        return round(float(self.__valuta_dict.get(self.from_).get(self.to)), 2)
