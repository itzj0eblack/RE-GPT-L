import requests
import time
import sys
import random

RESET = "\033[0m"
BOLD = "\033[1m"
PINK = "\033[95m"
PURPLE = "\033[35m"
WHITE = "\033[97m"

banner = rf"""{BOLD}{PINK}
  _____________________________      .____     
 /  _____/\______   \__    ___/      |    |    
/   \  ___ |     ___/ |    |  ______ |    |    
\    \_\  \|    |     |    | /_____/ |    |___ 
 \______  /|____|     |____|         |_______ \\
        \/                                   \/
{RESET}
"""

print(banner)

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
  
welcome_messages = [
    "Hello! How can I assist you today?",
    "Welcome! I'm here to help. What do you need?",
    "Hi there! Ask me anything.",
    "Greetings! I am GPT-L created by Oslositz. How can I help you today?",
    "Hey! Let's get started. What would you like to know?",
    "Hello! GPT-L here, crafted by Oslositz. How can I assist you?",
    "Welcome! Powered by Oslositz's expertise. What do you need today?"
]

typing_animation(random.choice(welcome_messages), prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)

network_error_messages = [
    "Please check your network so that I can work properly.",
    "Unable to connect to the internet. Kindly verify your connection.",
    "Network error detected. Please reconnect and try again.",
    "Oops! Looks like there’s a network issue. Check your connection.",
    "Connection failed. Make sure you have internet access."
]

while True:
    try:
        user_input = input(f"{BOLD}{PURPLE}You>{RESET} ")

        if user_input.lower() == "exit":
            typing_animation("Goodbye! Have a nice day!", prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)
            break

        url = f"https://text.pollinations.ai/{user_input}"

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                content = response.text
                typing_animation(content, prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)
            else:
                typing_animation("No content found for your request.", prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)
        except requests.exceptions.RequestException:
            error_message = random.choice(network_error_messages)
            typing_animation(error_message, prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)
    except KeyboardInterrupt:
        typing_animation("Session terminated by user.", prefix="GPT-L> ", prefix_color=PINK, text_color=WHITE)
        break
