"""Streamlit dashboard (moved to app/)

This file is an entrypoint for the demo UI. It imports library code from
the `modules` package.
"""
import streamlit as st
from modules import bed_allocation, fuzzy_triage, nlp_chatbot

st.title('AI Hospital Resource Management — Demo')

st.header('Patient Triage')
with st.form('triage'):
    temp = st.number_input('Temperature (C)', value=37.0)
    sbp = st.number_input('Systolic BP', value=120)
    pain = st.slider('Pain level', 0, 10, 3)
    submitted = st.form_submit_button('Compute Priority')
    if submitted:
        score = fuzzy_triage.compute_priority(temp, sbp, pain)
        st.write(f'Priority score: {score:.1f} (0-100)')

st.header('Bed Allocation (demo)')
if st.button('Allocate sample bed'):
    patient = {'id': 'demo', 'needs_icu': True, 'needs_vent': False, 'location': (2,2)}
    beds = [
        {'id': 'b1', 'is_occupied': False, 'icu': True, 'vent': False, 'location': (3,2)},
        {'id': 'b2', 'is_occupied': False, 'icu': False, 'vent': False, 'location': (10,10)},
    ]
    bed = bed_allocation.allocate_bed(patient, beds)
    st.write('Selected bed:', bed)

st.header('Chatbot')
q = st.text_input('Ask a question')
if q:
    st.write(nlp_chatbot.respond(q))
