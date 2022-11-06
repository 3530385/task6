import folium
import numpy as np
import pandas as pd
import streamlit as st
from model.analogs import get_analogs
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium


def add_analogs_to_map(df, map):
    analog, k_n = get_analogs(df)
    print(np.unique(analog[['lat', 'lng']].to_numpy()))
    for flat in np.unique(analog[['lat', 'lng']].to_numpy(), axis=0):
        folium.Marker(location=list(flat), icon=folium.Icon(color='red')).add_to(map)


st.title('По')
Cen = []
Kt = -0.045
Ka = -0.035
Ksk = -0.086
Kk = -0.02
Knb = -0.05
Kum = -0.026
Kc = -0.01

MP = st.sidebar.text_input('Местоположение')
KK = st.sidebar.text_input('Количество комнат')
CE = st.sidebar.text_input('Сегмент')
AD = st.sidebar.text_input('Этажность дома')
MT = st.sidebar.text_input('Материал стен')
data1 = {'Местоположение': [MP], 'Количество комнат': [KK],
         'Сегмент (Новостройка, современное жилье, старый жилой фонд)': [CE], 'Этажность дома': [AD],
         'Материал стен (Кипич, панель, монолит)': [MT]}
dfP = pd.DataFrame(data1)
st.write('Эталонный объект:')
st.dataframe(dfP)

# df = {'Местоположение': [MP],'Количество комнат': [KK], 'Сегмент (Новостройка, современное жилье, старый жилой фонд)': [CE], 'Этажность дома': [AD], 'Материал стен (Кирпич, панель, монолит)': [MT]}
df = dfP
uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    read_file = pd.read_csv(uploaded_file)
    # st.write(read_file)
    df = pd.DataFrame(read_file)
    kolvo = df.shape[0]

uploaded_files = st.sidebar.file_uploader("Choose a excel file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    ex = uploaded_file.name
    read_file = pd.read_excel(ex)
    # st.write(read_file)
    df = pd.DataFrame(read_file)
    kolvo = df.shape[0]

st.write('Аналоги')
df2 = df[df["Местоположение"].str.contains(MP) | df["Количество комнат"].astype(str).str.contains(KK)]
df2 = pd.DataFrame(df2)
kolvo = df2.shape[0]
st.dataframe(df2)

count = kolvo
# г. Москва ул. Ватутина д.9
i = 0
summu = 0
while i < kolvo:
    Cen.append(st.number_input('цена квартиры', key=i))
    summu = Cen[i] + summu
    i = i + 1
i = 0
kp = summu / kolvo
st.write(summu / kolvo)

if st.button('Рассчет стоимости эталонного объекта'):
    rp = kp * (1 + (Kt + Ka + Ksk + Kk + Knb + Kum + Kc))
    st.write('расчетная стоимость эталонного объека:  ' + str(rp))

geolocator = Nominatim(user_agent="INTA.py")
city = dfP.Местоположение[0].split(',', 1)
loc = city[1] + city[0]
location1 = geolocator.geocode(loc)
ndt = (location1.latitude, location1.longitude)
locationQ = [ndt[0], ndt[1]]
map = folium.Map(locationQ, zoom_start=16)
folium.Marker(location=locationQ, icon=folium.Icon(color='green')).add_to(map)
add_analogs_to_map(dfP,map)
st_data = st_folium(map, width=725)

st.write('Внесите поправки')
Fl = st.text_input('Этаж расположения')
Pl = st.text_input('Площадь квариты, кв.м')
Pk = st.text_input('Площадь кухни, кв.м')
NB = st.text_input('Наличие балкона/лоджии')
UM = st.text_input('Удаленность от метро')
CO = st.text_input('Состояние (без отделки, муниципальный ремонт, с современная отделка')
# df3 = {'Этаж расположения': [Fl],'Площадь квариты, кв.м': [Pl], 'Площадь кухни, кв.м': [Pk], 'Наличие балкона/лоджии': [NB],
# 'Удаленность от метро мин. пешком':[UM], 'Состояние (без отделки, муниципальный ремонт, с современная отделка)': [CO]}

new_row = {'Местоположение': [MP], 'Количество комнат': [KK],
           'Сегмент (Новостройка, современное жилье, старый жилой фонд)': [CE], 'Этажность дома': [AD],
           'Материал стен (Кипич, панель, монолит)': [MT],
           'Этаж расположения': [Fl], 'Площадь квариты, кв.м': [Pl], 'Площадь кухни, кв.м': [Pk],
           'Наличие балкона/лоджии': [NB],
           'Удаленность от метро мин. пешком': [UM],
           'Состояние (без отделки, муниципальный ремонт, с современная отделка)': [CO]}
if st.button('добавить элемент'):
    df2 = df2.append(new_row, ignore_index=True)
    kolvo = df2.shape[0]
    Dl = st.number_input('цена квариты')
    Cen.append(Dl)
    st.dataframe(df2)
    kolvo = df2.shape[0]
    rp = kp * (1 + (Kt + Ka + Ksk + Kk + Knb + Kum + Kc))
    st.write(rp)
if st.button('удалить элемент'):
    inda = st.number_input('индекс строки')
    df2 = df2.drop([int(inda)])
    kolvo = df2.shape[0]
    rp = kp * (1 + (Kt + Ka + Ksk + Kk + Knb + Kum + Kc))
    st.write(rp)
st.write(kolvo)
st.dataframe(df2)
# st.write('Формирование удельной стоимости с учетом поправок ')
# rach =  16,7*(1-0.045-0.035-0.086-0.02-0.05-0.026-0.01)
if st.button('Сохранить поправки ценообразующих факторов для всех элементов'):
    df2['Этаж расположения'] = Fl
    df2['Площадь квариты, кв.м'] = Pl
    df2['Площадь кухни, кв.м'] = Pk
    df2['Наличие балкона/лоджии'] = ''
    df2['Наличие балкона/лоджии'] = NB
    df2['Состояние (без отделки, муниципальный ремонт, с современная отделка'] = ''
    df2['Состояние (без отделки, муниципальный ремонт, с современная отделка'] = CO
    st.write('С учетом коррекции:')
    st.write(df2)
    st.write('Формирование удельной стоимости с учетом поправок ')
    rp = kp * (1 + (Kt + Ka + Ksk + Kk + Knb + Kum + Kc))
    st.dataframe(rp)
if st.button('Сохранить изменения для конкретного элемента пула'):
    numba = st.text_input('индекс строки')
    df2['Этаж расположения'][numba] = str(df2['Этаж расположения']) + Fl
    df2['Площадь квартиры, кв.м'][numba] = str(df2['Площадь квартиры, кв.м']) + Pl
    df2['Площадь кухни, кв.м'][numba] = str(df2['Площадь кухни, кв.м']) + Pk
    df2['Наличие балкона/лоджии'][numba] = ''
    df2['Наличие балкона/лоджии'][numba] = NB
    df2['Состояние (без отделки, муниципальный ремонт, с современная отделка)'][numba] = ''
    df2['Состояние (без отделки, муниципальный ремонт, с современная отделка)'][numba] = CO
    st.write('Формирование удельной стоимости с учетом поправок ')
    st.dataframe(df2)
    rp = kp * (1 + (Kt + Ka + Ksk + Kk + Knb + Kum + Kc))
    st.dataframe(rp)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


csv = convert_df(df2)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='tab.csv',
    mime='text/csv',
)
