from flask import render_template, request, jsonify
import json
from app import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def courses():
    with open('courses.json', 'r') as file:
        course_data = json.load(file)
    return render_template('courses.html', courses=course_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/courses', methods=['GET'])
def api_courses():
    with open('courses.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)


# API для записи на курс
@app.route('/api/enroll', methods=['POST'])
def enroll():
    try:
        # Получение данных из POST-запроса
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        course_id = data.get('course_id')

        # Проверка на наличие обязательных данных
        if not name or not email or not course_id:
            return jsonify({"error": "Все поля обязательны!"}), 400

        # Проверка формата email (упрощенная валидация)
        if "@" not in email or "." not in email:
            return jsonify({"error": "Некорректный email!"}), 400

        # Сохранение данных о записи
        enrollment = {
            "name": name,
            "email": email,
            "course_id": course_id
        }
        try:
            with open('enrollments.json', 'r') as file:
                enrollments = json.load(file)
        except FileNotFoundError:
            enrollments = []

        enrollments.append(enrollment)

        with open('enrollments.json', 'w') as file:
            json.dump(enrollments, file, indent=4)

        return jsonify({"message": "Вы успешно записаны на курс!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
from flask_mail import Message
from app import mail

@app.route('/api/enroll', methods=['POST'])
def enroll():
    try:
        # Получение данных из POST-запроса
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        course_id = data.get('course_id')

        # Проверка на наличие обязательных данных
        if not name or not email or not course_id:
            return jsonify({"error": "Все поля обязательны!"}), 400

        # Проверка формата email
        if "@" not in email or "." not in email:
            return jsonify({"error": "Некорректный email!"}), 400

        # Сохранение данных о записи
        enrollment = {
            "name": name,
            "email": email,
            "course_id": course_id
        }
        try:
            with open('enrollments.json', 'r') as file:
                enrollments = json.load(file)
        except FileNotFoundError:
            enrollments = []

        enrollments.append(enrollment)

        with open('enrollments.json', 'w') as file:
            json.dump(enrollments, file, indent=4)

        # Отправка уведомления на email
        send_enrollment_email(name, email, course_id)

        return jsonify({"message": "Вы успешно записаны на курс!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def send_enrollment_email(name, email, course_id):
    """Отправка email с подтверждением записи на курс."""
    with open('courses.json', 'r') as file:
        courses = json.load(file)

    # Найти название курса
    course_name = next((course['name'] for course in courses if course['id'] == int(course_id)), 'Неизвестный курс')

    subject = "Подтверждение записи на курс"
    body = f"""
    Здравствуйте, {name}!

    Вы успешно записались на курс: {course_name}.
    Мы скоро свяжемся с вами для уточнения деталей.

    С уважением,
    Школа иностранных языков
    """

    # Создание сообщения
    msg = Message(subject, sender='your_email@gmail.com', recipients=[email])
    msg.body = body

    # Отправка сообщения
    mail.send(msg)
    