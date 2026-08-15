import streamlit as st


def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #5865F2 !important;
                }

                div[data-testid="stColumn"]{
                    background-color:#E0E3FF !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                    }
        </style>  

                """
            ,unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: #E0E3FF !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        #MainMenu, footer, header {
            visibility: hidden;
        }

        .block-container {
            padding-top: 1.5rem !important;
        }

        .stApp {
            color: #2B2B2B !important;
        }

        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            color: #2B2B2B !important;
        }

        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem !important;
            line-height: 0.9 !important;
            margin-bottom: 0rem !important;
            color: #2B2B2B !important;
        }

        h3, h4 {
            font-family: 'Outfit', sans-serif !important;
            color: #2B2B2B !important;
        }

        p, label {
            color: #2B2B2B !important;
        }

        /* Default dark button */
        div.stButton > button,
        div.stButton > button * {
            color: white !important;
        }

        div.stButton > button {
            background-color: #333333 !important;
            border: none !important;
            border-radius: 8px !important;
        }

        div.stButton > button[kind="secondary"],
        div.stButton > button[kind="secondary"] * {
            background-color: #EB459E !important;
            color: black !important;
        }

        div.stButton > button[kind="secondary"] {
            border-radius: 1.5rem !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }

        div.stButton > button[kind="tertiary"],
        div.stButton > button[kind="tertiary"] * {
            background-color: #111111 !important;
            color: white !important;
        }

        div.stButton > button[kind="tertiary"] {
            border-radius: 1.5rem !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }


        div.stButton > button:hover {
            transform: scale(1.05);
        }

        [data-testid="stCameraInput"] button {
        background-color: #333333 !important;
        color: white !important;
        }

        [data-testid="stCameraInput"] button * {
            color: white !important;
        }

        [data-testid="stCameraInput"] label {
            color: #2B2B2B !important;
        }

        </style>
    """, unsafe_allow_html=True)