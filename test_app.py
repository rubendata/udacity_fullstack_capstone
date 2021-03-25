import os
import unittest
import json
from forms import *
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Post, Group

#tokens added: 25 March 2021 10pm CET
Authtokens = {
    "post_images" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpIZWk0Mmx0Q3dtWlZ2Tmo1UzU4MSJ9.eyJpc3MiOiJodHRwczovL29uc3RhZ3JhbS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1OGVjMTMxYWQxMWMwMDcwNmU0ZGQ5IiwiYXVkIjpbIm9uc3RhZ3JhbSIsImh0dHBzOi8vb25zdGFncmFtLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTY3MDU2NzAsImV4cCI6MTYxNjc5MjA3MCwiYXpwIjoiOWoxa2pzMDhJRG9BUUp3TG1kd0JYbGZ1c0ZIeko2RGEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicG9zdDppbWFnZXMiXX0.LOHHSGV5GVGAio2eQAFDET4Zktty_lbgpSCTy0pgWYH906TjM7qqrBr9K0V3BYGQdkPihs_7K-gEnOljy5e1uNAelz9KevQnf0FA7uJWIC2pqutwrKUFVbN8xQXI23k2I7XMeMjmf2THx69S3ZIY-VUV21OvPKw8523aq3z590Gj4weyD8pojS3uwbjairOvgmT7vwAwQy2jbya6ZWmy-H8TcqcYe-LphLd7bbl0WeouXFfKBcaTTgWO9dHq4CX_xQCQOMq6d_TgzVM9zUuc1-a1IXYqVtWaKkbWUAyAh3hTGamXGIY32ZdgDB8PIuyaQvyWlynY1CtIdgM-8WQLBQ",
    "post_groups" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpIZWk0Mmx0Q3dtWlZ2Tmo1UzU4MSJ9.eyJpc3MiOiJodHRwczovL29uc3RhZ3JhbS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1OGVhNTQyMzMwNjAwMDcwYjVkZDMyIiwiYXVkIjpbIm9uc3RhZ3JhbSIsImh0dHBzOi8vb25zdGFncmFtLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTY3MDU3NTMsImV4cCI6MTYxNjc5MjE1MywiYXpwIjoiOWoxa2pzMDhJRG9BUUp3TG1kd0JYbGZ1c0ZIeko2RGEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicG9zdDpncm91cHMiXX0.lEktq6M2_Cw6sC-zt2ho0khC8KGdX8A8jE6KBGPglO-Bhy7qGD0PmS3MoWOS_OVLJRgbEbThRpR7kZ2CP6AAkQRxqefCkZTYVnMcRZ5aARoN69hzpOwdT0StKT3CpulNyGTv9CaAW0KrdBOdo2pSherEDlLmGo8KINQQAi303rYEXlDT7VhuNIjRxUR7KxpGQT2GmpWhTeaYeK_XorimHO_OjTZi-nJ_8TmisG2EjvyUdB4Litij36qVkIWgZi3JP4Qnl26JtkMzYUZ-zSFR1HHThA58O4X9SiUNni1lQiRyMXN9uYAQ6gkO8JxCHyPCMUBEa3_VaxO1dpTdNCM5iw"
}


class OnstagramTestCase(unittest.TestCase):
    """This class represents the onstragram test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "onstagram_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.post_images = Authtokens["post_images"]
        self.post_groups = Authtokens["post_groups"]

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_index(self):
        res = self.client().get("/")
        self.assertEqual(res.status_code,200)


    def test_profile(self): #no token given -> expected: 401
        res = self.client().get('/profile')
        self.assertEqual(res.status_code,401)

    def test_create_post_get(self):
        res = self.client().get('/posts/create',headers={'Authorization':
                                str(self.post_images), 'Test': 'test'})
        self.assertEqual(res.status_code,200)
        res = self.client().get('/posts/create')
        self.assertEqual(res.status_code,401)
    
  
    def test_create_group_get(self):
        res = self.client().get('/groups/create',headers={'Authorization':
                                str(self.post_groups), 'Test': 'test'})
        self.assertEqual(res.status_code,200)
        res = self.client().get('/groups/create')
        self.assertEqual(res.status_code,401)

    def test_create_group_post(self):
        with self.app.test_request_context(
            '/groups/create', headers={'Authorization':
                                     str(self.post_groups), 'Test': 'test'}):
            form = GroupForm(
                name='test',
                
            )
            self.assertIsInstance(form, GroupForm)
            

    def test_filter_posts(self):
        res = self.client().get("/posts/1")
        self.assertEqual(res.status_code,200)
        res = self.client().get("/posts/99999999999")
        self.assertEqual(res.status_code,400)

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()