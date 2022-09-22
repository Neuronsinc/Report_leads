from cgitb import text
import datetime
import math
import streamlit as st
import graphviz as graphviz

st.set_page_config(layout="wide")
st.title("Creación de Reportes Sobre Leads y Efectividad de Citas")


numero_leads = []
numero_agendada = []
numero_realizada = []
dates = []

primer_dia_mes = datetime.date.today().replace(day=1)

start_date = st.date_input("Ingrese fecha inicial:")

today_date = datetime.date.today()
days = abs(today_date-start_date).days

number_of_weeks = math.ceil(days/7)

pages = 1 if number_of_weeks <= 3 else 2

col1, col2, col3 = st.columns(3)
col1.write("Numero de Leads")
col2.write("Citas Agendadas")
col3.write("Citas Realizadas")

curr_date = start_date
for i in range(number_of_weeks):
    col1.write(str(curr_date))
    col3.markdown('<p style="color:rgba(0, 0, 0, 0.5)">.</p>', unsafe_allow_html=True)
    if(curr_date + datetime.timedelta(days = 7) > today_date):
        dates.append(curr_date.strftime('%d/%m/%Y') + '-' +  today_date.strftime('%d/%m/%Y'))
        col2.write(today_date.strftime('%d/%m/%Y'))
    else:
        dates.append(curr_date.strftime('%d/%m/%Y') + ' - ' + (curr_date + datetime.timedelta(days = 7)).strftime('%d/%m/%Y'))
        col2.write(str(curr_date + datetime.timedelta(days = 7)))
        curr_date = curr_date + datetime.timedelta(days = 7)
    numero_leads.append(int(col1.text_input("",value="0",key="Lead" + str(i))))
    numero_agendada.append(int(col2.text_input("",value="0",key="citaA" + str(i))))
    numero_realizada.append(int(col3.text_input("",value="0",key="citaR" + str(i))))

'''
## Datos del mes pasado
'''

pasado_leads = int(st.text_input(value=0, label="Numero de leads mes pasado"))
pasado_agendada = int(st.text_input(value=0, label="Numero de citas agendadas mes pasado"))
pasado_realizada = int(st.text_input(value=0,label="Numero de citas realizadas mes pasado"))

'''
## Otros
'''
precio_lead_actual = int(st.text_input(value=0,label="Precio por lead mes actual"))
precio_lead_pasado = int(st.text_input(value=0,label="Precio por lead mes pasado"))

efectividad_agendada = []
efectividad_realizada = []
color_ef_agendada = []
color_ef_realizada = []
for i in range(number_of_weeks):
    if(numero_agendada[i] > 0 and numero_leads[i] > 0 and numero_realizada[i] > 0):
        efectividad_agendada.append(round(numero_agendada[i] / numero_leads[i], 4) *100)
        efectividad_realizada.append(round(numero_realizada[i] / numero_agendada[i], 4)*100)
        
        if(efectividad_agendada[i] < 7):
            color_ef_agendada.append("red")
        elif(efectividad_agendada[i] >= 7 and efectividad_agendada[i] < 10):
            color_ef_agendada.append("orange")
        elif(efectividad_agendada[i] >= 10):
            color_ef_agendada.append("green")

        if(efectividad_realizada[i] < 5):
            color_ef_realizada.append("red")
        elif(efectividad_realizada[i] >= 5 and efectividad_realizada[i] < 6):
            color_ef_realizada.append("orange")
        elif(efectividad_realizada[i] >= 6):
            color_ef_realizada.append("green")

