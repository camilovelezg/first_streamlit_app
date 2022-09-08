from xxlimited import foo
import streamlit
import pandas

streamlit.title("My parents healthy menu")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

food_df = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
food_df.set_index("Fruit")

streamlit.multiselect("Select some fruits", list(food_df.index))
streamlit.dataframe(food_df)