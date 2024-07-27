import requests
import webvtt
from openai import OpenAI

# change

client = OpenAI(api_key='sk-proj-5za883KvzW8wZfUxNyIET3BlbkFJRFZlBSvLOpgcySSiZk65')
import os

# Set up OpenAI API key

# Change from frontend

def get_transcript(vtt_url):
    response = requests.get(vtt_url)
    with open('transcript.vtt', 'wb') as file:
        file.write(response.content)

    transcript = ''
    for caption in webvtt.read('transcript.vtt'):
        transcript += caption.text + ' '

    return transcript

def summarize_transcript(transcript):
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": f"Summarize the following transcript into key points. Transcriptions may include topics like important date dates such as due date, small tasks, things to submit and important people. Be sure to include these :\n\n{transcript}"}
    ],
    max_tokens=200,
    n=1,
    stop=None,
    temperature=0.5)
    summary = response.choices[0].message.content.strip()
    return summary

def interact_with_summary(summary):
    print("\nSummary of the Transcript:\n")
    print(summary)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summary: {summary}\n\nUser: {user_input}"}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5)
        answer = response.choices[0].message.content.strip()
        print(f"AI: {answer}")

def main():
    # Replace with your actual VTT URL
    vtt_url = input("Enter the VTT file URL: ")

    print("Fetching the transcript...")
    transcript = get_transcript(vtt_url)

    print("Summarizing the transcript...")
    summary = summarize_transcript(transcript)

    print("You can now interact with the summary. Type 'exit' or 'quit' to end the conversation.")
    interact_with_summary(summary)

if __name__ == "__main__":
    main()
