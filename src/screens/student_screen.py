import streamlit as st
import numpy as np
from PIL import Image
from src.ui.base_layout import style_background_dashboard ,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
import time

from src.pipelines.face import predict_attendance , get_face_embeddings , train_classifier
from src.pipelines.voice import get_voice_embedding
from src.database.db import get_all_students ,create_student ,get_student_subjects , get_student_attendance , unenroll_student_to_subject
from src.components.dialoge_enroll_subject import create_subject_dialoge
from src.components.subject_card import subject_card
def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1 , c2 = st.columns(2)
    
    with c1:
        header_dashboard()
    
    with c2:
        st.subheader(f"welcome {student_data["name"]}")
        if st.button("log out " , shortcut="control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()
    
    st.space()

    col1 , col2 = st.columns(2)

    with col1:
        st.subheader("enroll the subject")

    with col2:
        if st.button("enroll now"):
            create_subject_dialoge()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']


        stats = stats_map.get(sid,{"total":0, "attended": 0} )
        def unenroll_button(subject_id):
                if st.button("Unenroll from this course",type="tertiary",width="stretch",icon=":material/delete_forever:",key=f"unenroll_{subject_id}"):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f'Unenrolled from {sub['name']} successfully!')
                    st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=lambda sub_id=sub['subject_id']: unenroll_button(sub_id)
            )
    footer_dashboard()



def student_screen():

    style_base_layout()
    style_background_dashboard()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False
    
    col1 , col2 = st.columns(2)
    with col1:
        header_dashboard()

    with col2:
        if st.button("go back to home" , type='secondary', key='loginbackbtn' ,shortcut="control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login Using FaceId" , text_alignment="center")
    st.space()
    st.space()

    show_registration = False
    photo = st.camera_input("position your face in the centre")

    if photo:
        img = np.array(Image.open(photo))

        with st.spinner("AI is scanning"):

            detected , all_ids , num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("face not found")
            elif num_faces > 1:
                st.warning("multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id), None)
                        

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"welcome back {student["name"]}")
                        time.sleep(1)
                        st.rerun()
                                 
                else:
                    st.info("face not recognized ! you might be new student")
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Register new profile")
            new_name = st.text_input("Enter your name" , placeholder="@aditya")

            st.subheader("optional : voice enrollment")
            st.info("enroll your for voice only attendance")

            audio_data = None

            try:
                audio_data = st.audio_input("record a short phrase like i am present my name is XYZ")
            except Exception:
                st.error("audio failed")

            if st.button("create account" , type="primary"):
                if new_name:
                    with st.spinner("creating profile"):
                        img = np.array(Image.open(photo))
                        encoding = get_face_embeddings(img)

                        if encoding:
                            face_emb = encoding[0].tolist()

                            voice_emb=None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            respose_data = create_student(new_name , face_embedding = face_emb , voice_embedding= voice_emb)

                            if respose_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = respose_data[0]
                                st.toast(f"profile created! hi{new_name}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("couldnt capture your face")                  

                else:
                    st.warning("please enter your name")



    footer_dashboard()
