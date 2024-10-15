import openai

# Set up your OpenAI API key
openai.api_key = 'your-api-key-here'
# set in powershell: $Env:OPENAI_API_KEY = 'your-api-key-here'
# check if set: echo $Env:OPENAI_API_KEY


def summarize_text(text):
    """Summarize the given text using OpenAI API"""
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or 'gpt-3.5-turbo'
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize this: {text}"}
        ],
        max_tokens=150,  # Adjust this for longer summaries if needed
        temperature=0.5  # Set creativity level
    )
    # Extract and return the summary
    return response['choices'][0]['message']['content']


def summarize_multiple_texts(text_list):
    """Summarize multiple texts"""
    summaries = []
    for text in text_list:
        summary = summarize_text(text)
        summaries.append(summary)
    return summaries


if __name__ == "__main__":
    # List of texts to summarize
    texts_to_summarize = [
        "Text 1 content goes here...",
        "Text 2 content goes here...",
        # Add more texts as needed
    ]
    
    # Get the summaries
    summaries = summarize_multiple_texts(texts_to_summarize)

    # Display the summaries
    for i, summary in enumerate(summaries, 1):
        print(f"Summary {i}: {summary}\n")



