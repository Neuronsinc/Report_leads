from cgitb import text
import datetime
from io import BytesIO
import math
import streamlit as st
import graphviz as graphviz
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.dml.color import RGBColor
from datetime import date
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

EFECTIVIDAD_BAJA = RGBColor(0xFF, 0x00, 0x00)
EFECTIVIDAD_MEDIA = RGBColor(0xFF,0xA5,0x00)
EFECTIVIDAD_ALTA = RGBColor(0x00, 0xFF, 0x00)

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

matriz_leads_citas = [[] for x in range(number_of_weeks)]


pages = 1 if number_of_weeks <= 3 else 2

col1, col2, col3 = st.columns(3)
col1.write("Numero de Leads")
col2.write("Citas Agendadas")
col3.write("Citas Realizadas")

curr_date = start_date
for i in range(number_of_weeks):
    col1.write(str(curr_date))
    col3.markdown('<p style="color:rgba(0, 0, 0, 0.5)">.</p>', unsafe_allow_html=True)
    if(curr_date + datetime.timedelta(days = 6) > today_date):
        dates.append(curr_date.strftime('%d/%m/%Y') + '-' +  today_date.strftime('%d/%m/%Y'))
        col2.write(today_date.strftime('%d/%m/%Y'))
    else:
        dates.append(curr_date.strftime('%d/%m/%Y') + ' - ' + (curr_date + datetime.timedelta(days = 7)).strftime('%d/%m/%Y'))
        col2.write(str(curr_date + datetime.timedelta(days = 6)))
        curr_date = curr_date + datetime.timedelta(days = 7)
    #numero_leads.append(int(col1.text_input("",value="0",key="Lead" + str(i))))
    #numero_agendada.append(int(col2.text_input("",value="0",key="citaA" + str(i))))
    #numero_realizada.append(int(col3.text_input("",value="0",key="citaR" + str(i))))'''

    matriz_leads_citas[i].append(col1.number_input("",value=0,key="Lead" + str(i), min_value=0))
    matriz_leads_citas[i].append(col2.number_input("",value=0,key="citaA" + str(i), min_value=0))
    matriz_leads_citas[i].append(col3.number_input("",value=0,key="citaR" + str(i), min_value=0))

st.write(matriz_leads_citas)

column1, column2 = st.columns(2)
with column1:
    '''
    ## Datos del mes actual
    '''

    actual_leads = int(st.text_input(value=0, label="Numero de leads mes actual"))
    actual_agendada = int(st.text_input(value=0, label="Numero de citas agendadas mes actual"))
    actual_realizada = int(st.text_input(value=0,label="Numero de citas realizadas mes actual"))

with column2:
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

efectividades = [[] for x in range(number_of_weeks)]

