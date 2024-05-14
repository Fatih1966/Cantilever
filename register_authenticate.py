import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from cantilever01 import cantilever
# from datetime import datetime
from crud import create_user,check_password,create_project
# from project import select_project



def login(email,password):
    try:
        user=auth.get_user_by_email(email)
        if check_password(user,password):
            st.sidebar.write('Welcome  '+user.email)

            cantilever(user)
        else :
            st.sidebar.warning('Password does not match. Re-enter the Password')
    except :
        st.warning("Login Failed")

def register_authenticate():
    

    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # db=firestore.client()
    # Firebase Authentication

    # auth = app.auth()

    # Database
    # db=app.database()
    # storage = app.storage()

    st.sidebar.title("Cantilever Wall")

    # Authentication


    choice = st.sidebar.selectbox('Login / Sign up',['Login','Sign up'])

    try:
        email=st.sidebar.text_input('Please enter your email address')
        password=st.sidebar.text_input('Please enter your password', type="password")

        if choice =='Sign up':
            submit=st.sidebar.button('Create my account')
            if submit:
                user = auth.create_user(email=email,password=password)
                create_user(user,password)
                create_project(user,"default")
                st.success('Your account is created and added to database successfully')
                st.markdown('Login now via login drop down')

                # user = auth.sign_in(email=email,password=password)
                # db.child(user['localId']).child("ID").set(user['localId'])
                # st.write('## Welcome  '+email)
                

        if choice=='Login':
            # login=st.sidebar.checkbox('Login')
            # if login:
            submit=st.sidebar.button('Login')
            if "submit_state" not in st.session_state:
                st.session_state.submit_state=False
            if submit or st.session_state.submit_state:
                st.session_state.submit_state=True
                login(email,password)
            # if st.sidebar.checkbox('Login'):
            #     login(email,password)

            # st.write('Welcome  '+email)
               
        
    except Exception as e:
        st.error(str(e))








