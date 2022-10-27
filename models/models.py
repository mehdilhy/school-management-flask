
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

print("DB_HOST: ", DB_HOST)
database_name = DB_NAME
database_path = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST+":"+DB_PORT, database_name)

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


class_to_teacher = db.Table('class_to_teacher',
                            db.Column('class_id', db.Integer, db.ForeignKey(
                                'class.id'), primary_key=True),
                            db.Column('teacher_id', db.Integer, db.ForeignKey(
                                'teacher.id'), primary_key=True)
                            )


class Class(db.Model):
    __tablename__ = 'class'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    teachers = db.relationship('Teacher', secondary=class_to_teacher,
                               backref=db.backref('class', lazy=True))

    students = db.relationship('Student', backref='class', lazy=True)

    def __init__(self, name, teacher):
        self.name = name
        self.teacher = teacher

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'teacher': [teacher.format() for teacher in self.teachers],
            'students': [student.format() for student in self.students]

        }

    def __repr__(self):
        return f'<Class ID: {self.id}, name: {self.name}>'


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    subject_results = db.relationship(
        'SubjectResult', backref='student', lazy=True)

    def __init__(self, name, age, class_id):
        self.name = name
        self.age = age
        self.class_id = class_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'class': self.class_id,

        }

    def __repr__(self):
        return f'<Student ID: {self.id}, name: {self.name}>'


class Teacher(db.Model):
    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)

    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
        }

    def __repr__(self):
        return f'<Teacher ID: {self.id}, name: {self.name}>'


class Subject(db.Model):
    __tablename__ = 'subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'teacher.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

    def __init__(self, name, teacher_id, class_id):
        self.name = name
        self.teacher_id = teacher_id
        self.class_id = class_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'teacher_id': self.teacher_id,
            'class_id': self.class_id,
        }

    def __repr__(self):
        return f'<Subject ID: {self.id}, name: {self.name}>'


class SubjectResult(db.Model):
    __tablename__ = 'subject_result'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey(
        'subject.id'), nullable=False)
    mark = db.Column(db.Integer, nullable=False)

    def __init__(self, student_id, subject_id):
        self.student_id = student_id
        self.subject_id = subject_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject_id': self.subject_id,
            'mark': self.mark
        }

    def __repr__(self):
        return f'<StudentSubject ID: {self.id}, student_id: {self.student_id}, subject_id: {self.subject_id}>, mark: {self.mark}>'
