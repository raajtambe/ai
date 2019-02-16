import sys

class vert:
    def __init__(self, name):
        self.name = name
        self.adj=[]
        self.color=-1 #-1 is white , 0 is grey , 1 is black
        self.dist=-1 #-1 to represent infinity
        self.parent=-1 #no parent ie will how index of parent

class graph:

    def __init__(self, name):
        self.name = name
        self.inci_matrix=[]
        self.vertices=[]

    def load(self,filename):
        ifile=open(filename)
        temp = []
        for l in ifile:
            temp.append(l.split())
        for r in temp:
            row=[]
            for dat in r:
                row.append(int(dat))
            self.inci_matrix.append(row)
        self.convert_inci_adj()

    def convert_inci_adj(self):
        #this is to convert the loaded incident matrix to adjcent list
        num_vetrices=len(self.inci_matrix)
        num_edges=len(self.inci_matrix[0])
        for i in range(0,num_vetrices):
            vertname='v';
            vertname=vertname+str(i)
            self.vertices.append(vert(vertname))
        for i in range(0,num_edges):
            connect=[]
            for j in range(0,num_vetrices):
                if(self.inci_matrix[j][i]==1):
                    connect.append(j);
            self.vertices[connect[0]].adj.append(connect[1])
            self.vertices[connect[1]].adj.append(connect[0])

    def bfs(self,vname):
        vert=-1

        for i in range(0,len(self.vertices)):
            if(self.vertices[i].name==vname):
                vert=i
                break
        if(vert!=-1):
            for u in self.vertices:
                u.dist=-1
                u.color=-1
                u.parent=-1
            self.vertices[vert].color=0
            self.vertices[vert].dist=0
            self.vertices[vert].parent=-1
            q=[]
            q.append(vert)
            while(len(q)!=0):
                u=q.pop(0)
                for i in self.vertices[u].adj:
                    if(self.vertices[i].color==-1):
                        self.vertices[i].color=0
                        self.vertices[i].dist=self.vertices[u].dist+1
                        self.vertices[i].parent=u
                        q.append(i)
                self.vertices[u].color=1

    def dumpbfstree(self,filename):
        dot=open(filename,'w')
        dot.write("digraph{\n")
        for i in self.vertices:
            if(i.parent!=-1):
                dot.write("\""+self.vertices[i.parent].name+"\" -> \""+i.name+"\"\n")
            if(len(i.adj)==0):
                dot.write("\""+i.name+"\"")
        dot.write("}")

    def dumpverticesnames(self):
        for i in self.vertices:
            print (i.name)

    def dumpgraph(self,filename):
        dot=open(filename,'w')
        dot.write("graph{\n")
        num_vetrices=len(self.inci_matrix)
        num_edges=len(self.inci_matrix[0])
        for i in range(0,num_edges):
            connect=[]
            for j in range(0,num_vetrices):
                if(self.inci_matrix[j][i]==1):
                    connect.append(j);
            dot.write("\""+self.vertices[connect[0]].name+"\" -- \""+self.vertices[connect[1]].name+"\"\n")
        for i in self.vertices:
            if(len(i.adj)==0):
                dot.write("\""+i.name+"\"")
        dot.write("}")

    def minpath(self,v1,v2):
        found=-1;
        for i in self.vertices:
            if(i.name==v1):
                self.bfs(v1)
                found=1
                break
        if(found!=-1):
            path=[]
            found2=-1
            for i in self.vertices:
                if(i.name==v2):
                    found=1
                    temp=i;
                    if(i.dist==-1):
                        path.append("not connect");
                    else:
                        while(temp.parent!=-1):
                            path.insert(0,temp.name)
                            temp=self.vertices[temp.parent]
                        path.insert(0,temp.name)
                    break
            return path
        else:
            return "vertex not found"
    def is_connected(self):
        self.bfs(self.vertices[0].name)
        for i in self.vertices:
            if(i.dist==-1):
                return 0
        return 1

temp=graph('test')
temp.load(sys.argv[1])
print (temp.inci_matrix)
temp.dumpgraph('graph')
temp.dumpverticesnames()
c=input("enter the vertex name--> ")
temp.bfs(c)
temp.dumpbfstree('tree')
c=input("enter the vertex1 name for shortest path--> ")
d=input("enter the vertex2 name for shortest path--> ")
print (temp.minpath(c,d))
print (temp.is_connected())
