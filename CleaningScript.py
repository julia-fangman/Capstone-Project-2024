import pandas as pd
import numpy as np

# Load the CSV file
csv_file_path = '/Users/juliafangman/Downloads/recidivism_full.csv'
df = pd.read_csv(csv_file_path)

# List of columns to keep
columns_to_keep = [
    'ID', 'Gender', 'Race', 'Age_at_Release', 'Gang_Affiliated', 'Education_Level', 
    'Dependents', 'Prison_Offense', 'Prison_Years', 'Prior_Arrest_Episodes_Felony', 
    'Prior_Arrest_Episodes_Misd', 'Prior_Arrest_Episodes_Violent', 
    'Prior_Arrest_Episodes_Property', 'Prior_Arrest_Episodes_Drug', 
    'Prior_Arrest_Episodes_PPViolationCharges', 'Prior_Arrest_Episodes_DVCharges', 
    'Prior_Arrest_Episodes_GunCharges', 'Prior_Conviction_Episodes_Felony', 
    'Prior_Conviction_Episodes_Misd', 'Prior_Conviction_Episodes_Viol', 
    'Prior_Conviction_Episodes_Prop', 'Prior_Conviction_Episodes_Drug', 
    'Prior_Conviction_Episodes_PPViolationCharges', 'Prior_Conviction_Episodes_DomesticViolenceCharges', 
    'Prior_Conviction_Episodes_GunCharges', 'Percent_Days_Employed', 'Jobs_per_Year', 
    'Employment_Exempt', 'Recidivism_Within_3years', 'Recidivism_Arrest_Year1', 
    'Recidivism_Arrest_Year2', 'Recidivism_Arrest_Year3'
]

# Exclude columns not in the dataset
columns_to_keep = [col for col in columns_to_keep if col in df.columns]

# Select columns to keep
df = df[columns_to_keep]

# Replace missing values in numeric columns with NaN and categorical columns with 'Unknown'
numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
df[numeric_columns] = df[numeric_columns].fillna(np.nan)
df = df.fillna('Unknown')

# Check if there are any remaining missing values
print("Number of missing values in each column after cleaning:")
print(df.isnull().sum())

# Replace "3 or more" with "3+"
df['Dependents'] = df['Dependents'].replace('3 or more', '3+')

# Columns to transform with "x or more" to "x+"
columns_to_transform = ['Prior_Conviction_Episodes_Drug', 'Prior_Conviction_Episodes_Prop', 'Prior_Conviction_Episodes_Misd',
                       'Prior_Conviction_Episodes_Felony', 'Prior_Arrest_Episodes_PPViolationCharges',
                       'Prior_Arrest_Episodes_Drug', 'Prior_Arrest_Episodes_Property', 'Prior_Arrest_Episodes_Violent',
                       'Prior_Arrest_Episodes_Misd', 'Prior_Arrest_Episodes_Felony']


# Define a function to replace "x or more" with "x+"
def replace_or_more(value):
   if ' or more' in value:
       return value.replace(' or more', '+')
   else:
       return value

# Apply the function to each column
for col in columns_to_transform:
   df[col] = df[col].apply(replace_or_more)

# Define a mapping dictionary for "Prison Years"
duration_mapping = {
   'More than 3 years': '3+ years',
   '1-2 years': '1-2 years',
   'Less than 1 year': '<1 year',
   'Greater than 2 to 3 years': '3+ years'
}

# Apply the mapping to "Prison Years"
df['Prison_Years'] = df['Prison_Years'].replace(duration_mapping)

# Define a mapping dictionary for "Education Level"
education_mapping = {
   'At least some college': 'Some College',
   'Less than HS diploma': '< HS Diploma',
   'High School Diploma': 'High School Diploma'
}

# Apply the mapping to "Education Level"
df['Education_Level'] = df['Education_Level'].replace(education_mapping)

# Columns to convert from string representations of boolean to actual boolean and then to integers
columns_to_convert = ['Gang_Affiliated', 'Prior_Arrest_Episodes_DVCharges', 'Prior_Arrest_Episodes_GunCharges',
                      'Prior_Conviction_Episodes_Viol', 'Prior_Conviction_Episodes_PPViolationCharges',
                      'Prior_Conviction_Episodes_DomesticViolenceCharges', 'Prior_Conviction_Episodes_GunCharges',
                      'Employment_Exempt', 'Recidivism_Within_3years', 'Recidivism_Arrest_Year1',
                      'Recidivism_Arrest_Year2', 'Recidivism_Arrest_Year3']

# Function to convert string representations to boolean
def str_to_bool(value):
    if isinstance(value, str):
        return value.lower() == 'true'
    else:
        return bool(value)

# Apply conversion for each column
for col in columns_to_convert:
    df[col] = df[col].apply(str_to_bool).astype(int)

# Save the cleaned DataFrame to a new CSV file
df.to_csv('/Users/juliafangman/Documents/Capstone-Project-2024/cleaned_recidivism_data.csv', index=False)

print("Cleaned data saved to cleaned_recidivism_data.csv")
