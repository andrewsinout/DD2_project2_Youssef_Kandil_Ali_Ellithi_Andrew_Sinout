from lef_parser import *
import hdlparse.verilog_parser as vlog
import sys, getopt
import os 
import argparse
from math import comb
import copy
import math


path = "./merged_unpadded.lef"
#lef_parser = LefParser(path)
#var = lef_parser.parse()

vlog_ex = vlog.VerilogExtractor()
vlog_mods = vlog_ex.extract_objects("spm.synthesis.v")

temp = []
ports = []

scale_unit = 1000.0
site_height     = 0.0 
site_width      = 0.0
no_of_sites     = 200
power_padding_x =1000.0
power_padding_y =2000.0
no_of_rows      = 20
no_of_cols      = 20
core_width = 0.0
core_hight = 0.0
area= 1.0
Core_area = 1.0
utalization = 0.5
aspect_l_w = 1.5
north           = "N"
flipped_south   ="FS"
site_name       ="site_name"


#printing the rows

c= sys.argv[0] .split(".")
c = c[0] + '_tb.def'
cc= sys.argv[0] .split(".")
file1 = open(c, "w")  # write mode





pins = []

def get_nets():
    wire_list=[[["","",""],"print string"]]

    f = open('./spm.synthesis.v')
    line = f.readline()
    for pin in pins:
        temp=[copy.deepcopy(pin.name)]
        string_temp="\t- "+temp[0]+" ( PIN "+temp[0]+" ) "
        push_temp=[temp,string_temp]
        wire_list.append(push_temp)
    #print(wire_list)
    while line:
        if ('wire' in line):
            x=line.split("wire")
            net= x[1]
            net=net[:-1]
            net=net[:-1]
            net=net[1:]
            temp=[net]
            string_temp="\t- "+temp[0]+" "
            push_temp=[temp,string_temp]
            wire_list.append(push_temp)
        line = f.readline()

    f.close()  
    wire_list.pop(0)
    #for wire in wire_list:
    #    print(wire)

#################################################################################

    f = open('./spm.synthesis.v')
    line = f.readline() 
    while line:
        component_name=""
        if ("sky130" in line):
            x=line.split(" ") 
            component_name=x[-2]
            tab_line = f.readline()
            while tab_line:
                if (");" in tab_line):
                    break
                for wire in wire_list:
                    if (wire[0][0] in tab_line):
                        t= tab_line.split(".")
                        #print(wire[0],t)
                        u=t[1]
                        ps=u.split("(")
                        fin=ps[0]
                        fin= component_name+" "+fin
                        wire[0].append(fin)
                        
                tab_line = f.readline()


        line= f.readline()
    wire_list_size=str(len(wire_list))
    print("NETS "+wire_list_size+" ;")
    file1.write("NETS "+wire_list_size+" ;" + "\n")
    for wire in wire_list:
        printing_string= wire[1]
        for i in range (1,len(wire[0])):
            printing_string+="( "+wire[0][i]+" ) "
        printing_string+="+ USE SIGNAL ;"
        print(printing_string)
        file1.write(printing_string+"\n")
    print("END NETS\nEND DESIGN")
    file1.write("END NETS\nEND DESIGN")
    









def calculate_params(area,utalization,site_height,site_width): # Aspect ratio * Core_area
    Core_area = float(area / utalization)
    core_width= float(math.sqrt(Core_area *(1.0/aspect_l_w)))
    core_hight= float(aspect_l_w* core_width)
    print ("Core height " , core_hight)
    print ("Core width " , core_width)
    no_of_sites =int(core_width/site_width)
    no_of_rows =int(core_hight/site_height)

    return Core_area,core_width,core_hight,no_of_sites,no_of_rows
    



# def get_pins():
#     # sys.argv[1]
#     vlog_ex = vlog.VerilogExtractor()
#     vlog_mods = vlog_ex.extract_objects("spm.synthesis.v")

#     temp = []
#     #pins = []

#     for m in vlog_mods:
#         for p in m.ports:
#             temp = p.data_type.split(":")
#             a= temp[0] 
#             a=a[2:]
#             if (a == ""):
#                 pins.append(p)     
#             else:
#                 name = p.name 
#                 for i in range (int (a)):
#                     temp = copy.deepcopy(p) 
#                     temp.name = name + "[" + str(i) + "]"   
#                     pins.append(temp)
                    
                    


