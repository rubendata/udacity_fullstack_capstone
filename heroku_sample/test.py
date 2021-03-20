class Post():  
  __tablename__ = 'posts'



  def __init__(self, title, content, author, date):
    self.title = title
    self.content = content
    self.author = author
    self.date = date

  
  def format(self):
    return {
    
      'title': self.title,
      'content': self.content,
      'author': self.author,
      'date': self.date,
    }
test = Post(title="asd", content="asdsad", author="c", date="s")
print (test.title)
print(test.format())