from .settings import get_database_connection



class Media():
    def __init__(self, path, Description):
        """ Create element from scratch"""
        self.id = -1
        self.path = path
        self.description = Description
        self.is_image = self.path.split(".")[-1] in ["jpg", "png", "webp"]
    def __str__(self):
        return f"ID: {self.id}, Path: {self.path}, Description: {self.description}, is_image: {self.is_image}"
    
    def load_parameters_from_database(self, id):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM files WHERE ID='{id}'")
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0],result[1],result[2])
            print(self)

    def createInDatabase(self):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            
            query = f"INSERT INTO files (path, description) VALUES ('{self.path}', '{self.description}')"
            print(query)
            cur.execute(query)
            conn.commit()
            self.id = cur.lastrowid
            conn.close() 
    
    def attachFileToElement(self, id):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            
            query = f"INSERT INTO file_connects (file_id, element_id) VALUES ('{self.id}', '{id}')"
            print(query)
            cur.execute(query)
            conn.commit()
            conn.close() 

def get_all_media():
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM files")
            all_meida = []
            for (ID, path, Description) in cur:
                current_media = Media(ID, path, Description)
                all_meida.append(current_media)
            return all_meida
        else:
             return []