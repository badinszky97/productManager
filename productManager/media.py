from .settings import get_database_connection



class Media():
    def __init__(self, ID, ElementID, FileType, path, Description):
        """ Create element from scratch"""
        self.id = id
        self.elementid = ElementID
        self.filetype = FileType
        self.path = path
        self.description = Description
    def __str__(self):
        return f"ID: {self.id}, ElementID: {self.elementid}, FileType: {self.filetype}, Path: {self.path}, Description: {self.description}"
    
    def load_parameters_from_database(self, id):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM files WHERE ID='{id}'")
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0],result[1],result[2],result[3],result[4])
            print(self)

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


def get_all_media():
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM files")
            all_meida = []
            for (ID, ElementID, FileType, path, Description) in cur:
                current_media = Media(ID, ElementID, FileType, path, Description)
                all_meida.append(current_media)
            return all_meida
        else:
             return []