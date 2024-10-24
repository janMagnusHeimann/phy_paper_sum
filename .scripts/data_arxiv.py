import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd
from pdfminer.high_level import extract_text
import os

# Function to query arXiv API with a broader search (across all categories)
def query_arxiv(start_index=0, max_results=10):
    base_url = 'http://export.arxiv.org/api/query'
    query_params = {
        'search_query': 'all',  # Broad search across all categories
        'start': start_index,
        'max_results': max_results
    }
    query_string = urllib.parse.urlencode(query_params)
    url = f'{base_url}?{query_string}'
    
    with urllib.request.urlopen(url) as response:
        data = response.read()
    return data

# Function to parse XML and extract paper information
def parse_arxiv_data(data):
    papers = []
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    
    root = ET.fromstring(data)
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace).text
        abstract = entry.find('atom:summary', namespace).text
        pdf_url = None
        for link in entry.findall('atom:link', namespace):
            if link.attrib.get('title') == 'pdf':
                pdf_url = link.attrib['href']
                break
        papers.append({'title': title, 'abstract': abstract, 'pdf_url': pdf_url})
    
    print(f"Parsed {len(papers)} papers.")
    return papers

# Function to download PDF
def download_pdf(pdf_url, file_name):
    urllib.request.urlretrieve(pdf_url, file_name)
    print(f'Downloaded PDF: {file_name}')

# Function to extract text from a PDF using PDFMiner
def extract_text_from_pdf(pdf_file):
    try:
        text = extract_text(pdf_file)
        if text.strip():  # Check if the text is not empty
            print(f"Extracted text from {pdf_file}")
            return text
        else:
            print(f"No text extracted from {pdf_file}")
            return ""
    except Exception as e:
        print(f"Failed to extract text from {pdf_file}: {e}")
        return ""

# Function to process multiple papers and extract text from them
def process_papers(start_index=0, max_results=10):
    data = query_arxiv(start_index, max_results)
    papers = parse_arxiv_data(data)
    dataset = []

    for idx, paper in enumerate(papers):
        print(f"Processing Paper {idx + 1}: {paper['title']}")
        pdf_file_name = f'paper_{idx + 1}.pdf'
        if paper['pdf_url']:
            download_pdf(paper['pdf_url'], pdf_file_name)
            pdf_text = extract_text_from_pdf(pdf_file_name)
            if pdf_text:
                dataset.append({'title': paper['title'], 'abstract': paper['abstract'], 'full_text': pdf_text})
            os.remove(pdf_file_name)  # Clean up the downloaded PDF

    if dataset:
        return pd.DataFrame(dataset)
    else:
        print("No data to save.")
        return pd.DataFrame()

# Example usage: process and save 10 papers
dataframe = process_papers(0, 10)
if not dataframe.empty:
    dataframe.to_csv('processed_papers.csv', index=False)
    print("Processed data saved to 'processed_papers.csv'")
else:
    print("No papers were processed.")

