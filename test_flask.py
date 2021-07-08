from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

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

        Post.query.delete() # Delete post first so there won't be any issues with deleting the user
        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url="https://www.google.com/search?q=smiley+face&sxsrf=ALeKk02sPyGVrwrhx3_qkZFrTAhc-1pq1A:1625257795150&tbm=isch&source=iu&ictx=1&fir=2ibD-NzxUXqVVM%252CEB-7l6d3ePZ1CM%252C%252Fm%252F06n05&vet=1&usg=AI4_-kTEuM_DHhhirLOpxs6L4Fo_bmtrcA&sa=X&ved=2ahUKEwjO8LCMncXxAhXGX80KHd-UDNIQ_B16BAgzEAE#imgrc=2ibD-NzxUXqVVM")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user_firstname = user.first_name
        self.user_lastname = user.last_name

        post = Post(title="Post Test", content="Flask Test")
        # tag = Tag(name="Tag Test", posts=[post])

        db.session.add(post)
        db.session.commit()

        self.post = post
        self.post_id = post.id
        self.post_title = post.title

        # self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Test that when a GET request is sent to the user list route, the page redirects and shows the user list"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        """Test that when a GET request is sent to the show user route, the page redirects and shows the user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_add_user(self):
        """Test that when a POST request is sent to the add user route, the page redirects and the user is added"""
        with app.test_client() as client:
            d = {"first-name": "Test", "last-name": "User", "img-url": 'https://www.google.com/search?q=smiley+face&sxsrf=ALeKk02sPyGVrwrhx3_qkZFrTAhc-1pq1A:1625257795150&tbm=isch&source=iu&ictx=1&fir=2ibD-NzxUXqVVM%252CEB-7l6d3ePZ1CM%252C%252Fm%252F06n05&vet=1&usg=AI4_-kTEuM_DHhhirLOpxs6L4Fo_bmtrcA&sa=X&ved=2ahUKEwjO8LCMncXxAhXGX80KHd-UDNIQ_B16BAgzEAE#imgrc=2ibD-NzxUXqVVM'}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)
    
    def test_show_user_edit(self):
        """Test that when a GET request is sent to the edit user route, the page redirects and shows the edit user form"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a User</h1>', html)

    def test_post_user_edit(self):
        """Test that when a POST request is sent to the edit user route, the page redirects and the user is edited"""
        with app.test_client() as client:
            user = User.query.one()
            
            d = {"first-name": "Edited", "last-name": "User", "img-url": 'https://www.google.com/search?q=smiley+face&sxsrf=ALeKk02sPyGVrwrhx3_qkZFrTAhc-1pq1A:1625257795150&tbm=isch&source=iu&ictx=1&fir=2ibD-NzxUXqVVM%252CEB-7l6d3ePZ1CM%252C%252Fm%252F06n05&vet=1&usg=AI4_-kTEuM_DHhhirLOpxs6L4Fo_bmtrcA&sa=X&ved=2ahUKEwjO8LCMncXxAhXGX80KHd-UDNIQ_B16BAgzEAE#imgrc=2ibD-NzxUXqVVM'}
            resp = client.post(f"/users/{user.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edited User </a></li>', html)

    def test_delete_user(self):
        """Test that when delete user route is followed, the page redirects and the user is gone from the database"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete", follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            
            user = User.query.first()

            self.assertEqual(user, None)
    
    def test_show_post_form(self):
        """Test that when a GET request is sent to the add post route, the page redirects and the add post form is shown"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new", follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>Add a Post for {self.user_firstname} {self.user_lastname}</h1>", html)

    def test_add_post(self):
        """Test that when a POST request is sent to the add post route, the page redirects and the post is added"""
        with app.test_client() as client:

            p = {"title": "Test", "content": "How testy of you", "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=p, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test", html)

    def test_show_post(self):
        """Test that when a GET request is sent to the show post route, the page redirects and shows the post"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{self.post_title}</h1>', html)
    
    def test_post_edit(self):
        """Test that when a GET request is sent to the edit post route, the page redirects and shows the edit post form"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>Edit Your Post</h1>', html)

    def test_process_post_edit(self):
        """Test that when a POST request is sent to the edit post route, the page redirects and the post is edited"""
        with app.test_client() as client:
            d = {"title": "Edit", "content": "How edited of you", "user_id": self.user_id}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>Edit</h1>', html)

    def test_post_delete(self):
        """Test that when delete post route is followed, the page redirectsand the post is gone from the database"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/delete",   follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
                
            post = Post.query.first()
            self.assertEqual(post, None)

    def test_show_tags(self):
        """Test that /tags shows all tags on page"""
        with app.test_client() as client:
            tag = Tag(name="Tag Test", posts=[self.post])

            db.session.add(tag)
            db.session.commit()

            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tag Test</a></li>', html)