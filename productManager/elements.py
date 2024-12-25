from .settings import get_database_connection
from .media import Media


class Element():
    def __init__(self, id=0, name="", type=0, code="", instock=0, icon=""):
        """ Create element from scratch"""
        self.id = id
        self.name = name
        self.type = type
        self.code = code
        self.instock = instock
        self.icon = icon
        self.mediaList = []

        self.conn = get_database_connection()
    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Type: {self.type}, Code: {self.code}, InStock: {self.instock}, Icon: {self.icon}"
    
    def load_parameters_from_database(self, part_id):
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT e.id, e.name, t.description, e.code, e.instock, IF(e.icon is null, null, f.path) as icon FROM elements as e, files as f, element_types as t WHERE e.ID={part_id} and  e.type=t.id and (e.icon=f.id or e.icon is null) LIMIT 1;")
            
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0], result[1], result[2], result[3], result[4], result[5])

            cur.execute(f"SELECT f.path, f.description FROM files as f, file_connects as fc, elements as e WHERE fc.file_id=f.id and e.id = fc.element_id and e.id={self.id}")
            for (path, description) in cur:
                current_element = Media(path, description)
                self.mediaList.append(current_element)
                print("UJ file: " + str(current_element))
            
    def change_icon(self, icon_path):
        if self.conn != None:
            cur = self.conn.cursor()
            print(f"UPDATE elements SET Icon=(SELECT ID FROM files WHERE path='{icon_path}') WHERE ID={self.id}")
            cur.execute(f"UPDATE elements SET Icon=(SELECT ID FROM files WHERE path='{icon_path}') WHERE ID={self.id}")
            self.conn.commit()
            self.conn.close() 


    def createInDatabase(self):
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"INSERT INTO elements (Name, Type, Code) VALUES ('{self.name}', (SELECT ID FROM element_types WHERE description=\'{self.type}\'), '{self.code}')"
            cur.execute(query)
            self.conn.commit()
            self.conn.close() 
    
    def delete(self):
        self.conn = get_database_connection()
        if self.conn != None:
            cur = self.conn.cursor()           
            query = f"DELETE FROM elements WHERE id={self.id}"
            cur.execute(query)
            self.conn.commit()
            self.conn.close() 
 

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
        
        
