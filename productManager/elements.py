from .settings import get_database_connection
from .media import Media
from joblib import Parallel,delayed 

import time



class Element():
    def __init__(self, id=0, name="", type="", code="", instock=0, icon=""):
        """ Create element from scratch"""
        self.id = id
        self.name = name
        self.type = type
        self.code = code
        self.instock = instock
        self.icon = icon

        self.conn = get_database_connection()
        #self.conn.autocommit = True
    def __del__(self):
        self.conn.close()

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Type: {self.type}, Code: {self.code}, InStock: {self.instock}, Icon: {self.icon}"
    
    def load_parameters_from_database(self, part_id):
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT e.id, e.Name, t.Description, e.Code, e.InStock, IF(e.Icon IS NULL, NULL, files.path) as Icon FROM (elements as e, element_types as t) LEFT JOIN files ON files.ID=e.Icon WHERE e.ID={part_id} and e.Type=t.ID;"
            cur.execute(query)
            
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0], result[1], result[2], result[3], result[4], result[5])

    @property
    def purchaseOpportunities(self):
        po_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT o.id, v.company, o.price, pu.ShortTerm, link, unit, o.orderCode FROM orderable as o, price_units as pu, vendors as v WHERE o.PriceUnit=pu.ID and o.ElementCode={self.id} and o.VendorCode=v.ID")
            for (id, company, price, priceunit, link, unit, code) in cur:
                po_array.append({'id' : id, 'company' : company, 'price' : price, 'priceunit' : priceunit, 'link' : link, 'unit' : unit, 'code' : code})
        return po_array

    @property
    def consist(self):
        consist_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT e.Name, c.Pieces, t.Description as Type, files.path as Icon, e.code, e.id FROM (consist as c, elements as e, element_types as t) LEFT JOIN files on files.ID=e.Icon where c.Container={self.id} and c.Element=e.id and t.id=e.Type"
            cur.execute(query)
            for (name, pieces, type, icon, code, elementID) in cur:
                consist_array.append({'name' : name, 'pieces' : pieces, 'type' : type, 'icon' : icon, 'code' : code, "elementID" : elementID})
        return consist_array

    @property
    def consist_short_list(self):
        consist_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT elements.id FROM consist, elements, element_types WHERE consist.Container={self.id} and consist.Element=elements.id and element_types.id=elements.Type;"
            cur.execute(query)
            for (elementID) in cur:
                new_element = Element()
                new_element.load_parameters_from_database(elementID[0])
                consist_array.append(new_element)
        return consist_array

    @property
    def get_tree_diagram_piece(self):
        start = time.time()
        tree_view = f"<div class=\"entry\">\n<span>{self.name}</span>\n"
        if(len(self.consist) > 0):
            tree_view = tree_view + "<div class=\"branch\">\n"
            for element in self.consist_short_list:
                tree_view = tree_view + element.get_tree_diagram_piece
            tree_view = tree_view + "</div>\n"

        tree_view = tree_view + "\n" + "</div>\n"
        stop = time.time()
        print(f"Tree execution time of {self.name}: " + str(stop-start))
        return tree_view
    

    @property
    def mediaList(self):
        media_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT f.path, f.description FROM files as f, file_connects as fc, elements as e WHERE fc.file_id=f.id and e.id = fc.element_id and e.id={self.id}")
            for (path, description) in cur:
                current_element = Media(path, description)
                media_array.append(current_element)
        return media_array
        
    
    @property
    def bom(self):
        bom_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"WITH RECURSIVE bom AS ( \
                            SELECT \
                                c1.Container as ContainerID, \
                                c1.Element as ElementID, \
                                c1.Pieces as Pieces, \
                                e1.name as ChildName, \
                                e1.Type, \
                                0 AS depth \
                            FROM \
                                consist as c1, \
                                elements as e1 \
                            WHERE \
                                c1.Element = e1.id \
                                and \
                                c1.Container={self.id} \
                            UNION ALL \
                                SELECT \
                                    c2.Container as ContainerID, \
                                    c2.Element as ElementID, \
                                    c2.Pieces * s.Pieces as Pieces, \
                                    e2.name as ChildName, \
                                    e2.Type , \
                                    depth + 1 \
                                FROM \
                                    consist as c2, \
                                    elements as e2, \
                                    bom as s \
                                WHERE \
                                    s.ElementID = c2.Container \
                                    and c2.Element = e2.id \
                            ) \
                        SELECT ContainerID,ElementID,Pieces,ChildName,t.Description, IF(Icon IS NULL, NULL, files.path) FROM (bom, elements as e, element_types as t) LEFT JOIN files ON files.ID = Icon WHERE e.id=ElementID AND e.type=t.id;"
            cur.execute(query)
            for (ContainerID, ElementID, Pieces, ChildName, Type, Icon) in cur:
                bom_array.append({'ContainerID' : ContainerID, 'ElementID' : ElementID, 'Pieces' : Pieces, 'ChildName' : ChildName, 'Type' : Type, "Icon" : Icon})
        return bom_array

    def change_icon(self, icon_path):
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"UPDATE elements SET Icon=(SELECT ID FROM files WHERE path='{icon_path}') WHERE ID={self.id}")
            self.conn.commit()
            self.load_parameters_from_database(self.id)


    def createInDatabase(self):
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"INSERT INTO elements (Name, Type, Code) VALUES ('{self.name}', (SELECT ID FROM element_types WHERE description=\'{self.type}\'), '{self.code}')"
            cur.execute(query)
            self.conn.commit()
            self.load_parameters_from_database(cur.lastrowid)
    
    def delete(self):
        if self.conn != None:
            cur = self.conn.cursor()           
            query = f"DELETE FROM elements WHERE id={self.id}"
            cur.execute(query)
            self.conn.commit()

    def add_purchase_opportunity(self, vendorCode, priceUnit, price, unit, code, link):
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"INSERT INTO orderable (VendorCode, ElementCode, PriceUnit, Price, unit, link, orderCode) VALUES ({vendorCode}, '{self.id}' ,'{priceUnit}', {price}, '{unit}', '{link}', '{code}')"
            cur.execute(query)
            self.conn.commit()
            self.load_parameters_from_database(self.id)

    def add_consist_element(self, childID, pieces):
        if self.conn != None:
            cur = self.conn.cursor()
            print(f"INSERT INTO consist (Container, Element, Pieces) VALUES ('{self.id}' ,'{childID}', {pieces})")
            query = f"INSERT INTO consist (Container, Element, Pieces) VALUES ('{self.id}' ,'{childID}', {pieces})"
            cur.execute(query)
            self.conn.commit()
            self.load_parameters_from_database(self.id)

    def modify_consist_element(self, childID, pieces):
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"UPDATE consist SET pieces={pieces} WHERE Element={childID} and Container={self.id}")
            self.conn.commit()
            self.load_parameters_from_database(self.id)

    def delete_consist_element(self, childID):
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"DELETE FROM consist WHERE Element={childID} and Container={self.id}"
            cur.execute(query)
            self.conn.commit()
            self.load_parameters_from_database(self.id)

    def delete_purchase_opportunity(self, opportunityID):
         if self.conn != None:
            cur = self.conn.cursor()
            query = f"DELETE FROM orderable WHERE id={opportunityID}"
            print(query)
            cur.execute(query)
            self.conn.commit()       
            self.load_parameters_from_database(self.id)
 

def get_all_elements(type="Part", name="", code=""):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()

            if(type=="all" or type==""):
                type_statement = ""
            else:
                type_statement = f"type=(SELECT ID FROM element_types WHERE description='{type}') and"
            query = ""
            query = f"SELECT * FROM elements WHERE {type_statement} UPPER(name) LIKE UPPER('%{name}%') and UPPER(code) LIKE UPPER('%{code}%')"
            
            print(query)
            cur.execute(query)
            all_elements = []
            for (id, name, type, code, instock, icon) in cur:
                current_element = Element(id, name, type, code, instock, icon)
                current_element.load_parameters_from_database(id)
                all_elements.append(current_element)
            return all_elements
        else:
             return []
        
        
