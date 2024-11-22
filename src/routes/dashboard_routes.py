from flask import Blueprint, render_template, request, session, redirect, url_for
import asyncio
from hook import Grade, Homework, Lesson
from services import EdupageService, UserDataManager
from datetime import datetime
from collections import defaultdict


dashboard_bp = Blueprint('dashboard', __name__)

edupage_service = EdupageService()
userdata = UserDataManager()

@dashboard_bp.route('', methods=['GET', 'POST'])
def dashboard():
    user = userdata.load_user_data()  
    if not user:
        return redirect(url_for('auth.login'))
    
    if 'grades' not in session:
        session['grades'] = None
    if 'homework' not in session:
        session['homework'] = None
    if 'timetable' not in session:
        session['timetable'] = None
    if 'waiting_for_server' not in session:
        session['waiting_for_server'] = False

    grades = session['grades']
    homework = session['homework']
    timetable = session['timetable']
    waiting_for_server = session['waiting_for_server']
    action = request.form.get('action', None) 

    if request.method == 'POST':
        date = request.form.get('date', None)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    

        try:
            if not edupage_service.is_logged_in():     
                loop.run_until_complete(edupage_service.login(
                    user['username'], user['password'], user['subdomain']
                
                ))
            else:
                print('success.....................................................')
        except Exception as e:
            return render_template('dashboard.html', error=f"Failed to log in: {e}")


        if action == 'Get Grades':
            session['waiting_for_server'] = True
            try:
                grades_data = asyncio.run(edupage_service.get_grades())
                if isinstance(grades_data, list):
                    newgrades = [
                         Grade(
                            subject_name=grade_data.subject_name, 
                            grade_n=grade_data.grade_n,  
                            title=grade_data.title,  
                            max_points=grade_data.max_points if hasattr(grade_data, 'max_points') else None,
                            percent=grade_data.percent if hasattr(grade_data, 'percent') else None
                        ) for grade_data in grades_data
                    ]

                    grades_by_subject = {}
                    for grade in newgrades:
                        if grade.subject_name not in grades_by_subject:
                            grades_by_subject[grade.subject_name] = []
                        grades_by_subject[grade.subject_name].append(grade.to_dict())
                
                    session['grades'] = grades_by_subject
                else:
                    session['grades'] = "Error: Grades data is not a list or is empty."
            except Exception as e:
                session['grades'] = f"Error fetching grades: {e}"
            finally:
                session['waiting_for_server'] = False

        elif action == 'Get Homework':
            waiting_for_server = True  
            try:
                homework_data = asyncio.run(edupage_service.get_homework())  
                if isinstance(homework_data, list):
                    newhomeworks = [
                         Homework(  
                            subject_name=hw.recipient,  
                            title=hw.additional_data.get('nazov', 'No title'), 
                            due_date=datetime.strptime(hw.additional_data.get('date', ''), '%Y-%m-%d') if hw.additional_data.get('date') else None, 
                            description=hw.additional_data.get('popis', None) 
                            ) for hw in homework_data 
                    ]

                    homework_by_subject = {}
                    for hw in newhomeworks:  
                        if hw.subject_name not in homework_by_subject:
                            homework_by_subject[hw.subject_name] = []
                        homework_by_subject[hw.subject_name].append(hw.to_dict()) 
    
                    session['homework'] = homework_by_subject

                else:
                    session['homework'] = "Error: Homework data is not a list or is empty."
            except Exception as e:
                session['homework'] = f"Error fetching homework: {e}"  
            finally:
                waiting_for_server = False
        
        elif action == 'Get Timetable':
            waiting_for_server = True  
            try:
                if not date:
                    date = datetime.today().date()
                else:
                    date = datetime.strptime(date, '%Y-%m-%d').date()

                timetable_data = asyncio.run(edupage_service.get_timetable(date))

                if isinstance(timetable_data, list) and timetable_data:
                    lessons = [
                        Lesson(
                        lesson["period"],
                        lesson["subject_name"],
                        lesson["teacher_name"]
                    )
                        for lesson in timetable_data
                    ]

                    timetable_by_subject = defaultdict(list)

                    for lesson in lessons:
                        timetable_by_subject[lesson.subject_name].append(lesson.to_dict())

                    session['timetable'] = dict(timetable_by_subject)
                else:
                    session['timetable'] = "Error: Your schedule list data is missing"
            except Exception as e:
                session['timetable'] = f"Error fetching timetable: {e}"  
            finally:
                waiting_for_server = False

        timetable = session.get('timetable')

    if action == 'Get Grades':
            return render_template('dashboard.html', grades=session['grades'], waiting_for_server=waiting_for_server, title = 'Оценки')
    elif action == 'Get Homework':
            return render_template('dashboard.html', homework=session['homework'], waiting_for_server=waiting_for_server, title = 'Домашки')
    elif action == 'Get Timetable':
            return render_template('dashboard.html', timetable=session['timetable'], waiting_for_server=waiting_for_server, title = 'Сегодняшние пары')

    return render_template('dashboard.html', grades=session['grades'], homework=session['homework'], timetable=session['timetable'], waiting_for_server=session['waiting_for_server'])
