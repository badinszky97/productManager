from .settings import get_database_connection
from .media import Media
from joblib import Parallel,delayed 

import time

class Element():
    """
        Egy osztály, amelyik egy elemet reprezentál a BOM listában. A hierarchia bármely szintjére alkalmazható, minden elem típust képes megvalósítani.
        
        Egy elem létrehozásához két lehetőség van:
            - Üres elem létrehozása a konstruktor kitöltésével
            - Elem betöltése az adatbázisból a load_parameters_from_database függvénnyel
    """
    def __init__(self, id=0, name="", type="", code="", icon=""):
        """
            Az osztály konstriktora. Üres elem létrehozásakor használatos.
            Itt készül egy új adatbáziskapcsolat ami kizárólag erre az elemre használatos.

            Bementi paraméterek:
                - id:<int> -> Az adatbázisban lévő egyedi azonosítója (default:0)
                - name:<str> -> Az elem neve (default:"")
                - type:<str> -> Az elem típusa sztringben kifejezve (default:"")
                - code:<str> -> Az elem egyedi kódja (default:"")
                - icon:<int> -> Referencia az elem kódjának rekorjára a fájlok táblában (default:"")
            
            Kimenet:
                - Egy objektum az elem reprezentálására
        """
        self.id = id
        self.name = name
        self.type = type
        self.code = code
        self.icon = icon

        self.conn = get_database_connection()

    def __del__(self):
        """ Az osztály destruktora. Törlés előtt az élő adatbáziskapcsolat bontása. """
        self.conn.close()

    def __str__(self):
        """ Az objektum alapadatainak kiiratása sztring formátumban. """
        return f"ID: {self.id}, Name: {self.name}, Type: {self.type}, Code: {self.code}, InStock: {self.instock}, Icon: {self.icon}"
    
    def load_parameters_from_database(self, part_id):
        """ 
            Az objektum belső változóinak feltöltése az adatbázisból letöltött adatokkal.
            A függvény lekérdezi az adatbázisból a kért elemet és feltölti az objektum következő változóit a letöltött értékekkel:
                -id
                -name
                -type
                -code
                -icon

            Bemeneti paraméterek:
                - part_id:<int> -> Az adatbázisban lévő elem egyedi azonosítója 
        """
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT e.id, e.Name, t.Description, e.Code, IF(e.Icon IS NULL, NULL, files.path) as Icon FROM (elements as e, element_types as t) LEFT JOIN files ON files.ID=e.Icon WHERE e.ID={part_id} and e.Type=t.ID;"
            cur.execute(query)
            
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                self.__init__(result[0], result[1], result[2], result[3], result[4])

    @property
    def instock(self):
        """
            @property
            Visszaadja egy elem raktárkészletét az adatbázisból.
            Visszatérési értékként egy összesített számot ad, amely az adattáblában lévő beszerzések értékének összege.
            Kimeneti érték:
                - raktárkészlet:<int>
        """
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT SUM(pieces) FROM inventory WHERE element_id={self.id}"
            cur.execute(query)
            result = cur.fetchone() 
            if(cur.rowcount > 0):
                if(result[0] == None):
                    return 0
                else:
                    return result[0]
        return 0

    @property
    def get_inventory(self):
        """
            @property
            Visszaadja egy elem beszerzési történetét az adatbázis alapján.
            Kimentként egy lista várandó amit tartalmazza az összes rekordot a beszerzések táblából, a szükséges mezők:
                - pieces
                - description
                - date
            Ennek a függvénynek a pieces mezőinek összesítése adja az instock() függvény eredményét.

            Kimeneti érték:
                - beszerzési_lista:<list> -> {"pieces", "description", "date"}
        """
        inventory_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT pieces, description, date FROM inventory WHERE element_id={self.id}"
            cur.execute(query)
            for (pieces, description, date) in cur:
                inventory_array.append({'pieces' : pieces, 'description' : description, 'date' : date})
        return inventory_array            

    @property
    def purchaseOpportunities(self):
        """
            @property
            Visszaadja egy elem beszerzési lehetőségeit az adatbázisból.
            Kimeneti érték:
                - beszerzési_lista:<list> -> {"company", "price", "priceunit", "link", "unit", "code"}
        """
        po_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            cur.execute(f"SELECT v.company, o.price, pu.ShortTerm, link, unit, o.orderCode FROM orderable as o, price_units as pu, vendors as v WHERE o.PriceUnit=pu.ID and o.ElementCode={self.id} and o.VendorCode=v.ID")
            for (company, price, priceunit, link, unit, code) in cur:
                po_array.append({'company' : company, 'price' : price, 'priceunit' : priceunit, 'link' : link, 'unit' : unit, 'code' : code})
        return po_array

    @property
    def consist(self):
        """
            @property
            Visszaadja, hogy az adott elem milyen más elemeket tartalmaz. A hierachia szint lefelé történő kibontása egy listába.
            A kibontás gyökérelemét minden esetben az objektum ID-ja határozza meg, ami nem egy bemenő paraméter.
            Visszatérési értékként egy listát ad az elemek adataival.

            Kimeneti érték:
                - tartalmaz_lista:<list> -> {"name", "pieces", "type", "icon", "code", "elementID"}
        """
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
        """
            @property
            Visszaadja, hogy az adott elem milyen más elemeket tartalmaz. A hierachia szint lefelé történő kibontása egy listába.
            A kibontás gyökérelemét minden esetben az objektum ID-ja határozza meg, ami nem egy bemenő paraméter.
            Visszatérési értékként egy listát ad amely az elemek objektumait tartalmazza.

            Kimeneti érték:
                - tartalmaz_lista:<list>
        """
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
        """
            Az elem és az ő által tartalmazott más elemek fa diagramjának kirajzolása HTML kódban.
            Kimeneti érték:
                -kód:<str> -> A HTML kódba közvetlenül beilleszthető kódrészlet amely a fa struktúra kirajzolását valósítja meg.
        """
        start = time.time()
        tree_view = f"<div class=\"entry\">\n<span>{self.name}</span>\n"
        if(len(self.consist) > 0):
            tree_view = tree_view + "<div class=\"branch\">\n"
            for element in self.consist_short_list:
                tree_view = tree_view + element.get_tree_diagram_piece
            tree_view = tree_view + "</div>\n"

        tree_view = tree_view + "\n" + "</div>\n"
        stop = time.time()
        return tree_view
    
    @property
    def mediaList(self):
        """
            @property
            Visszaadja, hogy az adott elemhez milyen fájlok vannak feltöltve az adatbázisban.
            Visszatérési értékként egy listát ad amely a feltöltött fájlok objektumait tartalmazza.

            Kimeneti érték:
                - fájl_lista:<list>
        """
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
        """
            @property
            Visszaadja az elem rekurzívan kidolgozott BOM listáját.
            A gyökér elem minden esetben az adott elem.
            A rekurzív feldolgozást az adatbázis valósítja meg.

            Kimeneti érték:
                - fájl_lista:<list> -> {"ContainerID", "ElementID", "Pieces", "ChildName", "Type", "Icon"}
        """
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
    
    @property
    def prices(self):
        """
            @property
            Visszaadja az elem BOM listájának az adatbázisban rögzített árainak összesítését.
            Ebben a listában szerepel az összes elem amit a szülő tartalmaz és azoknak az árai.
            Az árak mint egységár és mint darabszámmal felszorozott összesített ár is megjelennek.

            Kimeneti érték:
                - fájl_lista:<list> -> {"ElementID", "Pieces", "ChildName", "Description", "Icon", "min_price", "max_price", "min_sum_price", "max_sum_price", "UnitType"}
        """
        price_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT ElementID, Pieces, ChildName, Description, Icon, Min(Price) as min_price, Max(Price) as max_price, Pieces*Min(Price) as min_sum_price,Pieces*Max(Price) as max_sum_price , UnitType FROM \
                        (SELECT ElementID, SUM(Pieces) as Pieces, ChildName, Description, Icon FROM \
                            (WITH RECURSIVE bom AS( SELECT c1.Container AS ContainerID, c1.Element AS ElementID, c1.Pieces AS Pieces, e1.name AS ChildName, e1.Type, 0 AS depth FROM consist AS c1, elements AS e1 WHERE c1.Element = e1.id AND c1.Container = {self.id} UNION ALL SELECT c2.Container AS ContainerID, c2.Element AS ElementID, c2.Pieces * s.Pieces AS Pieces, e2.name AS ChildName, e2.Type, depth + 1 FROM consist AS c2, elements AS e2, bom AS s WHERE s.ElementID = c2.Container AND c2.Element = e2.id ) SELECT ContainerID, ElementID, Pieces, ChildName, t.Description, IF(Icon IS NULL, NULL, files.path) as Icon FROM ( bom, elements AS e, element_types AS t ) LEFT JOIN files ON files.ID = Icon WHERE e.id = ElementID AND e.type = t.id) bom \
                        WHERE (bom.Description = \"Operation\" OR bom.Description = \"Part\") GROUP BY ElementID) \
                        pricelist, orderable, price_units WHERE orderable.ElementCode = ElementID and PriceUnit = price_units.id \
                        GROUP BY ElementID;"
            print(query)
            cur.execute(query)
            for (ElementID, Pieces, ChildName, Description, Icon, min_price, max_price, min_sum_price, max_sum_price , UnitType) in cur:
                price_array.append({'ElementID' : ElementID, 'Pieces' : Pieces, 'ChildName' : ChildName, 'Description' : Description, 'Icon' : Icon, 'min_price' : min_price, 'max_price' : max_price, 'min_sum_price' : min_sum_price, 'max_sum_price' : max_sum_price, 'UnitType' : UnitType})
        return price_array
    
    @property
    def sum_price(self):
        """
            @property
            Visszaadja az elem BOM listájának az adatbázisban rögzített árainak összesítését.
            Ebben a listában szerepel az összes elem amit a szülő tartalmaz és azoknak az árai.
            Az árak mint egységár és mint darabszámmal felszorozott összesített ár is megjelennek.

            Kimeneti érték:
                - fájl_lista:<list> -> {"ChildName", "Description", "min_price", "max_price", "UnitType", "pieces", "unit"}
        """
        price_array = []
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"SELECT ChildName, Description, SUM(min_sum_price) as min, SUM(max_sum_price) as max, UnitType, Pieces, unit FROM \
                    (SELECT ChildName, Description, Pieces*Min(Price) as min_sum_price,Pieces*Max(Price) as max_sum_price , UnitType, Pieces, unit FROM \
                    (SELECT ElementID, SUM(Pieces) as Pieces, ChildName, Description, Icon FROM \
                    (WITH RECURSIVE bom AS( SELECT c1.Container AS ContainerID, c1.Element AS ElementID, c1.Pieces AS Pieces, e1.name AS ChildName, e1.Type, 0 AS depth FROM consist AS c1, elements AS e1 WHERE c1.Element = e1.id AND c1.Container = {self.id} UNION ALL SELECT c2.Container AS ContainerID, c2.Element AS ElementID, c2.Pieces * s.Pieces AS Pieces, e2.name AS ChildName, e2.Type, depth + 1 FROM consist AS c2, elements AS e2, bom AS s WHERE s.ElementID = c2.Container AND c2.Element = e2.id ) SELECT ContainerID, ElementID, Pieces, ChildName, t.Description, IF(Icon IS NULL, NULL, files.path) as Icon FROM ( bom, elements AS e, element_types AS t ) LEFT JOIN files ON files.ID = Icon WHERE e.id = ElementID AND e.type = t.id) bom \
                    WHERE (bom.Description = \"Operation\" OR bom.Description = \"Part\") GROUP BY ElementID) \
                    pricelist, orderable, price_units WHERE orderable.ElementCode = ElementID and PriceUnit = price_units.id \
                    GROUP BY ElementID) sumlist \
                    GROUP BY Description;"
            #print(query)
            cur.execute(query)
            for (ChildName, Description, min_price, max_price, UnitType, pieces, unit) in cur:
                price_array.append({'ChildName' : ChildName, 'Description' : Description, 'min_price' : min_price, 'max_price' : max_price, 'UnitType' : UnitType, 'pieces':pieces, 'unit':unit})
        return price_array

    def change_icon(self, icon_path):
        """
            Megváltoztatja az adatbázisban az elemhez rendelt ikon referenciát.

            Bemeneti érték:
                - icon_path:<int> -> A referencia a fájlok listához

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            cur = self.conn.cursor()
            try:
                cur.execute(f"UPDATE elements SET Icon=(SELECT ID FROM files WHERE path='{icon_path}') WHERE ID={self.id}")
                self.conn.commit()
                self.load_parameters_from_database(self.id)
            except:
                return False
            return True

    def createInDatabase(self):
        """
            Egy üres elem létrehozása, majd annak adatokkal történő feltöltése után ez a függvény hozza létre az elemet az adatbázisban.
            A konzisztencia megtartása végett az objektum ezután felülírja magát az adatbázisban tárolt információkkal.

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            cur = self.conn.cursor()
            
            query = f"INSERT INTO elements (Name, Type, Code) VALUES ('{self.name}', (SELECT ID FROM element_types WHERE description=\'{self.type}\'), '{self.code}')"
            try:
                cur.execute(query)
                self.conn.commit()
                self.load_parameters_from_database(cur.lastrowid)
            except:
                return False
            return True
    
    def delete(self):
        """
            Ez az eljárás kitörli az elemet az adatbázisból. Az objektum konstruktora nem hívódik meg automatikusan ebből.

            Kimeneti érték:
                - success:<boolean>
        """

        if self.conn != None:
            cur = self.conn.cursor()           
            query = f"DELETE FROM elements WHERE id={self.id}"
            try:
                cur.execute(query)
                self.conn.commit()
            except:
                return False
            return True

    def add_purchase_opportunity(self, vendorCode, priceUnit, price, unit, code, link):
        """
            Hozzáad az elemhez egy beszerzési lehetőséget az adatbázisban.
            Bemeneti értékek:
                - beszállító_kód:<str>
                - pénznem:<int> -> az adatbázisban tárolt értékek közüli ID
                - ár:<int>
                - egység:<str>
                - Beszerzési_kód:<str>
                - link:<str>

            Kimeneti érték:
                - success:<boolean>
        """

        if self.conn != None:
            cur = self.conn.cursor()
            query = f"INSERT INTO orderable (VendorCode, ElementCode, PriceUnit, Price, unit, link, orderCode) VALUES ({vendorCode}, '{self.id}' ,'{priceUnit}', {price}, '{unit}', '{link}', '{code}')"
            try:
                cur.execute(query)
                self.conn.commit()
                self.load_parameters_from_database(self.id)
            except:
                return False
            return True

    def add_consist_element(self, childID, pieces):
        """
            Egy elem hozzárendelése az adott objektumhoz. Ezzel a hierarchiában alá-fölé rendeltségi viszonyban lesznek.
            Bemeneti értékek:
                - childID:<int> -> a hozzáadandó elem ID-je
                - pieces:<int> ->  hozzáadandó darabszám

            Kimeneti érték:
                - success:<boolean>
        """

        if self.conn != None:
            print(str(f"ADDING: {childID} {self.id}"))
            if(int(childID) == int(self.id)):
                print("Cannot add itself to its own list")
                return False # prevent adding itself to its own contains list
            child = Element()
            child.load_parameters_from_database(childID)
            
            # prevent adding according to the bom list
            for item in child.bom:
                if(int(item["ElementID"]) == int(self.id)):
                    return False
            
            #return False
            cur = self.conn.cursor()
            #print(f"INSERT INTO consist (Container, Element, Pieces) VALUES ('{self.id}' ,'{childID}', {pieces})")
            query = f"INSERT INTO consist (Container, Element, Pieces) VALUES ('{self.id}' ,'{childID}', {pieces})"
            try:
                cur.execute(query)
                self.conn.commit()
                self.load_parameters_from_database(self.id)
            except:
                return False
            return True

    def modify_consist_element(self, childID, pieces):
        """
            Egy korábban már hozzáadott elem darabszámának módosítása a hierarchia fában.
            Bemeneti értékek:
                - childID:<int> -> a módosítandó elem ID-je
                - pieces:<int> ->  darabszám

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            try:
                cur = self.conn.cursor()
                cur.execute(f"UPDATE consist SET pieces={pieces} WHERE Element={childID} and Container={self.id}")
                self.conn.commit()
                self.load_parameters_from_database(self.id)
            except:
                return False
            return True

    def delete_consist_element(self, childID):
        """
            Egy korábban már hozzáadott elem törlése a listából, így kikerül az alá-fölé rendeltségi hierarchiából.
            Bemeneti értékek:
                - childID:<int> -> a törlendő elem ID-je

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"DELETE FROM consist WHERE Element={childID} and Container={self.id}"
            try:
                cur.execute(query)
                self.conn.commit()
                self.load_parameters_from_database(self.id)
            except:
                return False
            return True

    def delete_purchase_opportunity(self, orderCode):
        """
            Egy korábban már hozzáadott beszerzési lehetőség törlése az adatbázisból.
            Bemeneti értékek:
                - orderCode:<int> -> a törlendő elem ID-je

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            cur = self.conn.cursor()
            query = f"DELETE FROM orderable WHERE orderCode=\"{orderCode}\" and ElementCode={self.id}"
            try:
                cur.execute(query)
                self.conn.commit()       
                self.load_parameters_from_database(self.id)
            except:
                return False
            return True
    
    def add_to_inventory(self, qty, description):
        """
            Egy beszerzés regisztrálása az adatbázisban. Ezzel a függvénnyel növelhető (vagy akár csökkenthető) a raktárkészlete az adott terméknek.
            Bemeneti értékek:
                - qty:<int> -> a darabszám
                - description:<str> -> leírás a beszerzéshez (pl számla sorszám)

            Kimeneti érték:
                - success:<boolean>
        """
        allow_adding_process = True
        if self.conn != None:
            self.conn.autocommit = False
            for needed_element in self.consist:
                print(str(needed_element))
                subelement = Element()
                subelement.load_parameters_from_database(needed_element["elementID"])
                if(int(subelement.instock) < int(needed_element["pieces"]) * int(qty)):
                    allow_adding_process = False
                    break

            if(allow_adding_process):
                cur = self.conn.cursor()
                for needed_element in self.consist:
                    query = f"INSERT INTO inventory (element_id, pieces, description) VALUES ('{subelement.id}' ,'{str(int(needed_element["pieces"]) * -1 * int(qty))}', 'in: {needed_element["code"]}')"
                    cur.execute(query)
                    self.conn.commit()
                
                query = f"INSERT INTO inventory (element_id, pieces, description) VALUES ('{self.id}' ,'{qty}', '{description}')"
                cur.execute(query)
                self.conn.commit()
                self.load_parameters_from_database(self.id)


        return allow_adding_process
 
    def modify_name(self, new_name):
        """
            Módosítja az elem nevét az adatbázisban
            Bemeneti értékek:
                - new_name:<str> -> az új név

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            try:
                cur = self.conn.cursor()
                cur.execute(f"UPDATE elements SET Name='{new_name}' WHERE ID={self.id}")
                self.conn.commit()
                self.load_parameters_from_database(self.id)  
                return True
            except:
                return False

    def modify_code(self, new_code):
        """
            Módosítja az elem kódját az adatbázisban
            Bemeneti értékek:
                - new_code:<str> -> az új kód

            Kimeneti érték:
                - success:<boolean>
        """
        if self.conn != None:
            try:
                cur = self.conn.cursor()
                cur.execute(f"UPDATE elements SET Code='{new_code}' WHERE ID={self.id}")
                self.conn.commit()
                self.load_parameters_from_database(self.id)  
                return True
            except:
                return False

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
            
            #print(query)
            cur.execute(query)
            all_elements = []
            for (id, name, type, code, icon) in cur:
                current_element = Element(id, name, type, code, icon)
                current_element.load_parameters_from_database(id)
                all_elements.append(current_element)
            return all_elements
        else:
             return []
        
        
