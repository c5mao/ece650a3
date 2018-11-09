import sys
import re
#import intersect

# YOUR CODE GOES HERE
#Define the clase structure of database, include a name space and a coordination set x and y
class street_object:
  name =''
  vertices = []
  edges = []
  def __init__(self, name, vertices, edges):
    self.name = name          #string
    self.vertices = vertices  #point object
    self.edges = edges        #line object


#Parse the input into three parts:command, street name and coordination by xi and yi
def parse_line(line):
    
    regex = re.compile(r'''
         ".*?" | # double quoted substring
         \(.*?\) |# 
         \S+ # all the rest
         ''', re.VERBOSE)

    sp = regex.findall(line)
    #print sp
    #print 'length of sp =', len(sp)

    return (sp)

#Creat a street object
def creat_street(sp):
    numbers_rx = r'(-?[0-9]+)'
    text_rx = r'(\W)'
    i = 2
    vertices = []
    edges = []
    street_name = re.sub(text_rx,' ', sp[1]).lower()
    #print 'street name', street_name
    for i in range (2, len(sp)):
        cor = re.findall(numbers_rx, sp[i])
        if len(cor)==2:
            cor_x=int(cor[0])
            cor_y=int(cor[1])
            vertices.append(intersect.Point(cor_x, cor_y))
        else:
            return -1

    j = 0
    for j in range (0, len(vertices)-1):
        edges.append(intersect.Line(vertices[j], vertices[j+1]))


    street=street_object(street_name, vertices, edges)

    return street
    
#Manage the input into database
def db_management(sp, db_list, global_v_dic):
    command = sp[0]
    text_rx = r'(\W)'
    #print 'comand:',command

    if sp[0] == 'a': # Add a new street
        #Creat a street object
        if len(sp) > 3:
            error=creat_street(sp)
            if error == -1:
                return db_list, global_v_dic
            else:
                db=error
        else:
        	sys.stdout.write("Error: Not enough input arguments\n")
        	sys.stdout.flush()
        	return db_list, global_v_dic
        #Check if there exist a street with the same street name
        j=0
        name = re.sub(text_rx,' ', sp[1]).lower()
        for j in range (0,len(db_list)):
            if db_list[j].name == name:
                return db_list, global_v_dic
        db_list.append(db)
    elif sp [0] == 'r': #remove a street
        #remove all the streets for assignment 3
        del db_list[:]
        return db_list, global_v_dic
    elif sp [0] == 'c':#change a street
        if len(db_list)==0:
            sys.stdout.write("Error: NULL database\n")
            sys.stdout.flush()
            return db_list, global_v_dic

        j=0
        name = re.sub(text_rx,' ', sp[1]).lower()
        for j in range (0,len(db_list)):
            if db_list[j].name == name:
                if len(sp) > 3:
                    db_list[j]=creat_street(sp)
                else:
                    sys.stdout.write("Error: Not enough input arguments\n")
                    sys.stdout.flush()
                return db_list, global_v_dic
    elif sp [0] == 'g':#generate the graph
        if len(sp)>1:
            sys.stdout.write("Error: Invalid Command\n")
            sys.stdout.flush()
            return db_list, global_v_dic
        if len(db_list)==0:
            sys.stdout.write("Error: failed to generate valid input for 25 simultaneous attempts\n")
            sys.stdout.flush()
            return db_list, global_v_dic
        #print'Generate the graph according to the present streets'
        pres_v_dic={}
        pres_e_dic=[]
        pres_v_dic,pre_e_dic,global_v_dic = intersect.generate_graph(db_list,pres_v_dic,pres_e_dic,global_v_dic)
    else: 
        sys.stdout.write("Error: Invalid Command\n")
        sys.stdout.flush()


    return db_list, global_v_dic


def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    db_list = [] #List for storing street objects
    global_v_dic = {} #global vertices while the program running
    print 'running from python'
    while True:
        try:
            line = sys.stdin.readline()
            if line == "":
                break
        
            #Parse and save the input
            input_data = parse_line(line)
            #There is no need to have a global dic in assignment 3
            global_v_dic = {} #global vertices while the program running
            db_list, global_v_dic = db_management(input_data, db_list, global_v_dic)

        except:
            sys.stdout.write("Error: Invalid Input\n")
            sys.stdout.flush()

    sys.exit(0)

if __name__ == '__main__':
    main()
