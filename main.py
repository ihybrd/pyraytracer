from PIL import Image
import numpy as np

    
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


class HitRecord(object):
    def __init__(self):
        self.t = 0 # float
        self.p = np.array([0,0,0]) # vec3
        self.normal = np.array([0,0,0]) # vec3
        

class Hitable(object):
    def hit(self, r, t_min, t_max, rec):
        pass

                
class Sphere(Hitable):
    def __init__(self, center, r):
        self.center = center
        self.radius = r
        
    def hit(self, r, t_min, t_max, rec):
        oc = r.origin() - self.center
        a = np.dot(r.direction(), r.direction())
        b = np.dot(oc, r.direction())
        c = np.dot(oc, oc) - self.radius*self.radius
        discriminant = b*b - a*c
        if discriminant > 0:
            temp = (-b- pow(b*b-a*c, 0.5))/a
            if (temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center)/self.radius
                return True
            temp = (-b + pow(b*b-a*c, 0.5))/a
            if (temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center)/self.radius
                return True
        return False

       
class HitableList(Hitable):
    def __init__(self, hitablelist, n):
        self.list_size = n
        self.list = hitablelist
        
    def hit(self, r, t_min, t_max, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max
        for i in xrange(self.list_size):
            if self.list[i].hit(r, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything, rec
    

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

MAXFLOAT = 100.0        
def color(r, world):
    rec = HitRecord()
    is_hit, rec = world.hit(r, 0.0, MAXFLOAT, rec)  # the rec would make sense only if the is_hit is True.
    if is_hit:
        return 0.5*np.array([rec.normal[0]+1, rec.normal[1]+1, rec.normal[2]+1])
    else:
        unit_direction = unit_vector(r.direction())
        t = 0.5*(unit_direction[1]+1.0)
        return (1.0-t)*np.array([1.0,1.0,1.0])+t*np.array([0.5,0.7,1.0])

def main():
    # the size of the canvas 
    nx = 200
    ny = 100
    
    lower_left_corner = np.array([-2.0, -1.0, -1.0])
    horizontal = np.array([4.0, 0.0, 0.0])
    vertical = np.array([0.0, 2.0, 0.0])
    origin = np.array([0.0, 0.0, 0.0])
    
    hitablelist = [
        Sphere(np.array([0,0,-1]), 0.5),
        Sphere(np.array([0,-100.5,-1]), 100)
        ]
    
    world = HitableList(hitablelist, len(hitablelist))
    
    # create image
    img = Image.new('RGB', (nx, ny), (0,0,0))
     
    # draw pixels
    for w in xrange(img.width):
        for h in xrange(img.height):
            
            u = float(w)/float(nx)
            v = float(img.height - h)/float(ny)
            
            r = Ray(origin, lower_left_corner+u*horizontal+v*vertical)
            
            p = r.point_at_parameter(2.0)
            col = color(r, world)
                
            r = int(255.99*col[0])
            g = int(255.99*col[1])
            b = int(255.99*col[2])
            
            img.putpixel((w,h), (r,g,b))
    
    # show image
    img.show()
    
main()
