import requests
import time
import sys
import random

# ANSI color codes for console text formatting
RESET = "\033[0m"
BOLD = "\033[1m"
PINK = "\033[95m"
PURPLE = "\033[35m"
WHITE = "\033[97m"
SUCCESS = "\033[32m"
ERROR = "\033[31m"
INFO = "\033[34m"

# Chat bubble styling
def create_chat_bubble(message, sender="User"):
    if sender == "GPT-L":
        return f"{PINK}[GPT-L] >{RESET} {message}"
    else:
        return f"{PURPLE}[You] >{RESET} {message}"

# Function to simulate typing animation
def typing_animation(text, prefix="", prefix_color=WHITE, text_color=WHITE, normal_delay=0.05, fast_delay=0.005, pause_chance=0.15, short_pause=0.1, long_pause=1.5):
    pause_counter = 0
    speeding_up = False
    speed_up_end_time = 0

    sys.stdout.write(f"{BOLD}{prefix_color}{prefix}{RESET}{text_color}")
    sys.stdout.flush()

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()

        current_time = time.time()

        if speeding_up:
            if current_time < speed_up_end_time:
                time.sleep(fast_delay)
            else:
                speeding_up = False
                time.sleep(normal_delay)
        else:
            time.sleep(normal_delay)

        if random.random() < pause_chance:
            if pause_counter >= random.randint(3, 7):
                pause_duration = random.uniform(0.5, long_pause)
                pause_counter = 0
            else:
                pause_duration = random.uniform(0.05, short_pause)
                pause_counter += 1

            time.sleep(pause_duration)
            speeding_up = True
            speed_up_duration = random.uniform(0.2, 0.5)
            speed_up_end_time = current_time + speed_up_duration

    print(RESET)

# Function to get multiline input from user
def get_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

# Welcome messages
welcome_messages = [
    "Hello! How can I assist you today?",
    "Welcome! I'm here to help. What do you need?",
    "Hi there! Ask me anything.",
    "Greetings! I am GPT-L created by Oslositz. How can I help you today?",
    "Hey! Let's get started. What would you like to know?",
    "Hello! GPT-L here, crafted by Oslositz. How can I assist you?",
    "Welcome! Powered by Oslositz's expertise. What do you need today?"
]

# Display welcome message
typing_animation(random.choice(welcome_messages), prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)

# Network error messages
network_error_messages = [
    "Please check your network so that I can work properly.",
    "Unable to connect to the internet. Kindly verify your connection.",
    "Network error detected. Please reconnect and try again.",
    "Oops! Looks like there’s a network issue. Check your connection.",
    "Connection failed. Make sure you have internet access."
]

while True:
    try:
        user_input = get_multiline_input(f"{BOLD}{PURPLE}You>{RESET} ")

        if user_input.lower() == "exit":
            typing_animation("Goodbye! Have a nice day!", prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)
            time.sleep(1)
            break
        elif user_input.lower() == "help":
            help_message = """
Available commands:
- exit: Exit the program.
- help: Display this help message.
"""
            typing_animation(help_message, prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)
            continue

        url = f"https://text.pollinations.ai/{user_input}"

        try:
            # Make the request without the loading animation
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            content = response.text.strip()

            # Check if the response contains valid content or HTML
            if content.startswith("<!DOCTYPE html>") or "html" in content:
                typing_animation(f"{ERROR}It seems there was an issue with the request. Please try again.{RESET}", prefix="GPT-L> ", prefix_color=PINK, text_color=ERROR)
            else:
                typing_animation(content, prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)

        except requests.exceptions.HTTPError as e:
            typing_animation(f"{ERROR}API Error: {e}{RESET}", prefix="GPT-L> ", prefix_color=PINK, text_color=ERROR)
        except requests.exceptions.Timeout:
            typing_animation(f"{ERROR}Request timed out. Please try again.{RESET}", prefix="GPT-L> ", prefix_color=PINK, text_color=ERROR)
        except requests.exceptions.RequestException as e:
            error_message = random.choice(network_error_messages)
            typing_animation(f"{ERROR}{error_message}{RESET}", prefix="GPT-L> ", prefix_color=PINK, text_color=ERROR)

    except KeyboardInterrupt:
        typing_animation(f"{ERROR}Session terminated by user.{RESET}", prefix="GPT-L> ", prefix_color=PINK, text_color=ERROR)
        break
