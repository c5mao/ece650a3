import sys

class Point(object):
    def __init__ (self, x, y):
        self.x = round(float(x),2)
        self.y = round(float(y),2)
    def __str__ (self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

class Line(object):
    def __init__ (self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return str(self.src) + '-->' + str(self.dst)

#This function is used to sort the vertices and intersections in order
def sort_vertices(points_list,src_point):
    points_list.sort(key = lambda p: (p.x-src_point.x)**2+(p.y-src_point.y)**2)
    '''
    for value in points_list:
        print value
    '''
    return points_list

def intersect (l1, l2):

    p=[]

    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    #Case y=ax+b where x1!=x2 x3!=x4
    xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
    xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

    if abs(xnum)<=0.01 and abs(xden)<=0.01:
        if (abs(x1-x2)<=0.01 and abs(y1-y2)<=0.01) or (abs(x3-x4)<=0.01 and abs(y3-y4)<=0.01):
            return -3 #not a valid graph
        if abs(max(x1,x2,x3,x4)-min(x1,x2,x3,x4)-abs(x1-x2)-abs(x3-x4))<=0.01:
            p.append(l1.src)
            p.append(l1.dst)
            return p
        if max(x1,x2,x3,x4)-min(x1,x2,x3,x4) < abs(x1-x2)+abs(x3-x4):
            if max(x1,x2,x3,x4)-min(x1,x2,x3,x4)>max(abs(x1-x2),abs(x3-x4)):#overlap but not contain
                return -3 #not a valid graph
            else:
                if abs(x1-x2)<abs(x3-x4):
                    p.append(l1.src)
                    p.append(l1.dst)
                    return p
                else:
                    p.append(l1.src)
                    p.append(l1.dst)
                    p.append(l2.src)
                    p.append(l2.dst)
                    return p

    if abs(xden) <= 0.01:
        return -1 #parallel without intersection
    xcoor =  xnum / xden

    if xcoor>max(x1,x2) or xcoor>max(x3,x4) or xcoor<min(x1,x2) or xcoor<min(x3,x4):
        return -2 #intersection out of range

    ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)

    ycoor = ynum / yden

    if ycoor>max(y1,y2) or ycoor>max(y3,y4) or ycoor<min(y1,y2) or ycoor<min(y3,y4):
        return -2 #intersection out of range

    p.append(Point(xcoor, ycoor))

    return p



def save_intersect(intersect_points,pres_v_dic,pres_e_dic,global_v_dic):
    i=0
    x=0 
    for x in range (0,len(intersect_points)-1):
        edge_exist_flag=0
        if len(global_v_dic)==0:
            max_key=-1  # for assigment 3, key start from 0
        else:
            max_key=max(global_v_dic.keys())
        src_key = max_key + 1
        dst_key = max_key + 1
        for key, value in global_v_dic.iteritems():
            if abs(intersect_points[x+1].x-value.x)<=0.01 and abs(intersect_points[x+1].y-value.y)<=0.01:
                dst_key = key
            if abs(intersect_points[x].x-value.x)<=0.01 and abs(intersect_points[x].y-value.y)<=0.01:
                src_key = key
   
        if src_key==dst_key:
            dst_key = src_key + 1
        pres_v_dic[src_key]=intersect_points[x]
        pres_v_dic[dst_key]=intersect_points[x+1]

        if src_key not in global_v_dic.keys():
            global_v_dic[src_key]=intersect_points[x]
        if dst_key not in global_v_dic.keys():
            global_v_dic[dst_key]=intersect_points[x+1]

        for value in pres_e_dic:
            if value == '<'+str(src_key)+','+str(dst_key)+'>' or value == '<'+str(dst_key)+','+str(src_key)+'>':
                edge_exist_flag=1
                break
        if edge_exist_flag==0:
            pres_e_dic.append('<'+str(src_key)+','+str(dst_key)+'>')

    return pres_v_dic,pres_e_dic,global_v_dic


#This function is used to generate the graph based on the street object list
def generate_graph(db_list,pres_v_dic,pres_e_dic,global_v_dic):
    i=0
    j=0
    m=0
    n=0
    for i in range (0,len(db_list)):
        for j in range (0,len(db_list[i].edges)):
            intersect_points=[]
            for m in range (0,len(db_list)):
                for n in range (0,len(db_list[m].edges)):
                    if db_list[i].name == db_list[m].name:
                        break
                    error = intersect(db_list[i].edges[j],db_list[m].edges[n])
                    if error == -1:
                        #print db_list[i].edges[j], 'with', db_list[m].edges[n], 'no intersection'
                        pass
                    elif error == -2:
                        #print db_list[i].edges[j], 'with', db_list[m].edges[n], 'intersection out of range'
                        pass
                    elif error == -3:
                        print 'Error: Invalid Streets'
                        pres_v_dic={}
                        pres_e_dic=[]
                        return pres_v_dic,pres_e_dic,global_v_dic
                    else:
                        #print db_list[i].edges[j], 'with', db_list[m].edges[n], 'has intersections'
                        for p in error:
                            exist_flag=0
                            for value in intersect_points:
                               if abs(value.x-p.x)<=0.01 and abs(value.y-p.y)<=0.01:
                                exist_flag=1
                                break
                            if exist_flag==0:
                                intersect_points.append(p)

            if len(intersect_points)>0:
                src_exist_flag=0
                dst_exist_flag=0
                for value in range (0,len(intersect_points)):
                    if abs(db_list[i].edges[j].src.x-intersect_points[value].x)<=0.01 and abs(db_list[i].edges[j].src.y-intersect_points[value].y)<=0.01:
                        src_exist_flag=1

                    if abs(db_list[i].edges[j].dst.x-intersect_points[value].x)<=0.01 and abs(db_list[i].edges[j].dst.y-intersect_points[value].y)<=0.01:
                        dst_exist_flag=1

                if src_exist_flag==0:
                    intersect_points.append(db_list[i].edges[j].src)
                if dst_exist_flag==0:
                    intersect_points.append(db_list[i].edges[j].dst)

                intersect_points = sort_vertices(intersect_points,db_list[i].edges[j].src)
                #all the points in intersect_points should be unique
                pres_v_dic,pres_e_dic,global_v_dic=save_intersect(intersect_points,pres_v_dic,pres_e_dic,global_v_dic)


    sys.stdout.write("V %d\n" % len(pres_v_dic))
    sys.stdout.write("E {")
    for value in pres_e_dic:
        if value == pres_e_dic[-1]:
            sys.stdout.write(value)
        else:
            sys.stdout.write(value+',')
    sys.stdout.write("}\n")
    sys.stdout.flush()
 
    return pres_v_dic,pres_e_dic,global_v_dic

if __name__ == '__main__':
    p1=[]
    p2=[]
    p3=[]
