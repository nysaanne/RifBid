import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Read the CSV file into a DataFrame
csv_file_path = os.path.abspath(r'C:\Users\nysap\scraped_data.csv')
df = pd.read_csv(csv_file_path)

# Replace NaN values with empty strings
df.fillna('', inplace=True)

# Add line breaks to the description
df['Description'] = df['Description'].str.replace('\n', '<br>')

# Filter out columns with all empty strings
df_filtered = df.loc[:, df.apply(lambda col: col.str.strip().astype(bool).any(), axis=0)]

@app.route('/search')
def search_tenders():
    query = request.args.get('query', '').strip().lower()  # Get the search query from the URL parameter

    # Filter the DataFrame based on the search query
    df_filtered = df[df.apply(lambda row: any(query in str(row[col]).lower() for col in df.columns), axis=1)]

    if len(df_filtered) == 0:
        # No search results found, display a message
        return render_template('index.html', message="No results found.")

    # Search results found, display them
    return render_template('index.html', table=df_filtered, query=query)


@app.route('/')
def display_data():
    return render_template('index.html', table=df_filtered)

if __name__ == '__main__':
    app.run(debug=True)



    


