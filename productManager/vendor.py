from .settings import get_database_connection

class Vendor():
    """
        Egy osztály, amelyik egy létező beszállítót reprezentál.
    """
        
    def __init__(self, id, company, address):
        """
            Az osztály konstriktora. Üres elem létrehozásakor használatos.
            Itt készül egy új adatbáziskapcsolat ami kizárólag erre az elemre használatos.

            Bementi paraméterek:
                - id:<int> -> A fájl elérési útja (kötelező mező)
                - company:<str> -> A cég elnevezése (kötelező mező)
                - address:<str> -> A cég telephelyének címe (kötelező mező)
            
            Kimenet:
                - Egy objektum az elem reprezentálására
        """
        self.id = id
        self.company = company
        self.address = address
        self.conn = get_database_connection()

    def __str__(self):
        """ Az objektum alapadatainak kiiratása szöveges formátumban. """
        return f"ID: {self.id}, Company: {self.company}, Address: {self.address}"
    
    def load_parameters_from_database(self, id):
        """ 
            Az objektum belső változóinak feltöltése az adatbázisból letöltött adatokkal.
            A függvény lekérdezi az adatbázisból a kért elemet és feltölti az objektum következő változóit a letöltött értékekkel:
                -id
                -company
                -address

            Bemeneti paraméterek:
                - id:<int> -> Az adatbázisban lévő elem egyedi azonosítója 
        """

        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM vendors WHERE ID='{id}'")
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0],result[1],result[2])

    def createInDatabase(self):
        """
            Egy üres elem létrehozása, majd annak adatokkal történő feltöltése után ez a függvény hozza létre az elemet az adatbázisban.

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"INSERT INTO vendors (company, address) VALUES ('{self.company}', '{self.address}')"
            try:
                cur.execute(query)
                self.conn.commit()
                self.id = cur.lastrowid
            except:
                return False
            return True

    def delete(self):
        """
            A bejegyzés törlése az adatbázisból.
            A destruktor nem hívódik meg automatikusan az eljárás végén.

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"DELETE FROM vendors WHERE ID={self.id}"
            try:
                cur.execute(query)
                self.conn.commit()
            except:
                return False
            return True
       
def get_all_vendors(company="", address=""):
    conn = get_database_connection()
    if conn != None:
        cur = conn.cursor()
        query = ""

        if(company == "" and address == ""):
            query = f"SELECT * FROM vendors"
        elif(company != "" and address == ""):
            query = f"SELECT * FROM vendors WHERE company LIKE CONCAT('%', UPPER('{company}'), '%')"
        elif(company == "" and address != ""):
            query = f"SELECT * FROM vendors WHERE address LIKE CONCAT('%', UPPER('{address}'), '%')"
        elif(company != "" and address != ""):
            query = f"SELECT * FROM vendors WHERE company LIKE CONCAT('%', UPPER('{company}'), '%') and address LIKE CONCAT('%', UPPER('{address}'), '%')"

        cur.execute(query)
        all_vendors = []
        print(str(query))
        for (id, company, address) in cur:
            all_vendors.append(Vendor(id, company, address))
        return all_vendors
    else:
            return []
    
class PriceUnits():
    """
        A pénznemek kezelését segítő osztály. A pénznemek struktúráját tartalmazza és annak megjelenítését segíti elő.
    """
    def __init__(self, id, unittype, shortterm):
        """ Create element from scratch"""
        self.id = id
        self.unittype = unittype
        self.shortterm = shortterm
    def __str__(self):
        return f"ID: {self.id}, UnitType: {self.unittype}, ShortTerm: {self.shortterm}"

def get_all_price_units():
    conn = get_database_connection()
    if conn != None:
        cur = conn.cursor()
        query = f"SELECT * FROM price_units"
        cur.execute(query)
        all_price_units = []
        print(str(query))
        for (id, unittype, shortterm) in cur:
            all_price_units.append(PriceUnits(id, unittype, shortterm))
        return all_price_units
    else:
            return []