import requests
import pandas
from urllib.error import URLError

import streamlit
import snowflake.connector


streamlit.title("My parents healthy menu")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_cursor = snowflake.connector.connect(**streamlit.secrets["snowflake"]).cursor()
my_cursor.execute("select * from fruit_load_list")
my_snowflake_data = my_cursor.fetchall()
new_fruit = streamlit.text_input("Which fruit would you like to add?", "")
streamlit.text(f"Thank you for adding {new_fruit}")
# my_cursor.execute("insert into fruit_load_list (fruit_name) values(%(new_fruit)s)", {'new_fruit': new_fruit})
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_snowflake_data)

fruits_df = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruits_df = fruits_df.set_index("Fruit")


streamlit.header('FruityVice Menu')
try:
    fruityvice_selection = streamlit.text_input("Which fruit do you want to search", "kiwi")
    if not fruityvice_selection:
       streamlit.error('Please selecet a fruit')
    else: 
        streamlit.text(f'The user selected {fruityvice_selection}')
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruityvice_selection}")
        fruitvice_df = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruitvice_df)
except URLError as e:
    streamlit.error(e)



selected_fruits = streamlit.multiselect("Select some fruits", list(fruits_df.index))
fruits_to_show = fruits_df.loc[selected_fruits]
streamlit.dataframe(fruits_to_show)