import csv

def formatfile(filelocation):

    # Setting up from the output file

    f=open(str(filelocation),"r")
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
    periodic=[['NU', 0],['H', 1], ['HE', 2], ['LI', 3], ['BE', 4], ['B', 5], ['C', 6], ['N', 7], ['O', 8], ['F', 9], ['NE', 10], ['NA', 11], ['MG', 12], ['AL', 13], ['SI', 14], ['P', 15], ['S', 16], ['CL', 17], ['AR', 18], ['K', 19], ['CA', 20], ['SC', 21], ['TI', 22], ['V', 23], ['CR', 24], ['MN', 25], ['FE', 26], ['CO', 27], ['NI', 28], ['CU', 29], ['ZN', 30], ['GA', 31], ['GE', 32], ['AS', 33], ['SE', 34], ['BR', 35], ['KR', 36], ['RB', 37], ['SR', 38], ['Y', 39], ['ZR', 40], ['NB', 41], ['MO', 42], ['TC', 43], ['RU', 44], ['RH', 45], ['PD', 46], ['AG', 47], ['CD', 48], ['IN', 49], ['SN', 50], ['SB', 51], ['TE', 52], ['I', 53], ['XE', 54], ['CS', 55], ['BA', 56], ['LA', 57], ['CE', 58], ['PR', 59], ['ND', 60], ['PM', 61], ['SM', 62], ['EU', 63], ['GD', 64], ['TB', 65], ['DY', 66], ['HO', 67], ['ER', 68], ['TM', 69], ['YB', 70], ['LU', 71], ['HF', 72], ['TA', 73], ['W', 74], ['RE', 75], ['OS', 76], ['IR', 77], ['PT', 78], ['AU', 79], ['HG', 80], ['TL', 81], ['PB', 82], ['BI', 83], ['PO', 84], ['AT', 85], ['RN', 86], ['FR', 87], ['RA', 88], ['AC', 89], ['TH', 90], ['PA', 91], ['U', 92], ['NP', 93], ['PU', 94], ['AM', 95], ['CM', 96], ['BK', 97], ['CF', 98], ['ES', 99], ['FM', 100], ['MD', 101], ['NO', 102], ['LR', 103], ['RF', 104], ['DB', 105], ['SG', 106], ['BH', 107], ['HS', 108], ['MT', 109]]

    # Data Processing Step which translates data from string in the file into a matrix consisting of integers 
    for i1 in range(1,steps+1):
        start=countindex(file,"ISOTOPIC ABUNDANCES",i1)
        end=countindex(file[start:],'***************',1)
        data=file[start:end+start+1]
        eleno=data.count("=")
        elestart=data.find("H")
        index=elestart
        time=float(file[start-254:start-242])*(10**int(file[start-241:start-238]))
        for i in range(eleno):
            if i==0:
                if data[index+1]==" ":
                    isotopes.append([data[index],int(data[index+2:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
                else:
                    isotopes.append([data[index:index+2],int(data[index+2:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
                index+=17
            elif (i+1)%9==0:
                if data[index+1]==" ":
                    isotopes.append([data[index],int(data[index+2:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
                else:
                    isotopes.append([data[index:index+2],int(data[index+2:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
                index+=18
            else:
                if data[index+1]==" ":
                    isotopes.append([data[index],int(data[index+2:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
                else:
                    isotopes.append([data[index:index+2],int(data[index+2:index+5]),float(data[index+7:index+11])*float(10**int(data[index+12:index+16])),time])
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
            
    # Setting up frame for heat map
    neumax=0
    for isotope in isotopes:
        if isotope[4]==times[0]:
            if neumax<isotope[2]:
                neumax=isotope[2]
            else:
                continue
        else:
            continue
    promax=0
    for isotope in isotopes:
        if isotope[4]==times[0]:
            if promax<isotope[1]:
                promax=isotope[1]
            else:
                continue
        else:
            continue

    totalextra=[]
    for element in periodic:
        if element[1]>promax:
            continue
        extra=[]
        exineu=[]
        for isotope in isotopes:
            if isotope[0]==element[0] and isotope[4]==times[0]:
                exineu.append(isotope[2])
            else:
                continue
        extra=[value for value in range(0,neumax+1) if value not in exineu]
        for value in extra:
            for time in times:
                totalextra.append([element[0],element[1],value,0,time])
    isotopes+=totalextra

    def timetaken(list1):
        return list1[4]
    def pronumber(list1):
        return list1[1]
    def neunumber(list1):
        return list1[2]

    isotopes.sort(key=timetaken)

    # Changing abundance ratio to e-99

    for isotope in isotopes:
        if isotope[3]==0:
            isotope[3]=(10**(-99))
        else:
            continue

    # Creating Frames

    frameno=0
    for timestp in times:
        frameno+=1
        frame=[]

        for isotope in isotopes:
            if isotope[4]==timestp:
                frame.append(isotope)

        for isotopeframe in frame:
            if isotope[2]<0:
                print([isotopeframe[0],isotopeframe[1]])
        frame.sort(key=pronumber)
        newframe=[]
        for neuno in reversed(range(0,neumax+1)):
            subframe=[]
            for isotopeframe in frame:
                if neuno==isotopeframe[2]:
                    subframe.append(isotopeframe)
                else:
                    continue
            subframe.sort(key=pronumber)
            newframe+=subframe
        pronum=[]
        neunum=[]
        abunnum=[]
        timeint=[]
        names=[]
        totalframes=[frameno,len(times)]
        for isotopeframe in newframe:
            pronum.append(isotopeframe[1])
            neunum.append(isotopeframe[2])
            abunnum.append(isotopeframe[3])
            timeint.append(isotopeframe[4])
            names.append(isotopeframe[0])
        data=[list(range(0,promax+1)),]
        #Neutron number as row number and proton number as column number for matrix
        for neuno in range(0,neumax+1):
            nrow=[]
            for isotope in newframe:
                if isotope[2]==neuno:
                    nrow.append(isotope[3])
                else:
                    continue
            data.append(nrow)
        newfile=open('Frame %d.csv' %frameno,'w+',newline="")
        d=csv.writer(newfile)
        d.writerows(data)
        newfile.close()

    newfile1=open('Times.csv','w+',newline="")
    d=csv.writer(newfile1)
    d.writerow(["Time"],)
    for timestp in times:
        d.writerow([timestp,])
    newfile1.close()

    newfile2=open('Specs.csv','w+',newline="")
    e=csv.writer(newfile2)
    e.writerow(["Row/Neutron Max Value","Column/Proton Number"])
    e.writerow([neumax,promax])
    newfile2.close()
    return

formatfile("nucleo.txt")

