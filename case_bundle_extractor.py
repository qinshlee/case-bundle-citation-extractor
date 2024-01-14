# Import packages

import streamlit as st
from io import StringIO
import re
from contextlib import suppress

# Title of page

st.title('Case bundle citation extractor')
st.markdown('This app helps you to extract citations of statutes/laws from court bundles. :smile:')
st.caption('Prototype, Ver 1.0')

# Streamlit file uploader for court submission

st.divider()

uploaded_file = st.file_uploader('Step 1: Please upload text files here.',type='txt')
if uploaded_file is not None:
	# To convert to a string based IO:
	stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    
	# To read file as string:
	court_sub = stringio.read()
else:
	st.markdown("File not uploaded yet.")

# Streamlit dropdown options for default searches with citation

options = ('Acts, Codes & Charters','Laws','Rules of Court','Constitution & the Independence Agreement')
user_input1 = st.selectbox('Step 2: Please select from this list.', options, index=None, placeholder='Choose an option')

if user_input1 == "Acts, Codes & Charters":
	text_A = "(?:s|ss|section)"
	text_B = "(?:Act|Code|Charter)"
elif user_input1 == "Laws":
        text_A = "(?:art|article)"
        text_B = "Law"
elif user_input1 == "Rules of Court":
        text_A = "(?:o|ordinance)"
        text_B = "(?:ROC|Rules\sof\sCourt)"
elif user_input1 == "Constitution & the Independence Agreement":
        text_A = "(?:art|article)"
        text_B = "(?:Constitution|Independence)"
else: 
        st.markdown('No results.')
    
if user_input1 != None:
	if uploaded_file == None:
		with suppress(NameError):
			st.markdown('Please upload file in Step 1 first.')
	else:
		regex = fr'(?<=\s){text_A}\s.+?of\sthe\s.{{0,85}}{text_B}\s.{{0,125}}(?=\s)'
		regex_object = re.compile(regex, re.IGNORECASE)
		results1 = re.findall(regex_object, court_sub)
		st.write('Here are the results:\n')
		container1 = st.container(border=True)
		for i in results1:
			container1.write(i)

# Streamlit dropdown options for free-text searches for abbreviations with citation

user_input2 = st.text_input('Step 3: Please input abbreviation (up to 10 uppercase letters) to search.', value=None)

if uploaded_file == None:
	with suppress(NameError):
		st.markdown('Please upload file in Step 1 first.')
elif user_input2 == None and uploaded_file != None:
	st.markdown('No results.')
elif re.fullmatch(r'[A-Z]{2,10}', user_input2) == None and uploaded_file != None:
        st.markdown('Invalid keyword.')
else:	
	regex2 = fr'(?<=\s)(?:[sS]{{1,2}}|[sS]ection|[aA]rt|[aA]rticle|[oO]|[oO]rdinance)\s.+?of\sthe\s.{{0,85}}?{user_input2}\s.{{0,125}}(?=\s)'
	regex_object2 = re.compile(regex2)
	results2 = re.findall(regex_object2, court_sub)
	st.write('Here are the results:\n')
	container2 = st.container(border=True)
	for i in results2:
		container2.write(i)