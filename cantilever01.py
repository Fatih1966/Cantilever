# Modules
# import pickle
# from pathlib import Path
import streamlit as st
# import streamlit_authenticator as stauth
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import pyrebase
# from datetime import datetime

def cantilever():
    st.title("Embedded Cantilever Retaining Walls by HFK - Method 01")

    st.image('Figure01.jpg', caption='Cross-Section of Embedded Retaining Wall for Input and Output')

    st.write("### Input Data")
    col1, col2,col3= st.columns(3)

    Depth_excavation=col1.number_input("Depth of Excavation (H)",min_value=0.0, step=0.1,value=4.0)
    Depth_embedment=col2.number_input("Depth of Embedment (D)",min_value=0.0, step=0.1,value=4.0)
    Surcharge_load=col3.number_input("Surcharge Pressure",min_value=0, value=0)

    soil01_unitweight=col1.number_input("Unit Weight of Soil 1",min_value=0.0, value=20.0)
    soil01_friction=col2.number_input("Internal Friction of Soil 1",min_value=0, value=35)
    soil01_wall_friction=col3.number_input("Wall Friction of Soil 1",min_value=0, value=20)

    soil02_unitweight=col1.number_input("Unit Weight of Soil 2",min_value=0.0, value=20.0)
    soil02_friction=col2.number_input("Internal Friction of Soil 2",min_value=0, value=35)
    soil02_wall_friction=col3.number_input("Wall Friction of Soil 2",min_value=0, value=20)

    # Calculation

    def kactive(f,l):
        k1=math.cos(l)/(1+math.sin(f))
        k2=math.cos(l)
        k3=(math.sin(f))**2-(math.sin(l))**2
        k4=math.asin(math.sin(l)/(math.sin(f)))-l
        k5=math.exp(-k4*math.tan(f))
        ka=(k1*(k2-k3**0.5))*k5
        return ka

    def kpassive(f,l):
        k1=math.cos(l)/(1-math.sin(f))
        k2=math.cos(l)
        k3=(math.sin(f))**2-(math.sin(l))**2
        k4=math.asin(math.sin(l)/(math.sin(f)))+l
        k5=math.exp(k4*math.tan(f))
        ka=(k1*(k2+k3**0.5))*k5
        return ka

    # Geometry
    H=Depth_excavation
    D=Depth_embedment

    # for soil 01
    f1_r=soil01_friction*np.pi/180
    d1_r=soil01_wall_friction*np.pi/180
    Ka1 = kactive(f1_r,d1_r)

    Kp1 = 1/Ka1
    g1=soil01_unitweight
    q=g1*H+Surcharge_load
    Sa=0.5*Ka1*q*H
    y1=(1/3)*H


    # for soil 02
    f2_r=soil02_friction*np.pi/180
    d2_r=soil02_wall_friction*np.pi/180
    Ka2 = kactive(f2_r,d2_r)
    Kp2 = kpassive(f2_r,d2_r)
    g2=soil02_unitweight
    Pa=Ka2*q
    a=Pa/(g2*(Kp2-Ka2))
    Sb=(a/2)*Pa

    s=(D-a)*Pa/a
    x1=s*(D-a)**2
    x2=Sa*(y1+D)
    x3=Sb*(D-a/3)
    x4=s*(D-a)
    x5=Sa+Sb
    x=D-(x1-6*(x2+x3))/(x4-2*x5)

    s1=g2*(Kp2-Ka2)*x-Pa

    z1=s*(D-a)
    z2=Sa+Sb
    z3=s*(D-a)**2
    z4=Sa*(y1+D)
    z5=Sb*(D-a/3)
    s2=((z1-2*z2)**2)/(z3-6*(z4+z5))-s

    slim=g2*(Kp2-Ka2)*D+Kp2*q

    st.write("###")
    st.write("### Output Data")

    st.write("##### Critical Values")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Limiting Soil Pressure", value=f"{slim:,.0f}")
    col2.metric(label="Depth X", value=f"{x:,.2f}")
    col3.metric(label="Soil Pressure (sigma1) at Depth X", value=f"{s1:,.0f}")
    col4.metric(label="Soil Pressure (sigma2) at Depth D", value=f"{s2:,.0f}")

    st.write("###### Requirement 1 - Soil Pressure (sigma2) at Depth D < Limiting Soil Pressure ")
    st.write("###### Requirement 2 - Depth X < Depth D ")

    # Calculate Shear and Moment with Depth below Excavation Level
    Shear=[]
    Moment=[]
    i=0
    for i in range(20):
        z=(i)*D/20
        if z < x:
            T=0.5*g2*(Kp2-Ka2)*z**2+Pa*z+Sa
            M=(-1/6)*g2*(Kp2-Ka2)*z**3+0.5*Pa*(z**2)+Sa*(y1+z)
        else:
            T=((s1+s2)/(D-x))*((z-x)**2)/2-s1*(z-x)+Sa+Sb-0.5*s1*(x-a)
            M=((s1+s2)/(D-x))*((z-x)**3)/6-s1*((z-x)**2)/2+Sa*(y1+z)+Sb*(z-(1/3)*a)-0.5*s1*(x-a)*(z-(2/3)*x-(1/3)*a)
        Shear.append(T)
        Moment.append(M)
        i=i+1
    Shear.append(0)
    Moment.append(0)

    # Create a data-frame with the payment schedule.
    section_forces = []

    for i in range(0, 21):
        z=(i)*D/20
        shear=Shear[i]
        moment=Moment[i]
        section_forces.append(
            [
                i,
                z,
                shear,
                moment,
            ]
        )

    df = pd.DataFrame(
        section_forces,
        columns=["No","Depth", "Shear", "Moment"],
    )

    # Display the data-frame as a chart.
    st.write("### Sectional Forces")

    forces_df = df[["No","Depth","Shear", "Moment",]].groupby("No").min()
    st.dataframe(forces_df.map("{:,.1f}".format))



    # st.line_chart(forces_df)

    chart_data = pd.DataFrame(forces_df, columns=["Depth","Shear", "Moment"])

    st.line_chart(chart_data,x="Depth",color=["#f0f", "#04f"], use_container_width=True)

