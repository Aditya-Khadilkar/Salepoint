import streamlit as st
import requests
import json
import base64
import pandas as pd
#streamlit app that takes in a image or pdf file and returns a json download





def verify_file(file):
        
    CLIENT_ID = st.secrets["CLIENT_ID"]
    ENVIRONMENT_URL = st.secrets["ENVIRONMENT_URL"]
    username = st.secrets["username"]
    api_key = st.secrets["api_key"]


    
    process_file_url = '{0}api/v8/partner/documents/'.format(ENVIRONMENT_URL)
    headers = {
        "Accept": "application/json",
        "CLIENT-ID": CLIENT_ID,
        "AUTHORIZATION": "apikey {0}:{1}".format(username, api_key)
    }
    #save the file to the local directory
    with open(file.name, "wb") as f:
        f.write(file.getbuffer())
    
    # file path and file name
    image_path = file.name#'invoice.png'
    file_name = file.name#'invoice.png'

    # You can send the list of categories that is relevant to your case
    # Veryfi will try to choose the best one that fits this document
    categories = ["Office Expense", "Meals & Entertainment", "Utilities", "Automobile"]
    payload = {
        'file_name': file_name,
        'categories': categories
    }
    files = {'file': ('file', open(image_path, 'rb'), file.type)}
    response = requests.post(url=process_file_url, headers=headers, data=payload, files=files)
    return response.json()


def generate_csv(data):
    #convert json to csv
    keys = []
    vals = []
    for key, val in data.items():
        if val!=None:
            if type(val)!=dict or type(val)!=list:
                keys.append(key)
                vals.append(val)
    #make a dataframe
    df = pd.DataFrame([vals], columns=keys)
    return df

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    #button to download the csv file
    return st.download_button(label="Download CSV", data=csv, file_name='myfilename.csv', mime='text/csv')
        
    #return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'



#title is Salepoint. text gradient, center aligned
title = """<style>
h1 {
color: white;
  font-size: 72px;
  background-image: linear-gradient(60deg, #20D3FE, #9F37FE);
  background-clip: text;
    text-align: center;
border-radius: 15px;
}
.css-17ii5o0 {
margin-top: 5rem;
}
</style>
<h1>Salepoint</h1>"""



st.markdown(title, unsafe_allow_html=True)

welcome = """<style>
h4 {
color: black;
font-size: 16px;
margin-top: 2rem;
text-align: center;
}

</style>
<h4>Welcome Hornstra Farms</h4>"""


logo = """<style>
img {
  display: block;
  align: center;
    margin-left: auto;
    margin-right: auto;
    margin-top: 2rem;
    
}
</style>
<img src="https://hornstrafarms.com/wp-content/themes/wps-theme/_/img/logo.png" alt="Hornstra Farms" width="200">
"""
st.markdown(logo, unsafe_allow_html=True)
st.markdown(welcome, unsafe_allow_html=True)
#show the image logo
#https://hornstrafarms.com/wp-content/themes/wps-theme/_/img/logo.png center align



#st.image('https://hornstrafarms.com/wp-content/themes/wps-theme/_/img/logo.png', width=200)
file = st.file_uploader("Upload Invoice", type=["jpg", "png", "jpeg", "pdf"])
if file:
    data = verify_file(file)
    csv = generate_csv(data)
    #download the csv file
    get_table_download_link(csv)
    #st.markdown(get_table_download_link(csv), unsafe_allow_html=True)
    #st.write(data)
    #st.markdown(json.dumps(data), unsafe_allow_html=True)
    #st.markdown(get_table_download_link(data), unsafe_allow_html=True)