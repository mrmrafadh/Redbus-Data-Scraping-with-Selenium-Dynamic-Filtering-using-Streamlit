import streamlit as st
import mysql.connector as sql
import pandas as pd
from streamlit_option_menu import option_menu

add_sidebar = st.sidebar

mydb = sql.connect(host="localhost",
                   user="root",
                   password="root",
                   database= "redbus_data"
                  )
mycursor = mydb.cursor(buffered=True)




with add_sidebar:
    add_sidebar.title('Red Bus')
    add_sidebar.text('By Rafadh Rafeek')

    mycursor.execute(f'select DISTINCT depature from redbus_info_3')
    depature_loc = mycursor.fetchall()
    df_depature_loc = pd.DataFrame(depature_loc, columns=['from'])
    depature_location = add_sidebar.selectbox('From : ', df_depature_loc["from"],placeholder="From",index=None)

    mycursor.execute(f"SELECT DISTINCT destination FROM redbus_info_3 WHERE depature = '{depature_location}'")
    destination_loc = mycursor.fetchall()
    df_destination_loc = pd.DataFrame(destination_loc, columns=['destination'])
    destination = add_sidebar.selectbox('To : ', df_destination_loc["destination"],index=None,placeholder="To",key='Choose Destination')

    


    st.sidebar.header("Filters")

    st.sidebar.markdown("#### Order By Price")
    l_to_h = st.sidebar.radio("",["Lower To Higher","Higher To Lower"] ,key="low_high")
    
    st.sidebar.markdown("#### DEPARTURE TIME")
    dt_before_6am = st.sidebar.checkbox("Before 6 am", key="dt_before_6am")
    dt_6am_to_12pm = st.sidebar.checkbox("6 am to 12 pm", key="dt_6am_to_12pm")
    dt_12pm_to_6pm = st.sidebar.checkbox("12 pm to 6 pm", key="dt_12pm_to_6pm")
    dt_after_6pm = st.sidebar.checkbox("After 6 pm", key="dt_after_6pm")
    
    st.sidebar.markdown("#### BUS TYPES")
    bus_type_seater = st.sidebar.checkbox("SEATER", key="bus_type_seater")
    bus_type_sleeper = st.sidebar.checkbox("SLEEPER", key="bus_type_sleeper")
    bus_type_ac = st.sidebar.checkbox("AC", key="bus_type_ac")
    bus_type_nonac = st.sidebar.checkbox("NON AC", key="bus_type_nonac")
    
    st.sidebar.markdown("#### ARRIVAL TIME")
    at_before_6am = st.sidebar.checkbox("Before 6 am", key="at_before_6am")
    at_6am_to_12pm = st.sidebar.checkbox("6 am to 12 pm", key="at_6am_to_12pm")
    at_12pm_to_6pm = st.sidebar.checkbox("12 pm to 6 pm", key="at_12pm_to_6pm")
    at_after_6pm = st.sidebar.checkbox("After 6 pm", key="at_after_6pm")
    
    st.sidebar.markdown("#### STAR RATING")
    rating_3_plus = st.sidebar.checkbox("3+ Stars", key="rating_3_plus")
    rating_4_plus = st.sidebar.checkbox("4+ Stars", key="rating_4_plus")
    rating_5 = st.sidebar.checkbox("5 Stars", key="rating_5")



query = f"select bus_name,bus_type,departing_time,reaching_time,price,star_rating,seats_available,route_link,route_name from redbus_info_3 where depature = '{depature_location}' and destination = '{destination}' "

mycursor.execute(query)
depature_loc = mycursor.fetchall()
df_result = pd.DataFrame(depature_loc, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])

filtered_df=df_result.copy()


#--------------------------------------------------------------------------

 # Filter by departure time
