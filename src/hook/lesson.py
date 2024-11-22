class Lesson:
    def __init__(self, period, subject_name, teacher_name):
        self.period = period
        self.subject_name = subject_name
        self.teacher_name = teacher_name

    def to_dict(self):
        return {
            "period": self.period,
            "subject_name": self.subject_name,
            "teacher_name": self.teacher_name,
        }