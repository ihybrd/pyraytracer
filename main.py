from PIL import Image
import numpy as np

# the size of the canvas 
nx = 200
ny = 100

# create image
img = Image.new('RGB', (nx, ny), (0,0,0))
 
    
class Ray(object):
    def __init__(self, a, b):
        self.A = a
        self.B = b
        
    def origin(self):
        return self.A
        
    def direction(self):
        return self.B
        
    def point_at_parameter(t):
        return A + t*B

def unit_vector(v):
    length = pow(v[0]*v[0]+v[1]*v[1]+v[2]*v[2], 0.5)
    return v/length
    
def color(r):
    unit_direction = unit_vector(r.direction())
    t = 0.5*(unit_direction[1] + 1.0) # dir.y --> dir[1]
    return (1.0-t)*np.array([1.0,1.0,1.0])+t*np.array([0.5,0.7,1.0])


lower_left_corner = np.array([-2.0, -1.0, -1.0])
horizontal = np.array([4.0, 0.0, 0.0])
vertical = np.array([0.0, 2.0, 0.0])
origin = np.array([0.0, 0.0, 0.0])

# draw pixels
for w in xrange(img.width):
    for h in xrange(img.height):
        
        u = float(w)/float(nx)
        v = float(img.height - h)/float(ny)
        
        r = Ray(origin, lower_left_corner+u*horizontal+v*vertical)
        col = color(r)
            
        r = int(255.99*col[0])
        g = int(255.99*col[1])
        b = int(255.99*col[2])
        
        img.putpixel((w,h), (r,g,b))

# show image
img.show()
