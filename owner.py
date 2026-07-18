import streamlit as st
import sqlite3
import pandas as pd


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Owner Panel",
    page_icon="📋",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("📋 Poultry Owner Panel")

st.write("View all customer bookings.")


# --------------------------------------------------
# LOAD BOOKINGS
# --------------------------------------------------
connection = sqlite3.connect("poultry.db")

query = "SELECT * FROM bookings"

bookings = pd.read_sql_query(query, connection)

connection.close()


# --------------------------------------------------
# DISPLAY BOOKINGS
# --------------------------------------------------
if bookings.empty:

    st.warning("No bookings available.")

else:

    st.success(f"Total Bookings: {len(bookings)}")

    st.dataframe(
        bookings,
        use_container_width=True
    )