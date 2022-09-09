from urllib import request
import requests
import streamlit
import pandas

streamlit.title("My parents healthy menu")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

fruits_df = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
fruits_df = fruits_df.set_index("Fruit")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.header('FruityVice Menu')
streamlit.text(fruityvice_response.json())
selected_fruits = streamlit.multiselect("Select some fruits", list(fruits_df.index))
fruits_to_show = fruits_df.loc[selected_fruits]
streamlit.dataframe(fruits_to_show)