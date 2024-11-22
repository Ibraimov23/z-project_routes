from flask import Blueprint, render_template, request, redirect, url_for, session
from services import EdupageService, UserDataManager
from edupage_api.exceptions import BadCredentialsException, CaptchaException
from requests.exceptions import SSLError
import asyncio

auth_bp = Blueprint('auth', __name__)

edupage_service = EdupageService()
userdata = UserDataManager()

@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        subdomain = "tsiauca"
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            print("Attempting to log in...")
            await edupage_service.login(username, password, subdomain)
            print("Login successful!")
            
            userdata.save_user_data(username, password, subdomain)
            session['logged_in'] = True  
            return redirect(url_for('dashboard.dashboard'))  

        except BadCredentialsException:
            return render_template('login.html', error="Wrong username or password!", status_code=401)

        except CaptchaException:
            return render_template('login.html', error="Captcha required! Please complete the captcha to log in.", status_code=400)

        except SSLError:
            return render_template('login.html', error="SSL certificate verification failed. Please check your connection.", status_code=500)

        except Exception as e:
            return render_template('login.html', error=f"Failed to log in: {e}", status_code=500)

    return render_template('login.html')

