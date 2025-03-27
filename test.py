import unittest
from productManager.elements import Element
from productManager.settings import get_database_connection
from productManager.vendor import Vendor, get_all_vendors

def get_one_result_from_query(conn, query):
    if conn != None:
        cur = conn.cursor()
        cur.execute(query)
        result=cur.fetchone()
        print("One result: " + str(result[0]))
        return result[0]
    return None
                

class TestAddFunction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            f = open('databases/test.sql', 'r')
            query = f.read()
            for row in query.split(";"):
                if row.strip().replace("\n", "") != "":
                    query = str(row).strip().replace("\n", "") + ";" 
                    cur.execute(query)
                    conn.commit()

    @classmethod
    def tearDownClass(cls):
        print("Destructor")

    def test_Element_class_and_algorithm(self):
        conn = get_database_connection()
        conn.autocommit = True

    # check if the element table is empty
        res = get_one_result_from_query(conn, "SELECT COUNT(*) FROM elements")
        self.assertEqual(0, res, "The element table is not empty at the beginning")

    # Projects
        LaptopManufacturing = Element(name="Laptop manufacturing", type="Project", code="PM0001")
        LaptopManufacturing.createInDatabase()
    # Products
        Laptop1 = Element(name="Laptop-X", type="Product", code="PX0001")
        Laptop1.createInDatabase()
    # Assemblies
        LaptopScreenAssembly = Element(name="Laptop Screen Assembly", type="Assembly", code="LS0001")
        LaptopKeyboardAssembly = Element(name="Laptop Keyboard Assembly", type="Assembly", code="KA0001")
        LaptopMainboardAssembly = Element(name="Laptop Mainboard Assembly", type="Assembly", code="MA0001")
        LaptopScreenAssembly.createInDatabase()
        LaptopKeyboardAssembly.createInDatabase()
        LaptopMainboardAssembly.createInDatabase()
    # Operations
        AssembleDisplay = Element(name="Assemble Screen", type="Operation", code="OP0001")
        AssembleKeyboard = Element(name="Assemble Screen", type="Operation", code="OP0002")
        AssembleMainboard = Element(name="Assemble Mainboard", type="Operation", code="OP0003")
        AssembleLaptop = Element(name="Assemble Laptop", type="Operation", code="OP0004")
        AssembleDisplay.createInDatabase()
        AssembleKeyboard.createInDatabase()
        AssembleMainboard.createInDatabase()
        AssembleLaptop.createInDatabase()
    # Parts
        LaptopScreenPanel = Element(name="Laptop Screen Panel", type="Part", code="SP0001")
        LaptopScreenBazel = Element(name="Laptop Screen Bazel", type="Part", code="SB0001")
        LaptopDisplayCable = Element(name="Laptop Display Cable", type="Part", code="DC0001")
        LaptopKeyboard = Element(name="Laptop Keyboard", type="Part", code="KB0001")
        LaptopKeySwitch = Element(name="Laptop Key Switches", type="Part", code="KS0001")
        LaptopMainboard = Element(name="Laptop Key Switches", type="Part", code="KS0002")
        LaptopCPU = Element(name="Laptop CPU", type="Part", code="LC0001")
        LaptopRAM = Element(name="Laptop RAM", type="Part", code="LR0001")

        LaptopScreenPanel.createInDatabase()
        LaptopScreenBazel.createInDatabase()
        LaptopDisplayCable.createInDatabase()
        LaptopKeyboard.createInDatabase()
        LaptopKeySwitch.createInDatabase()
        LaptopMainboard.createInDatabase()
        LaptopCPU.createInDatabase()
        LaptopRAM.createInDatabase()

        res = get_one_result_from_query(conn, "SELECT COUNT(*) FROM elements")
        self.assertEqual(17, res, "Not all the 10 elements were added to the database")

    # Build consist table
    # Projects
        LaptopManufacturing.add_consist_element(Laptop1.id,1)
    # Products
        Laptop1.add_consist_element(LaptopScreenAssembly.id,1)
        Laptop1.add_consist_element(LaptopKeyboardAssembly.id,1)
        Laptop1.add_consist_element(LaptopMainboardAssembly.id,1)
        Laptop1.add_consist_element(AssembleLaptop.id,2)
    # Assemblies
        LaptopScreenAssembly.add_consist_element(LaptopScreenPanel.id,1)
        LaptopScreenAssembly.add_consist_element(LaptopScreenBazel.id,1)
        LaptopScreenAssembly.add_consist_element(LaptopDisplayCable.id,1)
        LaptopScreenAssembly.add_consist_element(AssembleDisplay.id,2)

        LaptopKeyboardAssembly.add_consist_element(LaptopKeyboard.id,1)
        LaptopKeyboardAssembly.add_consist_element(LaptopKeySwitch.id,101)
        LaptopKeyboardAssembly.add_consist_element(AssembleKeyboard.id,2)

        LaptopMainboardAssembly.add_consist_element(LaptopMainboard.id,1)
        LaptopMainboardAssembly.add_consist_element(LaptopCPU.id,1)
        LaptopMainboardAssembly.add_consist_element(LaptopRAM.id,4)
        LaptopMainboardAssembly.add_consist_element(AssembleMainboard.id,2)


        self.assertEqual(len(Laptop1.consist), 4, "Not all the 4 elements were added to the consist list of Laptop1")
        self.assertEqual(len(LaptopScreenAssembly.consist), 4, "Not all the 4 elements were added to the consist list of LaptopScreenAssembly")
        self.assertEqual(len(LaptopKeyboardAssembly.consist), 3, "Not all the 4 elements were added to the consist list of LaptopKeyboardAssembly")
        self.assertEqual(len(LaptopMainboardAssembly.consist), 4, "Not all the 4 elements were added to the consist list of LaptopMainboardAssembly")

        #Vendors
        Vendor1 = Vendor(1,"Vendor 1 name", "Address1")
        Vendor1.createInDatabase()
        Vendor2 = Vendor(2,"Vendor 2 name", "Address2")
        Vendor2.createInDatabase()
        Vendor3 = Vendor(3,"Vendor 3 name", "Address3")
        Vendor3.createInDatabase()
        Vendor4 = Vendor(4,"Vendor 4 name", "Address4")
        Vendor4.createInDatabase()

        self.assertEqual(len(get_all_vendors()), 4, "Not all the 4 elements were added to the vendor table")

        # Purchase opprotunities
        LaptopRAM.add_purchase_opportunity(1,1,1000,"pcs",123,"-") # 1000 HUF (it has 4 of them)
        LaptopMainboard.add_purchase_opportunity(1,1,2000,"pcs",1234,"-") # 2000 HUF
        self.assertEqual(LaptopManufacturing.sum_price[0]["min_price"], 6000.0, "The price of the full project does not match.")

if __name__ == '__main__':
    unittest.main()