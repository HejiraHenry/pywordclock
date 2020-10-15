from xml.etree.ElementTree import QName, ElementTree, Element, SubElement, register_namespace
from sys import stdout, stderr, argv
from ClockFace import ClockFace


letters = "ITSZATHALFBNTENQUARTERTWENTYPFIVEWAYTILPASTZOSEVENYNOONKBIRTHWDAYTMIDNIGHTTENFIVENINETWOELEVENEIGHTONESIXTHREEFOURZOCLOCK";



def drawclock(x_edge, y_edge, x_delta, y_delta, file_name):
    register_namespace('svg', "http://www.w3.org/2000/svg")
    root = svg.svg(
        # fill
        svg.rect(x="0", y="0", width="100", height="100", fill="#FFFFFF"),
        width="18in",
        height="18in",
        viewBox="0 0 100 100",
        version="1.1",
        );
    letters_elem = svg.g()

    x = 0
    y = 0


    for letter in letters:
        px = (x * x_delta) + x_edge
        py = (y * y_delta) + y_edge
        center_of_letter = ( px, py)
        label = svg.text(
            x=str(px),
            y=str(py),
            fill="#ffffff",
            attrib={
                "font-family": "Transport",
                "font-size": "8",
                "text-anchor": "middle",
                "stroke": "black",
                "stroke-width": "0.1"
                }
            )
        label.text = letter

        letters_elem.append( label)

        x += 1
        if x > 10:
            x = 0
            y += 1

    root.append(letters_elem)

    tree = ElementTree(root)
    #tree.write(stdout)
    tree.write(file_name)




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
    
    file_name = file_name + "-" + myargs['-x'] + "x" +  myargs['-y']  + ".svg"
    print ("File Name:  " + file_name)
    cf = ClockFace()

    #drawclock(x_edge, y_edge, x_delta, y_delta, file_name)
