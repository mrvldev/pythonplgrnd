import random

options = ["rock", "paper", "scissor"]
user_score = 0
computer_score = 0
rounds = 5

print("=== Rock, Paper, Scissor 5 Rounds Game ===")

for i in range(rounds):
    user_choice = input("Enter your choice (rock, paper, scissor): ").lower()
    if user_choice not in options:
        print("Invalid choice! Please choose rock, paper, or scissor.")
        continue

    computer_choice = random.choice(options)
    print(f"Computer chose: {computer_choice}")

    if user_choice == computer_choice:
        print("It's a tie!")
    elif (user_choice == "rock" and computer_choice == "scissor") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissor" and computer_choice == "paper"): 
        print("You win this round!")
        user_score += 1
    else:
        print("Computer wins this round!")
        computer_score += 1


print("\n=== Final Scores ===")
print(f"Your Score: {user_score}")
print(f"Computer Score: {computer_score}")  
if user_score > computer_score:
    print("Congratulations! You won the game!")
elif user_score < computer_score:
    print("Computer won the game! Better luck next time.")
else:
    print("The game is a tie!") 
