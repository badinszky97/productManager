from .settings import get_database_connection

class Media():
    def __init__(self, path, Description, refs=0, id=-1):
        """ Create element from scratch"""
        self.id = id
        self.path = path
        self.description = Description
        self.is_image = self.path.split(".")[-1] in ["jpg", "png", "webp"] if path != "" else False
        self.references = refs
        self.conn = get_database_connection()
    def __str__(self):
        return f"ID: {self.id}, Path: {self.path}, Description: {self.description}, is_image: {self.is_image}"
    
    def load_parameters_from_database(self, id):
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM files WHERE ID='{id}'")
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[1],result[2],0,result[0])
            #print(self)

    def createInDatabase(self):
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"INSERT INTO files (path, description) VALUES ('{self.path}', '{self.description}')"
            try:
                cur.execute(query)
                self.conn.commit()
                self.id = cur.lastrowid
            except:
                return False
            return True
    
    def attachFileToElement(self, id):
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"INSERT INTO file_connects (file_id, element_id) VALUES ('{self.id}', '{id}')"
            try:
                cur.execute(query)
                self.conn.commit()
            except:
                return False
            return True

    def delete(self):
        import os
        from .settings import PRODUCTMANAGER_VARIABLES
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"DELETE FROM files WHERE ID={self.id}"
            #print(str(query))
            try:
                cur.execute(query)
                self.conn.commit()
                os.remove(f"{PRODUCTMANAGER_VARIABLES["media_path"]}/{self.path}")
            except:
                return False
            return True


def get_all_media():
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()

            query = "SELECT files.id,path,Description, sum(if(icon is null, 0,1)) as refs FROM files LEFT JOIN elements ON elements.Icon=files.id group by files.id;"

            cur.execute(query)
            all_meida = []
            for (id, path, Description, refs) in cur:
                current_media = Media(path, Description, refs, id)
                all_meida.append(current_media)
            return all_meida
        else:
             return []