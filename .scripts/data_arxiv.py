import urllib.request
import xml.etree.ElementTree as ET
from pdfminer.high_level import extract_text


# Function to query arXiv API
def query_arxiv(start_index=0, max_results=10):
    url = (
        f"http://export.arxiv.org/api/query?search_query=cat:physics.gen-ph"
        f"&start={start_index}&max_results={max_results}"
    )
    with urllib.request.urlopen(url) as response:
        data = response.read()
    return data


# Function to parse XML and extract paper information
def parse_arxiv_data(data):
    papers = []

    # Define the namespace for Atom XML
    namespace = {"atom": "http://www.w3.org/2005/Atom"}

    # Parse the XML response
    root = ET.fromstring(data)

    # Find all entry elements (each paper is represented as an entry)
    for entry in root.findall(
         "atom:entry", namespace):
        title = entry.find(
            "atom:title", namespace).text
        abstract = entry.find(
            "atom:summary", namespace).text
        pdf_url = entry.find(
            'atom:link[@title="pdf"]', namespace).attrib["href"]
        papers.append({
            "title": title, "abstract": abstract, "pdf_url": pdf_url})

    return papers


# Function to download PDF
def download_pdf(pdf_url, file_name):
    urllib.request.urlretrieve(pdf_url, file_name)
    print(f"Downloaded PDF: {file_name}")


# Function to extract text from a PDF using PDFMiner
def extract_text_from_pdf(pdf_file):
    # Use PDFMiner to extract text from the PDF
    try:
        text = extract_text(pdf_file)
        return text
    except Exception as e:
        print(f"Failed to extract text from {pdf_file}: {e}")
        return ""


# Example usage to get papers, download PDFs, and extract text
def main():
    data = query_arxiv(0, 5)  # Get 5 papers from arXiv
    # print(f"Raw API response: {data}")
    # Decode the response to a string and print it nicely
    decoded_data = data.decode("utf-8")
    print(f"Raw API response:\n{decoded_data}")

    papers = parse_arxiv_data(data)
    print(f"Parsed papers: {papers}")

    for idx, paper in enumerate(papers):
        print(f"\nPaper {idx + 1}: {paper['title']}")
        print(f"Abstract: {paper['abstract']}")

        # Download the PDF
        pdf_file_name = f"paper_{idx + 1}.pdf"
        download_pdf(paper["pdf_url"], pdf_file_name)

        # Extract text from the downloaded PDF using PDFMiner
        pdf_text = extract_text_from_pdf(pdf_file_name)
        print(
            f"Extracted Text from PDF: {pdf_text[:500]}..."
        )  # Print first 500 characters of the text


if __name__ == "__main__":
    main()
