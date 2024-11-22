class Grade:
    def __init__(self, subject_name, grade_n, title, max_points=None, percent=None):
        self.subject_name = subject_name
        self.grade_n = grade_n
        self.title = title
        self.max_points = max_points
        self.percent = percent

    def to_dict(self):
        return {
            "subject_name": self.subject_name,
            "grade_n": self.grade_n,
            "title": self.title,
            "max_points": self.max_points,
            "percent": self.percent
        }
