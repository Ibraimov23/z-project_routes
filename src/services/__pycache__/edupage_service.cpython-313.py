�
    /?g^  �                   �$   � S SK Jr   " S S5      rg)�    )�Edupagec                   �2   � \ rS rSrS rS rS rS rS rSr	g)	�EdupageService�   c                 �"   � [        5       U l        g )N)r   �edupage)�selfs    �J   c:\Users\Nursultan\Desktop\проект-бот\services\edupage_service.py�__init__�EdupageService.__init__   s   � ��y���    c                 �<   � U R                   R                  XS5        g)u1   Авторизация в системе Edupage.zauca.kgN)r   �login)r	   �username�passwords      r
   r   �EdupageService.login   s   � ������8�y�9r   c                 �:   � U R                   R                  5       nU$ )u    Получение оценок.)r   �
get_grades)r	   �gradess     r
   r   �EdupageService.get_grades   s   � ����(�(�*���r   c                 �   � U R                   R                  5       nU Vs/ sH  o"R                  S:X  d  M  UPM     nnU$ s  snf )u5   Получение домашнего задания.�HOMEWORK)r   �get_notifications�
event_type)r	   �homework�hws      r
   �get_homework�EdupageService.get_homework   s<   � ��<�<�1�1�3��!)�I��2�]�]�j�-H�B���I���� Js   �?�?c                 �<   � U R                   R                  U5      nU$ )u(   Получение расписания.)r   �get_my_timetable)r	   �date�	timetables      r
   �get_timetable�EdupageService.get_timetable   s   � ��L�L�1�1�$�7�	��r   )r   N)
�__name__�
__module__�__qualname__�__firstlineno__r   r   r   r   r#   �__static_attributes__� r   r
   r   r      s   � �!�:��
�r   r   N)�edupage_apir   r   r*   r   r
   �<module>r,      s   �� �� r   