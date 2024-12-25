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

def get_all_vendors():
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            query = "SELECT * FROM vendors"

            cur.execute(query)
            all_vendors = []
            for (id, company, address) in cur:
                all_vendors.append(Vendor(id, company, address))
            return all_vendors
        else:
             return []