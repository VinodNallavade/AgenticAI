import streamlit as st
import time 
st.checkbox('Yes')

st.button('Click Me')
st.radio('Pick your gender', ['Male', 'Female'])
st.selectbox('Pick a fruit', ['Apple', 'Banana', 'Orange'])
st.multiselect('Choose a planet', ['Jupiter', 'Mars', 'Neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0, 50)

with st.container():    
    st.write("This is inside the container")
st.sidebar.title("Sidebar Title")
st.sidebar.markdown("This is the sidebar content")
st.sidebar.number_input('Pick a number', 0, 10)
st.sidebar.text_input('Email address')
st.sidebar.date_input('Traveling date')
st.sidebar.time_input('School time')
st.sidebar.text_area('Description')
st.sidebar.file_uploader('Upload a photo')
st.sidebar.color_picker('Choose your favorite color')


st.success("You did it!")
st.error("Error occurred")
st.warning("This is a warning")
st.info("It's easy to build a Streamlit app")
st.exception(RuntimeError("RuntimeError exception"))


st.balloons()  # Celebration balloons
st.snow()
st.progress(90)  # Progress bar
with st.spinner('Wait for it...'):    
    time.sleep(10)  # Simulating a process delay


