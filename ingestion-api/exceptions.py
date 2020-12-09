
class UploadProcessException(Exception):
  """Raised by the JSON upload processor whenever any error happens during the parsing or saving process."""

  def __init__(self, message, status_code=400):
    self.message = message
    self.status_code = status_code

  def __str__(self):
      return str(self.message)
