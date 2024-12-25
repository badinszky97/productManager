from .settings import get_database_connection

class Vendor():
    def __init__(self, id, company, address):
        """ Create element from scratch"""
        self.id = id
        self.company = company
        self.address = address
        self.conn = get_database_connection()
    def __str__(self):
        return f"ID: {self.id}, Company: {self.company}, Address: {self.address}"
    
    def load_parameters_from_database(self, id):
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT * FROM vendors WHERE ID='{id}'")
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0],result[1],result[2])

    def createInDatabase(self):
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"INSERT INTO vendors (company, address) VALUES ('{self.company}', '{self.address}')"
            cur.execute(query)
            self.conn.commit()
            self.id = cur.lastrowid

    def delete(self):
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"DELETE FROM vendors WHERE ID={self.id}"
            print(str(query))
            cur.execute(query)
            self.conn.commit()
       
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