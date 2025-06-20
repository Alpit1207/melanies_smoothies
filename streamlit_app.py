# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be", name_on_order)

cnx = st.connection(
    "sf_conn",                   # connection name
    type="snowflake",
    account="PZPPRIU-DS44040",
    user="alpitstudent2025",
    password="0*AlpitGoyal*0",
    role="SYSADMIN",
    warehouse="COMPUTE_WH",
    database="SMOOTHIES",
    schema="PUBLIC"
)
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON')
                                                                      )
# st.dataframe(data=my_dataframe, use_container_width=True)
#  convert the snowpark dataframe to a pandas dataframe so we use the loc function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()   

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = smoothiefroot_response.json()
        st.dataframe(data=sf_df, use_container_width=True)
        # st.stop()



    my_insert_stmt = """insert into smoothies.public.orders(ingredients,name_on_order)
    values('"""+ ingredients_string +"""', '""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")  
