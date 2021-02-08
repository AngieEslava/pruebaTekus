import streamlit as st
import pandas as pd
import os
import sys
from os import listdir
from os.path import isfile, isdir, join
from datetime import datetime, timedelta
from pandas import DataFrame
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import interact
from scipy import stats
import numpy as np
from pandas.plotting import scatter_matrix

#data = pd.read_csv('data.csv')
print('hecho')


@st.cache
def load_data():
    data = pd.read_csv('data.csv')
    return data
data = load_data()

@st.cache
def load_dcity():
    df_city =  pd.read_csv("ciudades.csv")
    return df_city
df_city = load_dcity()


nav_link = st.sidebar.radio(" ", ("Descripción", "Análisis Exploratorio de Datos", "Top 10 por Ciudades", "Top 10 por Producto", "Top Horario"))

if nav_link == "Descripción":
    st.write("""
    ### Prueba Técnica Data Scient
    
    """)
    st.write('El análisis de datos realizado al problema paso por las fases ETL, que corresponden a extraer, transformar y cargar los datos para ser presentados. Los datos que venian en un archivo zip fueron organizados en una sola base de datos que reflejaba todos los datos correspondientes a la información de las olla y se cruzaron posteriormente con los datos de la base de datos de SQL Server que contenia la información de las ciudades, formando asi el Data warehouse analizado.  ')
    
    st.write('Todos los cálculos correspondientes a los resultados presentados se pueden encontrar en el siguiente repositorio y en google colab  ')
    st.write('*Angie Eslava*')