#     pins_title="PINS "+str(len(pins))+" ;"
#     print(pins_title)
#     file1.write(pins_title + "\n")

#     for pin in pins:
#         pin_string= "\t- "+ pin.name+" + NET "+pin.name
#         pin_string+=" + DIRECTION "+pin.mode.upper()+" + USE SIGNAL\n\t\t+ PORT\n\t\t\t+ LAYER "
#         pin_string+="UNKNOWN"+" (0 0) (100 100) ;\n"
#         print(pin_string) 
#         file1.write(pin_string+"\n")
        
#     print("END PINS")
#     file1.write("END PINS"+"\n")







def get_pins(peremeter, die_width, die_height):
    # sys.argv[1]
    vlog_ex = vlog.VerilogExtractor()
    vlog_mods = vlog_ex.extract_objects("spm.synthesis.v")

    temp = []
    #pins = []

    for m in vlog_mods:
        for p in m.ports:
            temp = p.data_type.split(":")
            a= temp[0] 
            a=a[2:]
            if (a == ""):
                pins.append(p)     
            else:
                name = p.name 
                for i in range (int (a)):
                    temp = copy.deepcopy(p) 
                    temp.name = name + "[" + str(i) + "]"   
                    pins.append(temp)
                    
                    


    pins_title="PINS "+str(len(pins))+" ;"
    print(pins_title)

    ### getting pin locations
    seperation= int(peremeter/len(pins))
    step_x=0.0
    step_y=0.0

#+ PLACED ( 353510 2000 ) N ;
    side_one=True
    side_two=False
    side_three=False
    side_four=False

    for pin in pins:
        pin_string= "\t- "+ pin.name+" + NET "+pin.name
        pin_string+=" + DIRECTION "+pin.mode.upper()+" + USE SIGNAL\n\t\t+ PORT\n\t\t\t+ LAYER "

        if((side_one==True)):
            if((step_x <= die_width)):
                pin_string+="met2"+" ( -140 -2000 ) ( 140 2000 ) ;\n"
                pin_string+="\t\t\t+ PLACED ( "+str(int(step_x))+" "+str(int(step_y))+" ) N ;\n"
                step_x+=seperation
            else:
                step_x=0.0 
                side_one=False
                side_two=True
        elif(side_two==True):
            if((step_y <= die_height)):
                pin_string+="met3"+" ( -140 -2000 ) ( 140 2000 ) ;\n"
                pin_string+="\t\t\t+ PLACED ( "+str(int(step_x))+" "+str(int(step_y))+" ) N ;\n"
                step_y+=seperation
            else:
                side_one=False
                side_two=False
                side_three=True
        elif(side_three==True):
            if((step_x <= die_width)):
                pin_string+="met2"+" ( -140 -2000 ) ( 140 2000 ) ;\n"
                pin_string+="\t\t\t+ PLACED ( "+str(int(step_x))+" "+str(int(step_y))+" ) N ;\n"
                step_x+=seperation
            else:
                step_y=0.0 
                side_one=False
                side_two=False
                side_three=False
                side_four=True
        elif(side_four==True):
            if((step_y <= die_height)):
                pin_string+="met3"+" ( -140 -2000 ) ( 140 2000 ) ;\n"
                pin_string+="\t\t\t+ PLACED ( "+str(int(step_x))+" "+str(int(step_y))+" ) N ;\n"
                step_y+=seperation
            else:
                step_y=0.0 
                side_one=False
                side_two=False
                side_three=False
                side_four=True




        print(pin_string)
        file1.write(pin_string+"\n")
    print("END PINS")
    file1.write("END PINS")





















def get_components():

    components_list= [["",1,1.0]]
    
    f = open('./spm.synthesis.v')
    line = f.readline()
    components_printing_list=[]
    while line:
        
        if 'sky130_' in line:
            component_string="\t- "
            x=line.split(" ")
            new_component=""
           
            for i in range(len(x)):
                if('sky130_' in x[i]):
                    new_component=x[i]
                    component_string+=x[i+1]+" "+new_component+" ;"
                    components_printing_list.append(component_string)
            if (len(components_list)>0):
                flag=False
                for component in components_list:
                    if (new_component == component[0]):
                        component[1]=component[1]+ 1
                        flag=True
                if (flag==False):
                    components_list.append([new_component,1,1.0])
                    
        line = f.readline()
    f.close()
    components_list.pop(0)
  

    return components_list,components_printing_list



