import json
import unittest

from faker import Faker
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Class, Student, Subject, Teacher, setup_db
from settings import (ADMIN_TOKEN, DB_PASSWORD, DB_USER, STUDENT_TOKEN,
                      TEACHER_TOKEN)

fake = Faker()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MySchoolTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    new_question = {
        'question': 'What is the capital of France?',
        'answer': 'Paris',
        'category': 1,
        'difficulty': 1
    }
    quiz = {'previous_questions': [], 'quiz_category': {'id': "1"}}

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "my-school-test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, 'localhost:5432', self.database_name)
        self.student_token = STUDENT_TOKEN
        self.teacher_token = TEACHER_TOKEN
        self.admin_token = ADMIN_TOKEN
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.populate_tables()

    def populate_tables(self):
        '''
        Populate tables with data
        '''
        # clear tables
        self.db.session.query(Student).delete()
        self.db.session.query(Subject).delete()
        self.db.session.execute('DELETE FROM class_to_teacher')
        self.db.session.query(Class).delete()
        self.db.session.query(Teacher).delete()

        self.db.session.execute(
            "INSERT INTO class (id,name) VALUES ({},'{}')".format(1, fake.name()))
        self.db.session.execute(
            "INSERT INTO class (id,name) VALUES ({},'{}')".format(2, fake.name()))
        self.db.session.execute(
            "INSERT INTO class (id,name) VALUES ({},'{}')".format(3, fake.name()))
        self.db.session.execute(
            "INSERT INTO class (id,name) VALUES ({},'{}')".format(4, fake.name()))
        self.db.session.execute(
            "INSERT INTO student (id,name,age,class_id) VALUES ({},'{}',{},{})".format(1, fake.name(), 10, 1))
        self.db.session.execute(
            "INSERT INTO student (id,name,age,class_id) VALUES ({},'{}',{},{})".format(2, fake.name(), 10, 1))
        self.db.session.execute(
            "INSERT INTO student (id,name,age,class_id) VALUES ({},'{}',{},{})".format(3, fake.name(), 10, 1))
        self.db.session.execute(
            "INSERT INTO teacher (id,name,phone,email,address) VALUES ({},'{}',{},{},'{}')".format(1, fake.name(), 123456789, 123456789, fake.address()))
        self.db.session.execute(
            "INSERT INTO teacher (id,name,phone,email,address) VALUES ({},'{}',{},{},'{}')".format(2, fake.name(), 123456789, 123456789, fake.address()))
        self.db.session.execute(
            "INSERT INTO teacher (id,name,phone,email,address) VALUES ({},'{}',{},{},'{}')".format(3, fake.name(), 123456789, 123456789, fake.address()))
        self.db.session.execute(
            "INSERT INTO subject (id,name,teacher_id,class_id) VALUES ({},'{}',{},{})".format(1, fake.name(), 1, 1))
        self.db.session.execute(
            "INSERT INTO subject (id,name,teacher_id,class_id) VALUES ({},'{}',{},{})".format(2, fake.name(), 2, 1))
        self.db.session.execute(
            "INSERT INTO subject (id,name,teacher_id,class_id) VALUES ({},'{}',{},{})".format(3, fake.name(), 3, 1))

        self.db.session.commit()

        pass

    def tearDown(self):
        """Executed after reach test"""
        pass

    # students tests

    def test_get_students_no_token(self):
        '''
        Test get students without token
        '''
        res = self.client().get('/students')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401, bcolors.FAIL +
                         "Get Students Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Students Without Token OK ✓" + bcolors.ENDC)

    def test_get_students_with_student_token(self):
        '''
        Test get students with student token
        '''
        res = self.client().get('/students', headers={
            'Authorization': 'Bearer {}'.format(self.student_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Get Students With Student Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Students With Student Token OK ✓" + bcolors.ENDC)

    def test_get_students_with_teacher_token(self):
        '''
        Test get students with teacher token
        '''
        res = self.client().get('/students', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True,
                         bcolors.FAIL + "Get Students With Teacher Token Fail X" + bcolors.ENDC)
        self.assertTrue(data['students'])
        print('\n'+bcolors.OKGREEN +
              "Get Students With Teacher Token OK ✓" + bcolors.ENDC)

    def test_get_students_with_admin_token(self):
        '''
        Test get students with admin token
        '''
        res = self.client().get('/students', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True,
                         bcolors.FAIL + "Get Students With Admin Token Fail X" + bcolors.ENDC)
        self.assertTrue(data['students'])
        print('\n'+bcolors.OKGREEN +
              "Get Students With Admin Token OK ✓" + bcolors.ENDC)

    def test_get_student_no_token(self):
        '''
        Test get student without token
        '''
        res = self.client().get('/students/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Get Student Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Student Without Token OK ✓" + bcolors.ENDC)

    def test_get_student_with_student_token(self):
        '''
        Test get student with student token
        '''
        res = self.client().get('/students/1', headers={
            'Authorization': 'Bearer {}'.format(self.student_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Student With Student Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Student With Student Token OK ✓" + bcolors.ENDC)

    def test_get_student_with_teacher_token(self):
        '''
        Test get student with teacher token
        '''
        res = self.client().get('/students/1', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Student With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Student With Teacher Token OK ✓" + bcolors.ENDC)

    def test_get_student_with_admin_token(self):
        '''
        Test get student with admin token
        '''
        res = self.client().get('/students/1', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Student With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Student With Admin Token OK ✓" + bcolors.ENDC)

    def test_get_student_not_found(self):
        '''
        Test get student not found
        '''
        res = self.client().get('/students/1000', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404,
                         bcolors.FAIL + "Get Student Not Found Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Student Not Found OK ✓" + bcolors.ENDC)

    def test_post_student_no_token(self):
        '''
        Test post student without token
        '''
        res = self.client().post('/students', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Post Student Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Student Without Token OK ✓" + bcolors.ENDC)

    def test_post_student_with_student_token(self):
        '''
        Test post student with student token
        '''
        res = self.client().post('/students', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.student_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Post Student With Student Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Student With Student Token OK ✓" + bcolors.ENDC)

    def test_post_student_with_teacher_token(self):
        '''
        Test post student with teacher token
        '''
        res = self.client().post('/students', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Post Student With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Student With Teacher Token OK ✓" + bcolors.ENDC)

    def test_post_student_with_admin_token(self):
        '''
        Test post student with admin token
        '''
        res = self.client().post('/students', json={
            'name': 'test',
            'class_id': 2,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Post Student With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Post Student With Admin Token OK ✓" + bcolors.ENDC)

    def test_post_student_with_admin_token_fail(self):
        '''
        Test post student with admin token fail
        '''
        res = self.client().post('/students', json={
            'name': 'test',
            'class_id': 1000,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422,
                         bcolors.FAIL + "Post Student With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Student With Admin Token Fail OK ✓" + bcolors.ENDC)

    def test_patch_student_no_token(self):
        '''
        Test patch student without token
        '''
        res = self.client().patch('/students/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Patch Student Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Student Without Token OK ✓" + bcolors.ENDC)

    def test_patch_student_with_student_token(self):
        '''
        Test patch student with student token
        '''
        res = self.client().patch('/students/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.student_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Patch Student With Student Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Student With Student Token OK ✓" + bcolors.ENDC)

    def test_patch_student_with_teacher_token(self):
        '''
        Test patch student with teacher token
        '''
        res = self.client().patch('/students/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Patch Student With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Student With Teacher Token OK ✓" + bcolors.ENDC)

    def test_patch_student_with_admin_token(self):
        '''
        Test patch student with admin token
        '''
        res = self.client().patch('/students/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Patch Student With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Patch Student With Admin Token OK ✓" + bcolors.ENDC)

    def test_patch_student_with_admin_token_fail(self):
        '''
        Test patch student with admin token fail
        '''
        res = self.client().patch('/students/1000', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404,
                         bcolors.FAIL + "Patch Student With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Student With Admin Token Fail OK ✓" + bcolors.ENDC)

    def test_delete_student_no_token(self):
        '''
        Test delete student without token
        '''
        res = self.client().delete('/students/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Delete Student Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Student Without Token OK ✓" + bcolors.ENDC)

    def test_delete_student_with_student_token(self):
        '''
        Test delete student with student token
        '''
        res = self.client().delete('/students/1', headers={
            'Authorization': 'Bearer {}'.format(self.student_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Delete Student With Student Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Student With Student Token OK ✓" + bcolors.ENDC)

    def test_delete_student_with_teacher_token(self):
        '''
        Test delete student with teacher token
        '''
        res = self.client().delete('/students/1', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Delete Student With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Student With Teacher Token OK ✓" + bcolors.ENDC)

    def test_delete_student_with_admin_token(self):
        '''
        Test delete student with admin token
        '''
        res = self.client().delete('/students/1', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Delete Student With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Delete Student With Admin Token OK ✓" + bcolors.ENDC)

    def test_delete_student_with_admin_token_fail(self):
        '''
        Test delete student with admin token fail
        '''
        res = self.client().delete('/students/1000', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404,
                         bcolors.FAIL + "Delete Student With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Student With Admin Token Fail OK ✓" + bcolors.ENDC)

    def test_get_teachers_no_token(self):
        '''
        Test get teachers without token
        '''
        res = self.client().get('/teachers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401, bcolors.FAIL +
                         "Get Teachers Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Teachers Without Token OK ✓" + bcolors.ENDC)

    def test_get_teachers_with_teacher_token(self):
        '''
        Test get teachers with teacher token
        '''
        res = self.client().get('/teachers', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Get Teachers With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Teachers With Teacher Token OK ✓" + bcolors.ENDC)

    def test_get_teachers_with_teacher_token(self):
        '''
        Test get teachers with teacher token
        '''
        res = self.client().get('/teachers', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True,
                         bcolors.FAIL + "Get Teachers With Teacher Token Fail X" + bcolors.ENDC)
        self.assertTrue(data['teachers'])
        print('\n'+bcolors.OKGREEN +
              "Get Teachers With Teacher Token OK ✓" + bcolors.ENDC)

    def test_get_teachers_with_admin_token(self):
        '''
        Test get teachers with admin token
        '''
        res = self.client().get('/teachers', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True,
                         bcolors.FAIL + "Get Teachers With Admin Token Fail X" + bcolors.ENDC)
        self.assertTrue(data['teachers'])
        print('\n'+bcolors.OKGREEN +
              "Get Teachers With Admin Token OK ✓" + bcolors.ENDC)

    def test_get_teacher_no_token(self):
        '''
        Test get teacher without token
        '''
        res = self.client().get('/teachers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Get Teacher Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Teacher Without Token OK ✓" + bcolors.ENDC)

    def test_get_teacher_with_teacher_token(self):
        '''
        Test get teacher with teacher token
        '''
        res = self.client().get('/teachers/1', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_get_teacher_with_teacher_token(self):
        '''
        Test get teacher with teacher token
        '''
        res = self.client().get('/teachers/1', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_get_teacher_with_admin_token(self):
        '''
        Test get teacher with admin token
        '''
        res = self.client().get('/teachers/1', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Teacher With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Teacher With Admin Token OK ✓" + bcolors.ENDC)

    def test_get_teacher_not_found(self):
        '''
        Test get teacher not found
        '''
        res = self.client().get('/teachers/1000', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404,
                         bcolors.FAIL + "Get Teacher Not Found Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Teacher Not Found OK ✓" + bcolors.ENDC)

    def test_post_teacher_no_token(self):
        '''
        Test post teacher without token
        '''
        res = self.client().post('/teachers', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Post Teacher Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Teacher Without Token OK ✓" + bcolors.ENDC)

    def test_post_teacher_with_teacher_token(self):
        '''
        Test post teacher with teacher token
        '''
        res = self.client().post('/teachers', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Post Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_post_teacher_with_teacher_token(self):
        '''
        Test post teacher with teacher token
        '''
        res = self.client().post('/teachers', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Post Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_post_teacher_with_admin_token(self):
        '''
        Test post teacher with admin token
        '''
        res = self.client().post('/teachers', json={
            'name': 'test',
            'phone': '123456789',
            'email': 'test@test.com',
            'address': 'test',
            'class_id': 1,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Post Teacher With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Post Teacher With Admin Token OK ✓" + bcolors.ENDC)

    def test_post_teacher_with_admin_token_fail(self):
        '''
        Test post teacher with admin token fail
        '''
        res = self.client().post('/teachers', json={
            'name': 'test',
            'phone': '123456789',
            'e': 'test@test.com',
            'address': 'test',
            'class_id': 1,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400,
                         bcolors.FAIL + "Post Teacher With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Post Teacher With Admin Token Fail OK ✓" + bcolors.ENDC)

    def test_patch_teacher_no_token(self):
        '''
        Test patch teacher without token
        '''
        res = self.client().patch('/teachers/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Patch Teacher Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Teacher Without Token OK ✓" + bcolors.ENDC)

    def test_patch_teacher_with_teacher_token(self):
        '''
        Test patch teacher with teacher token
        '''
        res = self.client().patch('/teachers/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Patch Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_patch_teacher_with_teacher_token(self):
        '''
        Test patch teacher with teacher token
        '''
        res = self.client().patch('/teachers/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Patch Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_patch_teacher_with_admin_token(self):
        '''
        Test patch teacher with admin token
        '''
        res = self.client().patch('/teachers/1', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Patch Teacher With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Patch Teacher With Admin Token OK ✓" + bcolors.ENDC)

    def test_patch_teacher_with_admin_token_fail(self):
        '''
        Test patch teacher with admin token fail
        '''
        res = self.client().patch('/teachers/1000', json={
            'name': 'test',
            'class_id': 1,
            'age': 10,
        }, headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404,
                         bcolors.FAIL + "Patch Teacher With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Patch Teacher With Admin Token Fail OK ✓" + bcolors.ENDC)

    def test_delete_teacher_no_token(self):
        '''
        Test delete teacher without token
        '''
        res = self.client().delete('/teachers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Delete Teacher Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Teacher Without Token OK ✓" + bcolors.ENDC)

    def test_delete_teacher_with_teacher_token(self):
        '''
        Test delete teacher with teacher token
        '''
        res = self.client().delete('/teachers/1', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Delete Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_delete_teacher_with_teacher_token(self):
        '''
        Test delete teacher with teacher token
        '''
        res = self.client().delete('/teachers/1', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Delete Teacher With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Teacher With Teacher Token OK ✓" + bcolors.ENDC)

    def test_delete_teacher_with_admin_token(self):
        '''
        Test delete teacher with admin token
        '''
        res = self.client().delete('/teachers/1', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Delete Teacher With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Delete Teacher With Admin Token OK ✓" + bcolors.ENDC)

    def test_delete_teacher_with_admin_token_fail(self):
        '''
        Test delete teacher with admin token fail
        '''
        res = self.client().delete('/teachers/1000', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404,
                         bcolors.FAIL + "Delete Teacher With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Delete Teacher With Admin Token Fail OK ✓" + bcolors.ENDC)

    def test_get_classes_no_token(self):
        '''
        Test get classes without token
        '''
        res = self.client().get('/classes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401,
                         bcolors.FAIL + "Get Classes Without Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Classes Without Token OK ✓" + bcolors.ENDC)

    def test_get_classes_with_teacher_token(self):
        '''
        Test get classes with teacher token
        '''
        res = self.client().get('/classes', headers={
            'Authorization': 'Bearer {}'.format(self.teacher_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Classes With Teacher Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Classes With Teacher Token OK ✓" + bcolors.ENDC)

    def test_get_classes_with_admin_token(self):
        '''
        Test get classes with admin token
        '''
        res = self.client().get('/classes', headers={
            'Authorization': 'Bearer {}'.format(self.admin_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200,
                         bcolors.FAIL + "Get Classes With Admin Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], True)
        print('\n'+bcolors.OKGREEN +
              "Get Classes With Admin Token OK ✓" + bcolors.ENDC)

    def test_get_classes_with_student_token(self):
        '''
        Test get classes with student token
        '''
        res = self.client().get('/classes', headers={
            'Authorization': 'Bearer {}'.format(self.student_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403,
                         bcolors.FAIL + "Get Classes With Student Token Fail X" + bcolors.ENDC)
        self.assertEqual(data['success'], False)
        print('\n'+bcolors.OKGREEN +
              "Get Classes With Student Token OK ✓" + bcolors.ENDC)


if __name__ == "__main__":
    unittest.main()
