from .settings import get_database_connection


class Element():
    def __init__(self, id=0, name="", type=0, code="", instock=0, icon=""):
        """ Create element from scratch"""
        self.id = id
        self.name = name
        self.type = type
        self.code = code
        self.instock = instock
        self.icon = icon
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Type: {self.type}, Code: {self.code}, InStock: {self.instock}, Icon: {self.icon}"
    
    def load_parameters_from_database(self, part_id):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            cur.execute(f"SELECT e.id, e.name, t.description, e.code, e.instock, IF(e.icon is null, null, f.path) as icon FROM elements as e, files as f, element_types as t WHERE e.ID={part_id} and  e.type=t.id and (e.icon=f.id or e.icon is null) LIMIT 1;")
            
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0], result[1], result[2], result[3], result[4], result[5])
            print(self)

    def createInDatabase(self):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            
            query = f"INSERT INTO elements (Name, Type, Code) VALUES ('{self.name}', (SELECT ID FROM element_types WHERE description=\'{self.type}\'), '{self.code}')"
            print(query)
            cur.execute(query)
            conn.commit()
            conn.close() 
 
            print("Hozzáadva")


def get_all_elements(type="Part"):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            print(f"SELECT * FROM elements WHERE type=(SELECT ID FROM element_types WHERE description='{type}')")
            cur.execute(f"SELECT * FROM elements WHERE type=(SELECT ID FROM element_types WHERE description='{type}')")
            all_elements = []
            for (id, name, type, code, instock, icon) in cur:
                current_element = Element(id, name, type, code, instock, icon)
                current_element.load_parameters_from_database(id)
                all_elements.append(current_element)
            print(str(all_elements))
            return all_elements
        else:
             return []
        
        
