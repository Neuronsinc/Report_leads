from cgitb import text
import datetime
import math
from turtle import textinput
import streamlit as st

st.set_page_config(initial_sidebar_state="expanded")

'''
## Ingrese la fecha inicial
'''

numero_leads = []
numero_agendada = []
numero_realizada = []

primer_dia_mes = datetime.date.today().replace(day=1)

start_date = st.date_input("Ingrese fecha inicial:")

today_date = datetime.date.today()
days = abs(today_date-start_date).days

number_of_weeks = math.ceil(days/7)
col1, col2, col3 = st.columns(3)
col1.write("Numero de Leads")
col2.write("Citas Agendadas")
col3.write("Citas Realizadas")

curr_date = start_date
for i in range(number_of_weeks):
    col1.write(str(curr_date))
    col3.markdown('<p style="color:rgba(0, 0, 0, 0.5)">.</p>', unsafe_allow_html=True)
    if(curr_date + datetime.timedelta(days = 7) > today_date):
        col2.write(str(today_date))
    else:
        col2.write(str(curr_date + datetime.timedelta(days = 7)))
        curr_date = curr_date + datetime.timedelta(days = 7)
    numero_leads.append(int(col1.text_input("",value="0",key="Lead" + str(i))))
    numero_agendada.append(int(col2.text_input("",value="0",key="citaA" + str(i))))
    numero_realizada.append(int(col3.text_input("",value="0",key="citaR" + str(i))))


for i in range(number_of_weeks):
    if(numero_agendada[i] > 0 and numero_leads[i] > 0 and numero_realizada[i] > 0):
        efectividad_agendada = numero_agendada[i] / numero_leads[i]
        efectividad_realizada = numero_realizada[i] / numero_agendada[i]
        if(efectividad_agendada < 0.07 or numero_agendada[i] == 0):
            new_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Red</p>'
        elif(efectividad_agendada >= 0.07 and efectividad_agendada < 0.1):
            new_title = '<p style="font-family:sans-serif; color:Orange; font-size: 42px;">Orange</p>'
        elif(efectividad_agendada >= 0.1):
            new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Green</p>'
        st.markdown(new_title, unsafe_allow_html=True)

        if(efectividad_realizada < 0.05 or numero_realizada[i] == 0 ):
            new_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Red</p>'
        elif(efectividad_realizada >= 0.05 and efectividad_realizada < 0.6):
            new_title = '<p style="font-family:sans-serif; color:Orange; font-size: 42px;">Orange</p>'
        elif(efectividad_realizada >= 0.06):
            new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Green</p>'
        st.markdown(new_title, unsafe_allow_html=True)

'''
## Datos del mes pasado
'''

pasado_leads = int(st.text_input(value=0, label="Numero de leads mes pasado"))
pasado_agendada = int(st.text_input(value=0, label="Numero de citas agendadas mes pasado"))
pasado_realizada = int(st.text_input(value=0,label="Numero de citas realizadas mes pasado"))

'''
## Otros
'''
cl = int(st.text_input(value=0,label="a"))
cl2 = int(st.text_input(value=0,label="b"))