efectividad_agendada = []
efectividad_realizada = []
color_ef_agendada = []
color_ef_realizada = []
for i in range(number_of_weeks):
    if(all(x > 0 for x in matriz_leads_citas[i])):
        efectividad_agendada = round(matriz_leads_citas[i][1] / matriz_leads_citas[i][0], 4) * 100
        efectividad_realizada = round(matriz_leads_citas[i][2] / matriz_leads_citas[i][1], 4)* 100
        if(efectividad_agendada < 7):
            efectividades[i].append([format(efectividad_agendada,'.2f'), EFECTIVIDAD_BAJA])
        elif(efectividad_agendada >= 7 and efectividad_agendada < 10):
            efectividades[i].append([format(efectividad_agendada,'.2f'), EFECTIVIDAD_MEDIA])
        elif(efectividad_agendada >= 10):
            efectividades[i].append([format(efectividad_agendada,'.2f'), EFECTIVIDAD_ALTA])

        if(efectividad_realizada < 5):
            efectividades[i].append([format(efectividad_realizada,'.2f'), EFECTIVIDAD_BAJA])
        elif(efectividad_realizada >= 5 and efectividad_realizada < 6):
            efectividades[i].append([format(efectividad_realizada,'.2f'), EFECTIVIDAD_MEDIA])
        elif(efectividad_realizada >= 6):
            efectividades[i].append([format(efectividad_realizada,'.2f'), EFECTIVIDAD_ALTA])



        def srt(grp):
            sort_shape = grp.shapes[0]
            print(sort_shape)
            if sort_shape.has_text_frame:
                return sort_shape.text

        prs = Presentation('test.pptx')
        for slide in prs.slides:
            group_shapes = [
                shape for shape in slide.shapes
                if shape.shape_type == MSO_SHAPE_TYPE.GROUP
            ]
            group_shapes.sort(key=srt)
            for group_shape in group_shapes:
                i = int(group_shape.shapes[0].text) - 1
                group_shape.shapes[0].text = ''
                group_shape.shapes[0].text = dates[i]               
                j = 0
                k = 0
                for oval in [shape for shape in group_shape.shapes if shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and shape.auto_shape_type == MSO_SHAPE.OVAL]:
                    oval.text = ''
                    p = oval.text_frame.paragraphs[0]
                    p.alignment = PP_ALIGN.CENTER
                    run = p.add_run()
                    run.text = str(matriz_leads_citas[i][j])
                    font = run.font
                    print(oval.text)
                    j = j+1

                for textbox in [shape for shape in group_shape.shapes if shape.shape_type == MSO_SHAPE_TYPE.TEXT_BOX and shape != group_shape.shapes[0]]:
                    textbox.text = ''
                    print(textbox.text)
                    p = textbox.text_frame.paragraphs[0]
                    p.alignment = PP_ALIGN.CENTER
                    run = p.add_run()
                    run.text = efectividades[i][k][0]
                    font = run.font
                    font.color.rgb = efectividades[i][k][1]
                    print(textbox.text)
                    k = k+1

                print('---------')


        binary_output = BytesIO()
        prs.save(binary_output) 

        st.download_button( 

            label = 'Download ppw',
            data = binary_output.getvalue(),

            file_name='reporte_' + date.today().strftime("%d_%m_%Y") + '.pptx',

            mime='application/vnd.openxmlformats-officedocument.presentationml.presentation',

        )



'''
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
        graph.node('7', label=str(numero_leads[2]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('8', label=str(numero_agendada[2]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('9', label=str(numero_realizada[2]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.edge('7', '8', label=str(format(efectividad_agendada[2],'.2f')) + '%', fontcolor=color_ef_agendada[2])
        graph.edge('8', '9', label=str(format(efectividad_realizada[2],'.2f')) + '%', fontcolor=color_ef_realizada[2])
        graph.node(dates[2], shape='plaintext', style="", fontcolor="black")
        

        graph.node('4', label=str(numero_leads[1]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('5', label=str(numero_agendada[1]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('6', label=str(numero_realizada[1]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.edge('4', '5', label=str(format(efectividad_agendada[1], '.2f')) + '%', fontcolor=color_ef_agendada[1])
        graph.edge('5', '6', label=str(format(efectividad_realizada[1],'.2f')) + '%', fontcolor=color_ef_realizada[1])
        graph.node(dates[1], shape='plaintext', style="", fontcolor="black")

        
        graph.node('1', label=str(numero_leads[0]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('2', label=str(numero_agendada[0]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.node('3', label=str(numero_realizada[0]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
        graph.edge('1', '2', label=str(format(efectividad_agendada[0],'.2f')) + '%', fontcolor=color_ef_agendada[0])
        graph.edge('2', '3', label=str(format(efectividad_realizada[0],'.2f')) + '%', fontcolor=color_ef_realizada[0])
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
                graph6.node('1', label=str(numero_leads[3]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
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
                grap.node('1', label=str(numero_leads[4]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
                grap.node('2', label=str(numero_agendada[4]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
                grap.node('3', label=str(numero_realizada[4]), fontsize="12", fontcolor="black", shape="circle", style='filled', fillcolor='#FFD14C', color="#FFD14C")
                grap.edge('1', '2', label=str(format(efectividad_agendada[4],'.2f')) + '%', fontcolor=color_ef_agendada[4])
                grap.edge('2', '3', label=str(format(efectividad_realizada[4],'.2f')) + '%', fontcolor=color_ef_realizada[4])
                grap.node(dates[3], shape='plaintext', style="", fontcolor="black")

              
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
            if(precio_lead_actual >= 0 and precio_lead_pasado >= 0 and precio_lead_actual != None):
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
'''