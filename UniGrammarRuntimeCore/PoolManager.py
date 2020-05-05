class PoolManager:
	__slots__ = ("constructed",)

	def __init__(self):
		self.constructed = {}

	def __call__(self, constuctorClass: type, *args, **kwargs):
		if constuctorClass not in self.constructed:
			obj = constuctorClass(*args, **kwargs)
			self.constructed[obj.__class__] = obj
		else:
			obj = self.constructed[constuctorClass]
		return obj
