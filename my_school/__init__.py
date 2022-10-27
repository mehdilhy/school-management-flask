from auth.auth import AuthError, requires_auth
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models.models import (Class, Student, Subject, SubjectResult, Teacher,
                           setup_db)

ELEMENTS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    ######################################## Teacher ########################################

    @app.route('/teachers', methods=['GET'])
    @requires_auth('get:teachers')
    def get_teachers(payload):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ELEMENTS_PER_PAGE
        end = start + ELEMENTS_PER_PAGE
        teachers = Teacher.query.all()
        formatted_teachers = [teacher.format()
                              for teacher in teachers][start:end]
        if len(formatted_teachers) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'teachers': formatted_teachers,
        })

    @app.route('/teachers/<int:teacher_id>', methods=['GET'])
    @requires_auth('get:teacher')
    def get_teacher(payload, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if teacher is None:
            abort(404)
        return jsonify({
            'success': True,
            'teacher': teacher.format()
        })

    @app.route('/teachers', methods=['POST'])
    @requires_auth('post:teachers')
    def create_teacher(payload):
        body = request.get_json()
        name = body.get('name', None)
        phone = body.get('phone', None)
        email = body.get('email', None)
        address = body.get('address', None)
        class_id = body.get('class_id', None)
        if not name or not phone or not email or not address:
            abort(400)
        try:
            teacher = Teacher(name=name, phone=phone,
                              email=email, address=address)
            print(name, phone, email, address)
            teacher.insert()
            if class_id:
                class_to_teacher = Class.query.get(class_id)
                class_to_teacher.teachers.append(teacher)
                class_to_teacher.update()

            return jsonify({
                'success': True,
                'teacher': teacher.format()
            })
        except:
            abort(422)

    @app.route('/teachers/<int:teacher_id>', methods=['PATCH'])
    @requires_auth('patch:teachers')
    def update_teacher(payload, teacher_id):
        teacher = Teacher.query.filter(Teacher.id == teacher_id).one_or_none()
        if not teacher:
            abort(404)
        body = request.get_json()
        name = body.get('name', None)
        if not name:
            abort(400)
        try:
            teacher.name = name
            teacher.update()
            return jsonify({
                'success': True,
                'teacher': teacher.format()
            })
        except:
            abort(422)

    @app.route('/teachers/<int:teacher_id>', methods=['DELETE'])
    @requires_auth('delete:teachers')
    def delete_teacher(payload, teacher_id):
        teacher = Teacher.query.filter(Teacher.id == teacher_id).one_or_none()
        if not teacher:
            abort(404)
        try:
            classes = Class.query.all()
            for class_ in classes:
                if teacher in class_.teachers:
                    class_.teachers.remove(teacher)
                    class_.update()

            subject_to_teacher = Subject.query.filter(
                Subject.teacher_id == teacher_id).all()
            for subject in subject_to_teacher:
                subject.teacher_id = None
                subject.update()
            teacher.delete()
            return jsonify({
                'success': True,
                'delete': teacher_id
            })

        except:
            abort(422)

    @app.route('/teachers/<int:teacher_id>/subjects', methods=['GET'])
    @requires_auth('get:teachers')
    def get_teacher_subjects(payload, teacher_id):
        teacher = Teacher.query.filter(Teacher.id == teacher_id).one_or_none()

        if not teacher:
            abort(404)
        subjects = Subject.query.filter(Subject.teacher_id == teacher_id).all()
        formatted_subjects = [subject.format() for subject in subjects]
        if (len(formatted_subjects) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'subjects': formatted_subjects,
        })

    ######################################## END TEACHER ########################################

    ######################################## STUDENTS ########################################

    @app.route('/students', methods=['GET'])
    @requires_auth('get:students')
    def get_students(payload):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ELEMENTS_PER_PAGE
        end = start + ELEMENTS_PER_PAGE
        formatted_students = [student.format()
                              for student in Student.query.all()][start:end]
        if len(formatted_students) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'students': formatted_students,
        })

    @app.route('/students/<int:student_id>', methods=['GET'])
    @requires_auth('get:student')
    def get_student(payload, student_id):
        student = Student.query.get(student_id)
        if student is None:
            abort(404)
        return jsonify({
            'success': True,
            'student': student.format()
        })

    @app.route('/students', methods=['POST'])
    @requires_auth('post:students')
    def create_student(payload):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        class_id = body.get('class_id', None)
        if not name or not class_id or not age:
            abort(400)
        try:
            student = Student(name=name, class_id=class_id, age=age)
            student.insert()
            return jsonify({
                'success': True,
                'student': student.format()
            })
        except:

            abort(422)

    @app.route('/students/<int:student_id>', methods=['PATCH'])
    @requires_auth('patch:students')
    def update_student(payload, student_id):
        student = Student.query.filter(Student.id == student_id).one_or_none()
        if not student:
            abort(404)
        body = request.get_json()
        name = body.get('name', None)
        class_id = body.get('class_id', None)
        if not name or not class_id:
            abort(400)
        try:
            student.name = name
            student.class_id = class_id
            student.update()
            return jsonify({
                'success': True,
                'student': student.format()
            })
        except:
            abort(422)

    @app.route('/students/<int:student_id>', methods=['DELETE'])
    @requires_auth('delete:students')
    def delete_student(payload, student_id):
        student = Student.query.filter(Student.id == student_id).one_or_none()
        if not student:
            abort(404)
        try:
            student.delete()
            return jsonify({
                'success': True,
                'student': student_id
            })
        except:
            abort(422)

    @app.route('/students/<int:student_id>/subjects', methods=['GET'])
    @requires_auth('get:students')
    def get_student_subjects(payload, student_id):
        student = Student.query.filter(Student.id == student_id).one_or_none()

        if not student:
            abort(404)
        subjects = Subject.query.filter(
            Subject.class_id == student.class_id).all()
        formatted_subjects = [subject.format() for subject in subjects]
        if (len(formatted_subjects) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'subjects': formatted_subjects,
        })

    ######################################## END STUDENTS ########################################

    ######################################## Class ########################################

    @app.route('/classes', methods=['GET'])
    @requires_auth('get:classes')
    def get_classes(payload):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ELEMENTS_PER_PAGE
        end = start + ELEMENTS_PER_PAGE
        formatted_classes = [class_.format()
                             for class_ in Class.query.all()][start:end]
        if len(formatted_classes) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'classes': formatted_classes,
        })

    @app.route('/classes', methods=['POST'])
    @requires_auth('post:classes')
    def create_class(payload):
        body = request.get_json()
        name = body.get('name', None)
        if not name:
            abort(400)
        try:
            class_ = Class(name=name)
            class_.insert()
            return jsonify({
                'success': True,
                'class': class_.format()
            })
        except:
            abort(422)

    @app.route('/classes/<int:class_id>', methods=['PATCH'])
    @requires_auth('patch:classes')
    def update_class(payload, class_id):
        class_ = Class.query.filter(Class.id == class_id).one_or_none()
        if not class_:
            abort(404)
        body = request.get_json()
        name = body.get('name', None)
        if not name:
            abort(400)
        try:
            class_.name = name
            class_.update()
            return jsonify({
                'success': True,
                'class': class_.format()
            })
        except:
            abort(422)

    @app.route('/classes/<int:class_id>', methods=['DELETE'])
    @requires_auth('delete:classes')
    def delete_class(payload, class_id):
        class_ = Class.query.filter(Class.id == class_id).one_or_none()
        if not class_:
            abort(404)
        try:
            class_.delete()
            return jsonify({
                'success': True,
                'class': class_id
            })
        except:
            abort(422)

    @app.route('/classes/<int:class_id>/subjects', methods=['GET'])
    @requires_auth('get:classes')
    def get_class_subjects(payload, class_id):
        class_ = Class.query.filter(Class.id == class_id).one_or_none()

        if not class_:
            abort(404)
        subjects = Subject.query.filter(Subject.class_id == class_id).all()
        formatted_subjects = [subject.format() for subject in subjects]
        if (len(formatted_subjects) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'subjects': formatted_subjects,
        })

    ######################################## END Class ########################################

    ######################################## Subjects ########################################

    @app.route('/subjects', methods=['GET'])
    @requires_auth('get:subjects')
    def get_subjects(payload):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ELEMENTS_PER_PAGE
        end = start + ELEMENTS_PER_PAGE
        formatted_subjects = [subject.format()
                              for subject in Subject.query.all()][start:end]
        if len(formatted_subjects) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'subjects': formatted_subjects,
        })

    @app.route('/subjects', methods=['POST'])
    @requires_auth('post:subjects')
    def create_subject(payload):
        body = request.get_json()
        name = body.get('name', None)
        class_id = body.get('class_id', None)
        teacher_id = body.get('teacher_id', None)
        if not name:
            abort(400)
        try:
            subject = Subject(name=name, class_id=class_id,
                              teacher_id=teacher_id)
            subject.insert()
            return jsonify({
                'success': True,
                'subject': subject.format()
            })
        except:
            abort(422)

    @app.route('/subjects/<int:subject_id>', methods=['PATCH'])
    @requires_auth('patch:subjects')
    def update_subject(payload, subject_id):
        subject = Subject.query.filter(Subject.id == subject_id).one_or_none()
        if not subject:
            abort(404)
        body = request.get_json()
        name = body.get('name', None)
        class_id = body.get('class_id', None)
        teacher_id = body.get('teacher_id', None)
        if not name:
            abort(400)
        try:
            subject.name = name
            subject.class_id = class_id
            subject.teacher_id = teacher_id
            subject.update()
            return jsonify({
                'success': True,
                'subject': subject.format()
            })
        except:
            abort(422)

    @app.route('/subjects/<int:subject_id>', methods=['DELETE'])
    @requires_auth('delete:subjects')
    def delete_subject(payload, subject_id):
        subject = Subject.query.filter(Subject.id == subject_id).one_or_none()
        if not subject:
            abort(404)
        try:
            subject.delete()
            return jsonify({
                'success': True,
                'subject': subject_id
            })
        except:
            abort(422)

    ######################################## END Subjects ########################################

    ######################################## Subject Result ########################################

    @app.route('/subject/results', methods=['GET'])
    @requires_auth('get:subjects')
    def get_subject_results(payload):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ELEMENTS_PER_PAGE
        end = start + ELEMENTS_PER_PAGE
        formatted_subject_results = [subject_result.format()
                                     for subject_result in SubjectResult.query.all()][start:end]
        if len(formatted_subject_results) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'subject_results': formatted_subject_results,
        })

    @app.route('/subject/results', methods=['POST'])
    @requires_auth('post:subjects')
    def create_subject_result(payload):
        body = request.get_json()
        subject_id = body.get('subject_id', None)
        student_id = body.get('student_id', None)
        result = body.get('result', None)
        if not subject_id or not student_id or not result:
            abort(400)
        try:
            subject_result = SubjectResult(subject_id=subject_id, student_id=student_id,
                                           result=result)
            subject_result.insert()
            return jsonify({
                'success': True,
                'subject_result': subject_result.format()
            })
        except:
            abort(422)

    @app.route('/subject/results/<int:subject_result_id>', methods=['PATCH'])
    @requires_auth('patch:subjects')
    def update_subject_result(payload, subject_result_id):
        subject_result = SubjectResult.query.filter(
            SubjectResult.id == subject_result_id).one_or_none()
        if not subject_result:
            abort(404)
        body = request.get_json()
        subject_id = body.get('subject_id', None)
        student_id = body.get('student_id', None)
        mark = body.get('mark', None)

        try:
            subject_result.subject_id = subject_id
            subject_result.student_id = student_id
            subject_result.mark = mark
            subject_result.update()
            return jsonify({
                'success': True,
                'subject_result': subject_result.format()
            })
        except:
            abort(422)

    @app.route('/subject/results/<int:subject_result_id>', methods=['DELETE'])
    @requires_auth('delete:subjects')
    def delete_subject_result(payload, subject_result_id):
        subject_result = SubjectResult.query.filter(
            SubjectResult.id == subject_result_id).one_or_none()
        if not subject_result:
            abort(404)
        try:
            subject_result.delete()
            return jsonify({
                'success': True,
                'subject_result': subject_result_id
            })
        except:
            abort(422)

    ######################################## END Subject Result ########################################

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code
    return app
