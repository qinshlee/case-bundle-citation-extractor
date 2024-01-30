# Import packages

import streamlit as st
from io import StringIO
import re
from contextlib import suppress

# Define functions for regex search and displaying results

def regex_search(regex, text, ignore_case = False):
	""" Processes regex search.
	Args:
		regex (str): Regular expression to search for result.
		text (str): Text to search through. (String keys are utf-8 decoded.)  
		ignore_case (bool) = False: Optional argument to choose a search that ignores cases (if True).
	Returns:
		A list of strings from the text string that fits the regex search.
	"""
	regex_object = re.compile(regex, flags=re.IGNORECASE if ignore_case else 0)
	return re.findall(regex_object, text)
	
def display_results(results):
	"""Takes a list	of strings and displays it string by string, in a Streamlit container."""
	st.write('Here are the results:\n')
	container = st.container(border=True)
	try:
		for i in results: 
			container.write(i)
	finally:
		container.write('Nil results.')

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
if user_input1 == "Laws":
    text_A = "(?:art|article)"
    text_B = "Law"
if user_input1 == "Rules of Court":
    text_A = "(?:o|ordinance)"
    text_B = "(?:ROC|Rules\sof\sCourt)"
if user_input1 == "Constitution & the Independence Agreement":
    text_A = "(?:art|article)"
    text_B = "(?:Constitution|Independence)"
    
if uploaded_file == None:
	with suppress(NameError):
		st.markdown('Please upload file in Step 1 first.')
elif user_input1 == None and uploaded_file != None:
	st.markdown('There are no results.')
else:
	regex1 = fr'(?<=\s){text_A}\s.+?of\sthe\s.{{0,85}}{text_B}\s.{{0,125}}(?=\s)'
	results1 = regex_search(regex1, court_sub, ignore_case=True)
	display_results(results1)

# Streamlit dropdown options for free-text searches for abbreviations with citation

user_input2 = st.text_input('Step 3: Please input abbreviation (up to 10 uppercase letters) to search.', value=None)

if uploaded_file == None:
	with suppress(NameError):
		st.markdown('Please upload file in Step 1 first.')
elif user_input2 == None and uploaded_file != None:
	st.markdown('Please input abbreviation.')
elif re.fullmatch(r'[A-Z]{2,10}', user_input2) == None and uploaded_file != None:
    st.markdown('Invalid keyword.')
else:	
	regex2 = fr'(?<=\s)(?:[sS]{{1,2}}|[sS]ection|[aA]rt|[aA]rticle|[oO]|[oO]rdinance)\s.+?of\sthe\s.{{0,85}}?{user_input2}\s.{{0,125}}(?=\s)'
	results2 = regex_search(regex2, court_sub, ignore_case=False)
	display_results(results2)
	