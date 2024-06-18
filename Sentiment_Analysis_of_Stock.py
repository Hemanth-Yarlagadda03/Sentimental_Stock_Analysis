import os
import pandas as pd
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure NLTK's VADER lexicon is available
nltk.download('vader_lexicon')

# Initialize the dictionary to store HTML tables
html_tables = {}

# Define the datasets directory
datasets_dir = 'C:/Users/kowshik/Study/Projects/Stock-Prediction-System-Application/sentiment/datasets'

# Check if the directory exists
if not os.path.exists(datasets_dir):
    print(f"Error: The directory {datasets_dir} does not exist.")
else:
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

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Process each HTML table
for file_name, html_table in html_tables.items():
    # Determine the company name based on file_name
    if 'fb' in file_name.lower():
        company_name = 'FB'
    elif 'tsla' in file_name.lower():
        company_name = 'TSLA'
    else:
        company_name = 'Unknown'  # Handle other companies as needed

    # Extract news data from HTML table
    news_data = []
    for row in html_table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 1:  # Assuming at least two columns for date and headline
            date = columns[0].text.strip()
            headline = columns[1].text.strip()
            news_data.append({'date': date, 'headline': headline, 'company': company_name})

    # Convert news data to DataFrame
    news_df = pd.DataFrame(news_data)

    # Perform sentiment analysis
    news_df['scores'] = news_df['headline'].apply(lambda x: sid.polarity_scores(x))
    news_df = pd.concat([news_df.drop(['scores'], axis=1), news_df['scores'].apply(pd.Series)], axis=1)

    # Convert 'date' column to datetime
    news_df['date'] = pd.to_datetime(news_df['date'], errors='coerce').dt.date

    # Drop rows with invalid dates
    news_df = news_df.dropna(subset=['date'])

    # Group by 'date' and 'company', and calculate the mean of the numeric columns
    numeric_columns = news_df.select_dtypes(include='number').columns
    mean_scores = news_df.groupby(['date', 'company'])[numeric_columns].mean().unstack(level=1)

    # Print the mean sentiment scores
    print(f"Mean sentiment scores for {company_name} from {file_name}:")
    print(mean_scores)
    print("\n" + "-"*50 + "\n")

#import os
#import pandas as pd
#from bs4 import BeautifulSoup
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#
## Ensure NLTK's VADER lexicon is available
#import nltk
#nltk.download('vader_lexicon')
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
## Assuming 'html_tables' is populated with the necessary data, let's proceed with sentiment analysis
#sid = SentimentIntensityAnalyzer()
#
## Example dataframe creation from parsed HTML tables (pseudo code, replace with actual parsing logic)
#news_data = []  # Replace with actual data extraction from html_tables
#
#for file_name, html_table in html_tables.items():
#    for row in html_table.find_all('tr'):
#        columns = row.find_all('td')
#        if len(columns) > 1:  # Assuming at least two columns for date and headline
#            date = columns[0].text.strip()
#            headline = columns[1].text.strip()
#            news_data.append({'date': date, 'headline': headline, 'company': 'fb'})  # Replace 'FB' with actual company
#
#news_df = pd.DataFrame(news_data)
#
## Perform sentiment analysis
#news_df['scores'] = news_df['headline'].apply(lambda x: sid.polarity_scores(x))
#news_df = pd.concat([news_df.drop(['scores'], axis=1), news_df['scores'].apply(pd.Series)], axis=1)
#
## Convert 'date' column to datetime
#news_df['date'] = pd.to_datetime(news_df['date'], errors='coerce').dt.date
#
## Drop rows with invalid dates
#news_df = news_df.dropna(subset=['date'])
#
## Group by 'date' and 'company', and calculate the mean of the numeric columns
#numeric_columns = news_df.select_dtypes(include='number').columns
#mean_scores = news_df.groupby(['date', 'company'])[numeric_columns].mean().unstack(level=1)
#
#print(mean_scores)
#