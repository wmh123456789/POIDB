
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree,Element  
  
def read_xml(in_path):
    tree = ElementTree()
    tree.parse(in_path)  
    return tree  
  
def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8",xml_declaration=True)  
  
def if_match(node, kv_map):  
    for key in kv_map:  
        if node.get(key) != kv_map.get(key):  
            return False  
    return True  
  
#---------------search -----  
  
def find_nodes(tree, path):  
    return tree.findall(path)  
  
  
def get_node_by_keyvalue(nodelist, kv_map):  
    result_nodes = []  
    for node in nodelist:  
        if if_match(node, kv_map):  
            result_nodes.append(node)  
    return result_nodes  
  
#---------------change -----  
  
def change_node_properties(nodelist, kv_map, is_delete=False):  
    for node in nodelist:  
        for key in kv_map:  
            if is_delete:   
                if key in node.attrib:  
                    del node.attrib[key]  
            else:  
                node.set(key, kv_map.get(key))  
              
def change_node_text(nodelist, text, is_add=False, is_delete=False):  
    for node in nodelist:  
        if is_add:  
            node.text += text  
        elif is_delete:  
            node.text = ""  
        else:  
            node.text = text  
              
def create_node(tag, property_map, content):  
    element = Element(tag, property_map)  
    element.text = content  
    return element  
          
def add_child_node(nodelist, element):  
    for node in nodelist:  
        node.append(element)  
          
def del_node_by_tagkeyvalue(nodelist, tag, kv_map):  
    for parent_node in nodelist:  
        children = parent_node.getchildren()  
        for child in children:  
            if child.tag == tag and if_match(child, kv_map):  
                parent_node.remove(child)  
                          

def insert_mall(father,bldid,aleph,py,nm,bldtype = '1',logo = 'new.jpg',lng = '116.0',lat = '40.0',sinatopic = 'sina'):
  NewMall = ET.SubElement(father,'mall')
  NewMall.set('aleph',aleph)
  NewMall.set('py',py)
  NewMall.set('nm',nm)
  NewMall.set('type',bldtype)
  NewMall.set('logo',logo)
  NewMall.set('lng',lng)
  NewMall.set('lat',lat)
  NewMall.set('sinatopic',sinatopic)
  NewMall.set('id',bldid)


  

# -- Modify Malls --
filePath = 'E:\= Workspaces\Python Space\Modify_XML\\0101.xml'
tree = read_xml(filePath)
root = tree.getroot()
target_del_node = del_node_by_tagkeyvalue([root], "mall", {"id" : "7004"})
insert_mall(root,"7004",'WFJ','WangFuJing','王府井')

nodes = find_nodes(tree, "mall") 
result_nodes = get_node_by_keyvalue(nodes, {"id":"7002"})
change_node_properties(result_nodes, {"logo": "new1.jpg"}) 

tree.write(filePath)


# -- Modify Space --
# filePath = 'E:\= Workspaces\Python Space\Modify_XML\\Template.xml'
# tree = read_xml(filePath)
# root = tree.getroot()
# nodes = find_nodes(tree, "floor") 

# for node in nodes:
#   node.set("brief",node.get("nm"))

# tree.write(filePath)