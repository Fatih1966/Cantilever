# Modules
# import pickle
# from pathlib import Path
import streamlit as st
# import streamlit_authenticator as stauth
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patheffects
import math
import numpy as np
# import firebase
# from dbCRUD import create
# from datetime import datetime
# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials
from crud import create_project,save_project_input,get_projects,get_project_data,delete_a_project



def project_create_browse(user):
    
    data_projects={}
    data_gen={}
    data_str={}
    data_soils=[]

    if "flag2" not in st.session_state:
        st.session_state["flag2"]=False


    if "create" not in st.session_state:
        st.session_state["create"]=True

    def session_reset(create):
        if create==False:
            st.session_state["create"]=True
    
    # st.stop()

    try:
        
        choice = st.selectbox('Create A New Project / Browse Existing Projects / Delete A Project',['Create A New Project','Browse Existing Projects','Delete A Project'],
                          on_change=session_reset,args=(st.session_state["create"],))
        if choice =='Create A New Project':
            # with st.form("Database"): 
            col1, col2= st.columns([2,1])
            with col1:
                project_file_name = st.text_input(
                        label="Enter A File Name",
                        max_chars=50,
                        # on_change=session_reset(st.session_state["create"]),
                        placeholder='Enter A Project File Name',
                        label_visibility='collapsed'
                )
            with col2:
                created_pressed=st.button("Create A Project File",help="Once clicked, a register with the project file name will be created in the database",type="primary",use_container_width=True)
                # created_pressed=st.checkbox("create")
                # st.warning("Enter A Project File Name and Press Enter to Apply")
            if created_pressed and st.session_state["create"] and project_file_name:
                data_gen,data_str,data_soils,st.session_state["flag2"]=create_project(user,project_file_name)
                if st.session_state["flag2"]==True:
                    st.session_state["create"]=False
            if st.session_state["create"]==False and st.session_state["flag2"]:
                data_gen,data_str,data_soils=get_project_data(user,project_file_name)
            if  project_file_name==False:
                st.warning("Enter A Project File Name and Press Enter to Apply")
                st.session_state["flag2"]=False



        # if choice =='Create A New Project' and st.session_state["created"]==False:
        #     data_gen,data_str,data_soils=get_project_data(user,project_file_name)
        #     flag2=True



        # if choice =='Create A New Project':
        #     project_file_name=st.text_input("Enter A Project File Name")
        #     if project_file_name and st.session_state["flag"]:
        #         data_gen,data_str,data_soils=create_project(user,project_file_name)
        #         st.session_state["flag"]=False
        #         if len(data_soils) !=0:
        #             flag2=True
        #     if project_file_name and st.session_state["flag"]==False:
        #         data_gen,data_str,data_soils=get_project_data(user,project_file_name)
        #         flag2=True
        #     else:
        #         st.warning("Enter A Project File Name and Press Enter to Apply")
        #         flag2=False

            # with st.form("Database"): 
            #     col1, col2= st.columns([2,1])
            #     with col1:
            #         # project_file_name=st.text_input(label="",max_chars=20,placeholder='Enter A Project File Name')
            #         project_file_name = st.text_input(
            #                 label="Enter A File Name",
            #                 max_chars=50,
            #                 placeholder='Enter A Project File Name',
            #                 label_visibility='collapsed'
            #         )
            #     with col2:
            #         created=st.form_submit_button("Create A Project File",help="Once clicked, a register with the project file name will be created in the database",type="primary",use_container_width=True)
            #     if project_file_name and created:

            #         if "created_state" not in st.session_state:
            #             st.session_state.created_state=False
            #         if created:
            #             st.session_state.created_state=True
            #             data_projects,data_gen,data_str,data_soils=create_project(user,project_file_name)
            #         flag=True
            #     else:
            #         st.warning("Enter A Project File Name")
                    

        if choice=="Browse Existing Projects":

            projects_name=get_projects(user)
            
            project_file_name=st.selectbox(label="Select A Project",options=projects_name,index=None,placeholder="Choose an option...")
            if project_file_name:
                data_gen,data_str,data_soils=get_project_data(user,project_file_name)
                st.warning(f"A Project ({project_file_name}) is Selected and Its Data is Populated")      
                st.session_state["flag2"]=True
            else:
                st.session_state["flag2"]=False
                st.warning("Select A Project")
         
        if choice=="Delete A Project":
            st.session_state["create"]=True
            st.session_state["flag2"]=False
            project_file_name=""
            projects_name=get_projects(user)
            project_file_name=st.selectbox(label="Select A Project",options=projects_name,index=None,placeholder="Choose an option...")
            if project_file_name:
                delete_a_project(user,project_file_name)
                st.warning(f"A Project ({project_file_name}) is Selected and deleted") 




        # if project_file_name:
        #     flag2=True
        #     return data_projects,data_gen,data_str,data_soils,flag2
        # else:
        #     st.warning("Enter or Select A Project File Name")

    except Exception as e:
        st.error(str(e))

    # st.write(choice,"     create= ",st.session_state["create"],"flag2= ",st.session_state["flag2"],"project file name= ",project_file_name)
    # st.write(data_gen,data_str,data_soils)   

    return data_gen,data_str,data_soils,st.session_state["flag2"]



