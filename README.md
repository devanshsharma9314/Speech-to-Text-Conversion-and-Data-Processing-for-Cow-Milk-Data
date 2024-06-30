# Speech-to-Text-Conversion-and-Data-Processing-for-Cow-Milk-Data

Description: 
This project involves the use of AssemblyAI's Speech-to-Text API to convert audio files
into text transcriptions. The transcribed text is then processed to extract relevant
information about cow IDs and milk quantities, which are updated in a provided CSV file

Technologies Used:
AssemblyAI API: For converting audio files into text transcriptions.  
Python: The main programming language used for scripting and data processing.  
pandas: For data manipulation, reading, and writing CSV files.  
numpy: For numerical operations.  
inflect: For converting numbers to words.  
re (Regular Expressions): For pattern matching in text.  
Custom Python Modules:  
no_dict.py: Contains mappings for number word conversions.  
api_communication.py: Contains functions to communicate with AssemblyAI API.  
API Key Management: Secure handling of the AssemblyAI API key using a separate api_secrets module.  
