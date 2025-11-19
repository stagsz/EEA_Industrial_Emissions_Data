#!/usr/bin/env python3
"""
Script to convert Access database to other formats (SQLite, CSV, etc.)
"""

import pyodbc
import pandas as pd
import sqlite3
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AccessDatabaseConverter:
    def __init__(self, access_db_path):
        self.access_db_path = Path(access_db_path)
        self.connection = None
        
    def connect_to_access(self):
        """Connect to the Access database"""
        try:
            # Connection string for Access database
            conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={self.access_db_path};'
            self.connection = pyodbc.connect(conn_str)
            logger.info(f"Successfully connected to Access database: {self.access_db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Access database: {e}")
            return False
    
    def get_table_names(self):
        """Get all table names from the Access database"""
        if not self.connection:
            return []
        
        try:
            cursor = self.connection.cursor()
            tables = []
            for table_info in cursor.tables(tableType='TABLE'):
                table_name = table_info.table_name
                # Filter out system tables
                if not table_name.startswith('MSys') and not table_name.startswith('~'):
                    tables.append(table_name)
            return tables
        except Exception as e:
            logger.error(f"Error getting table names: {e}")
            return []
    
    def get_table_info(self, table_name):
        """Get information about a specific table"""
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            
            # Get column information
            columns = []
            for column in cursor.columns(table=table_name):
                columns.append({
                    'name': column.column_name,
                    'type': column.type_name,
                    'size': column.column_size
                })
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            row_count = cursor.fetchone()[0]
            
            return {
                'table_name': table_name,
                'columns': columns,
                'row_count': row_count
            }
        except Exception as e:
            logger.error(f"Error getting table info for {table_name}: {e}")
            return None
    
    def export_table_to_dataframe(self, table_name):
        """Export a table to pandas DataFrame"""
        if not self.connection:
            return None
        
        try:
            query = f"SELECT * FROM [{table_name}]"
            df = pd.read_sql(query, self.connection)
            logger.info(f"Exported table '{table_name}' with {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Error exporting table {table_name}: {e}")
            return None
    
    def convert_to_sqlite(self, output_path):
        """Convert the entire Access database to SQLite"""
        if not self.connection:
            logger.error("No connection to Access database")
            return False
        
        try:
            # Create SQLite connection
            sqlite_conn = sqlite3.connect(output_path)
            
            tables = self.get_table_names()
            logger.info(f"Found {len(tables)} tables to convert")
            
            for table_name in tables:
                logger.info(f"Converting table: {table_name}")
                df = self.export_table_to_dataframe(table_name)
                if df is not None:
                    # Convert to SQLite
                    df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)
                    logger.info(f"Successfully converted table '{table_name}' to SQLite")
            
            sqlite_conn.close()
            logger.info(f"Successfully converted database to SQLite: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting to SQLite: {e}")
            return False
    
    def convert_to_csv(self, output_dir):
        """Convert each table to a separate CSV file"""
        if not self.connection:
            logger.error("No connection to Access database")
            return False
        
        try:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            tables = self.get_table_names()
            logger.info(f"Found {len(tables)} tables to convert")
            
            for table_name in tables:
                logger.info(f"Converting table: {table_name}")
                df = self.export_table_to_dataframe(table_name)
                if df is not None:
                    csv_file = output_path / f"{table_name}.csv"
                    df.to_csv(csv_file, index=False)
                    logger.info(f"Successfully saved table '{table_name}' to {csv_file}")
            
            logger.info(f"Successfully converted database to CSV files in: {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting to CSV: {e}")
            return False
    
    def analyze_database(self):
        """Analyze and print database structure"""
        if not self.connect_to_access():
            return
        
        tables = self.get_table_names()
        print(f"\n=== ACCESS DATABASE ANALYSIS ===")
        print(f"Database: {self.access_db_path}")
        print(f"Total tables found: {len(tables)}")
        print("\n" + "="*60)
        
        for table_name in tables:
            info = self.get_table_info(table_name)
            if info:
                print(f"\nTable: {table_name}")
                print(f"Rows: {info['row_count']:,}")
                print("Columns:")
                for col in info['columns']:
                    print(f"  - {col['name']} ({col['type']})")
        
        print("\n" + "="*60)
    
    def close_connection(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

def main():
    # Path to the Access database
    access_db_path = r"C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\1215_Public_Product_Full Access_v8.accdb"
    
    # Create converter instance
    converter = AccessDatabaseConverter(access_db_path)
    
    try:
        # Analyze the database structure
        print("Analyzing Access database structure...")
        converter.analyze_database()
        
        # Ask user for conversion preference
        print("\nConversion options:")
        print("1. SQLite database (.db)")
        print("2. CSV files (one per table)")
        print("3. Both SQLite and CSV")
        
        choice = input("\nSelect conversion option (1, 2, or 3): ").strip()
        
        if choice in ['1', '3']:
            sqlite_path = r"C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\converted_database.db"
            print(f"\nConverting to SQLite: {sqlite_path}")
            if converter.convert_to_sqlite(sqlite_path):
                print("✓ SQLite conversion completed successfully!")
            else:
                print("✗ SQLite conversion failed!")
        
        if choice in ['2', '3']:
            csv_dir = r"C:\Users\staff\anthropicFun\EEA_Industrial_Emissions_Data\converted_csv"
            print(f"\nConverting to CSV files in: {csv_dir}")
            if converter.convert_to_csv(csv_dir):
                print("✓ CSV conversion completed successfully!")
            else:
                print("✗ CSV conversion failed!")
        
        if choice not in ['1', '2', '3']:
            print("Invalid choice. No conversion performed.")
    
    finally:
        converter.close_connection()

if __name__ == "__main__":
    main()