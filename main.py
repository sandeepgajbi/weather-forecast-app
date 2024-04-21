import streamlit as st
import plotly.express as px
from backend import get_data

# Title and user input
st.title("Weather Forecast for the Next Days")
place = st.text_input('Place')
days = st.slider('Forecast Days', min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox('Select the data to view', ('Temperature', 'Sky'))

# Display weather data based on user selection
st.subheader(f"{option.title()} for next {days} days in {place.title()}")

if place:
    if option == "Temperature":
        # Fetch and display temperature data
        date, data = get_data(place=place, forecast_day=days, kind=option)
        figure = px.line(x=date, y=data, labels={"x": "Dates", "y": "Temperature (C)"})
        st.plotly_chart(figure)
    elif option == "Sky":
        # Fetch and display sky data
        date, data = get_data(place=place, forecast_day=days, kind=option)
        image_urls = [f"images/{item.lower()}.png" for item in data]
        st.image(image_urls, caption=date, width=100)
