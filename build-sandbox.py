#!/usr/bin/env python3
"""
Refactors the build-sandbox.py that accepts custom CSV imports (BankComplaints.csv)
"""

import os
import sqlite3
import seaborn as sns
import pandas as pd
import sys

def get_user_confirmation(prompt):
    """Ask user for yes/no confirmation."""
    while True:
        response = input(prompt + " (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        if response in ['no', 'n']:
            return False
        print("Please answer 'yes' or 'no'")

def create_database():
    """Create a new SQLite database and populate it with Bank Complaints Dataset"""
    
    # Check if database exists and get confirmation before deleting
    if os.path.exists('sandbox.db'):
        # Ask user if they wish to keep the existing database
        if not get_user_confirmation("Database 'sandbox.db' already exists. Delete and recreate?"):
            print("Aborted. Existing database was not modified.")
            sys.exit(0)
        # Overwrite if user indicates no desire to keep existing database
        os.remove('sandbox.db')
    
    # Create a connection to the new database
    conn = sqlite3.connect('sandbox.db')
    
    try:
        # Load MPG data
        try:
            print("\nLoading MPG dataset...")
            mpg_data = sns.load_dataset('mpg')
            mpg_data.to_sql('mpg', conn, index=False)
            print(f"✅ Successfully loaded MPG dataset with {len(mpg_data)} rows")
        except Exception as e:
            print(f"❌ Error loading MPG dataset: {str(e)}")
        
        # Load tips data
        try:
            print("\nLoading tips dataset...")
            tips_data = sns.load_dataset('tips')
            tips_data.to_sql('tips', conn, index=False)
            print(f"✅ Successfully loaded tips dataset with {len(tips_data)} rows")
        except Exception as e:
            print(f"❌ Error loading tips dataset: {str(e)}")
        
        # Load penguins data
        try:
            print("\nLoading penguins dataset...")
            penguins_data = sns.load_dataset('penguins')
            penguins_data = penguins_data.dropna()  # Remove rows with missing values
            penguins_data.to_sql('penguins', conn, index=False)
            print(f"✅ Successfully loaded penguins dataset with {len(penguins_data)} rows")
        except Exception as e:
            print(f"❌ Error loading penguins dataset: {str(e)}")

        # Load bank complaints
        try:
            print("\nLoading bank complaints dataset...")
            url = 'https://raw.githubusercontent.com/adamrossnelson/confident/refs/heads/main/data/complaints-bank.csv'
            bankcomplaints_data = pd.read_csv(url,index_col=0)
            bankcomplaints_data = bankcomplaints_data.dropna()  # Remove rows with missing values
            bankcomplaints_data.to_sql('bank_complaints', conn, index=False) # transfer to sql?
            print(f"✅ Successfully loaded bank complaints dataset with {len(bankcomplaints_data)} rows")
        except Exception as e:
            print(f"❌ Error loading bank complaints dataset: {str(e)}")
            
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        print("Starting database build process...")
        create_database()
        print("\nDatabase build process completed!")
    except Exception as e:
        print(f"\n❌ Critical Error: {str(e)}")
        if os.path.exists('sandbox.db'):
            os.remove('sandbox.db')
        exit(1)