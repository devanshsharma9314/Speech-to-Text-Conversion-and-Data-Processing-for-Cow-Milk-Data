import pandas as pd
import numpy as np
import inflect
import re
from no_dict import *
import sys
from api_communication import *



df2 = pd.read_csv('Cow_List.csv')
df2_new = pd.read_csv('Cow_List.csv')
df2['Milk in Kg'] = 0

# Function to convert numbers to words
def convert_numbers_to_words(text):
    p = inflect.engine()
    words = []
    for word in text.split():
        if re.match(r'^\D*\d+\D*$', word):  # Word contains both letters and digits
            parts = re.findall(r'\D+|\d+', word)  # Split into alphabetic and numeric parts
            converted_parts = [p.number_to_words(part) if part.isdigit() else part for part in parts]
            words.append(''.join(converted_parts))
        elif word.isdigit():  # Entire word is numeric
            words.append(p.number_to_words(word))
        else:
            words.append(word)
    return ' '.join(words)

# Function to extract the kg value from text
def extract_kg_value(text):
    # Check for digit followed by 'kg'
    digit_match = re.search(r'(\d+)\s*kg', text)
    if digit_match:
        return int(digit_match.group(1))
    
    # Check for number words followed by 'kg'
    words = text.split()
    for i in range(len(words) - 1):
        if words[i + 1].lower() == 'kg':
            word = words[i].lower()
            if word in number_words:
                return number_words[word]
    
    return 0  # Return 0 if no number is found

# Function to process text and update the DataFrame
def text_processing(df1, df1_new, df2, df2_new):
    # Process 'Cow Id' in df2_new:
    # Convert to lowercase
    df2_new['Cow Id'] = df2_new['Cow Id'].str.lower()
    # Add a space after each digit to separate them
    df2_new['Cow Id'] = df2_new['Cow Id'].str.replace(r'(\d)', r'\1 ', regex=True)
    # Convert numbers to words using convert_numbers_to_words function
    df2_new['Cow Id'] = df2_new['Cow Id'].apply(convert_numbers_to_words)
     # Remove spaces and non-alphanumeric characters
    df2_new['Cow Id'] = df2_new['Cow Id'].str.replace(r'\s+|[^A-Za-z0-9]+', '', regex=True)
    
    # Process 'Text' in df1_new:
    # Convert to lowercase
    df1_new['Text'] = df1_new['Text'].str.lower()
    # Add a space after each digit to separate them
    df1_new['Text'] = df1_new['Text'].str.replace(r'(\d)', r'\1 ', regex=True)
    # Convert numbers to words using a custom function
    df1_new['Text'] = df1_new['Text'].apply(convert_numbers_to_words)
    # Remove spaces and non-alphanumeric characters
    df1_new['Text'] = df1_new['Text'].str.replace(r'\s+|[^A-Za-z0-9]+', '', regex=True)

    # Iterate through each 'Cow Id' in df2_new to find matches in df1_new
    for i in range(len(df2_new)):
        pattern = df2_new['Cow Id'][i]
        
        # Check if the pattern is contained in any text in df1
        df1_new['contains_substring'] = df1_new['Text'].str.contains(pattern, regex=True)
        
        # Check if any row in 'contains_substring' column is True
        if df1_new['contains_substring'].any():
            df1_new['contains_substring'] = pattern
            print("The cow Id is:", pattern)
            # Extract the 'Milk in Kg' value from df1 using a custom extraction function
            a = df1['Text'].apply(extract_kg_value)
            # Assuming you want the first value if multiple found
            if not a.empty:
                df2.loc[i, 'Milk in Kg'] += a.iloc[0]
            break
        elif i == len(df2_new) - 1:
            print("No match found")
    
    return df2



# Loop to process files until "End" is entered
while True:
    filename1 = input("Enter the file name which you want to convert into text (or 'End' to finish):")
    if filename1.lower() == "end":
        break
    audio_url = upload(filename1)
    
    filename2 =save_transcript(audio_url, filename1)
 
    if filename2.lower() == "end":
        print("Error")
        break

    df1 = pd.read_csv(filename2, header=None)
    df1_new = pd.read_csv(filename2, header=None)
    print(df1)
    
    df1_new.columns = ['Text']
    df1.columns = ['Text']

    df2 = text_processing(df1, df1_new, df2, df2_new)
    print(df2)
