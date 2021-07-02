from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="https://www.google.com/search?q=smiley+face&sxsrf=ALeKk02sPyGVrwrhx3_qkZFrTAhc-1pq1A:1625257795150&tbm=isch&source=iu&ictx=1&fir=2ibD-NzxUXqVVM%252CEB-7l6d3ePZ1CM%252C%252Fm%252F06n05&vet=1&usg=AI4_-kTEuM_DHhhirLOpxs6L4Fo_bmtrcA&sa=X&ved=2ahUKEwjO8LCMncXxAhXGX80KHd-UDNIQ_B16BAgzEAE#imgrc=2ibD-NzxUXqVVM")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first-name": "Test", "last-name": "User", "img-url": 'https://www.google.com/search?q=smiley+face&sxsrf=ALeKk02sPyGVrwrhx3_qkZFrTAhc-1pq1A:1625257795150&tbm=isch&source=iu&ictx=1&fir=2ibD-NzxUXqVVM%252CEB-7l6d3ePZ1CM%252C%252Fm%252F06n05&vet=1&usg=AI4_-kTEuM_DHhhirLOpxs6L4Fo_bmtrcA&sa=X&ved=2ahUKEwjO8LCMncXxAhXGX80KHd-UDNIQ_B16BAgzEAE#imgrc=2ibD-NzxUXqVVM'}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)
