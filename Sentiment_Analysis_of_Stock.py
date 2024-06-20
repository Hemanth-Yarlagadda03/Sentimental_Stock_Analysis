import os
import pandas as pd
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt

# Ensure NLTK's VADER lexicon is available
nltk.download('vader_lexicon')

# Initialize the dictionary to store HTML tables
html_tables = {}

# Define the datasets directory
datasets_dir = 'C:/Users/kowshik/Study/Projects/sentiment/datasets'
output_dir = 'C:/Users/kowshik/Study/Projects/sentiment/visualizations'

# Check if the output directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Check if the datasets directory exists
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

# Define the sentiment classification function
def classify_sentiment(current, previous):
    if current > 0.5 and previous <= 0.5:
        return 'buy'
    elif current < 0.0 and previous >= 0.0:
        return 'sell'
    else:
        return 'hold'

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

    # Prepare data for classification and visualization
    mean_scores_flat = mean_scores.stack(level=1).reset_index()
    mean_scores_flat['previous_compound'] = mean_scores_flat.groupby('company')['compound'].shift(1)
    mean_scores_flat['decision'] = mean_scores_flat.apply(
        lambda row: classify_sentiment(row['compound'], row['previous_compound']), axis=1)

    # Print the decisions
    print(f"Decisions based on sentiment scores for {company_name} from {file_name}:")
    print(mean_scores_flat[['date', 'company', 'compound', 'decision']])

    # Determine the final decision based on recent sentiment (e.g., last 3 days)
    recent_decisions = mean_scores_flat.tail(3)['decision']
    final_decision = 'buy' if 'buy' in recent_decisions.values else 'sell' if 'sell' in recent_decisions.values else 'hold'
    
    print(f"Final Decision for {company_name} from {file_name}: {final_decision}")
    print("\n" + "="*50 + "\n")

    # Visualization
    for company in mean_scores.columns.levels[1]:
        plt.figure(figsize=(14, 7))
        plt.plot(mean_scores.index, mean_scores['compound', company], marker='o', label=f'{company} Compound Score')
        plt.axhline(y=0.5, color='g', linestyle='--', label='Buy Threshold')
        plt.axhline(y=0.0, color='y', linestyle='--', label='Hold Threshold')
        plt.axhline(y=-0.0, color='r', linestyle='--', label='Sell Threshold')
        plt.title(f'Compound Sentiment Scores for {company}')
        plt.xlabel('Date')
        plt.ylabel('Compound Score')
        plt.legend()
        plt.grid(True)

        # Highlight buy/sell points
        buy_points = mean_scores_flat[(mean_scores_flat['company'] == company) & (mean_scores_flat['decision'] == 'buy')]
        sell_points = mean_scores_flat[(mean_scores_flat['company'] == company) & (mean_scores_flat['decision'] == 'sell')]

        plt.scatter(buy_points['date'], buy_points['compound'], color='green', s=100, label='Buy Signal')
        plt.scatter(sell_points['date'], sell_points['compound'], color='red', s=100, label='Sell Signal')

        # Add annotations for buy/sell points
        for i in range(len(buy_points)):
            plt.annotate('Buy', (buy_points['date'].iloc[i], buy_points['compound'].iloc[i]),
                         textcoords="offset points", xytext=(0,10), ha='center', color='green')

        for i in range(len(sell_points)):
            plt.annotate('Sell', (sell_points['date'].iloc[i], sell_points['compound'].iloc[i]),
                         textcoords="offset points", xytext=(0,10), ha='center', color='red')

        # Add final decision text annotation
        plt.text(0.95, 0.01, f"Recommendation: {final_decision}", verticalalignment='bottom', horizontalalignment='right',
                 transform=plt.gca().transAxes, color='blue', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

        # Save the plot
        plot_file_name = f"{company}_{file_name.replace('.html', '')}.png"
        plt.savefig(os.path.join(output_dir, plot_file_name))
        plt.close()

        print(f"Visualization saved for {company_name} as {plot_file_name}")
