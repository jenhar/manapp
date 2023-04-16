# Libraries
import streamlit as st
from PIL import Image

from module.fetch_module import fetchData

image = Image.open('/data/assets/iconmap/mandiri-logo.png')
st.image(image, width=300)

st.title('BUSINESS CASE TRIAL INTELLIGENT BUSINESS ECOSYSTEM')

st.subheader('Territory dan Market Landscape Mapping')
st.write(
    """
    Mapping the distribution of the BMRI network,
    competitors, and business locations near the location of
    Branches as well as socidemographic conditions.
    """
)

st.subheader('Knowing the Customer Better')
st.write(
    """
    Identifying detailed information of
    targeted customers, consisting both
    customer profiles and portfolios in Bank
    Mandiri.
    """
)

st.subheader('Prioritizing Target Market')
st.write(
    """
    Leveraging data analytics to obtain
    recommendation of prioritized targeted
    customers (leads) for intensification and
    extensification
    """
)

st.subheader('Territory Share')
st.write(
    """
    Identifying the current condition of
    penetration of Bank Mandiri to measure
    the business domination in particular
    Branch.
    """
)
