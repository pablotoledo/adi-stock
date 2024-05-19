from financials.models import FinancialData

def insert_financial_data(financial_data, ticker_symbol):
    for date, data in financial_data.iterrows():
        FinancialData.objects.update_or_create(
            ticker=ticker_symbol,
            date=date,
            defaults={
                'total_revenue': data['Sales'],
                'ebitda': data['EBITDA'],
                'ebit': data['EBIT'],
                'interest_expense': data['Interest Expense'],
                'pretax_income': data['Pretax Income'],
                'income_taxes': data['Income Taxes'],
                'net_income': data['Consolidated Net Income'],
                'diluted_eps': data['Diluted EPS'],
                'diluted_average_shares': data['Diluted Average Shares'],
                'yoy_growth': data['Y/Y Growth %'],
                'ebitda_margin': data['EBITDA Margin %'],
                'ebit_margin': data['EBIT Margin %'],
                'tax_rate': data['Tax Rate'],
                'net_margin': data['Net Margin %'],
            }
        )
