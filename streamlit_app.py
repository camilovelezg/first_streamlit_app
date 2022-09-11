import requests
import pandas
from urllib.error import URLError

import streamlit
import snowflake.connector

def get_fruityvice_df(selected_fruit):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{selected_fruit}")
    return pandas.json_normalize(fruityvice_response.json())

def get_snowflake_data(connection):
    streamlit.header("The fruit list contains:")
    with connection.cursor() as cursor:
        return cursor.execute("select * from fruit_load_list").fetchall()

def add_fruits(connection, new_fruits):
    streamlit.text(f"Thank you for adding {new_fruits}")
    with connection.cursor() as cursor:
        new_fruits = new_fruits.split(",")
        query = ''
        for fruit in new_fruits:
            query += f"({fruit.strip()}),"
        query = query[:-1]
        streamlit.text(query)
        streamlit.text("insert into fruit_load_list (fruit_name) values %(query)s", {'query': query})
        cursor.execute("insert into fruit_load_list (fruit_name) values %(query)s", {'query': query})


streamlit.title("My parents healthy menu")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

new_fruits = streamlit.text_input("Which fruits would you like to add?", "")
if streamlit.button("Add fruits"):
    snowflake_connection = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    add_fruits(snowflake_connection, new_fruits)
    snowflake_connection.close()

if streamlit.button("Get fruit list"):
    snowflake_connection = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.dataframe(get_snowflake_data(snowflake_connection))
    snowflake_connection.close()

fruits_df = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruits_df = fruits_df.set_index("Fruit")


streamlit.header('FruityVice Menu')
try:
    fruityvice_selection = streamlit.text_input("Which fruit do you want to search")
    if not fruityvice_selection:
       streamlit.error('Please selecet a fruit')
    else: 
        streamlit.text(f'The user selected {fruityvice_selection}')  
        streamlit.dataframe(get_fruityvice_df(fruityvice_selection))
except URLError as e:
    streamlit.error(e)



selected_fruits = streamlit.multiselect("Select some fruits", list(fruits_df.index))
fruits_to_show = fruits_df.loc[selected_fruits]
streamlit.dataframe(fruits_to_show)