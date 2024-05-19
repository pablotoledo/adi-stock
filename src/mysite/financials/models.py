from django.db import models

class FinancialData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    ebitda = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    ebit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    interest_expense = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pretax_income = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    income_taxes = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    net_income = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    diluted_eps = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    diluted_average_shares = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    yoy_growth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ebitda_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ebit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    net_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = (('ticker', 'date'),)
        indexes = [
            models.Index(fields=['ticker', 'date']),
        ]

    def __str__(self):
        return f"{self.ticker} - {self.date}"