elif nav_link == "Análisis Exploratorio de Datos":
    st.title(" Análisis Exploratorio de Datos")
    st.write('Para el análisis exploratorio de datos es importante tener muy en cuenta las variables y sus significados como se muestran a continuación:')
    
    st.write('**MovementInteractions:** Indica la cantidad de veces que movieron la olla' )
    st.write('**ArkboxInteractions:** Indica la cantidad de veces que el usuario interactuó con el extraordinario panel de un solo botón')
    st.write('**Duration:** Describe la duración en segundos de la interacción que tuvo el usuario con la olla.')
    st.write('**MovementDuration:** Indica la duración en segundos del movimiento que registró la olla')



    st.write('## Diagrama de flujo de datos')
    st.image('./DiagramaFlujoDatos.JPG')
    st.write('El diagrama de flujo de datos representa como se realiza la captación de datos del producto. Según lo planteado el usuario al interactuar con el panel de un solo botón y al mover la olla, genera la información por fecha, hora, referencia y localización principalmente')


    df = pd.merge(left = data, right = df_city, left_on='Key', right_on='Key')
    df = df.drop(['idCity'],axis=1)
    df.ArkboxInteractions = pd.to_numeric(df.ArkboxInteractions)
    df.Duration = pd.to_numeric(df.Duration)
    df.MovementDuration = pd.to_numeric(df.MovementDuration)
    df.MovementInteractions = pd.to_numeric(df.MovementInteractions)

    st.write('### Descripción Estadística de Datos')
    st.write(df.describe())
    st.write('El análisis descriptivo de los datos muestra varias interpretaciones interesantes de las variables a analizar, por ejemplo, en la variable __ArkboxInteractions__ vemos que la media de los datos es de 167.53 veces, lo que nos diría que en promedio el usuario interactuó con el panel de control 167 veces según la medición, pero viendo la mediana en el cuartil 50 el valor es 24 veces lo que quiere decir que el 50% de los datos están por debajo de ese valor y que el valor máximo de los datos de esa variable es de 164863 interacciones el cual es bastante mayor a la media registrada, e incluso el 75% de los datos estan en un valor menor a 120 veces por lo cual no es recomendable tomar decisiones con base a los valores promedios de las variables y si proceder a analizar los outliers que pueden reflejar información valiosa sobre el comportamiento del negocio.')
    st.write('Realizando el mismo tipo de análisis sobre los cuartiles de los datos, para las variables como __MovementDuration__ y __MovementInteractions__ vemos que en el cuartil 50 los datos tenen el valor de cero y en el cuartil 75 de los datos se empiezan a ver valores como 5 y 1 respectivamente, saltando a un valor máximo bastante alejado de estos valores. Esto quiere decir que prácticamente el valor de 0 es lo que explicaría un comportamiento normal de los datos, reflejando también la importancia del valor cero en cada variable. Por tanto, si la mayoría de registros de la variable __MovementInteractions__ es cero quiere decir que las ollas no se mueven mucho y si los registros de __MovementDuration__ tambien son cero nos muestra que no hay duración de esos movimientos.')

    # arreglos para ejes de las gráficas
    key = df.loc[:, 'Key'] 
    key.drop_duplicates(inplace=True)
    ciudad = df.loc[:, 'City'] 
    ciudad.drop_duplicates(inplace=True)

    st.write('En esta gráfica se puede seleccionar en la lista desplegable la variable que se desea analizar por cada referencia y ver sus valores correspondientes. ')

    vble = st.selectbox(
     'Seleccionar variable: ',
     ('MovementInteractions','ArkboxInteractions',
                 'Duration',
                 'MovementDuration'))
    st.write(' ', vble)

    def grafico_1(vble):
        sns.catplot(x="Key", y=vble, data=df).fig.set_size_inches(25,5) # Tomado de : https://stackoverflow.com/questions/33446029/how-to-change-a-figures-size-in-python-seaborn-package
        plt.xticks([r for r in range(len(key))] , key, rotation = 'vertical')#https://seaborn.pydata.org/generated/seaborn.catplot.html
    # Tomado de : https://jdvelasq.github.io/courses/notebooks/aexp/01-tecnicas-estadisticas-para-exploracion-de-datos.html
    st.pyplot(grafico_1(vble))

    st.write('Para la variable **MovementInteractions** que nos indica la cantidad de veces que movieron la olla, vemos claramente que los datos se concentran en su gran mayoria en valores muy cercanos al cero con excepción de la referencia **[1e8656...]** con puntos de color verde en la que se ve como los valores crecen hasta mas o menos 800 interacciones y lo mismo para la referencia **[02a5d1...]** donde se ve también una concentración importante de interacciones que llega hasta el valor máximo de 1620 interacciones.')
    st.write('En la variable **ArkboxInteractions** que nos muestra la cantidad de interacciones del usuario con el panel, a pesar de que se ve una concentración muy alta en 0, los datos empiezan a distribuirse en mas referencias en un rango un poco mas amplio, por lo cual vemos la importancia del panel un poco mas marcada en mas referencias y mostrando una gran cantidad de interacciones en la referencia **[31c0afa...]**.')
    st.write('Las variables **Duration** y **MovementDuration** muestran una distribución de datos altas en la referencia **[318c42...]** de color azul, esto nos indica que los movimientos registrados y la interaccion con el panel tienen una duración mayor en esta referencia.')
    st.write('Analizando las referencias con mayor cantidad de datos registrados para las variables observadas, se puede llegar a formar un segmento de productos potenciales de acuerdo la usabilidad que le dan los usuarios a dichas referencias y también se podría dar una utilidad mayor si se concentran los esfuerzos en la comercialización de estas referencias mas que en las otras.')

    st.write('Ahora veamos cada variable por ciudad.')

    vble = st.selectbox(
     'Seleccionar variable: ',
     ('Duration','ArkboxInteractions',
                 'MovementDuration',
                 'MovementInteractions'))
    st.write(' ', vble)
    def grafico_1(vble):
        sns.catplot(x="City", y=vble, data=df).fig.set_size_inches(15,5) # Tomado de : https://stackoverflow.com/questions/33446029/how-to-change-a-figures-size-in-python-seaborn-package
        plt.xticks([r for r in range(len(ciudad))] , ciudad, rotation = 'vertical')
    st.pyplot(grafico_1(vble))


    st.write('Al entrar a analizar las variables por ciudad vemos que las variables **Duration** y **MovementDuration** registraron mayores duraciones, tanto de interacción como de movimiento, en ciudades como Medellín, Murillo, Barranquilla y Cartagena, con lo cual se podría entrar a explorar que usos mas específicos le dan los clientes a la olla en esas ciudades, como por ejemplo restaurantes, negocios o si es doméstico, que condiciones asociadas están a los clientes que hacen uso de la olla.')
    st.write('Otras ciudades que se resaltan por su uso en la cantidad de interacciones son Cartagena e Itagui con la cantidad de interacciones y la cantidad de movimientos registrados respectivamente entonces también es importante considerarlas en los análisis.')

    st.write('#### Gráficas de Dispersion de todas las variables')

    sm = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    st.pyplot()

    st.write('#### Matriz de Correlación')
    df.corr()
    st.write(df.corr())

    st.write('Hay dos variables que estan altamente correlacionadas que son tales las cuales son MovementDuration y Duration las demás variables presentan muy bajo porcentaje de correlacion.')

    vbleb = st.selectbox(
     'Seleccionar variable: ',
     ('ArkboxInteractions',
                 'Duration',
                 'MovementDuration',
                 'MovementInteractions'))
    st.write(' ', vbleb)
    def grafico_1(vbleb):
        data.boxplot(column=[vbleb])
    st.pyplot(grafico_1(vbleb))


    st.write('Se puede ver en los boxplot la distribución de los datos por cada variable, teniendo en cuenta que un gran porcentaje de los datos es cero lo que se apreciaria en la grafica como datos atípicos seria la representación de la distribución de los datos que quedan, por eso es interesante ver en esta gráfica como los datos atípicos de magnitud cobran gran relevancia para cada una de las variables.')

    df = pd.DataFrame({
    'Variable': ['MovementInteractions','ArkboxInteractions',
                    'Duration',
                    'MovementDuration'
                    ],
    'Significado': ['62.07%', '29.74%', '0.26%', '65.64%']
        })
    st.write('El procentaje de ceros que se encuentran en los datos es muy alto, en la variable **MovementInteractions** que hace referencia a la cantidad de veces que movieron la olla corresponde a un 62.07% y la variable **MovementDuration** que indica la duración en segundos del movimiento de la olla corresponde a un 65.64% lo que indicaría que la mayoría de las ollas no se estan moviendo.')
    st.write('En ese orden de ideas para las otras variables que hacen referencia a la duración de la interaccion del cliente con el paner de un solo botón y a la cantidad de veces que se presenta esta interacción, **Duration** presenta un porcentaje de ceros del 0.27% y **ArkboxInteractions** tiene un porcentaje de ceros del 29.75% lo cual puede ser un indicio de que los clientes interactuan mas con el panel de un solo botón a diferencia de mover la olla.')


