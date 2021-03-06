import numpy as np
import pickle
import csv
import random
from numpy.random import choice
##Define IP address for node number
##Compute node address except switch
IP_add = ['10.10.20.52','10.10.20.139','10.10.20.254','10.10.20.77','10.10.20.32','None','10.10.20.54','10.10.20.148','10.10.20.7']
SFC = ['nat1,firewall1,ids1','nat2,ids2','nat3,firewall3']
SFC_2 = ['nat,firewall,ids,NA','nat,ids,NA,NA','nat,firewall,NA,NA']
penalty_fix = '0.00000010'
Node_list = [0,1,2,3,4,6,7,8]
SFC_type_list=[0,1,2]

traf_ILP = ['a','b','c']
traf_SFCR = ['a','b','c']


random.shuffle(SFC_type_list)
random.shuffle(Node_list)

num_SFC = choice([1,2,3],p=[(30825/37110),(4023/37110),(2262/37110)])
#num_SFC = choice([1,2,3],p=[0,0,1])

print("Generator working now")

dummy_src_dst = []
for j in range(0,num_SFC):
        Num_add = Node_list[j] #src setting
        bw = random.randint(20,100)
        delay = random.randint(700,750)
        SFC_type = SFC_type_list[j]
        #SFC_type = random.randint(0,2)
        src_dst_list = []
        for i in range(2):
                while Num_add in src_dst_list:
                        Num_add = random.choice(Node_list)    
                src_dst_list.append(Num_add)

        #ILP
        traf_ILP[j] = '0,'+str(src_dst_list[0])+','+str(src_dst_list[1])+','+str(bw)+','+str(delay)+','+str(penalty_fix)+','+str(SFC[SFC_type])
        #SFCR
        traf_SFCR[j] = '1,0,'+str(IP_add[src_dst_list[0]])+','+str(IP_add[src_dst_list[1]])+','+str(bw)+','+str(delay)+','+str(penalty_fix)+','+str(SFC_2[SFC_type])


#ILP_Save
with open('solver_src/logs/traf-testbed-8-00001', 'w') as f_traf_ILP:
        for j in range(0,num_SFC):
                if j >0:
                        f_traf_ILP.write('\n')
                f_traf_ILP.write(traf_ILP[j]) 
f_traf_ILP.close()
with open('solver_src/logs/traf-testbed-8-00002', 'w') as f_traf_ILP:
        for j in range(0,num_SFC):
                if j >0:
                        f_traf_ILP.write('\n')
                f_traf_ILP.write(traf_ILP[j]) 
f_traf_ILP.close()


#SFCR_Save
with open('traf.txt', 'w') as f_traf_SFCR:
        for j in range(0,num_SFC):
                if j >0:
                        f_traf_SFCR.write('\n')
                f_traf_SFCR.write(traf_SFCR[j])  
f_traf_SFCR.close()

#one for ML


Type1_name = ['nat1','firewall1','ids1']
Type2_name = ['nat2','ids2']
Type3_name = ['nat3','firewall3']

Type1 = [1,0,0]
Type2 = [0,1,0]
Type3 = [0,0,1]

Server0 = [1,0,0,0,0,0,0,0,0,0,0,0,0]
Server1 = [0,1,0,0,0,0,0,0,0,0,0,0,0]
Server2 = [0,0,1,0,0,0,0,0,0,0,0,0,0]
Server3 = [0,0,0,1,0,0,0,0,0,0,0,0,0]
Server4 = [0,0,0,0,1,0,0,0,0,0,0,0,0]
Server5 = [0,0,0,0,0,1,0,0,0,0,0,0,0]
Server6 = [0,0,0,0,0,0,1,0,0,0,0,0,0]
Server7 = [0,0,0,0,0,0,0,1,0,0,0,0,0]
Server8 = [0,0,0,0,0,0,0,0,1,0,0,0,0]
Server9 = [0,0,0,0,0,0,0,0,0,1,0,0,0]
Server10 =[0,0,0,0,0,0,0,0,0,0,1,0,0]
Server11 =[0,0,0,0,0,0,0,0,0,0,0,1,0]
Server12 =[0,0,0,0,0,0,0,0,0,0,0,0,1]

Base = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def check_type(t):
    if np.array_equal(Type1_name,t):
        return Type1
    elif np.array_equal(Type2_name,t):
        return Type2
    elif np.array_equal(Type3_name,t):
        return Type3

def check_server(s):
    if s=='0':
        return Server0
    elif s=='1':
        return Server1
    elif s=='2':
        return Server2
    elif s=='3':
        return Server3
    elif s=='4':
        return Server4
    elif s=='5':
        return Server5
    elif s=='6':
        return Server6
    elif s=='7':
        return Server7
    elif s=='8':
        return Server8
    elif s=='9':
        return Server9
    elif s=='10':
        return Server10
    elif s=='11':
        return Server11
    elif s=='12':
        return Server12

temp = []
pickle_request = []

for i in range (0, 1):##Scenario number

    for j in range(0, num_SFC):##max_SFC_number
        one_request = traf_ILP[j].split(',')
        one_length = len(one_request)
        sfc_type = one_request[6:one_length]
        bandwidth = [int(one_request[3])]
        _delay = [int(one_request[4])]
        src = one_request[1]
        dst = one_request[2]

        pickle_src = check_server(src)
        pickle_dst = check_server(dst)
        pickle_type = check_type(sfc_type)


        t1 = np.asarray(pickle_src)
        t2 = np.asarray(pickle_dst)
        test = np.sum([t1,t2],axis=0)
        test = test.tolist()

        finished_one_hot = pickle_type + pickle_src + pickle_dst + bandwidth + _delay
        temp.append(finished_one_hot)

    for jj in range(num_SFC, 3):
        temp.append(Base)
    
    print("print pickle")
    print(temp)
    pickle_request.append(temp)

with open('X1_sfc1_ni.pickle', 'wb') as f:   
    pickle.dump(pickle_request, f, pickle.HIGHEST_PROTOCOL)

#one for SFCR




