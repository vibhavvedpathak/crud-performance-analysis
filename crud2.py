import mysql.connector
import streamlit as st
import pandas as pd
from pathlib import Path
from data_analysis import DataReader
import matplotlib.pyplot as plt

# Connecting to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # Replace with your actual password
    database="crud2"
)

mycursor = mydb.cursor()
print("Connection Established")

def main():
    st.title("CRUD Operations for Employee Data")   

    option = st.sidebar.selectbox("Select an Operation", ("CREATE", "READ", "UPDATE", "DELETE","EMPLOYEE ANALYSIS"))

    if option == "CREATE":
        st.subheader("Create a New Employee Record")
        emp_id = st.number_input("Enter Employee ID", min_value=1)  # Ensure ID is unique and positive
        name = st.text_input("Enter Employee Name")
        email = st.text_input("Enter Employee Email")

        # Email validation using regular expression
        import re
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_regex, email):
            st.error("Invalid email format. Please enter a valid email address like name@example.com.")
        else:
            if st.button("Create"):
                sql = "INSERT INTO users(id, name, email) VALUES (%s, %s, %s)"
                val = (emp_id, name, email)
                mycursor.execute(sql, val)
                mydb.commit()
                st.success("Record Created Successfully")

    elif option == "READ":
        st.subheader("Read Records")
        sql = "SELECT * FROM users"  # No filtering needed since all records are active
        mycursor.execute(sql)
        result = mycursor.fetchall()
        if result:
            st.write("**Employee Data:**")
            for row in result:
                st.write(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
        else:
            st.info("No records found.")

    elif option == "UPDATE":
        st.subheader("Update an Existing Record")

        # Retrieve the ID to update
        emp_id = st.number_input("Enter Employee ID", min_value=1)

        if emp_id:
            sql = "SELECT * FROM users WHERE id = %s"  # Check for ID existence
            val = (emp_id,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()
            if result:
                name = st.text_input("Name", value=result[1])  # Pre-fill name
                email = st.text_input("Email", value=result[2])  # Pre-fill email
                if st.button("Update"):
                    sql = "UPDATE users SET name = %s, email = %s WHERE id = %s"
                    val = (name, email, emp_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.success("Record Updated Successfully")
            else:
                st.error("Employee ID not found.")

    elif option == "DELETE":
        st.subheader("Delete a Record")

        # Retrieve the ID to delete
        emp_id = st.number_input("Enter Employee ID", min_value=1)

        if emp_id:
            sql = "SELECT * FROM users WHERE id = %s"
            val = (emp_id,)
            mycursor.execute(sql, val)
            result = mycursor.fetchone()

            if result:
                st.write("**Employee Details:**")
                st.write(f"ID: {result[0]}")
                st.write(f"Name: {result[1]}")
                st.write(f"Email: {result[2]}")

                if st.button("Confirm Delete"):
                    sql = "DELETE FROM users WHERE id = %s"
                    val = (emp_id,)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.success("Record Deleted Successfully")
            else:
                st.error("Employee ID not found.")
    
    elif option == "EMPLOYEE ANALYSIS":
        st.subheader("Data Analysis")

        # Radio buttons for analysis selection
        analysis_option = st.radio("Select Analysis", ("Describe Data", "Attrition Correlation with Age"))

        # File upload (optional)
        if analysis_option == 'Describe Data':
            uploaded_file = st.file_uploader("Upload CSV File")
            if uploaded_file is not None:
                try:
                    data_reader = DataReader()
                    data_reader.load_data(uploaded_file)
                    df = data_reader.df
                    st.write(df.describe())
                    st.write(data_reader.display_head())
                except FileNotFoundError as e:
                    st.error(e)
                except pd.errors.ParserError as e:
                    st.error("Error parsing the uploaded file. Please ensure it's a valid CSV format.")

            




if __name__ == "__main__":
    main() 
    
