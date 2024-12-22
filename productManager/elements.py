from .settings import get_database_connection


class Part():
    def __init__(self, id, name, type, code, instock):
        self.id = id
        self.name = name
        self.type = type
        self.code = code
        self.instock = instock
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Type: {self.type}, Code: {self.code}, InStock: {self.instock}"
    
    def createInDatabase(self):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            
            query = f"INSERT INTO elements (Name, Type, Code) VALUES ('{self.name}', (SELECT ID FROM element_types WHERE description=\'Part\'), '{self.code}')"
            print(query)
            cur.execute(query)
            conn.commit()
            conn.close() 
 
            print("Hozzáadva")


def get_all_parts():
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM elements WHERE type=(SELECT ID FROM element_types WHERE description='Part')")
            all_parts = []
            for (id, name, type, code, instock) in cur:
                current_part = Part(id, name, type, code, instock)
                all_parts.append(current_part)
            return all_parts
        else:
             return []