def input_data(data_gen,data_str,data_soils):
    Unit_Weight=[]
    Internal_Friction=[]
    Wall_Friction=[]
    data_soils_input=[]

    # st.write(int(data_str["Surcharge_load"]))

    project_file_name=data_gen["project_file_name"]
    project_title=st.text_input("### Enter A Project Title : ",value=data_gen["project_title"])
    col1, col2,col3= st.columns(3)

    Depth_excavation=col1.number_input("Excavation Depth (H)",min_value=0.0,step=0.1,value=float(data_str["Depth_excavation"]))
    Depth_embedment=col2.number_input("Embedment Depth (D)",min_value=0.0,step=0.1,value=float(data_str["Depth_embedment"]))
    Surcharge_load=col3.number_input("Surcharge Pressure (q)",min_value=0,step=1,value=int(data_str["Surcharge_load"]))

    for counter in range(1,3):
        unit_weight=col1.number_input(f"Unit Weight(\u03B3 {counter})",min_value=0., step=0.1,value=float(data_soils[counter-1][f"Unit_Weight{counter}"]))
        
        internal_friction=col2.number_input(f"Internal Friction(\u03C6 {counter})",min_value=0.,step=0.5, value=float(data_soils[counter-1][f"Internal_Friction{counter}"]))
        wall_friction=col3.number_input(f"Wall Friction(\u03B4 {counter})",min_value=0.,step=0.5, value=float(data_soils[counter-1][f"Wall_Friction{counter}"]))
        Unit_Weight.append(unit_weight)
        Internal_Friction.append(internal_friction)
        Wall_Friction.append(wall_friction)


    data_gen={"project_file_name":project_file_name,"project_title":project_title}
    data_str={"project_file_name":project_file_name,"Depth_excavation":Depth_excavation,"Depth_embedment":Depth_embedment,"Surcharge_load":Surcharge_load}

    for counter in range(1,3):
        data_soil_layer={"project_file_name":project_file_name,f"Unit_Weight{counter}":Unit_Weight[counter-1],f"Internal_Friction{counter}":Internal_Friction[counter-1],f"Wall_Friction{counter}":Wall_Friction[counter-1]}
        data_soils_input.append(data_soil_layer)
    
    return data_gen,data_str,data_soils_input

    
