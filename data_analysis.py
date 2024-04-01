import streamlit
import pymongo
import pandas as pd
import matplotlib as plt
from pathlib import Path
import streamlit as st

class DataReader:
    def __init__(self,data_path=None):
        self.data_path = data_path
        self.df = None

    def load_data(self, uploaded_file):
        if uploaded_file is not None:
            self.data_path = Path(uploaded_file.name)  
            try:
                self.df = pd.read_csv(self.data_path)
            except FileNotFoundError as e:
                st.error("Error: File not found. Please check the path and try again.")  
            except pd.errors.ParserError as e:
                st.error("Error parsing the CSV file. Please ensure it's a valid CSV format.")

    def display_head(self,num_rows=5):
        if self.df is not None:
            print(f"Head of DataFrame (showing {num_rows}):")
            print(self.df.head(num_rows))
        else:
            print("No data loaded yet. Please use the load_data() first.")






