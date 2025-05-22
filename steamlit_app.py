# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want.
  """
)

#option = st.selectbox(
#    "What is your favorite Fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite Fruit is:", option)





cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name on Order")
st.write("Name on Smoothie will be:", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 Ingredients:', my_dataframe,max_selections=5)

#st.dataframe(data=my_dataframe, use_container_width=True)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen
      st.sunheader(fruit_chosen + ' Nutrition')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df=st.dataframe(date=smoothiefroot_response.json(),use_container_width=true)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """' )"""

    st.write(my_insert_stmt)
    st.stop

    
    time_to_insert = st.button('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")







