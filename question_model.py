class Question:
    """A class to manage questions in the quiz app."""

    def __init__(self, q_text, q_answer, q_incorrect_answers):
        """Initialize the attributes of a question."""
        self.text = q_text
        self.answer = q_answer
        self.incorrect_answer = q_incorrect_answers
