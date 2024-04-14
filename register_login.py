

# Modules
import pyrebase
import streamlit as st
from datetime import datetime


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
      login=st.sidebar.button('Login')
      if login:
          user=auth.sign_in_with_email_and_password(email,password)
          st.title('Welcome  '+email)
except Exception as e:
    st.error(str(e))
