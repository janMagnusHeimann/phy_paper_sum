# pip install openai

import openai
import time

# Set up your OpenAI API key
# openai.api_key = 'your-api-key-here'

# Free-tier limits for gpt-3.5-turbo
MAX_RPM = 3  # Requests per minute, 3 on free plan
MAX_TOKENS_PER_MIN = 40000  # Tokens per minute, 40000 on free plan


def summarize_text(text):
    """Summarize the given text using OpenAI API."""
    try:
        response = openai.completions.create(  # Correct method for new version
            model="gpt-3.5-turbo",
            # Using prompt instead of messages
            prompt=f"Summarize this: {text}",  
            max_tokens=150,  # Adjust this as needed
            temperature=0.5  # Set creativity level
        )
        return response.choices[0].text.strip()  # Adjusted for the new response structure
    except Exception as e:
        print(f"Error: {e}")
        return None


def summarize_multiple_texts(text_list):
    """Summarize multiple texts with rate limiting."""
    summaries = []
    for i, text in enumerate(text_list):
        if i > 0 and i % MAX_RPM == 0:
            # Wait to respect the RPM rate limit
            print("Rate limit reached. Waiting for 60 seconds...")
            time.sleep(60)

        # Summarize the text
        summary = summarize_text(text)
        if summary:
            summaries.append(summary)
            print(f"Text {i+1} summarized.")
        else:
            print(f"Text {i+1} failed.")
    return summaries


if __name__ == "__main__":
    # Example list of texts to summarize
    texts_to_summarize = [
        "This is the first text to summarize.",
        "Here is another text that needs to be summarized.",
        # Add more texts as needed
    ]
    
    # Get summaries with rate limiting
    summaries = summarize_multiple_texts(texts_to_summarize)

    # Print the summaries
    for i, summary in enumerate(summaries, 1):
        print(f"Summary {i}: {summary}\n")