if dt_before_6am:
    query = query + ' and HOUR(departing_time) < 6'
    mycursor.execute(query)
    depature_loc1 = mycursor.fetchall()
    filtered_df = pd.DataFrame(depature_loc1, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
    #filtered_df = filtered_df[pd.to_datetime(filtered_df["departing_time"]).dt.time < pd.to_datetime("06:00").time()]
if dt_6am_to_12pm:
    query = query + ' and HOUR(departing_time) >= 6 and HOUR(departing_time) < 12'
    mycursor.execute(query)
    depature_loc2 = mycursor.fetchall()
    filtered_df = pd.DataFrame(depature_loc2, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
                                
    #filtered_df = filtered_df[(pd.to_datetime(filtered_df["departing_time"]).dt.time >= pd.to_datetime("06:00").time()) & 
                                #(pd.to_datetime(filtered_df["departing_time"]).dt.time < pd.to_datetime("12:00").time())]
if dt_12pm_to_6pm:
    query = query + ' and HOUR(departing_time) >= 12 and HOUR(departing_time) < 18'
    mycursor.execute(query)
    depature_loc3 = mycursor.fetchall()
    filtered_df = pd.DataFrame(depature_loc3, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])

    #filtered_df = filtered_df[(pd.to_datetime(filtered_df["departing_time"]).dt.time >= pd.to_datetime("12:00").time()) & 
                                #(pd.to_datetime(filtered_df["departing_time"]).dt.time < pd.to_datetime("18:00").time())]
if dt_after_6pm:
    query = query + ' and HOUR(departing_time) >= 18'
    mycursor.execute(query)
    depature_loc1 = mycursor.fetchall()
    filtered_df = pd.DataFrame(depature_loc1, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
 
    #filtered_df = filtered_df[pd.to_datetime(filtered_df["departing_time"]).dt.time >= pd.to_datetime("18:00").time()]


#--------------------------------------------------------------------------

# Filter by bus type
if bus_type_seater:
    query = query + ' and bus_type LIKE "%Seater%"'
    mycursor.execute(query)
    bus_type1 = mycursor.fetchall()
    filtered_df = pd.DataFrame(bus_type1, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
    #     filtered_df = filtered_df[filtered_df["Bus Type"].str.contains(r'\bSEATER\b', case=False, regex=True)]
if bus_type_sleeper:
    query = query + ' and bus_type LIKE "%sleeper%"'
    mycursor.execute(query)
    bus_type1 = mycursor.fetchall()
    filtered_df = pd.DataFrame(bus_type1, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
    #     filtered_df = filtered_df[filtered_df["Bus Type"].str.contains(r'\bSLEEPER\b', case=False, regex=True)]
if bus_type_ac:
    query = query + ' and bus_type NOT LIKE "%NON%"'
    mycursor.execute(query)
    bus_type1 = mycursor.fetchall()
    filtered_df = pd.DataFrame(bus_type1, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
    #     filtered_df = filtered_df[filtered_df["Bus Type"].str.contains(r'\bA[./]?C\b', case=False, regex=True) & 
    #                               ~filtered_df["Bus Type"].str.contains(r'\bNON\b', case=False, regex=True)]
if bus_type_nonac:
    query = query + ' and bus_type LIKE "%NON%"'
    mycursor.execute(query)
    bus_type1 = mycursor.fetchall()
    filtered_df = pd.DataFrame(bus_type1, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
    #     filtered_df = filtered_df[filtered_df["Bus Type"].str.contains(r'\bNON AC\b', case=False, regex=True)]


#--------------------------------------------------------------------------

 # Filter by departure time
if at_before_6am:
    query = query + ' and HOUR(reaching_time) < 6'
    mycursor.execute(query)
    arr_time = mycursor.fetchall()
    filtered_df = pd.DataFrame(arr_time, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
    #filtered_df = filtered_df[pd.to_datetime(filtered_df["departing_time"]).dt.time < pd.to_datetime("06:00").time()]
if at_6am_to_12pm:
    query = query + ' and HOUR(reaching_time) >= 6 and HOUR(reaching_time) < 12'
    mycursor.execute(query)
    arr_time = mycursor.fetchall()
    filtered_df = pd.DataFrame(arr_time, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
                                
    #filtered_df = filtered_df[(pd.to_datetime(filtered_df["departing_time"]).dt.time >= pd.to_datetime("06:00").time()) & 
                                #(pd.to_datetime(filtered_df["departing_time"]).dt.time < pd.to_datetime("12:00").time())]
if at_12pm_to_6pm:
    query = query + ' and HOUR(reaching_time) >= 12 and HOUR(reaching_time) < 18'
    mycursor.execute(query)
    arr_time = mycursor.fetchall()
    filtered_df = pd.DataFrame(arr_time, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])

    #filtered_df = filtered_df[(pd.to_datetime(filtered_df["departing_time"]).dt.time >= pd.to_datetime("12:00").time()) & 
                                #(pd.to_datetime(filtered_df["departing_time"]).dt.time < pd.to_datetime("18:00").time())]
if at_after_6pm:
    query = query + ' and HOUR(reaching_time) >= 18'
    mycursor.execute(query)
    arr_time = mycursor.fetchall()
    filtered_df = pd.DataFrame(arr_time, columns=['bus_name','Bus Type','departing_time','reaching_time','price','star_rating','seats_available','route_link','route_name'])
 
    #filtered_df = filtered_df[pd.to_datetime(filtered_df["departing_time"]).dt.time >= pd.to_datetime("18:00").time()]


#--------------------------------------------------------------------------

# Filter by star rating
if rating_3_plus:
    filtered_df = filtered_df[filtered_df["star_rating"] >= 3]
if rating_4_plus:
    filtered_df = filtered_df[filtered_df["star_rating"] >= 4]
if rating_5:
    filtered_df = filtered_df[filtered_df["star_rating"] == 5]


#--------------------------------------------------------------------------

# order by price
if l_to_h == "Lower To Higher":
    filtered_df = filtered_df.sort_values(by=['price'], ascending=True)
else:
    filtered_df = filtered_df.sort_values(by=['price'], ascending=False)


#--------------------------------------------------------------------------
if not(depature_location and destination):
    st.warning('Please select a departure location and destination.')
elif filtered_df.empty:
    st.error('No busses found that match the given criteria.')
else:
    filtered_df.index += 1
    st.dataframe(filtered_df)

st.text('Total Number of Busses : ' + str(len(filtered_df)))