elif nav_link == 'Top Horario':
    st.write('# ¿Cuáles son los horarios entre semana y fines de semana en dónde se presentan más desplazamientos de ollas?')
    st.write('### Resultados entre semana')

    data_f = data.copy(deep=False)
    data_f.Date = pd.to_datetime(data_f.Date)
    data_f.Fecha = pd.to_datetime(data_f.Fecha)

    data_semana = data_f[data_f['Date'].apply(lambda x: x.weekday()) < 5]
    data_semana.Date = data_semana['Date'].apply(lambda x: x.strftime('%H'))
    data_semana.groupby('Date').sum().MovementInteractions.plot(kind='bar',color = 'coral')
    st.pyplot()
    st.write('El horario entre semana que presenta una mayor cantidad de movimientos son las 21 horas o 9 pm, también se ve como empiezan a incrementar la cantidad de movimientos desde las dos de la tarde, lo que nos da un indicio del comportamiento de la gente con el uso de la olla con lo que se podrían plantear automatizaciones horarias para las funcionalidades de la olla en un futuro cercano si se complementa con información cualitativa sobre las necesidades de los clientes.')
   
    st.write('### Resultados fin de semana')
    data_finsemana = data_f[data_f['Date'].apply(lambda x: x.weekday()) >= 5]
    data_finsemana.Date = data_finsemana['Date'].apply(lambda x: x.strftime('%H'))
    data_finsemana.groupby('Date').sum().MovementInteractions.plot(kind='bar',color = 'aqua')
    st.pyplot()
    st.write('En el fin de semana el pico mas alto de desplazamientos se ve a las 20 horas u 8 de la noche, lo cual no es muy alejado del horario que se tenia entre semana con una distinción de una hora de diferencia en el horario de mayor uso. En este caso los otros horarios con mayor uso de la olla son a las 10 pm y a las 4 pm, muy contrario al uso entre semana donde se veia que era a las 2pm.')

