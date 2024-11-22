class Homework:
    def __init__(self, subject_name, title, due_date, description=None):
        self.subject_name = subject_name
        self.title = title
        self.due_date = due_date
        self.description = description

    def to_dict(self):
        return {
            "subject_name": self.subject_name,
            "title": self.title,
            "due_date": self.due_date,
            "description": self.description
        }