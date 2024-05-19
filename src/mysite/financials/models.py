from django.db import models

class FinancialData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    ebitda = models.DecimalField(max_digits=15, decimal_places=2)
    ebit = models.DecimalField(max_digits=15, decimal_places=2)
    interest_expense = models.DecimalField(max_digits=15, decimal_places=2)
    pretax_income = models.DecimalField(max_digits=15, decimal_places=2)
    income_taxes = models.DecimalField(max_digits=15, decimal_places=2)
    net_income = models.DecimalField(max_digits=15, decimal_places=2)
    diluted_eps = models.DecimalField(max_digits=15, decimal_places=2)
    diluted_average_shares = models.DecimalField(max_digits=15, decimal_places=2)
    yoy_growth = models.DecimalField(max_digits=5, decimal_places=2)
    ebitda_margin = models.DecimalField(max_digits=5, decimal_places=2)
    ebit_margin = models.DecimalField(max_digits=5, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    net_margin = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = (('ticker', 'date'),)
        indexes = [
            models.Index(fields=['ticker', 'date']),
        ]

    def __str__(self):
        return f"{self.ticker} - {self.date}"
