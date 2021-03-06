from model import Model
import database

class Tag(Model):
  idnum = -1
  name = "Default Tag Name"
  description = "Default Tag Description"
  color = [0, 0, 0] # Store color as RGB list, I guess. Probably FIXME
  creator = None # User who created the tag
  privacy = "private" # We probably want something more like an enum here, FIXME
  bookmarks = [] # Bookmarks with this tag
  def __init__(self, name=None, idnum=-1):
    if name:
        self.name = name
        print name
    else:
        self.idnum = idnum
    super(Tag, self).__init__()
  def __repr__(self):
    return "<Tag %d>"%self.idnum
  def load(self):
    variables = database.getTag(self)
    if len(variables) == 1:
      self.idnum = variables[0]
    else:
      self.name = variables[1]
      self.description = variables[2]
      self.color = variables[3]
      self.creator = variables[4]
      self.privacy = variables[5]
      self.bookmarks = variables[6]
  def unload(self):
    database.setTag(self)
