import streamlit as st
import plotly.graph_objects as go

def plot_historical_and_projected_data(historical_data, projections):
    fig = go.Figure()

    # Datos históricos
    fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data['Ventas'],
                             mode='lines+markers', name='Ventas Históricas'))
    
    # Proyecciones
    fig.add_trace(go.Scatter(x=projections.index, y=projections['Ventas'],
                             mode='lines+markers', name='Ventas Proyectadas',
                             line=dict(dash='dash')))

    fig.update_layout(title='Ventas Históricas y Proyectadas',
                      xaxis_title='Año',
                      yaxis_title='Ventas')

    st.plotly_chart(fig)

def plot_valuation_metrics(historical_data, projections):
    fig = go.Figure()

    # Margen operativo histórico
    historical_margin = historical_data['Beneficio Operativo'] / historical_data['Ventas'] * 100
    fig.add_trace(go.Scatter(x=historical_data.index, y=historical_margin,
                             mode='lines+markers', name='Margen Operativo Histórico'))
    
    # Margen operativo proyectado
    projected_margin = projections['Beneficio Operativo'] / projections['Ventas'] * 100
    fig.add_trace(go.Scatter(x=projections.index, y=projected_margin,
                             mode='lines+markers', name='Margen Operativo Proyectado',
                             line=dict(dash='dash')))

    fig.update_layout(title='Margen Operativo Histórico y Proyectado',
                      xaxis_title='Año',
                      yaxis_title='Margen Operativo (%)')

    st.plotly_chart(fig)