def cantilever(user):
    try:

        # Application Default credentials are automatically created.
        # Use the application default credentials.
        # cred = credentials.ApplicationDefault()

        # firebase_admin.initialize_app(cred)
        # db1 = firestore.client()

        # st.title("Embedded Cantilever Wall")

        st.write("### File Management")
        
    
        data_gen1,data_str1,data_soils1,flag2=project_create_browse(user)


        # st.write(project_file_name)

        if flag2:
                
            st.write("### Input Data") 
            st.image('Figure01rev01.tif', caption="Cross-Section")

            data_gen,data_str,data_soils=input_data(data_gen1,data_str1,data_soils1)
        
            updated=st.button("Update & Save Project File",help="At Every Click, Input Data will be Updated and Saved in the Project File Register",
                              type="primary", use_container_width=True)
        
            if updated:
                save_project_input(user,data_gen,data_str,data_soils)

            
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
            H=data_str.get("Depth_excavation")
            D=data_str.get("Depth_embedment")
            Surcharge_load=data_str.get("Surcharge_load")


            # for soil 01
            f1_r=data_soils[0].get("Internal_Friction1")*np.pi/180
            d1_r=data_soils[0].get("Wall_Friction1")*np.pi/180
            Ka1 = kactive(f1_r,d1_r)


            Kp1 = 1/Ka1
            g1=data_soils[0].get("Unit_Weight1")
            q=g1*H+Surcharge_load
            Sa=0.5*Ka1*(q+Surcharge_load)*H
            y1=(1/3)*H*(q+2*Surcharge_load)/(Surcharge_load+q)



            # for soil 02
            f2_r=data_soils[1].get("Internal_Friction2")*np.pi/180
            d2_r=data_soils[1].get("Wall_Friction2")*np.pi/180
            Ka2 = kactive(f2_r,d2_r)
            Kp2 = kpassive(f2_r,d2_r)
            g2=data_soils[1].get("Unit_Weight2")
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
            col1.metric(label="Limit Soil Pressure \u03C3", value=f"{slim:,.0f}")
            col2.metric(label="Depth X", value=f"{x:,.2f}")
            col3.metric(label="Soil Pressure \u03C3 1", value=f"{s1:,.0f}")
            col4.metric(label="Soil Pressure \u03C3 2", value=f"{s2:,.0f}")
            if s2<0 :
                st.error("###### Soil Pressure (\u03C3 2) must be positive !")
            if slim/3<s1 or slim/3<s2:
                st.error("###### Limiting Soil Pressure (\u03C3) / Factor of Safety(assumed 3) must be higher than Soil Pressures (\u03C3 2) !")
            if x>D:
                st.error("###### Depth X must be less than Depth D !")

            # Calculate Shear and Moment with Depth above Excavation Level
            Depth=[]
            Shear=[]
            Moment=[]
            Zero=[]
            i=0
            for i in range(21):
                z=(i)*H/20
                T=0.5*(g1*z+2*Surcharge_load)*Ka1*z
                M=T*z/3*(q+2*Surcharge_load)/(Surcharge_load+q)
                Zet=0.
                Depth.append(z)
                Shear.append(T)
                Moment.append(M)
                Zero.append(Zet)
                i=i+1


            # Calculate Shear and Moment with Depth below Excavation Level

            for i in range(21,41):
                z=(i-20)*D/20
                depth=z+H
                if z < x:
                    T=0.5*g2*(Kp2-Ka2)*z**2+Pa*z+Sa
                    M=(-1/6)*g2*(Kp2-Ka2)*z**3+0.5*Pa*(z**2)+Sa*(y1+z)
                    Zet=0.
                else:
                    T=((s1+s2)/(D-x))*((z-x)**2)/2-s1*(z-x)+Sa+Sb-0.5*s1*(x-a)
                    M=((s1+s2)/(D-x))*((z-x)**3)/6-s1*((z-x)**2)/2+Sa*(y1+z)+Sb*(z-(1/3)*a)-0.5*s1*(x-a)*(z-(2/3)*x-(1/3)*a)
                    Zet=0.
                Depth.append(depth)
                Shear.append(T)
                Moment.append(M)
                Zero.append(Zet)
                i=i+1

            Depth.append(0)
            Shear.append(0)
            Moment.append(0)
            Zero.append(0)

            # Create a data-frame with the payment schedule.
            section_forces = []

            for i in range(0, 41):
                depth=Depth[i]
                shear=Shear[i]
                moment=Moment[i]
                zero=Zero[i]
                section_forces.append(
                    [
                        i,
                        -depth,
                        shear,
                        moment,
                        zero,
                    ]
                )

            df = pd.DataFrame(
                section_forces,
                columns=["No","Depth", "Shear", "Moment","Zero"],
            )

            # Display the data-frame as a chart.
            st.write("##### Sectional Forces")

            forces_df = df[["No","Depth","Shear", "Moment"]].groupby("No").min()
            chart_data = pd.DataFrame(df, columns=["Depth","Shear", "Moment","Zero"])
            # st.write(chart_data)

            # st.line_chart(forces_df)

            # st.line_chart(chart_data,x="Depth",color=["#f0f", "#04f"], use_container_width=True)

            def plot(df):
                fig,ax=plt.subplots(1,1)
                ax.plot(df["Shear"],df["Depth"])
                ax.plot(df["Moment"],df["Depth"])
                ax.plot(df["Zero"],df["Depth"],color="black",linewidth=6)
                ax.plot([np.max(Shear), 0], [-H, -H], label="Line",
                path_effects=[patheffects.withTickedStroke(spacing=7, angle=135)],color="black")
                ax.plot([np.min(Shear), 0], [0, 0], label="Line",
                path_effects=[patheffects.withTickedStroke(spacing=7, angle=-45)],color="black")
                ax.plot([np.min(Shear), 0], [-H, -H], label="Line",linestyle="dotted",color="black")
                # ax.plot(x=df['Moment'],y=df['Depth'],color='tab:orange')
                ax.set_xlabel('Moment & Shear')
                ax.set_ylabel('Depth')
                ax.grid(True)
                ax.legend(["Shear","Moment"], loc="lower right")
                t = ax.text(np.min(Shear)*2/3, -H/2, "Layer1", rotation=0, size=12, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="b", lw=2))
                t = ax.text(np.min(Shear)*2/3, -(H+D/2), "Layer2", rotation=0, size=12, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="b", lw=2))
                st.pyplot(fig)

            c1,c2=st.tabs(["Graph","Table"])

            with c1:
                plot(chart_data)
            with c2:
                st.dataframe(forces_df.map("{:,.1f}".format))

    except Exception as e:
        st.error(str(e))
        st.error("Check if above requirements are satisfied")




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



