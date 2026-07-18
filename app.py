import json
import sqlite3

import pandas as pd
import streamlit as st

from database import create_bookings_table, save_booking


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Poultry Hen Booking System",
    page_icon="🐔",
    layout="wide"
)


# --------------------------------------------------
# CREATE DATABASE TABLE
# --------------------------------------------------
create_bookings_table()


# --------------------------------------------------
# UI STYLE
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #fffaf3;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #7a3e00;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #6b5b4b;
        margin-bottom: 30px;
    }

    div.stButton > button {
        background-color: #d97706;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 22px;
        font-weight: 700;
    }

    div.stButton > button:hover {
        background-color: #b45309;
        color: white;
    }

    .booking-card {
        background-color: #fff7ed;
        padding: 18px;
        border-radius: 12px;
        border-left: 6px solid #d97706;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .owner-card {
        background-color: #fff7ed;
        padding: 16px;
        border-radius: 12px;
        border-left: 6px solid #7a3e00;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "customer_submitted" not in st.session_state:
    st.session_state.customer_submitted = False

if "booking_completed" not in st.session_state:
    st.session_state.booking_completed = False


# --------------------------------------------------
# MAIN TITLE
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🐔 Poultry Hen Booking System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Simple and easy poultry booking demo application</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
page = st.sidebar.radio(
    "Select Page",
    [
        "Customer Booking",
        "Owner Panel"
    ]
)


# ==================================================
# CUSTOMER BOOKING PAGE
# ==================================================
if page == "Customer Booking":

    st.header("👤 Customer Details")

    customer_name = st.text_input(
        "Customer Name",
        value=st.session_state.get("customer_name", "")
    )

    mobile_number = st.text_input(
        "Mobile Number",
        value=st.session_state.get("mobile_number", "")
    )

    village = st.text_input(
        "Village / City",
        value=st.session_state.get("village", "")
    )

    continue_button = st.button("Continue")


    # --------------------------------------------------
    # CUSTOMER DETAILS VALIDATION
    # --------------------------------------------------
    if continue_button:

        if customer_name and mobile_number and village:

            if mobile_number.isdigit() and len(mobile_number) == 10:

                st.session_state.customer_submitted = True
                st.session_state.customer_name = customer_name
                st.session_state.mobile_number = mobile_number
                st.session_state.village = village

                st.success(
                    "Customer details submitted successfully."
                )

            else:
                st.error(
                    "Please enter a valid 10-digit mobile number."
                )

        else:
            st.error(
                "Please fill in all customer details."
            )


    # --------------------------------------------------
    # AVAILABLE HENS
    # --------------------------------------------------
    if st.session_state.customer_submitted:

        try:
            with open(
                "data/hens.json",
                "r",
                encoding="utf-8"
            ) as file:

                hens = json.load(file)

        except FileNotFoundError:
            st.error(
                "hens.json file was not found inside the data folder."
            )
            st.stop()

        except json.JSONDecodeError:
            st.error(
                "hens.json contains invalid JSON data."
            )
            st.stop()


        st.header("🐔 Available Hens")

        heading_columns = st.columns(
            [3, 2, 2, 2, 1]
        )

        heading_columns[0].markdown("**Hen Breed**")
        heading_columns[1].markdown("**Age**")
        heading_columns[2].markdown("**Purpose**")
        heading_columns[3].markdown("**Price**")
        heading_columns[4].markdown("**Select**")

        st.divider()

        selected_hens = []


        # --------------------------------------------------
        # DISPLAY HENS
        # --------------------------------------------------
        for hen in hens:

            row_columns = st.columns(
                [3, 2, 2, 2, 1]
            )

            row_columns[0].write(
                hen["breed"]
            )

            row_columns[1].write(
                hen["age"]
            )

            row_columns[2].write(
                hen["purpose"]
            )

            row_columns[3].write(
                f"₹{hen['price']}"
            )

            selected = row_columns[4].checkbox(
                "Choose",
                key=f"hen_{hen['id']}",
                label_visibility="collapsed"
            )

            if selected:
                selected_hens.append(hen)

            st.divider()


        # --------------------------------------------------
        # BOOKING SECTION
        # --------------------------------------------------
        if selected_hens:

            st.success(
                f"{len(selected_hens)} hen(s) selected."
            )

            total_price = sum(
                hen["price"]
                for hen in selected_hens
            )

            st.info(
                f"Total Price: ₹{total_price}"
            )

            book_button = st.button(
                "📌 Book Selected Hen"
            )


            # --------------------------------------------------
            # SAVE BOOKING
            # --------------------------------------------------
            if book_button:

                try:

                    for hen in selected_hens:

                        save_booking(
                            st.session_state.customer_name,
                            st.session_state.mobile_number,
                            st.session_state.village,
                            hen["breed"],
                            hen["age"],
                            hen["purpose"],
                            hen["price"]
                        )

                    st.session_state.booking_completed = True

                    st.success(
                        "🎉 Booking Successful! "
                        "Booking details saved successfully."
                    )


                    # --------------------------------------------------
                    # BOOKING DETAILS
                    # --------------------------------------------------
                    st.markdown(
                        """
                        <div class="booking-card">
                            <h3>🐔 Booked Hen Details</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(
                        "### 👤 Customer Information"
                    )

                    st.write(
                        f"Customer Name: "
                        f"{st.session_state.customer_name}"
                    )

                    st.write(
                        f"Mobile Number: "
                        f"{st.session_state.mobile_number}"
                    )

                    st.write(
                        f"Village / City: "
                        f"{st.session_state.village}"
                    )

                    st.write("---")

                    st.write(
                        "### 🐔 Selected Hen Information"
                    )

                    for hen in selected_hens:

                        st.write(
                            f"Breed Name: {hen['breed']}"
                        )

                        st.write(
                            f"Hen Age: {hen['age']}"
                        )

                        st.write(
                            f"Purpose: {hen['purpose']}"
                        )

                        st.write(
                            f"Hen Price: ₹{hen['price']}"
                        )

                        st.write("---")

                    st.write(
                        f"### 💰 Total Booking Amount: "
                        f"₹{total_price}"
                    )

                except sqlite3.Error as error:

                    st.error(
                        f"Booking could not be saved: {error}"
                    )

        else:
            st.info(
                "Please select at least one hen "
                "to continue booking."
            )


# ==================================================
# OWNER PANEL PAGE
# ==================================================
elif page == "Owner Panel":

    st.markdown(
        """
        <div class="owner-card">
            <h2>📋 Poultry Owner Panel</h2>
            <p>View all customer booking details.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    owner_password = st.text_input(
        "Enter Owner Password",
        type="password"
    )

    if owner_password == "admin123":

        try:
            connection = sqlite3.connect(
                "poultry.db"
            )

            query = """
            SELECT
                id,
                customer_name,
                mobile_number,
                village,
                breed,
                age,
                purpose,
                price
            FROM bookings
            ORDER BY id DESC
            """

            bookings = pd.read_sql_query(
                query,
                connection
            )

            connection.close()


            if bookings.empty:

                st.warning(
                    "No bookings available."
                )

            else:

                st.success(
                    f"Total Booking Records: "
                    f"{len(bookings)}"
                )

                bookings = bookings.rename(
                    columns={
                        "id": "Booking ID",
                        "customer_name": "Customer Name",
                        "mobile_number": "Mobile Number",
                        "village": "Village / City",
                        "breed": "Hen Breed",
                        "age": "Hen Age",
                        "purpose": "Purpose",
                        "price": "Price"
                    }
                )

                st.dataframe(
                    bookings,
                    use_container_width=True,
                    hide_index=True
                )

                total_revenue = bookings[
                    "Price"
                ].sum()

                st.info(
                    f"💰 Total Booking Amount: "
                    f"₹{total_revenue}"
                )

                csv_data = bookings.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="📥 Download Bookings CSV",
                    data=csv_data,
                    file_name="poultry_bookings.csv",
                    mime="text/csv"
                )

        except sqlite3.Error as error:

            st.error(
                f"Could not load bookings: {error}"
            )

    elif owner_password:

        st.error(
            "Incorrect owner password."
        )

    else:

        st.info(
            "Please enter the owner password "
            "to view bookings."
        )