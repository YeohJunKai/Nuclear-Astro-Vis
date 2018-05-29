# Setting up from the output file
f=open("fullOutput","r")
file=f.read()
f.close()


# Processing the data from the output file into a list
# Defining the function needed for processing the data
def countindex(text,word,count):
    if count==1:
        return text.find(word)
    elif count>1:
        return text.find(word,countindex(text,word,count-1)+1)
steps=file.count("ISOTOPIC ABUNDANCES")

# Replacing the special isotope Aluminium name for ease of processing
file=file.replace("NE  1", "NU  1")
file=file.replace("AL *6","AL 26")

# Setting up the empty list which will be populated with the isotopes and abundance ratios
isotopes=[]

# Periodic List of elements and their proton numbers for reference
periodic=[['H', 1],['NU', 0], ['HE', 2], ['LI', 3], ['BE', 4], ['B', 5], ['C', 6], ['N', 7], ['O', 8], ['F', 9], ['NE', 10], ['NA', 11], ['MG', 12], ['AL', 13], ['SI', 14], ['P', 15], ['S', 16], ['CL', 17], ['AR', 18], ['K', 19], ['CA', 20], ['SC', 21], ['TI', 22], ['V', 23], ['CR', 24], ['MN', 25], ['FE', 26], ['CO', 27], ['NI', 28], ['CU', 29], ['ZN', 30], ['GA', 31], ['GE', 32], ['AS', 33], ['SE', 34], ['BR', 35], ['KR', 36], ['RB', 37], ['SR', 38], ['Y', 39], ['ZR', 40], ['NB', 41], ['MO', 42], ['TC', 43], ['RU', 44], ['RH', 45], ['PD', 46], ['AG', 47], ['CD', 48], ['IN', 49], ['SN', 50], ['SB', 51], ['TE', 52], ['I', 53], ['XE', 54], ['CS', 55], ['BA', 56], ['LA', 57], ['CE', 58], ['PR', 59], ['ND', 60], ['PM', 61], ['SM', 62], ['EU', 63], ['GD', 64], ['TB', 65], ['DY', 66], ['HO', 67], ['ER', 68], ['TM', 69], ['YB', 70], ['LU', 71], ['HF', 72], ['TA', 73], ['W', 74], ['RE', 75], ['OS', 76], ['IR', 77], ['PT', 78], ['AU', 79], ['HG', 80], ['TL', 81], ['PB', 82], ['BI', 83], ['PO', 84], ['AT', 85], ['RN', 86], ['FR', 87], ['RA', 88], ['AC', 89], ['TH', 90], ['PA', 91], ['U', 92], ['NP', 93], ['PU', 94], ['AM', 95], ['CM', 96], ['BK', 97], ['CF', 98], ['ES', 99], ['FM', 100], ['MD', 101], ['NO', 102], ['LR', 103], ['RF', 104], ['DB', 105], ['SG', 106], ['BH', 107], ['HS', 108], ['MT', 109]]

# Data Processing Step which translates data from string in the file into a matrix consisting of integers 
for i1 in range(1,steps+1):
    start=countindex(file,"ISOTOPIC ABUNDANCES",i1)
    data=file[start:3664+start]
    eleno=data.count("=")
    elestart=data.find("H")
    index=elestart
    time=float(file[start-254:start-242])*(10**int(file[start-241:start-238]))
    for i in range(eleno):
        if i==0:
            if data[index+1]==" ":
                isotopes.append([data[index],int(data[index+3:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
            else:
                isotopes.append([data[index:index+2],int(data[index+3:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
            index+=17
        elif (i+1)%9==0:
            if data[index+1]==" ":
                isotopes.append([data[index],int(data[index+3:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
            else:
                isotopes.append([data[index:index+2],int(data[index+3:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
            index+=18
        else:
            if data[index+1]==" ":
                isotopes.append([data[index],int(data[index+3:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
            else:
                isotopes.append([data[index:index+2],int(data[index+3:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
            index+=17
times=[isotopes[0][3],]
for isotope in isotopes:
    for timestp in times:
        if timestp==isotope[3]:
            break
        elif (len(times)-1)==times.index(timestp):
            times.append(isotope[3])
        else:
            continue
        

# Additional Conversion Step for Aluminum 26 isotopes
# Combining abundance ratios for AL 26 isotopes
aliso26=[["AL",26],["AL",1],["AL",2],["AL",3],["AL",-6]]


for timestp in times:
    sumAL=0
    for isotope in isotopes:
        if timestp==isotope[3]:
            if isotope[0]=="AL" and isotope[1] in [26,1,2,3,-6]:
                sumAL+=isotope[2]
            else:
                continue
        else:
            continue
    for isotope in isotopes:
        if timestp==isotope[3]:
            if isotope[0]=="AL" and isotope[1]==26:
                isotope[2]=sumAL
            else:
                continue
        else:
            continue

# Removing AL 26 excited states
isotopes=[isotope for isotope in isotopes if not (isotope[0]=="AL" and isotope[1] in [1,2,3,-6])]

# Additional conversion step to obtain final matrix with 5 different components. [Name, Proton Number, Neutron Number, Abundance Ratio, Time]
for isotope in isotopes:
    for element in periodic:
        if element[0]==isotope[0]:
            isotope.insert(1,element[1])
            isotope[2]=isotope[2]-element[1]
        else:
            continue

# Frame 1
frame1=[]
for isotope in isotopes:
    if isotope[4]==times[0]:
        frame1.append(isotope)
for isotope in frame1:
    if isotope[2]<0:
        print([isotope[0],isotope[1]])
print(frame1)
pronum=[]
neunum=[]
abunnum=[]
for isotope1 in frame1:
    pronum.append(isotope1[1])
    neunum.append(isotope1[2])
    abunnum.append(isotope1[3])
data1=[pronum,neunum,abunnum]


