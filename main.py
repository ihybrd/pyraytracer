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
        
    def point_at_parameter(self, t):
        return self.A + t*self.B

def unit_vector(v):
    length = pow(v[0]*v[0]+v[1]*v[1]+v[2]*v[2], 0.5)
    return v/length

def hit_sphere(center, radius, r):
    oc = r.origin() - center
    a = np.dot(r.direction(), r.direction())
    b = 2.0 * np.dot(oc, r.direction())
    c = np.dot(oc, oc) - radius*radius
    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return -1.0
    else:
        return (-b- pow(discriminant, 0.5))/(2.0*a)
            
def color(r):
    t = hit_sphere(np.array([0,0,-1]), .5, r)
    if t > 0.:
        N = unit_vector(r.point_at_parameter(t)- np.array([0,0,-1]))
        return 0.5*np.array([N[0]+1, N[1]+1, N[2]+1])
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