def get_sizes(components_list):
    f = open('./merged_unpadded.lef')
    line = f.readline()
    while line:
        for component in components_list:
            if (component[0] in line):
                area=1.0
                flagg=False
                while (flagg== False):
                    tab_line= f.readline()
                    if ("SIZE" in tab_line):
                        flagg= True   
                        x=tab_line.split(" ")
                        #print (x)       
                        for word in x:
                            if(len(word)>0):
                                if (word[0].isdigit()):
                                    area*=float(word)
                component[2]=area                   
        line = f.readline()

    f.close()
    return components_list


def calculate_cells_overall_area(components_list, area):
   
    for component in l:
        area+= float(component[1])*scale_unit * float(component[2]) * scale_unit

    return area




def calculate_total_die_peremeter():
    die_width=(power_padding_x*2)+core_width
    die_height=(power_padding_y*2)+core_hight
    peremeter= (die_width*2)+(die_height*2)
    return peremeter, die_width, die_height



def get_rows():
    for m in vlog_mods:
        for p in m.ports:
            temp = p.data_type.split(":")
            a= temp[0]
            a=a[2:]
            if (a == ""):                
                ports.append(p)                
            else:
                name = p.name 
                for i in range (int (a)):
                    p.name = name + "[" + str(i) + "]"
                    temp = p
                    ports.append(temp)

    row_y=power_padding_y

    for row in range (no_of_rows):

        row_string= "ROW ROW_"+ str(row) +" "+str(site_name)+" "+str(int(power_padding_x))+" "+str(int(row_y))
        row_y+= float(site_height)
        if ((row%2)==0):
            row_string+=" "+str(north)+" DO "+str(no_of_sites)+" BY "+ "1"+" STEP "+str(int(site_width))+" 0 ;"
        else:
            row_string+=" "+str(flipped_south)+" DO "+str(no_of_sites)+" BY "+ "1"+" STEP "+str(int(site_width))+" 0 ;"

        print(row_string)
        file1.write(row_string +"\n")



def get_site(site_width,site_height):

    f = open(path)
    line = f.readline()
    while line:
        
            if ('SITE' in line):
              
                flagg=False
                while (flagg== False):
                    tab_line= f.readline()
                    if ("SIZE" in tab_line):
                        flagg= True   
                        x=tab_line.split(" ")       
                        for word in x:
                            if(len(word)>0):
                                if (word[0].isdigit()):
                                    if(site_width == 0.0):
                                        site_width= word
                                    else:
                                        site_height=word   
                                        f.close()

                                        return site_height,site_width
            line = f.readline()

    
    f.close()




print ("VERSION 5.8 ;")
print ("DIVIDERCHAR / ;")
print ("BUSBITCHARS [] ;")
print ("DESIGN lut_s44 ;")
print ("UNITS DISTANCE MICRONS 1000 ;")
file1.write("VERSION 5.8 ;"+"\n")
file1.write("DIVIDERCHAR / ;"+"\n")
file1.write("BUSBITCHARS [] ;"+"\n")
file1.write("UNITS DISTANCE MICRONS 1000 ;"+"\n")

com_list, print_com_list=get_components()

l=get_sizes(com_list)

area =calculate_cells_overall_area(l,area)

site_height,site_width = get_site(site_width,site_height)
site_height = float(site_height) *scale_unit
site_width = float(site_width) *scale_unit
#print (str(site_height) , str(site_width))
Core_area,core_width,core_hight,no_of_sites,no_of_rows=  calculate_params(area,utalization,site_height,site_width)
peremeter, die_width, die_height = calculate_total_die_peremeter()
print ("DIEAREA (0 0) ( " + str(int(die_width)) + " " + str(int(die_height)) + " )"  )
file1.write("DIEAREA (0 0) ( " + str(int(die_width)) + " " + str(int(die_height)) + " )" +"\n" )
#print("Area= "+str(area))
#file1.write( "Area= "+str(area) + "\n")

print ( "Core_area = " , Core_area)
print ( Core_area,core_width,core_hight,no_of_sites,no_of_rows )
get_rows()


#print components
print("COMPONENTS "+str(len(print_com_list))+" ;")
file1.write("COMPONENTS "+str(len(print_com_list))+" ;" + "\n")
for comp in print_com_list:
    print(comp)
print("END COMPONENTS ")

get_pins(peremeter, die_width, die_height)
file1.write("END COMPONENTS "+"\n")
#get_pins()
get_nets()
#cc = float(site_height)*scale_unit
#print (cc)


