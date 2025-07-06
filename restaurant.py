class Restaurant:
    def __init__(self, store_id, city, address):
        self.store_id = store_id
        self.city = city
        self.address = address
        self.parties_in_line = None

    def name(self):
        return f"Big Way {self.city}"
    
    def set_line_size(self, count):
        self.parties_in_line = count

    def to_dict(self):
        return{
            "name": self.name,
            "city": self.city,
            "address": self.address,
            "store_id": self.store_id,
            "parties_in_line": self.parties_in_line
        }
    
    def __repr__(self):
        return f"{self.name} - {self.parties_in_line} parties ({self.address})"