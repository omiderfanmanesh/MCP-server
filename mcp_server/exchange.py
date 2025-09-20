from dataclasses import dataclass
from typing import Dict


@dataclass
class ExchangeRates:
    base: str
    rates: Dict[str, float]

    def convert(self, amount: float, from_ccy: str, to_ccy: str) -> float:
        from_c = from_ccy.upper()
        to_c = to_ccy.upper()
        if from_c == to_c:
            return amount
        # Normalize to base, then to target
        # rates are relative to base (1 base = rate[target])
        if from_c == self.base:
            if to_c not in self.rates:
                raise ValueError(f"Unknown currency: {to_c}")
            return amount * self.rates[to_c]
        if to_c == self.base:
            if from_c not in self.rates:
                raise ValueError(f"Unknown currency: {from_c}")
            return amount / self.rates[from_c]
        if from_c not in self.rates or to_c not in self.rates:
            missing = from_c if from_c not in self.rates else to_c
            raise ValueError(f"Unknown currency: {missing}")
        base_amount = amount / self.rates[from_c]
        return base_amount * self.rates[to_c]


def default_rates() -> ExchangeRates:
    # Synthetic dataset relative to USD
    return ExchangeRates(
        base="USD",
        rates={
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 147.0,
            "CAD": 1.35,
            "AUD": 1.52,
            "CHF": 0.86,
            "CNY": 7.25,
            "INR": 83.1,
            "BRL": 5.2,
        },
    )

