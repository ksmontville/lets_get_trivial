from random import shuffle


class QuizBrain:
    """A class to manage the logic in the quiz app."""

    def __init__(self, question_bank):
        """Initialize the attributes of the quiz module."""
        self.question_bank = question_bank
        self.question_number = 0
        self.score = 0

    def ask_question(self):
        """Ask the user a numbered question from a bank of questions. Returns user answer as a string."""
        print(f"Question {self.question_number + 1}. {self.question_bank[self.question_number].text}\n")

        answer_choices = [
            self.question_bank[self.question_number].answer,
            self.question_bank[self.question_number].incorrect_answer[0],
            self.question_bank[self.question_number].incorrect_answer[1],
            self.question_bank[self.question_number].incorrect_answer[2],
        ]

        shuffle(answer_choices)

        answer_dict = {
            '1': answer_choices[0],
            '2': answer_choices[1],
            '3': answer_choices[2],
            '4': answer_choices[3]
        }

        for key, value in answer_dict.items():
            print(f"{key}. {value}")

        return answer_dict

    def questions_remaining(self):
        """Returns True if there are questions in the question bank, else returns False."""
        return self.question_number < len(self.question_bank)

    def check_answer(self, answer_dict):
        """Checks the users answer against the correct answer. If correct, return True. Else return False."""
        try:
            answer = input("\nAnswer: ").lower()
            if answer_dict[answer] == self.question_bank[self.question_number].answer:
                print("\nCorrect!")
                self.score += 1
                self.question_number += 1
                return True
            else:
                print("\nIncorrect.")
                print(f"\nThe correct answer was '{self.question_bank[self.question_number].answer}'.")
                self.question_number += 1
                return False
        except KeyError:
            print("\nInvalid selection.")

    def calculate_score(self):
        percent_score = int((self.score/len(self.question_bank)) * 100)
        return f"{percent_score} %"
