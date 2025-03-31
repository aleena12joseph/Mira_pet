[10:02 PM, 3/26/2025] Sneha.D: import random

def generate_number(lower=1, upper=15):
    """Generate a random number between lower and upper limits."""
    return random.randint(lower, upper)

def get_user_guess():
    """Get user input (with validation)."""
    while True:
        guess = input("Enter your guess: ").strip()
        if guess.isdigit():
            return int(guess)
        print("Invalid input. Please enter a valid number.")

def check_guess(guess, target):
    """Compare guess with target and return feedback."""
    if guess < target:
        return "Too low!"
    elif guess > target:
        return "Too high!"
    else:
        return "Correct!"

def play_game(difficulty):
    """Main game logic."""
    if difficulty == "Easy":
        lower, upper = 1, 10
    elif dif…
[10:02 PM, 3/26/2025] Sneha.D: guessing game nte code
[10:03 PM, 3/26/2025] Aleena: Level okke choikkano
[10:03 PM, 3/26/2025] Aleena: Just otta level pore
[10:04 PM, 3/26/2025] Sneha.D: chat gpt thannu njan ayachu
[10:07 PM, 3/26/2025] Sneha.D: import random

def generate_number(lower, upper):
    return random.randint(lower, upper)

def get_user_guess():
    while True:
        guess = input("Enter your guess: ").strip()
        if guess.isdigit():
            return int(guess)
        print("Invalid input. Please enter a valid number.")

def check_guess(guess, target):
    if guess < target:
        return "Too low!"
    elif guess > target:
        return "Too high!"
    else:
        return "Correct!"

def play_game():
    lower, upper = 1, 10
    target = generate_number(lower, upper)
    print("Guess a number between 1 and 10:")
    while True:
        guess = get_user_guess()
        result = check_guess(guess, target)
        print(result)
        if result == "Correct!":
            break

def main():
    while True:
        play_game()
        play_again = input("Play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            break

if _name_ == "_main_":
    main()
