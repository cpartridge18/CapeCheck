class Food:
	def __init__(self, id, name, timestamp):
		self.id = id
		self.title = tile
		self.name = name
		self.timestamp = timestamp

	def __repr__(self):
		return '<id {}>'.format(self.id)
	
	def serialize(self):
		return {
			'id':self.id,
			'title':self.title,
			'name':self.name,
			'timestamp':self.timestamp
			}
			
			
