import sys

class vert:
    def __init__(self, name):
        self.name = name
        self.adj=[]
        self.adj_w=[]#corresponding weight list
        self.color=-1 #-1 is white , 0 is grey , 1 is black
        self.v_time=-1
        self.f_time=-1
        self.dist=-1 #-1 to represent infinity
        self.mintree=[]
        self.parent=-1 #no parent ie will how index of parent

class graph:
    t=0
    def __init__(self, name):
        self.name = name
        self.adj_matrix=[]
        self.vertices=[]
        self.mst=[]
        self.mstk=[]
        self.edges=[]
        self.verti=[]
        self.topo=[]

    def load(self,filename):
        ifile=open(filename)
        temp = []
        for l in ifile:
            temp.append(l.split())
        for r in temp:
            row=[]
            for dat in r:
                row.append(int(dat))
            self.adj_matrix.append(row)
        self.convert_adjmat_adj()

    def convert_adjmat_adj(self):
        num_vetrices=len(self.adj_matrix)
        for i in range(0,num_vetrices):
            vertname='v';
            vertname=vertname+str(i+1)
            self.vertices.append(vert(vertname))
        for i in range(0,num_vetrices):
            for j in range(0,num_vetrices):
                if(self.adj_matrix[i][j]!=0):
                    self.vertices[i].adj.append(j)
                    self.vertices[i].adj_w.append(self.adj_matrix[i][j])
                    # self.vertices[j].adj.append(i)
                    # self.vertices[j].adj_w.append(self.adj_matrix[i][j])

    def dumpbfstree(self,filename):
        dot=open(filename,'w')
        dot.write("digraph{\n")
        for i in self.verti:
            if(i.parent!=-1):
                dot.write("\""+self.verti[i.parent].name+"\" -> \""+i.name+"\"\n")
            if(len(i.adj)==0):
                dot.write("\""+i.name+"\"")
        dot.write("}")

    #returns 0 if there is no path connecting v1 and v2
    def is_connected(self,v1,v2):
        found1=-1
        found2=-1
        p=0
        for i in self.mstk:
            if(i[0]==v1 or i[1]==v1):
                found1=p
                break
            p+=1
        p=0
        for i in self.mstk:
            if(i[0]==v2 or i[1]==v2):
                found2=p
                break
            p+=1
        if(found2*found1<0 or (found1<0 and found2<0)):
            return 0
        else:
            pointer=v1
            connected=0
            traversed=[]
            for k in range(0,len(self.mstk)):
                # print (traversed)
                for i in self.mstk:
                    if(i not in traversed):
                        if(i[0]==pointer):
                            if(i[1]==v2):
                                connected=1
                                traversed.append(i)
                                break
                            pointer=i[1]
                        elif(i[1]==pointer):
                            if(i[0]==v2):
                                connected=1
                                break
                            pointer=i[0]
            return connected

    def mst_prim(self):
        num_vertices=len(self.vertices)
        v=self.vertices[0]
        connected=[v]
        mst_total_weight=0
        while(len(connected)!=num_vertices):
            minw=100000
            minvert=''
            tover=-1
            ind=-1
            for vert in connected:
                for i in range(0,len(vert.adj)):
                    if(minw>vert.adj_w[i]):
                        minw=vert.adj_w[i]
                        minvert=vert
                        tover=self.vertices[vert.adj[i]]
                        ind=i
            for i in range(0,len(tover.adj)):
                if(self.vertices[tover.adj[i]].name==minvert.name):
                    del tover.adj[i]
                    del tover.adj_w[i]
                    break
            del minvert.adj_w[ind]
            del minvert.adj[ind]
            if(tover not in connected):
                connected.append(tover)
                edge=[minvert.name,tover.name,minw]
                # print ("1   ",edge)
                self.mst.append(edge)
                mst_total_weight+=minw
        self.convert_adjmat_adj()
        return mst_total_weight
        # for i in self.mst:
        #     # print (i[0],"   ",i[1],"    ",i[2])

    def create_edges(self):
        for i in self.vertices:
            for j in range(0,len(i.adj)):
                edge=[i.name,self.vertices[i.adj[j]].name,i.adj_w[j]]
                rev_edge=[self.vertices[i.adj[j]].name,i.name,i.adj_w[j]]
                # print (edge,"  ",rev_edge)
                if((edge not in self.edges) and (rev_edge not in self.edges)):
                    self.edges.append(edge)
                    # dot.write("\""+i.name+"\" -- \""+self.vertices[i.adj[j]].name+"\""+" [label="+str(i.adj_w[j])+"]\n")


    def mst_kruskal(self):
        self.create_edges()
        num_vertices=len(self.vertices)
        # print (self.edges)
        connected=[]
        while(len(self.edges)>0):
            ind=-1
            minw=1000000
            for i in range(0,len(self.edges)):
                if(minw>self.edges[i][2]):
                    minw=self.edges[i][2]
                    ind=i
            # self.convert_adjmat_adj()
            # print (self.is_connected(self.edges[ind][0],self.edges[ind][1]))
            found1=-1
            found2=-1
            # print (self.is_connected(self.edges[ind][0],self.edges[ind][1]))
            if(self.is_connected(self.edges[ind][0],self.edges[ind][1])==0):
                self.mstk.append(self.edges[ind])
            del self.edges[ind]

    def visit(self,u):
        uind=-1
        # print (u,"----->vi11111")
        for i in range(0,len(self.vertices)):
            if(self.vertices[i].name==u):
                uind=i
                break
        if(uind!=-1):
            self.vertices[uind].color=0
            self.t+=1
            self.vertices[uind].v_time=self.t
            for v in self.vertices[uind].adj:
                if(self.vertices[v].color==-1):
                    # print(self.vertices[v].name)
                    self.vertices[v].parent=uind
                    self.visit(self.vertices[v].name)
            self.vertices[uind].color=1
            self.t=self.t+1
            self.vertices[uind].f_time=self.t+1
            self.topo.append(self.vertices[uind].name)

    def visit2(self,u):
        uind=-1
        # print (u,"----->vi11111")
        for i in range(0,len(self.vertices)):
            if(self.vertices[i].name==u):
                uind=i
                break
        if(uind!=-1):
            self.vertices[uind].color=0
            self.t+=1
            self.vertices[uind].v_time=self.t
            for v in self.vertices[uind].adj:
                if(self.vertices[v].color==-1):
                    # print(self.vertices[v].name)
                    self.vertices[v].parent=uind
                    self.visit(self.vertices[v].name)
            self.vertices[uind].color=1
            self.t=self.t+1
            self.vertices[uind].f_time=self.t+1
            self.topo.append(self.vertices[uind].name);

    def dfs(self,vname):
        ind=-1
        self.topo=[]
        for i in range(0,len(self.vertices)):
            if(self.vertices[i].name==vname):
                ind=i
                break
        if(ind>=0):
            for i in self.vertices:
                i.color=-1
                i.parent=-1
            self.t=0
            self.visit(vname)
            for i in self.vertices:
                if(i.color==-1 and i.name!=vname):
                    self.visit(i.name)
    def topological_sort(self,vname):
        ind=-1
        self.topo=[]
        for i in range(0,len(self.vertices)):
            if(self.vertices[i].name==vname):
                ind=i
                break
        if(ind>=0):
            for i in self.vertices:
                i.color=-1
                i.parent=-1
            self.t=0
            # self.visit2(vname)
            for i in self.vertices:
                if(i.color==-1):# and i.name!=vname):
                    self.visit2(i.name)
        t=[]
        while(len(self.topo)>0):
            t.append(self.topo.pop())
        self.topo=t
        return self.topo


    def dump(self,filename):
        dot=open(filename,'w')
        dot.write("graph{\n")
        num_vetrices=len(self.adj_matrix)
        connected=[]
        # print (self.mstk)
        for i in self.vertices:
            for j in range(0,len(i.adj)):
                edge=[i.name,self.vertices[i.adj[j]].name,i.adj_w[j]]
                rev_edge=[self.vertices[i.adj[j]].name,i.name,i.adj_w[j]]
                # print (edge,"  ",rev_edge)
                if((edge not in self.mst) and (rev_edge not in self.mst) and (edge not in connected) and (rev_edge not in connected)):
                    dot.write("\""+i.name+"\" -- \""+self.vertices[i.adj[j]].name+"\""+" [label="+str(i.adj_w[j])+"]\n")
                    connected.append(edge)
                    connected.append(rev_edge)
                elif((edge not in connected) and (rev_edge not in connected)):
                    dot.write("\""+i.name+"\" -- \""+self.vertices[i.adj[j]].name+"\""+" [label="+str(i.adj_w[j])+",color=\"blue\"]\n")
                    connected.append(edge)
                    connected.append(rev_edge)
        dot.write("}")


    def dumpk(self,filename):
        dot=open(filename,'w')
        dot.write("graph{\n")
        num_vetrices=len(self.adj_matrix)
        connected=[]
        # print ("20002",self.mstk)
        for i in self.vertices:
            for j in range(0,len(i.adj)):
                edge=[i.name,self.vertices[i.adj[j]].name,i.adj_w[j]]
                rev_edge=[self.vertices[i.adj[j]].name,i.name,i.adj_w[j]]
                # print (edge,"  ",rev_edge)
                if((edge not in self.mstk) and (rev_edge not in self.mstk) and (edge not in connected) and (rev_edge not in connected)):
                    dot.write("\""+i.name+"\" -- \""+self.vertices[i.adj[j]].name+"\""+" [label="+str(i.adj_w[j])+"]\n")
                    connected.append(edge)
                    connected.append(rev_edge)
                elif((edge not in connected) and (rev_edge not in connected)):
                    dot.write("\""+i.name+"\" -- \""+self.vertices[i.adj[j]].name+"\""+" [label="+str(i.adj_w[j])+",color=\"blue\"]\n")
                    connected.append(edge)
                    connected.append(rev_edge)
        dot.write("}")

    def dumpdfstree(self,filename):
        dot=open(filename,'w')
        dot.write("digraph{\n")
        for i in self.vertices:
            if(i.parent!=-1):
                dot.write("\""+self.vertices[i.parent].name+"\" -> \""+i.name+"\"\n")
            else:
                dot.write("\""+i.name+"\"")
        dot.write("}")

    def dumpgraph(self,filename):
        dot=open(filename,'w')
        dot.write("graph{\n")
        num_vetrices=len(self.adj_matrix)
        connected=[]
        for i in self.vertices:
            for j in range(0,len(i.adj)):
                edge=[i.name,self.vertices[i.adj[j]].name]
                rev_edge=[self.vertices[i.adj[j]].name,i.name]
                if((edge not in connected) and (rev_edge not in connected)):
                    dot.write("\""+i.name+"\" -- \""+self.vertices[i.adj[j]].name+"\""+" [label="+str(i.adj_w[j])+"]\n")
                    connected.append(edge)
                    connected.append(rev_edge)
        dot.write("}")

    def dumpverticesnames(self):
        for i in self.vertices:
            print (i.name)
            # print (i.adj)
            # print (i.adj_w)



temp=graph('test')
temp.load(sys.argv[1])
print (temp.adj_matrix)
temp.dumpgraph('graph')
temp.dumpverticesnames()
temp.mst_prim()
temp.dump('mst')
temp.mst_kruskal()
temp.dumpk('mst2')
print (temp.topological_sort('v1'))
temp.dumpdfstree('dfs')
