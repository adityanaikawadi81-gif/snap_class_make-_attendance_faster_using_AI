import streamlit as st

from src.database.db import create_subject

@st.dialog("create new subject")
def create_subject_dialoge(teacher_id):
    st.write("enter the details of new sbject")
    sub_name = st.text_input("enter the subject name " , placeholder="physics")
    sub_code = st.text_input("enter the subject code" , placeholder="CS10")
    sub_section = st.text_input("enter the section" , placeholder="A")

    if st.button("create subject now"):
        if sub_name and sub_code and sub_section:
            try:
                create_subject(sub_name , sub_code , sub_section , teacher_id)
                st.toast("subject created")
                st.rerun()
            except Exception as e:
                st.error(f"error {str(e)}")
        else:
            st.warning("please fill all the details")