# # # --- USER AUTHENTICATION ---

# # Configuartion Key
# firebaseConfig = {
#   'apiKey': "AIzaSyAWoeU7jrcz2iJWUHUQpOfKa-W7TI-uQFE",
#   'authDomain': "cantilever-f038d.firebaseapp.com",
#   'projectId' : "cantilever-f038d",
#   'storageBucket': "cantilever-f038d.appspot.com",
#   'databaseURL' : "https://cantilever-f038d-default-rtdb.europe-west1.firebasedatabase.app/",
#   'messagingSenderId': "842228941349",
#   'appId': "1:842228941349:web:66fe01f52468cc2c84f5cc",
#   'measurementId': "G-HS27WBF5MK"
# }

# app=firebase.initialize_app(firebaseConfig)

# # cred = credentials.Certificate("serviceAccountKey.json")
# # firebase_admin.initialize_app(cred)

# # db=firestore.client()
# # Firebase Authentication

# auth = app.auth()

# # Database
# db=app.database()
# storage = app.storage()

# st.sidebar.title("Cantilever Wall")

# # Authentication

# choice = st.sidebar.selectbox('Login/Signup',['Login','Sign up'])

# try:
#   email=st.sidebar.text_input('Please enter your email address')
#   password=st.sidebar.text_input('Please enter your password')
# #   create()

#   if choice =='Sign up':
#       submit=st.sidebar.button('Create my account')
#       if submit:
#           user = auth.create_user_with_email_and_password(email,password)
#           st.success('Your account is created successfully')
#           user = auth.sign_in_with_email_and_password(email,password)
#         #   db.child(user['localId']).child("ID").set(user['localId'])
#           st.write('## Welcome  '+email)
#           st.info('Login now via login drop down')

#   if choice=='Login':
#       login=st.sidebar.checkbox('Login')
#       if login:
#           user=auth.sign_in_with_email_and_password(email,password)
#           st.write('Welcome  '+email)
#           cantilever()

# except Exception as e:
#     st.error(str(e))


