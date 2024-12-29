# Title and Introduction
st.title("🎈 Dashboard")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

1 import os  
2 import openai  
3 import streamlit as st  
4 import pandas as pd  
5 from dotenv import load_dotenv  
6  
7 from pandasai import SmartDataframe  
8 from pandasai.llm.openai import OpenAI  
9  
10 load_dotenv()  
11 openai_api_key = os.environ["OPENAI_API_KEY"]  
12 llm = OpenAI(api_token=openai_api_key)  
13  
14 st.title("Your Data Analysis")  
15  
16 uploaded_csv_file = st.file_uploader("Upload a csv file for analysis", type=['csv'])  
17  
18 if uploaded_csv_file is not None:  
19  df = pd.read_csv(uploaded_csv_file)  
20  sdf = SmartDataframe(df, config={"llm":llm})  
21  st.write(sdf.head(4))  
22  
23 prompt = st.text_area("Enter your prompt")  
24  
25 if st.button("Generate"):  
26  if prompt:  
27  with st.spinner("Generating Response..."):  
28  response = sdf.chat(prompt)  
29  st.success(response)  
30  st.set_option('deprecation.showPyplotGlobalUse', False)  
31  st.pyplot()  
32  else:  
33  st.warning("Please enter a prompt")  
34  
35
