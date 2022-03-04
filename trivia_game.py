import os
import json
from operator import itemgetter
from datetime import datetime
from random import shuffle
from prettytable import PrettyTable

from art import logo, game_over
from question_model import Question
from quiz_brain import QuizBrain
from data_fetcher import DataFetcher


def get_leaderboard_data(post_game_dict, json_file):
    """ Returns leaderboard data as a JSON object."""
    with open(json_file, 'r') as f:
        game_data = json.load(f)

    new_game_data = [post_game_dict]
    for game_dictionary in game_data:
        new_game_data.append(game_dictionary)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(new_game_data, f, sort_keys=True, indent=4)

    with open(json_file, 'r', encoding='utf-8') as f:
        leaderboard_data_json = json.load(f)

    return sorted(leaderboard_data_json, key=itemgetter('score'), reverse=True)


def show_leaderboard(leaderboard_data_json):
    see_leaderboard = input("\nPress 'L' to see the leaderboard. ").lower()
    if see_leaderboard == 'l':
        leaderboard = PrettyTable()
        leaderboard.field_names = ["Player", "Score", "Difficulty", "Date"]
        for game_dict in leaderboard_data_json[:10]:
            leaderboard.add_row([
                game_dict['player'],
                game_dict['score'],
                game_dict['difficulty'],
                game_dict['date'],
            ])
        leaderboard.sortby = "Score"
        leaderboard.reversesort = True
        print(f"\n{leaderboard}")


def get_post_game_data(player, category, difficulty, score, date):
    """Returns a dictionary of post game data to build the leaderboard."""
    return {
        'player': player,
        'category': category,
        'difficulty': difficulty,
        'score': score,
        'date': date.strftime("%d/%m/%y %H:%M:%S"),
            }


# Input name, select category, difficulty, number of questions
print(logo)
player_name = input("Your name: ")

print("\n---------- Categories Available ----------\n")
category_url = 'https://opentdb.com/api_category.php'
category_file = r'C:\users\montv\python_work\100_days_of_code\day_17\quiz_categories.json'

category_data_fetcher = DataFetcher(category_url, category_file)
get_categories = category_data_fetcher.make_api_call()
list_of_category_dicts = category_data_fetcher.convert_to_json(get_categories)

for category_dict in list_of_category_dicts['trivia_categories']:
    print(category_dict['id'], category_dict['name'])
print("\n------------------------------------------")

selected_category = int(input("\nSelect a category number from list above: "))

for dictionary in list_of_category_dicts['trivia_categories']:
    if dictionary['id'] == selected_category:
        category_name = dictionary['name']

selected_difficulty = input("\nSelect a question difficulty (Easy/Medium/Hard/Mixed): ").lower()

number_questions = int(input("\nSelection a number of questions (10/20/30): "))

# Create API URL from user parameters
if selected_difficulty == 'mixed':
    question_url = f"https://opentdb.com/api.php?amount={number_questions}&category={selected_category}&type=multiple"
else:
    question_url = f"https://opentdb.com/api.php?amount={number_questions}&category={selected_category}" \
                   f"&difficulty={selected_difficulty}&type=multiple"

question_file = r'C:\users\montv\python_work\100_days_of_code\day_17\quiz_questions.json'

# Input user parameters to filter through the list of category questions
question_data_fetcher = DataFetcher(question_url, question_file)
get_questions = question_data_fetcher.make_api_call()
list_of_question_dicts = question_data_fetcher.convert_to_json(get_questions)

question_bank = []
for question in list_of_question_dicts['results']:
    new_question = Question(question['question'], question['correct_answer'], question['incorrect_answers'])
    question_bank.append(new_question)
shuffle(question_bank)

# Begin game
current_date_time = datetime.now()
quiz = QuizBrain(question_bank)
while quiz.questions_remaining():
    os.system('cls')
    print(logo)

    print(f"\nPlayer - {player_name}")
    print(f"\nCategory - {category_name}")
    print(f"\nDifficulty - {selected_difficulty.title()}")
    print(f"\n\nCurrent Score - {quiz.calculate_score()}\n")

    answer = quiz.ask_question()
    quiz.check_answer(answer)
    game_continue = input("Press any key to continue, or press 'q' to quit. ")
    if game_continue == 'q':
        break

# End game and write to leaderboard
os.system('cls')
print(game_over)
final_score = quiz.calculate_score()
print(f"\n\nFinal Score: {final_score}\n\nThanks for playing!")

high_score_file = r'C:\users\montv\python_work\100_days_of_code\day_17\quiz_high_scores.json'
post_game_data = get_post_game_data(player_name, selected_category, selected_difficulty, final_score, current_date_time)
leaderboard_data = get_leaderboard_data(post_game_data, high_score_file)
show_leaderboard(leaderboard_data)
