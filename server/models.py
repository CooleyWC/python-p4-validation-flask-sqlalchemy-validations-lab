from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):

        all_authors = Author.query.all()

        for author in all_authors:
            if name == author.name:
                raise ValueError('author already exists')
        if len(name) < 1:
             raise ValueError('name must be greater than zero')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if not isinstance(number, str) or len(number) != 10 or not number.isdigit():
            raise ValueError('needs to be 10 digits')
        return number
    


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('error - needs a title')
        clickbaits = ["Won't Believe", "Secret", "Top", "Guess"]
        bait_check = False
        for bait in clickbaits:
            if bait in title:
                bait_check = True
        if not bait_check:
            raise ValueError('needs to be clickbait')
        
        return title
    
    @validates('content')
    def validate_content(self, key, content):
        print(content)
        if len(content) < 250:
            raise ValueError('needs to be at least 250 characters long')
        return content
    

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('can be no more than 250 characters')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        categories = ['Fiction', 'Non-Fiction']

        if category not in categories:
            raise ValueError('category must be either Fiction or Non-Fiction')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
