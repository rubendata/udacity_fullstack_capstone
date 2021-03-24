import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Post, Group


Authtokens = {
    "post_images" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpIZWk0Mmx0Q3dtWlZ2Tmo1UzU4MSJ9.eyJpc3MiOiJodHRwczovL29uc3RhZ3JhbS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1OGVjMTMxYWQxMWMwMDcwNmU0ZGQ5IiwiYXVkIjpbIm9uc3RhZ3JhbSIsImh0dHBzOi8vb25zdGFncmFtLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTY2NzY0OTEsImV4cCI6MTYxNjc2Mjg5MSwiYXpwIjoiOWoxa2pzMDhJRG9BUUp3TG1kd0JYbGZ1c0ZIeko2RGEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicG9zdDppbWFnZXMiXX0.QTzRW4_LPcPliRuBkArKwCv_RTP9Kw_0Mwhbp4wpkLkjxkSZytI6AIZznA5xVDhibqL9GitIn67J0FCYLqp7J2HzXgrOq700Tvs1UgmIfq2k9YC8NpSmpaIFF1gI0XCmida9RXSDmtROjuI7E5n2FIA_CqOBdZNF8w1MIpnbUXIRgX5l4kaXI00e_eJAmJkmkUp_Ig2ZZZCAxxsfUa61b4DBky6ggQ1WICFJDDK8BF5as-gOHgsFnIEX6GVGA-etMxf1OBs_USxHx2bopr06MOpHtLy5ZnZ8V21KmEPVsqRRvvz6JXuTkS4E7X0nNT46BBSMRu9oFfs3Fxu8FrVEcg",
    "post_groups" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpIZWk0Mmx0Q3dtWlZ2Tmo1UzU4MSJ9.eyJpc3MiOiJodHRwczovL29uc3RhZ3JhbS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA1OGVhNTQyMzMwNjAwMDcwYjVkZDMyIiwiYXVkIjpbIm9uc3RhZ3JhbSIsImh0dHBzOi8vb25zdGFncmFtLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTY2NzY0NzEsImV4cCI6MTYxNjc2Mjg3MSwiYXpwIjoiOWoxa2pzMDhJRG9BUUp3TG1kd0JYbGZ1c0ZIeko2RGEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsicG9zdDpncm91cHMiXX0.czaxBh6PdfEto-qvG7sqtCpQIVm2C_bV4QJizOFjfSiWGj6c8Y1dKwuIuo6nce_O5wnm08wVmzl4VwYnnV47X2LS-ZUKtgcXdg2C1u727miFH1IOOVXVWba578REEZQNo7iPD9UHtfV33us5SXxaEHmen2XObJVlbW_XZns8rXjsC4E3zb4AWNmUrmXTUhDA9rU5eIutO9JlLzo0EqyRy4sH6zSwheYc0elFaLOsUpf2dVTKSi-zHFeesgKx4yw3XMVKIm6La0BgVxnyXhuR8iLaOlSEhQz8G1trV6Gxa0IGDIZMhyk1n2IJn0eP_tgK1yqJ-dRtc7h2anxVa1pVJw"
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()