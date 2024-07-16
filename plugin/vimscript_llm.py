import sys
import os
from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_output(args):
    # Combine the arguments into a single string
    prompt = " ".join(args)

    # Prepare the message for the API
    messages = [
        {"role": "system", "content": "You are an assistant that generates valid Vim commands. Respond with only the command, no explanations."},
        {"role": "user", "content": f"Generate a single valid Vim command that does the following: {prompt}"}
    ]

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Using the latest GPT-4 model
            messages=messages,
            max_tokens=100,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the generated command
        command = response.choices[0].message.content.strip()
        with open("/Users/v/llm-log", "a") as f:
            f.write("New Response")
            f.write(command + "\n")

        # Ensure the response is a single line (Vim commands are typically single-line)
        command = command.split('\n')[0]
        if command.startswith(":"):
            command = command[1:]

        return command

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    args = sys.argv[1:]  # Get all arguments passed to the script
    output = generate_output(args)
    print(output, end='')
    sys.stdout.flush()
