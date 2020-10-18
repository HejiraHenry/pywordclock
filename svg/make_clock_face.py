from xml.etree.ElementTree import QName, ElementTree, Element, SubElement, register_namespace
from sys import stdout, stderr, argv
from ClockFace import ClockFace



letters = "ITSZATHALFBNTENQUARTERTWENTYPFIVEWAYTILPASTZOSEVENYNOONKBIRTHWDAYTMIDNIGHTTENFIVENINETWOELEVENEIGHTONESIXTHREEFOURZOCLOCK";



def getopts(argv):
    opts = {} 
    while argv: 
        if argv[0][0] == '-':  
            opts[argv[0]] = argv[1]  
        argv = argv[1:]  
    return opts




if __name__ == '__main__':
    x_edge = 0
    y_edge = 0
    x_delta = 0
    y_delta = 0
    file_name = 'foo'
    num_letters_row = 11
    num_letters_col = 11
    
    myargs = getopts(argv)
    if '-f' in myargs: 
        file_name = myargs['-f']
    if '-x' in myargs: 
        x_delta = float(myargs['-x'])
    if '-y' in myargs: 
        y_delta = float(myargs['-y'])
    
    # Logic to center the placement of letters on the X & Y axis 
    # (based on % of the size of plate)
    x_edge = (100 - ((num_letters_row -1) * x_delta))/2
    y_edge = (100 - ((num_letters_row -1)* y_delta))/2

    # or you can override the computed values 
    if '-xs' in myargs: 
        x_edge= float(myargs['-xs'])
    if '-ys' in myargs: 
        y_edge= float(myargs['-ys'])
    
    print("Y Delta:  ",y_delta)
    print("X Delta:  ",x_delta)
    print("X Edge:  ", x_edge)
    print("Y Edge:  ", y_edge)
    
    file_name = file_name + "-" + str(x_delta) + "x" +  str(y_delta)  + ".svg"
    print ("File Name:  " + file_name)
    cf = ClockFace()
    cf.letters = letters

    cf.drawclock(x_edge, y_edge, x_delta, y_delta, file_name)
