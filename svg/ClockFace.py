from xml.etree.ElementTree import QName, ElementTree, Element, SubElement, register_namespace                          

class SVG(object):                                                         
    def __getattr__(self, name):
        def f(*children, **kwargs):
            qname = QName("http://www.w3.org/2000/svg", name)
            e = Element(qname, **kwargs)
            e.extend(children)
            return e
        return f

svg = SVG()



class ClockFace:
    letters =""
    def __init__(self):
        self.data = []
        svg = SVG()

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

