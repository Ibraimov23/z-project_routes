from edupage_api import Edupage
from edupage_api.timeline import EventType
import traceback
import asyncio

class EdupageService:
    def __init__(self):
        self.edupage = Edupage()
    async def login(self, username, password, subdomain):
        username += '@auca.kg'
        return await asyncio.to_thread(self.edupage.login, username, password, subdomain)

    def is_logged_in(self):
        return self.edupage is not None and self.edupage.is_logged_in

    async def get_grades(self):
        if not self.edupage.is_logged_in:
            raise Exception("User is not logged in. Please log in first.")
        try:
            print("Fetching grades...")
            grades = await asyncio.to_thread(self.edupage.get_grades)  
            if grades:
                print("Grades fetched successfully:", grades)
            else:
                print("No grades returned by the API.")
            return grades
        except Exception as e:
            print(f"An error occurred while fetching grades: {e}")
        traceback.print_exc()
        return None

    async def get_homework(self):
        if not self.edupage.is_logged_in:
            raise Exception("User is not logged in. Please log in first.")
        try:
            print("Fetching homework...")
            notifications = await asyncio.to_thread(self.edupage.get_notifications)
        
            homework = list(filter(lambda x: x.event_type == EventType.HOMEWORK, notifications))
        
            return homework
        except Exception as e:
            print(f"An error occurred while fetching homework: {e}")
        traceback.print_exc()
        return None

    async def get_timetable(self, date):
        if not self.edupage.is_logged_in:
            raise Exception("User is not logged in. Please log in first.")   
        try:
            print("Fetching timetable...")
            timetable = await asyncio.to_thread(self.edupage.get_my_timetable, date)
        
            lessons = []
            for lesson in timetable:
                teacher_names = []
                if lesson.teachers: 
                    teacher_names = [teacher.name for teacher in lesson.teachers] 
                teacher_name = ", ".join(teacher_names) if teacher_names else "No teacher assigned"
                lessons.append({
                    'period': lesson.period,
                    'subject_name': "".join(lesson.subject.name),
                    'teacher_name': "".join(teacher_name)
                })
            return lessons
        except Exception as e:
            print(f"An error occurred while fetching timetable: {e}")
            traceback.print_exc()
        return None
    
