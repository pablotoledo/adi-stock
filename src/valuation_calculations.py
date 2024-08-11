import pandas as pd
import numpy as np

def calculate_valuation(historical_data, years, growth_rate, operating_margin, tax_rate):
    last_year = historical_data.index[-1]
    last_year_data = historical_data.loc[last_year]
    
    # Convert last_year to integer
    start_year = last_year.year + 1
    end_year = start_year + years
    
    projections = pd.DataFrame(index=range(start_year, end_year))
    
    # Proyectar ventas
    projections['Ventas'] = last_year_data['Ventas'] * (1 + growth_rate/100) ** (projections.index - start_year + 1)
    
    # Proyectar beneficio operativo
    projections['Beneficio Operativo'] = projections['Ventas'] * operating_margin / 100
    
    # Proyectar impuestos
    projections['Impuestos'] = projections['Beneficio Operativo'] * tax_rate / 100
    
    # Calcular beneficio neto
    projections['Beneficio Neto'] = projections['Beneficio Operativo'] - projections['Impuestos']
    
    # Calcular flujo de caja libre (simplificado)
    projections['FCF'] = projections['Beneficio Neto']
    
    return projections

def calculate_intrinsic_value(projections, discount_rate=10):
    fcf = projections['FCF']
    terminal_value = fcf.iloc[-1] * (1 + 0.02) / (discount_rate/100 - 0.02)  # Asumiendo crecimiento perpetuo del 2%
    
    present_values = fcf / (1 + discount_rate/100) ** np.arange(1, len(fcf)+1)
    intrinsic_value = present_values.sum() + terminal_value / (1 + discount_rate/100) ** len(fcf)
    
    return intrinsic_value