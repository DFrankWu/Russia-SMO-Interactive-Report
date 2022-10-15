import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import pydeck as pdk
import os
from helper import load_data, convert_to_csv, read_image_url

dir_path = os.path.dirname(os.path.realpath(__file__))
# Pre-plotting
st.title(':ru: Special Military Operation Report')

equipment_monthly_data = load_data(dir_path + '/datasets/monthly_cummulative_loss_count.csv').reset_index(drop=True)
equipment_value_data = load_data(dir_path + '/datasets/cummulative_loss_value.csv').reset_index(drop=True)
city_data = load_data(dir_path + '/datasets/most_contested_city.csv').reset_index(drop=True)
people_data = load_data(dir_path + '/datasets/smo_people_loss.csv').reset_index(drop=True)
## Loading complete ##

# Intro image and background audio
intro_image = Image.open(dir_path + '/assets/intro.png')
st.image(intro_image, caption='Graphical art by Max Butterworth / NBC News')
with open(dir_path + '/assets/radio.mp3', 'rb') as audio_file:
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

st.subheader(':flag-ua: The Battlefields and Affected Population :man-woman-girl-boy:')
battle_image = Image.open(dir_path + '/assets/city.png')
refugee_image = Image.open(dir_path + '/assets/refugee.png')
st.image(battle_image, caption='Picture by PATRICK TOMBOLA')
st.image(refugee_image, caption='Picture from internet')

st.markdown('**Hexagon:** affected population')
st.markdown('**Circle**: center of battle')
# Heat of Battle map
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=48.5,
        longitude=36,
        zoom=5,
        pitch=40,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=city_data,
           get_position='[Lon, Lat]',
           get_elevation='Population_Proper',
           radius=20000,
           elevation_scale=100,
           elevation_range=[400, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=city_data,
            get_position='[Lon, Lat]',
            get_color='[200, 30, 0, 160]',
            get_radius='Frequency',
            radius_scale=2000,
        ),
    ],
))




column_list = ['Aircraft', 'Helicopter', 'Tank', 'Apc', 'Field Artillery', 'Mrl', 'Anti-Aircraft Warfare', 'Military Auto', 'Drone','Naval Ship'] 
# Selectbox for different plot
st.subheader(':ru: Military Equipment Loss')
equipment_image = Image.open(dir_path + '/assets/equipment.png')
st.image(equipment_image, caption='Picture by Reuters')


graph_choice = st.selectbox(
        'Which graph do you want to see?',
        ("Equipment Loss Value by Month", "Monthly Equipment Loss Count")
    )


# Monthly Value loss areaplot 
if graph_choice == "Equipment Loss Value by Month":
    st.subheader(':ru: Russian Military Equipment Loss Value by Month :warning:')
    col1, col2, col3, col4, col5 = st.columns(5)
    col6, col7, col8, col9, col10 = st.columns(5)

    col_list = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10]
    select_list = []
    for i in range(10):
        with col_list[i]:
            temp_name = column_list[i]
            value_box = st.checkbox(temp_name)
            if value_box:
                select_list.append(temp_name)
    st.area_chart(data=equipment_value_data, x='Date', y=select_list)

# Monthly equipment loss count (barplot)
elif graph_choice == "Monthly Equipment Loss Count":
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(column_list)
    tab_list = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10]
    emoji_list = [':small_airplane:', ':helicopter:' ,':steam_locomotive:', ':tractor:', ':gun:', ':rocket:', ':airplane_arriving:', ':railway_car:' , ':satellite:', ':motor_boat:']

    for i in range(10):
        with tab_list[i]:
            temp_name = column_list[i]
            st.subheader(f':ru: Number of {temp_name} Loss by Month {emoji_list[i]}')
            st.bar_chart(data=equipment_monthly_data, x='Date', y=temp_name)  




# Casualties lineplot
st.subheader(':ru: Russian Military Personnel Casualties by Day :skull_and_crossbones:')
start_day, end_day = st.slider(
    'Select Day Range', 
    2, 228, (2,228)
)
filtered_data = people_data[(people_data['Day'] >= start_day) & (people_data['Day'] <= end_day)]
st.line_chart(data=filtered_data, x='Day', y='Personnel')
last_day = people_data['Date'].dt.to_period('D').iloc[-1]
last_death_count = people_data['Personnel'].iloc[-1]
st.markdown(f' As of **{last_day}**, a **total** of ***{last_death_count}*** Russian personnels are **KIA**')
death_image = Image.open(dir_path + '/assets/death.png')
st.image(death_image, caption='Picture from Adobe Stock')



# Show raw data function
if st.checkbox('Show raw data'):
    option = st.selectbox(
        "Which raw data do you want to see?",
        ("Monthly Equipment Loss Count", "Montly Equipment Loss Value", "Most Contested Cities", "Daily Personnel Casualties")
    )
    st.write('You selected:', option)
    st.subheader('Raw data')
    if option == 'Monthly Equipment Loss Count':
        st.write(equipment_monthly_data)
        if st.checkbox('Do you want to download this data?'):
            csv = convert_to_csv(equipment_monthly_data)
            if st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name= f'{option}.csv',
                mime='text/csv'
            ):
                st.write('Data Downloaded!')
    elif option == 'Montly Equipment Loss Value':
        st.write(equipment_value_data)
        if st.checkbox('Do you want to download this data?'):
            csv = convert_to_csv(equipment_value_data)
            if st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name= f'{option}.csv',
                mime='text/csv'
            ):
                st.write('Data Downloaded!')
    elif option == 'Most Contested Cities':
        st.write(city_data)
        if st.checkbox('Do you want to download this data?'):
            csv = convert_to_csv(city_data)
            if st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name= f'{option}.csv',
                mime='text/csv'
            ):
                st.write('Data Downloaded!')
    elif option == 'Daily Personnel Casualties':
        st.write(people_data)
        if st.checkbox('Do you want to download this data?'):
            csv = convert_to_csv(people_data)
            if st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name= f'{option}.csv',
                mime='text/csv'
            ):
                st.write('Data Downloaded!')

# Peace quote
st.header('May Peace Prevail On Earth :dove_of_peace:')
st.caption('“Peace cannot be kept by force. It can only be achieved by understanding.” - Albert Einstein')

outro_image = Image.open(dir_path + '/assets/end.png')
st.image(outro_image, caption='Source: wallpapercave.com')

st.markdown('Original data provided by [Petro](https://www.kaggle.com/datasets/piterfm/2022-ukraine-russian-war) @ Kaggle.com')
st.markdown('Processed and cleaned by [Donghang Wu](https://github.com/DFrankWu), access raw data via [Kaggle](https://www.kaggle.com/datasets/xc1011/ukraine-russia-war-clean-datasets) ')
st.caption('*According to author, "main data sources are Armed Forces of Ukraine and Ministry of Defence of Ukraine. They gathered data from different points of the country. The calculation is complicated by the high intensity of hostilities."')