import random

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

if __name__ == "__main__":
    main()
