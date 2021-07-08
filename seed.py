"""Seed file to make sample data for db"""

from models import Post, PostTag, User, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

jim = User(first_name="Jim", last_name="Halpert", image_url = "https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/11/asset/buzzfeed-prod-fastlane-01/sub-buzz-22381-1502291405-3.jpg?downsize=700%3A%2A&output-quality=auto&output-format=auto")
pam = User(first_name="Pam", last_name="Beesley", image_url = "https://i.pinimg.com/474x/b4/37/0b/b4370be92a23d01d414d94983c2fb925.jpg")
michael = User(first_name="Michael", last_name="Scott", image_url = "https://pbs.twimg.com/profile_images/1258083294870036481/T-f9OgNq_400x400.jpg")

p1 = Post(title="World's Best Boss", content="I am the world's best boss. Everyone says so. They bought me this mug.", user_id=3)
p2 = Post(title="To the Receptionist", content="Ur cute", user_id=1)
p3 = Post(title="To Roy", content="Hurry up and plan our wedding", user_id=2)
p4 = Post(title="To Dwight", content="Dwight, you lazy slut", user_id=3)

db.session.add_all([jim, pam, michael])
db.session.commit()

funny = Tag(name="funny", posts=[p1, p2])
flirty = Tag(name="flirty", posts=[p2, p3])
to_someone = Tag(name="to_someone", posts=[p2, p3, p4])
unassigned = Tag(name="unassigned")

# funny.posts.append(p1, p4)
# flirty.posts.append(p2, p3)
# to_someone.posts.append(p2, p3, p4)

# The following receives: AttributeError: 'Tag' object has no attribute 'parent_token'

# p1.tags.append(funny)
# p2.tags.append(to_someone, flirty)
# p3.tags.append(to_someone, flirty)
# p4.tags.append(funny,to_someone)

db.session.add_all([p1, p2, p3, p4])
db.session.commit()

db.session.add_all([funny, flirty, to_someone, unassigned])
db.session.commit()