elif nav_link == 'Top 10 por Ciudades':
    st.write('# ¿Cuál es el top 10 de las ciudades con más movimientos registrados por los usuarios?')
    top_city =  pd.merge(left = data, right = df_city, left_on='Key', right_on='Key')
    top_city = top_city.groupby('City').sum().sort_values('MovementInteractions', ascending=False).head(10)
    top_city
    st.write('El top de las ciudades que registraron la mayor cantidad de movimientos esta encabezado por Cartagena con 66631 cantidad de movimientos de acuerdo a esto y al conteo que se habia realizado por ciudad con cada variable, Cartagena representa una oportunidad de mercado que puede ser aprovechable en cuanto se incrementen los esfuerzos por incentivar estrategias de mercadeo en esta ciudad. Además Murillo, Medellín, Nuquí y Bello que son parte del Top cinco de ciudades, también son puntos potenciales para estrategias de mercadeo haciendo una caracterización de la zona y de los clientes.')   

    top_city.MovementInteractions.plot(kind = 'bar', color='darkturquoise')
    plt.show() 
    st.pyplot()

    st.write('### Top de las ciudades por cada variable')
    vblec = st.selectbox(
     'Seleccionar variable: ',
     ('ArkboxInteractions',
                 'Duration',
                 'MovementDuration',
                 'MovementInteractions'))
    st.write(' ', vblec)
    def grafico_1(vblec):
        top_city[vblec].plot(kind = 'bar', color='mediumvioletred')
        plt.show()
    st.pyplot(grafico_1(vblec))

elif nav_link == "Top 10 por Producto":
    st.write('# ¿Cuál es el top 10 de las ollas con más interacciones de los usuarios con el extraordinario panel interactivo de un solo botón?')
    top_olla = data.groupby('Key').sum()
    top_olla = top_olla.sort_values(by=['ArkboxInteractions'], ascending=[False]).head(10)
    top_olla

    vbled = st.selectbox(
     'Seleccionar variable: ',
     ('ArkboxInteractions',
                 'Duration',
                 'MovementDuration',
                 'MovementInteractions'))
    st.write(' ', vbled)
    def grafico_1(vbled):
        top_olla[vbled].plot(kind = 'bar', color='mediumspringgreen')
        plt.show()
    st.pyplot(grafico_1(vbled))
    st.write('Las interacciones que mas se han registrado corresponden a la referencia **[115c61b...]** y en segundo lugar a la referencia **[02a5d1c...]** por lo cual, es recomendable entrar analizar cuales son las características que tienen estas referencias y potencializarlas, para concentrar los esfuerzos en vender estas referencias o combinar las mejores caracteristicas de ambas. ')
    st.write('Para un análisis mas completo podria mirarse la relación de estas ollas con las ventas para poder definir si tomar la decisión de unificar algunos productos y quitar otros de la comercialización, puesto que en la usabilidad final del usuario muestra que las referencias donde mas se usa el panel interactivo son estas, las demás podrían eliminarse el inventario para no incurrir en otros costos que afectan en general al negocio.')


