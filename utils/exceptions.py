class NotInTypeError(Exception):
    def __init__(self, collection, type):
        self.type = type
        self.collection = collection
        self.message = f"Type '{self.type}' of {self.collection} is not supported"
        super().__init__(self.message)
