from .settings import get_database_connection

class Media():
    """
        Egy osztály, amelyik egy feltöltött fájlt reprezentál.
    """
    
    def __init__(self, path, Description, refs=0, id=-1):
        """
            Az osztály konstriktora. Üres elem létrehozásakor használatos.
            Itt készül egy új adatbáziskapcsolat ami kizárólag erre az elemre használatos.

            Bementi paraméterek:
                - path:<str> -> A fájl elérési útja (kötelező mező)
                - Description:<str> -> A fájl leírása (kötelező mező)
                - id:<int> -> Az adatbáizban lévő egyedi ID (default: -1, nincs az adatbázisban)
            
            Kimenet:
                - Egy objektum az elem reprezentálására
        """
        self.id = id
        self.path = path
        self.description = Description
        self.is_image = self.path.split(".")[-1] in ["jpg", "png", "webp"] if path != "" else False
        self.references = refs
        self.conn = get_database_connection()

    def __str__(self):
        """ Az objektum alapadatainak kiiratása szöveges formátumban. """
        return f"ID: {self.id}, Path: {self.path}, Description: {self.description}, is_image: {self.is_image}"
    
    def load_parameters_from_database(self, id):
        """ 
            Az objektum belső változóinak feltöltése az adatbázisból letöltött adatokkal.
            A függvény lekérdezi az adatbázisból a kért elemet és feltölti az objektum következő változóit a letöltött értékekkel:
                -id
                -path
                -description

            Bemeneti paraméterek:
                - id:<int> -> Az adatbázisban lévő elem egyedi azonosítója 
        """
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM files WHERE ID='{id}'")
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[1],result[2],0,result[0])

    def createInDatabase(self):
        """
            Egy üres elem létrehozása, majd annak adatokkal történő feltöltése után ez a függvény hozza létre az elemet az adatbázisban.
            A konzisztencia megtartása végett az objektum ezután felülírja magát az adatbázisban tárolt információkkal.

            Kimeneti érték:
                - success:<boolean>
        """
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
        """
            A fájl hozzárendelése egy elemhez az adatbázisban. Itt alá-fölé rendeltségi viszony alakul ki az elem és a fájl között.

            Kimeneti érték:
                - success:<boolean>
        """
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
        """
            A fájl törlése az adatbázisból és a fájlrendszerről is.
            A destruktor nem hívódik meg automatikusan az eljárás végén.

            Kimeneti érték:
                - success:<boolean>
        """
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