# # --- USER AUTHENTICATION ---
# names = ["Fatih Kulac","Sinan Kulac"]
# usernames=["fkulac","skulac"]
# # load hashed passwors
# file_path=Path(__file__).parent/"hashed_pw.pk1"
# with file_path.open("rb") as file:
#     hashed_passwords=pickle.load(file)


# authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"sales_dashboard", "abcdef", cookie_expiry_days=30)



# name,authentication_status,username = authenticator.login("Login","main")



# authenticator.logout("Logout","main")

# if authentication_status == False:
#     st.error("Username/password is incorrect")

# if authentication_status == None:
#     st.warning("Please enter your username and password")

# if authentication_status:

    # st.sidebar.title(f"Welcome {name}")



# # --- USER AUTHENTICATION ---

# Configuartion Key
firebaseConfig = {
  'apiKey': "AIzaSyAWoeU7jrcz2iJWUHUQpOfKa-W7TI-uQFE",
  'authDomain': "cantilever-f038d.firebaseapp.com",
  'projectId' : "cantilever-f038d",
  'storageBucket': "cantilever-f038d.appspot.com",
  'databaseURL' : "https://cantilever-f038d-default-rtdb.europe-west1.firebasedatabase.app/",
  'messagingSenderId': "842228941349",
  'appId': "1:842228941349:web:66fe01f52468cc2c84f5cc",
  'measurementId': "G-HS27WBF5MK"
}

# Firebase Authentication
firebase=pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db=firebase.database()
storage = firebase.storage()

st.sidebar.title("Cantilever Wall")

# Authentication

choice = st.sidebar.selectbox('Login/Signup',['Login','Sign up'])

try:
  email=st.sidebar.text_input('Please enter your email address')
  password=st.sidebar.text_input('Please enter your password')


  if choice =='Sign up':
      submit=st.sidebar.button('Create my account')
      if submit:
          user = auth.create_user_with_email_and_password(email,password)
          st.success('Your account is created successfully')
          user = auth.sign_in_with_email_and_password(email,password)
          db.child(user['localId']).child("ID").set(user['localId'])
          st.title('Welcome  '+email)
          st.info('Login now via login drop down')

  if choice=='Login':
      login=st.sidebar.checkbox('Login')
      if login:
          user=auth.sign_in_with_email_and_password(email,password)
          st.title('Welcome  '+email)
          cantilever()
except Exception as e:
    st.error(str(e))


