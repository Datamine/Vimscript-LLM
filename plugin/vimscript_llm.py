import sys
import os
from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import pynvim
import subprocess


def log(message):
    with open("/Users/v/llm-log", "a") as f:
        f.write(message + "\n")

# def is_valid_vim_command(command):
#     try:
#         nvim = pynvim.attach('child', argv=["nvim", "--headless"])
#         nvim.command(command)
#         return True
#     except Exception as e:
#         print(f"Error: {e}")  # This will help us understand why a command might be invalid
#         return False
#     finally:
#         if 'nvim' in locals():
#             nvim.quit()
#

def is_valid_vim_command(command):
    try:
        result = subprocess.run(['vim', '--headless', '-es', '-c', f'silent! {command}',
                                 '-c', 'if v:errmsg != "" | cquit | else | quit | endif'],
                                check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False



def generate_output(args):
    # Combine the arguments into a single string
    prompt = " ".join(args)

    # Prepare the message for the API
    messages = [
        {"role": "system", "content": "You are an assistant that generates valid Vim commands. You may only generate vanilla Vim commands. Do not output any commands that would require a Vim plugin. Respond with only the command, no explanations. Place the command inside backticks ```."},
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
        log("New Response")
        log(command)

        # Ensure the response is a single line (Vim commands are typically single-line)
        #command = command.split('\n')[]
        command = command.strip("`")
        if command.startswith(":"):
            command = command[1:]

        return command

    except Exception as e:
        return f"Error: {str(e)}"


def generate_command(args):
    attempt = 0
    while attempt < 10:
        attempted_command = generate_output(args)
        log(attempted_command)
        if is_valid_vim_command(attempted_command):
            log("valid")
            return attempted_command
        else:
            log("invalid")

    return "Error: could not generate command!"


if __name__ == "__main__":
    args = sys.argv[1:]  # Get all arguments passed to the script
    output = generate_command(args)
    print(output, end='')
    sys.stdout.flush()
