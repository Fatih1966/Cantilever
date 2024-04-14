import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher


names = ["Fatih Kulac","Sinan Kulac"]
usernames=["fkulac","skulac"]
passwords=["6316HFKu","6316SEKu"]

hashed_passwords = Hasher(passwords).generate()


file_path=Path(__file__).parent/"hashed_pw.pk1"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)
