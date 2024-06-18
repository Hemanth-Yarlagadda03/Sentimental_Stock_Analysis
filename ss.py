import os
from bs4 import BeautifulSoup

# Initialize the dictionary to store HTML tables
html_tables = {}

# Define the datasets directory
datasets_dir = 'C:/Users/kowshik/Study/Projects/Stock-Prediction-System-Application/sentiment/datasets'

# Iterate over files in the datasets directory
for file_name in os.listdir(datasets_dir):
    file_path = os.path.join(datasets_dir, file_name)

    # Process only HTML files
    if file_name.endswith('.html'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file_object:
                html = BeautifulSoup(file_object, 'html.parser')
                # Find the headlines table with id 'news-table'
                html_table = html.find(id='news-table')
                
                # Check if the 'news-table' id exists
                if html_table:
                    # Add the table to the dictionary with file_name as key
                    html_tables[file_name] = html_table
                else:
                    print(f"Warning: 'news-table' not found in {file_name}")
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except UnicodeDecodeError:
            print(f"Error: Could not decode {file_name} with 'utf-8' encoding.")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
    else:
        print(f"Skipping non-HTML file: {file_name}")

# Debug output of collected tables
for file, table in html_tables.items():
    print(f"Processed table from {file}")

#import os
#from bs4 import BeautifulSoup
#
## Initialize the dictionary to store HTML tables
#html_tables = {}
#
## Define the datasets directory
#datasets_dir = 'C:/Users/kowshik/Study/Projects/Stock-Prediction-System-Application/sentiment/datasets'
#
## Check if the directory exists
#if not os.path.exists(datasets_dir):
#    print(f"Error: The directory {datasets_dir} does not exist.")
#else:
#    # Iterate over files in the datasets directory
#    for file_name in os.listdir(datasets_dir):
#        file_path = os.path.join(datasets_dir, file_name)
#
#        # Process only HTML files
#        if file_name.endswith('.html'):
#            try:
#                with open(file_path, 'r', encoding='utf-8') as file_object:
#                    html = BeautifulSoup(file_object, 'html.parser')
#                    # Find the headlines table with id 'news-table'
#                    html_table = html.find(id='news-table')
#
#                    # Check if the 'news-table' id exists
#                    if html_table:
#                        # Add the table to the dictionary with file_name as key
#                        html_tables[file_name] = html_table
#                    else:
#                        print(f"Warning: 'news-table' not found in {file_name}")
#            except FileNotFoundError:
#                print(f"Error: The file {file_path} does not exist.")
#            except UnicodeDecodeError:
#                print(f"Error: Could not decode {file_name} with 'utf-8' encoding.")
#            except Exception as e:
#                print(f"Error processing {file_name}: {e}")
#        else:
#            print(f"Skipping non-HTML file: {file_name}")
#
#    # Debug output of collected tables
#    for file, table in html_tables.items():
#        print(f"Processed table from {file}")
#