
import pandas as pd
import os

pooling_file = 'data/SampleSheets_files/SampleSheets.xlsx'

plate_to_file = {
    1: 'data/index_files_biolabs/E6440_ Reverse Complement Workflow Sample Sheet.csv',
    2: 'data/index_files_biolabs/E6442_ Reverse Complement Workflow Sample Sheet.csv',
    3: 'data/index_files_biolabs/E6444_ Reverse Complement Workflow Sample Sheet.csv',
    4: 'data/index_files_biolabs/E6446_ Reverse Complement Workflow Sample Sheet.csv',
    5: 'data/index_files_biolabs/E6448_ Reverse Complement Workflow Sample Sheet.csv',
}

def load_csv_with_header(file_path):
    df = pd.read_csv(file_path, skiprows=16)
    df.columns = df.iloc[0] 
    df = df[1:].reset_index(drop=True)    
    return df

def process_sample_sheet(sample_sheet_df):
    results = []

    # Process each plate number separatly 
    for plate_number, e644_file in plate_to_file.items():
        subset_df = sample_sheet_df[sample_sheet_df['Sample_Plate'] == plate_number]
        
        if not subset_df.empty:
            e644_df = load_csv_with_header(e644_file)
            
            required_columns = ['Sample_Well', 'index', 'index2']
            missing_columns = [col for col in required_columns if col not in e644_df.columns]
            
            if missing_columns:
                raise ValueError(f"CSV file {e644_file} is missing columns: {', '.join(missing_columns)}")
    
            # Merge the subset with the CSV file based on 'Sample_Well'
            merged_df = subset_df.merge(
                e644_df[['Sample_Well', 'index', 'index2']],
                on='Sample_Well',
                how='left'
            )

            results.append(merged_df)
    
    combined_df = pd.concat(results, ignore_index=True)
    
    
    return combined_df

with pd.ExcelFile(pooling_file) as xls:
    for sheet_name in xls.sheet_names:
        if sheet_name.startswith("SampleSheet"):
            sample_sheet_df = pd.read_excel(pooling_file, sheet_name=sheet_name)
            
            updated_df = process_sample_sheet(sample_sheet_df)
            
            # Save the updated sample sheet back to the pooling file
            with pd.ExcelWriter(pooling_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                updated_df.to_excel(writer, sheet_name=sheet_name, index=False)

                
