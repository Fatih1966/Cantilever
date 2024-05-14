import streamlit as st
from firebase_admin import firestore
from datetime import datetime
import pandas as pd

def create_user(user,password):

    db=firestore.client()
    data={'password':password, 'uid': user.uid,'date':datetime.now()}
    db.collection('users').document(user.email).set(data)

def check_password(user,password):
    db=firestore.client()
    user_in_database=db.collection("users").document(user.email).get()
    password_in_database=user_in_database.get('password')
    if password_in_database==password:
        return True

def create_project(user,project_file_name):

    db=firestore.client()

    data_projects={}
    data_gen={}
    data_str={}
    data_soils=[]
    flag2=True
    # get all projects under this user

    projects_name=get_projects(user)


    # default data for new project item to be added to the database
    data_soils=[]
    data_projects={"name":project_file_name,'date':datetime.now(),"user":user.email}
    data_gen={"project_file_name":project_file_name,"project_title":""}
    data_str={"project_file_name":project_file_name,"Depth_excavation":4.0,"Depth_embedment":4.0,"Surcharge_load":0}
    for counter in range(1,3):
        data_soils.append({"project_file_name":project_file_name,f"Unit_Weight{counter}":20.0,f"Internal_Friction{counter}":35.0,f"Wall_Friction{counter}":20.0})
    
    for project_name in projects_name:

        if project_file_name==project_name:
            st.warning("A project with this file name already exists. Assign a different file name")
            flag2=False
            

    if flag2:
            project_ref=db.collection("projects").document(project_file_name+"-"+user.email).set(data_projects)
            data_ref_gen=db.collection("data_gen").document(project_file_name+"-"+user.email).set(data_gen)
            data_ref_str=db.collection("data_str").document(project_file_name+"-"+user.email).set(data_str)
            for counter in range(2):
                data_soil_ref=db.collection("data_soils").document(project_file_name+"-"+user.email).set(data_soils[counter],merge=True)
            st.warning(f"project name : {project_file_name} is added to the database under username : {user.email}")

    return data_gen,data_str,data_soils,flag2

def get_projects(user):
    db=firestore.client()
    projects_name=[]
    projects=(
        db.collection("projects")
        .where("user","==",user.email)
        .stream()
    )
    for project in projects:
        project_name=project.get('name')
        projects_name.append(project_name)

    return projects_name


def delete_a_project(user,project_file_name):
    db=firestore.client()
 
    db.collection("data_gen").document(project_file_name+"-"+user.email).delete()
    db.collection("data_soils").document(project_file_name+"-"+user.email).delete()
    db.collection("data_str").document(project_file_name+"-"+user.email).delete()
    db.collection("projects").document(project_file_name+"-"+user.email).delete()



def save_project_input(user,data_gen,data_str,data_soils):
    db=firestore.client()
    project_file_name=data_gen["project_file_name"]
    data_ref_gen=db.collection("data_gen").document(project_file_name+"-"+user.email).set(data_gen)
    data_ref_str=db.collection("data_str").document(project_file_name+"-"+user.email).set(data_str)

    for counter in range(2):
        data_soil_ref=db.collection("data_soils").document(project_file_name+"-"+user.email).set(data_soils[counter],merge=True)

    st.warning("data updated")


def get_project_data(user,project_file_name):
    db=firestore.client()

    #data_projects
    data_projects_db=db.collection("projects").document(project_file_name+"-"+user.email).get()
    name=data_projects_db.get("name")
    date=data_projects_db.get("date")
    user_mail=data_projects_db.get("user")
    data_projects={"name":name,'date':date,"user":user_mail}


    #data_gen
    data_gen_db=db.collection("data_gen").document(project_file_name+"-"+user.email).get()
    project_file_name_db=data_gen_db.get("project_file_name")
    project_title_db=data_gen_db.get("project_title")
    data_gen={"project_file_name":project_file_name_db,"project_title":project_title_db}


    #data_str
    data_str_db=db.collection("data_str").document(project_file_name+"-"+user.email).get()
    project_file_name_db=data_str_db.get("project_file_name")
    depth_excavation_db=data_str_db.get("Depth_excavation")
    depth_embedment_db=data_str_db.get("Depth_embedment")
    surcharge_load_db=data_str_db.get("Surcharge_load")
    data_str={"project_file_name":project_file_name_db,"Depth_excavation":depth_excavation_db,"Depth_embedment":depth_embedment_db,"Surcharge_load":surcharge_load_db}

    #data_soils
    data_soils=[]
    internal_friction=[]
    wall_friction=[]
    unit_weight=[]


    data_soils_db=db.collection("data_soils").document(project_file_name+"-"+user.email).get()
    project_file_name_db=data_soils_db.get("project_file_name")
    for counter in range(1,3):
        friction=data_soils_db.get(f"Internal_Friction{counter}")
        adhesion=data_soils_db.get(f"Wall_Friction{counter}")
        weight=data_soils_db.get(f"Unit_Weight{counter}")
        internal_friction.append(friction)
        wall_friction.append(adhesion)
        unit_weight.append(weight)
    
    for counter in range(1,3):
        data_soils.append({"project_file_name":project_file_name,f"Unit_Weight{counter}":unit_weight[counter-1],f"Internal_Friction{counter}":internal_friction[counter-1],f"Wall_Friction{counter}":wall_friction[counter-1]})



    return data_gen,data_str,data_soils
