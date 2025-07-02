import streamlit as se



se.title("AI Travel Agent")
se.subheader("AI Travel Agent Subheading")
se.header("AI Travel Agent Subheading")

se.columns()



location= se.selectbox("Please select Start Location :",["Mumbia","Pune","Hyderabed"])
se.write(f"Selected location : {location}")


is_bike = se.checkbox("Bike")
is_cab=se.checkbox("Cab")
if is_bike:
    se.write(f"Selected Mode of Transport : Bike")
elif is_cab :
    se.write("Selected Mode of Transport : Cab")
else:
    se.write("Please select mode of transport")   


selected_mode = se.radio("Please select transport ",["Cab","BUS","Auto"],horizontal=True)
se.write(selected_mode)   



