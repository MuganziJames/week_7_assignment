#!/usr/bin/env python3
"""
Data Download Script for COMPAS Dataset
Downloads the COMPAS recidivism dataset from ProPublica's GitHub repository
"""

import pandas as pd
import os

def download_compas_data(save_path='data/'):
    """
    Download COMPAS dataset from ProPublica GitHub repository
    
    Args:
        save_path (str): Directory to save the dataset
    """
    # Create data directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)
    
    # ProPublica COMPAS dataset URL
    url = "https://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv"
    
    try:
        print("📥 Downloading COMPAS dataset from ProPublica...")
        df = pd.read_csv(url)
        
        # Save to local file
        output_file = os.path.join(save_path, 'compas-scores-two-years.csv')
        df.to_csv(output_file, index=False)
        
        print(f"✅ Dataset downloaded successfully!")
        print(f"📁 Saved to: {output_file}")
        print(f"📊 Dataset shape: {df.shape}")
        print(f"📋 Columns: {len(df.columns)} features")
        
        # Display basic info
        print("\n=== Dataset Overview ===")
        print(f"Total records: {len(df):,}")
        print(f"Date range: {df['c_jail_in'].min()} to {df['c_jail_in'].max()}")
        
        if 'race' in df.columns:
            print(f"\nRace distribution:")
            print(df['race'].value_counts())
        
        if 'two_year_recid' in df.columns:
            recid_rate = df['two_year_recid'].mean()
            print(f"\nOverall two-year recidivism rate: {recid_rate:.1%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False

def download_alternative_datasets():
    """Download additional datasets that might be useful for analysis"""
    datasets = {
        'compas_analysis': 'https://raw.githubusercontent.com/propublica/compas-analysis/master/cox-parsed.csv',
        'compas_violent': 'https://raw.githubusercontent.com/propublica/compas-analysis/master/cox-violent-parsed.csv'
    }
    
    for name, url in datasets.items():
        try:
            print(f"\n📥 Downloading {name}...")
            df = pd.read_csv(url)
            output_file = f'data/{name}.csv'
            df.to_csv(output_file, index=False)
            print(f"✅ {name} saved to {output_file} (shape: {df.shape})")
        except Exception as e:
            print(f"⚠️ Could not download {name}: {e}")

if __name__ == "__main__":
    print("COMPAS Dataset Download Script")
    print("=" * 40)
    
    success = download_compas_data()
    
    if success:
        print("\n📦 Downloading additional datasets...")
        download_alternative_datasets()
        
        print("\n🎉 All downloads completed!")
        print("\nNext steps:")
        print("1. Run 'python compas_audit.py' for bias analysis")
        print("2. Open 'ai_ethics_analysis.ipynb' in Jupyter")
        print("3. Review the data in the 'data/' directory")
    else:
        print("\n❌ Primary dataset download failed.")
        print("Please check your internet connection and try again.")
