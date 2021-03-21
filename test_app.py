import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Post, Group


Authtokens = {
    "game_master" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpoSWFSYWdqMUxtU0pEazZESTJDdiJ9.eyJpc3MiOiJodHRwczovL2Rldi10ZXN0LWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzc0YWIzNGU1MmFiMDA2OWQyZjRlNSIsImF1ZCI6WyJucGMtdHJhY2tlciIsImh0dHBzOi8vZGV2LXRlc3QtZnNuZC5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjE0MzMwNjUyLCJleHAiOjE2MTQ0MTcwNTIsImF6cCI6ImR2YlhLdEw0ajR5dTRKTDNnUXNXc3dzN0J3RklsWFBGIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDpucGMiLCJkZWxldGU6bnBjIiwiZWRpdDpucGMiLCJnZXQ6bnBjcyJdfQ.w6dLjcRY3VrSi1pqNAiKyI3ATqL6INebvqIg5jvUEcJUBCC_3l7_kVNv55iW_tSD9qDV5XT_uGAUyvEdqgxx7eOTKATB8SjTZUYxoufJs9bhBRgo-URKytBi83Te_TzExTSxvFV_e3412aZ1FcOXcJ1DiWdON6D1gxaJa2kSCQ0x5blxCrp9FUJWF3EIn0JEy_2FKspZx86hqfBs-qHsUFb5oNaplZhnLV7L01g7nUX0-5Fb4ndCgO4ZZX1r7J3TzMuK-Yz1DzSyg1BErOSJgg5aHj-RJBT6K81MSRWLMLtGv34qLY2WsPpiRZVjcJmxb_JeHBW5QVj-tKoBSvZEIA",
    "viewer" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpoSWFSYWdqMUxtU0pEazZESTJDdiJ9.eyJpc3MiOiJodHRwczovL2Rldi10ZXN0LWZzbmQuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwMzc0YThhYWQ2NTRhMDA2YTM3Y2YyYyIsImF1ZCI6WyJucGMtdHJhY2tlciIsImh0dHBzOi8vZGV2LXRlc3QtZnNuZC5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjE0MzMwNjk5LCJleHAiOjE2MTQ0MTcwOTksImF6cCI6ImR2YlhLdEw0ajR5dTRKTDNnUXNXc3dzN0J3RklsWFBGIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDpucGMiLCJnZXQ6bnBjcyJdfQ.MKyCfzoY1malLqXrJiu8eA1qtrqc4-BvGGDuL_2ynytsB2puoZx2HVODr6TAHWwgps2G6UepEt4qZ9Bxb0g-S53aZ0m4C3q1KVkY8Di2v-QQi-mFvhmNK8PQQ9iKuogiYrJ2C4LXan8CLgXMryzj6ADpQASiJ1vjqIBAysgW7SXA-9UHchaxdd7heuqiA_f831wT4kvXnBiqEeE0WD_7AwyQkJwh8rB6gAWMRpblwp5Qhv4E0nG811kb6AcHyOiMl97I0cYg0obm8vY6VId75-_NcBmecfI6ziiYjS1e-LMg8fzOuIZAtKE4uJvqGkmZxdiWMlELBDgnMerSMpzqFQ"
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
   



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()