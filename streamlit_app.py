import streamlit
import snowflake.connector

import requests
import pandas


streamlit.title("My parents healthy menu")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_cursor = snowflake.connector.connect(**streamlit.secrets["snowflake"]).cursor()
my_cursor.execute("select * from fdc_food_ingest limit 15")
my_secret_data = my_cursor.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_secret_data)

fruits_df = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruits_df = fruits_df.set_index("Fruit")


streamlit.header('FruityVice Menu')
fruit_selection = streamlit.text_input("Which fruit do you want to search", "kiwi")
streamlit.text(f'The user selected {fruit_selection}')
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_selection}")
fruitvice_df = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruitvice_df)


selected_fruits = streamlit.multiselect("Select some fruits", list(fruits_df.index))
fruits_to_show = fruits_df.loc[selected_fruits]
streamlit.dataframe(fruits_to_show)