if(len(numero_leads) > 0 and len(numero_agendada) > 0 and len(numero_realizada) > 0 and len(efectividad_agendada) > 0 and len(efectividad_realizada) > 0):
   with st.container():

    col1, col2 = st.columns([5, 2], gap="large")
    with col1:
    # Create a graphlib graph object
        graph = graphviz.Digraph(
            graph_attr={'rankdir':'LR'},
            node_attr={
                'width':'1',
                'fontsize': '8',
                'style':'filled',
                'shape': 'circle',
                'fontcolor':'white',
                'fixedsize': 'false'
            },
            edge_attr={'weight':'1'}
        )
        graph.node('1', label=str(numero_leads[0]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#85A0FE', color="#85A0FE")
        graph.node('2', label=str(numero_agendada[0]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('3', label=str(numero_realizada[0]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.edge('1', '2', label=str(format(efectividad_agendada[0],'.2f')) + '%', fontcolor=color_ef_agendada[0])
        graph.edge('2', '3', label=str(format(efectividad_realizada[0],'.2f')) + '%', fontcolor=color_ef_realizada[0])
        graph.node(dates[2], shape='plaintext', style="", fontcolor="black")


        graph.node('4', label=str(numero_leads[1]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#85A0FE', color="#85A0FE")
        graph.node('5', label=str(numero_agendada[1]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('6', label=str(numero_realizada[1]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.edge('4', '5', label=str(format(efectividad_agendada[1], '.2f')) + '%', fontcolor=color_ef_agendada[1])
        graph.edge('5', '6', label=str(format(efectividad_realizada[1],'.2f')) + '%', fontcolor=color_ef_realizada[1])
        graph.node(dates[1], shape='plaintext', style="", fontcolor="black")

        graph.node('7', label=str(numero_leads[2]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#85A0FE', color="#85A0FE")
        graph.node('8', label=str(numero_agendada[2]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('9', label=str(numero_realizada[2]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.edge('7', '8', label=str(format(efectividad_agendada[2],'.2f')) + '%', fontcolor=color_ef_agendada[2])
        graph.edge('8', '9', label=str(format(efectividad_realizada[2],'.2f')) + '%', fontcolor=color_ef_realizada[2])


        graph.node(dates[0], shape='plaintext', style="", fontcolor="black")

        graph.node('Leads', shape='plaintext', style="", fontcolor="black")
        graph.node('Citas Agendadas', shape='plaintext', style="", fontcolor="black")
        graph.node('Citas Realizadas', shape='plaintext', style="", fontcolor="black")
        graph.edge('Leads', 'Citas Agendadas', style="invis")
        graph.edge('Citas Agendadas', 'Citas Realizadas', style="invis")
        st.graphviz_chart(graph)
    

    total_leads = sum(numero_leads)
    total_agendada = sum(numero_agendada)
    total_realizada = sum(numero_realizada)

    if(total_leads > 0 and total_agendada > 0 and total_realizada > 0):
            ef_ag_total = total_agendada / total_leads
            ef_re_total = total_realizada / total_agendada
            
            if(ef_ag_total < 7):
                color_final_ag = "red"
            elif(ef_ag_total >= 7 and ef_ag_total < 10):
                color_final_ag="orange"
            elif(ef_ag_total >= 10):
                color_final_ag="green"

            if(ef_re_total < 5):
                color_final_re = "red"
            elif(ef_re_total >= 5 and ef_re_total < 6):
                color_final_re = "orange"
            elif(ef_re_total >= 6):
                color_final_re = "Green"

            with col2:
                graph2 = graphviz.Digraph(
                    node_attr={
                        'height': '1',
                        'width': '1.5',
                        'shape': 'box',
                        'fontsize': '8',
                        'style': 'filled',
                        'color': '#85A0FE',
                        'fixedsize': 'true',
                        'fontcolor': 'white',
                        'fillcolor': '#85A0FE'
                    }
                )   
                graph2.node('1', label=str(total_leads), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                graph2.node('2', label=str(total_agendada), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                graph2.node('3', label=str(total_realizada), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                graph2.node('MES ACTUAL', shape='plaintext', style="", fontcolor="black", height="", width="")
                graph2.edge('MES ACTUAL', '1', style="invis")
                graph2.edge('1', '2', label=str(format(ef_ag_total*100, '.2f')) + '%', fontcolor=color_final_ag)
                graph2.edge('2', '3', label=str(format(ef_re_total*100, '.2f')) + '%', fontcolor=color_final_re)

                st.graphviz_chart(graph2)


    if(number_of_weeks > 3):
        if(number_of_weeks >= 4):
            with col1:
                graph6 = graphviz.Digraph(
                graph_attr={'rankdir':'LR'},
                node_attr={
                    'width':'1',
                    'fontsize': '8',
                    'style':'filled',
                    'shape': 'circle',
                    'fontcolor':'white',
                    'fixedsize': 'false'
                },
                edge_attr={'weight':'1'}
                )
                # Create a graphlib graph2 object
                graph6.node('1', label=str(numero_leads[3]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                graph6.node('2', label=str(numero_agendada[3]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
                graph6.node('3', label=str(numero_realizada[3]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
                graph6.edge('1', '2', label=str(format(efectividad_agendada[3],'.2f')) + '%', fontcolor=color_ef_agendada[3])
                graph6.edge('2', '3', label=str(format(efectividad_realizada[3],'.2f')) + '%', fontcolor=color_ef_realizada[3])
                graph6.node(dates[3], shape='plaintext', style="", fontcolor="black")

                graph6.node('Leads', shape='plaintext', style="", fontcolor="black")
                graph6.node('Citas Agendadas', shape='plaintext', style="", fontcolor="black")
                graph6.node('Citas Realizadas', shape='plaintext', style="", fontcolor="black")
                graph6.edge('Leads', 'Citas Agendadas', style="invis")
                graph6.edge('Citas Agendadas', 'Citas Realizadas', style="invis")
                st.graphviz_chart(graph6)




        if(number_of_weeks == 5):
            with col1:
                grap = graphviz.Digraph(
                graph_attr={'rankdir':'LR'},
                node_attr={
                    'width':'1',
                    'fontsize': '8',
                    'style':'filled',
                    'shape': 'circle',
                    'fontcolor':'white',
                    'fixedsize': 'false'
                },
                edge_attr={'weight':'1'}
                )
                # Create a graphlib graph2 object
                grap.node('1', label=str(numero_leads[4]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                grap.node('2', label=str(numero_agendada[4]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
                grap.node('3', label=str(numero_realizada[4]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
                grap.edge('1', '2', label=str(format(efectividad_agendada[4],'.2f')) + '%', fontcolor=color_ef_agendada[4])
                grap.edge('2', '3', label=str(format(efectividad_realizada[4],'.2f')) + '%', fontcolor=color_ef_realizada[4])
                grap.node(dates[3], shape='plaintext', style="", fontcolor="black")

                grap.node('Leads', shape='plaintext', style="", fontcolor="black")
                grap.node('Citas Agendadas', shape='plaintext', style="", fontcolor="black")
                grap.node('Citas Realizadas', shape='plaintext', style="", fontcolor="black")
                grap.edge('Leads', 'Citas Agendadas', style="invis")
                grap.edge('Citas Agendadas', 'Citas Realizadas', style="invis")
                st.graphviz_chart(grap)

        total_leads = sum(numero_leads)
        total_agendada = sum(numero_agendada)
        total_realizada = sum(numero_realizada)

        if(total_leads > 0 and total_agendada > 0 and total_realizada > 0):
            ef_ag_total = total_agendada / total_leads
            ef_re_total = total_realizada / total_agendada
            
            if(ef_ag_total < 7):
                color_final_ag = "red"
            elif(ef_ag_total >= 7 and ef_ag_total < 10):
                color_final_ag="orange"
            elif(ef_ag_total >= 10):
                color_final_ag="green"

            if(ef_re_total < 5):
                color_final_re = "red"
            elif(ef_re_total >= 5 and ef_re_total < 6):
                color_final_re = "orange"
            elif(ef_re_total >= 6):
                color_final_re = "Green"
            with col2:
                st.markdown("#")
                st.markdown("#")
                st.markdown("###")
                graph2 = graphviz.Digraph(
                node_attr={
                    'height': '1',
                    'width': '1.5',
                    'shape': 'box',
                    'fontsize': '8',
                    'style': 'filled',
                    'color': '#85A0FE',
                    'fixedsize': 'true',
                    'fontcolor': 'white',
                    'fillcolor': '#85A0FE'
                }
            )   
                graph2.node('1', label=str(total_leads), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                graph2.node('2', label=str(total_agendada), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                graph2.node('3', label=str(total_realizada), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
                graph2.node('MES ACTUAL', shape='plaintext', style="", fontcolor="black", height="", width="")
                graph2.edge('MES ACTUAL', '1', style="invis")
                graph2.edge('1', '2', label=str(format(ef_ag_total*100, '.2f')) + '%', fontcolor=color_final_ag)
                graph2.edge('2', '3', label=str(format(ef_re_total*100, '.2f')) + '%', fontcolor=color_final_re)

                st.graphviz_chart(graph2)


        

with st.container():

  col1, col2, col3 = st.columns(3, gap="large")

  with col1:
    if(pasado_agendada > 0 and pasado_leads > 0 and pasado_realizada > 0):
        graphanterior = graphviz.Digraph(
        node_attr={
            'height': '1',
            'width': '1.3',
            'shape': 'box',
            'fontsize': '8',
            'style': 'filled',
            'color': '#FE839C',
            'fixedsize': 'true',
            'fontcolor': 'white',
            'fillcolor': '#FE839C'
        }
        )
        
        graphanterior.node('1', label=str(pasado_leads), fontsize="12", fontcolor="black", shape="box", style='filled')
        graphanterior.node('2', label=str(pasado_agendada), fontsize="12", fontcolor="black", shape="box", style='filled')
        graphanterior.node('3', label=str(pasado_realizada), fontsize="12", fontcolor="black", shape="box", style='filled')
        graphanterior.node('MES ANTERIOR', shape='plaintext', style="", fontcolor="black", height="", width="")
        graphanterior.edge('MES ANTERIOR', '1', style="invis")
        graphanterior.edge('1', '2', label=str(format((pasado_agendada/pasado_leads)*100, '.2f')) + '%', fontcolor=color_final_ag)
        graphanterior.edge('2', '3', label=str(format((pasado_realizada/pasado_agendada)*100, '.2f')) + '%', fontcolor=color_final_re)

        st.graphviz_chart(graphanterior)
    if(total_leads > 0 and total_agendada > 0 and total_realizada > 0):
        with col2:
            graph2 = graphviz.Digraph(
                node_attr={
                    'height': '1',
                    'width': '1.5',
                    'shape': 'box',
                    'fontsize': '8',
                    'style': 'filled',
                    'color': '#85A0FE',
                    'fixedsize': 'true',
                    'fontcolor': 'white',
                    'fillcolor': '#85A0FE'
                }
            )   
            graph2.node('1', label=str(total_leads), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
            graph2.node('2', label=str(total_agendada), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
            graph2.node('3', label=str(total_realizada), fontsize="12", fontcolor="black", shape="box", style='filled', fillcolor='#85A0FE', color="#85A0FE")
            graph2.node('MES ACTUAL', shape='plaintext', style="", fontcolor="black", height="", width="")
            graph2.edge('MES ACTUAL', '1', style="invis")
            graph2.edge('1', '2', label=str(format(ef_ag_total*100, '.2f')) + '%', fontcolor=color_final_ag)
            graph2.edge('2', '3', label=str(format(ef_re_total*100, '.2f')) + '%', fontcolor=color_final_re)

            st.graphviz_chart(graph2)
    if(precio_lead_actual > 0 and precio_lead_pasado > 0):
        with col3:
            graph = graphviz.Digraph(
            graph_attr={'rankdir':'LR'},
            edge_attr={
                'style':'invis'
            }
            )
            graph.node('5', label=str(precio_lead_pasado), shape="box", style="filled", width="2", color='#FE839C', fillcolor="#FE839C")
            graph.node('4', label='Costo por lead:', shape="plaintext", height="0.01", width="")
            graph.node('3', label='', shape="plaintext", width="")
            graph.node('2', label=str(precio_lead_actual), shape="box", style="filled", width="2", color='#85A0FE', fillcolor="#85A0FE")
            graph.node('1', label='Costo por lead:', shape="plaintext", height="0.01", width="")
            # graph.edge('1', '2')
            # graph.edge('2', '3')
            # graph.edge('3', '4')

            st.graphviz_chart(graph)