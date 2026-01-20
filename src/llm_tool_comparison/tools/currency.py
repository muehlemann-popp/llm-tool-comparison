"""Currency converter tool with mock data."""

from typing import Dict
from haystack import component


# Mock exchange rates (as of a fixed date for consistency)
EXCHANGE_RATES = {
    "USD": {
        "JPY": 149.50,
        "EUR": 0.92,
        "GBP": 0.79
    },
    "JPY": {
        "USD": 0.0067,
        "EUR": 0.0061,
        "GBP": 0.0053
    }
}


@component
class CurrencyConverterTool:
    """Convert between currencies."""

    @component.output_types(conversion=Dict)
    def run(self, amount: float, from_currency: str, to_currency: str) -> Dict:
        """Convert currency.

        Args:
            amount: Amount to convert
            from_currency: Source currency code (e.g., "USD")
            to_currency: Target currency code (e.g., "JPY")

        Returns:
            Conversion result with rate and converted amount
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return {"conversion": {
                "amount": amount,
                "from": from_currency,
                "to": to_currency,
                "result": amount,
                "rate": 1.0
            }}

        rate = EXCHANGE_RATES.get(from_currency, {}).get(to_currency)

        if rate is None:
            return {"conversion": {
                "error": f"Exchange rate not available for {from_currency} to {to_currency}"
            }}

        result = amount * rate

        return {"conversion": {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "result": round(result, 2),
            "rate": rate
        }}
