from PIL import Image
import numpy as np
import random

    
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


class Material(object):
    def scatter(self, r_in, rec, attenuation):
        pass

class HitRecord(object):
    def __init__(self):
        self.t = 0 # float
        self.p = np.array([0,0,0]) # vec3
        self.normal = np.array([0,0,0]) # vec3
        self.mat_ptr = None
        

class Hitable(object):
    def hit(self, r, t_min, t_max, rec):
        pass

def reflect(v, n):
    return v - 2*np.dot(v, n)*n

class Lambertian(Material):
    def __init__(self, a):
        self.albedo = a
        
    def scatter(self, r_in, rec):
        target = rec.p + rec.normal + random_in_unit_sphere()
        scattered = Ray(rec.p, target - rec.p)
        attenuation = self.albedo
        return True, scattered, attenuation
        
                        
class Metal(Material):
    def __init__(self, a):
        self.albedo = a
        
    def scatter(self, r_in, rec):
        reflected = reflect(unit_vector(r_in.direction()), rec.normal)
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return np.dot(scattered.direction(), rec.normal)>0, scattered, attenuation
    
                
class Sphere(Hitable):
    def __init__(self, center, r, m):
        self.center = center
        self.radius = r
        self.mat_ptr = m
        
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
                rec.mat_ptr = self.mat_ptr
                return True, rec
            temp = (-b + pow(b*b-a*c, 0.5))/a
            if (temp < t_max and temp > t_min):
                rec.t = temp
                rec.p = r.point_at_parameter(rec.t)
                rec.normal = (rec.p - self.center)/self.radius
                rec.mat_ptr = self.mat_ptr
                return True, rec
        return False, rec

       
class HitableList(Hitable):
    def __init__(self, hitablelist, n):
        self.list_size = n
        self.list = hitablelist
        
    def hit(self, r, t_min, t_max, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max
        for i in xrange(self.list_size):
            is_hit, temp_rec = self.list[i].hit(r, t_min, closest_so_far, temp_rec)
            if is_hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                rec = temp_rec
        return hit_anything, rec
    

class Camera (object):
    def __init__(self):
        self.lower_left_corner = np.array([-2.0, -1.0, -1.0])
        self.horizontal = np.array([4.0, 0.0, 0.0])
        self.vertical = np.array([0.0, 2.0, 0.0])
        self.origin = np.array([0.0, 0.0, 0.0])
        
    def get_ray(self, u, v):
        return Ray(self.origin, self.lower_left_corner+u*self.horizontal+v*self.vertical)
    
  
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


def random_in_unit_sphere():
    while 1:
        p = np.array(
            [
                random.randint(-100,100)/100.0,
                random.randint(-100, 100)/100.0,
                random.randint(-100, 100)/100.0
            ]
        )
        length_squre = p[0]*p[0]+p[1]*p[1]+p[2]*p[2]
        if length_squre >= 1:
            continue
        else:
            return p


MAXFLOAT = 100.0
def color(r, world, depth):
    rec = HitRecord()
    is_hit, rec = world.hit(r, 0.001, MAXFLOAT, rec)  # the rec would make sense only if the is_hit is True.
    if is_hit: 
        attenuation = np.array([1,1,1])
        is_scattered, scattered, attenuation = rec.mat_ptr.scatter(r, rec)
        if is_scattered and depth < 50:
            return attenuation*color(scattered, world, depth+1)
        else:
            return np.array([0,0,0])
    else:
        unit_direction = unit_vector(r.direction())
        t = 0.5*(unit_direction[1]+1.0)
        return (1.0-t)*np.array([1.0,1.0,1.0])+t*np.array([0.5,0.7,1.0])

def white_color(pixel_color, samples_per_pixel):
    r = pixel_color[0]
    g = pixel_color[1]
    b = pixel_color[2]

    scale = 1.0/samples_per_pixel

    r = pow(scale*r, 0.5)
    g = pow(scale*g, 0.5)
    b = pow(scale*b, 0.5)

    return r, g, b

def main():
    # the size of the canvas 
    nx = 200
    ny = 100
    samples_per_pixel = 2  # higher and1lower the performance, 1 for preview
    max_depth = 50
    
    hitablelist = [
        Sphere(np.array([0,0,-1]), 0.5, Lambertian(np.array([0.8,0.3,0.3]))),
        Sphere(np.array([0,-100.5,-1]), 100, Lambertian(np.array([0.8,0.8,0.0]))),
        Sphere(np.array([1,0,-1]), 0.5, Metal(np.array([0.8,0.6,0.2]))),
        Sphere(np.array([-1,0,-1]), 0.5, Metal(np.array([0.8,0.8,0.8])))
        ]
    
    world = HitableList(hitablelist, len(hitablelist))
    cam = Camera()
    # create image
    img = Image.new('RGB', (nx, ny), (0,0,0))
     
    # draw pixels
    for w in xrange(img.width):
        for h in xrange(img.height):
            pixel_color = np.array([0,0,0])
            for s in xrange(samples_per_pixel):
                u = float(w+random.randint(0,100)/100.0)/(float(nx)-1)
                v = float(img.height - h+random.randint(0,100)/100.0)/(float(ny)-1)
                r = cam.get_ray(u, v)
                p = r.point_at_parameter(2.0)
                pixel_color = pixel_color + color(r, world, 0)
            r, g, b = white_color(pixel_color, samples_per_pixel)
            img.putpixel((w,h), (int(r*256),int(g*256),int(b*256)))
    
    # show image
    img.show()
    
main()
