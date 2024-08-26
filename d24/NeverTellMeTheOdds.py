import numpy as np

class Hailstone():
    # def __init__(self, input_str):
    #     if len(input_str) < 3:
    #         return
    #     pos_str, acc_str = input_str.strip().split("@")
    #     self.X = int(pos_str.split(", ")[0])
    #     self.Y = int(pos_str.split(", ")[1])
    #     self.Z = int(pos_str.split(", ")[2])

    #     self.vX = int(acc_str.split(", ")[0])
    #     self.vY = int(acc_str.split(", ")[1])
    #     self.vZ = int(acc_str.split(", ")[2])

    def __init__(self, x, y, z, vx, vy, vz):
        self.X = x
        self.Y = y
        self.Z = z

        self.vX = vx
        self.vY = vy
        self.vZ = vz

    @classmethod
    def fromString(cls, input_str):
        pos_str, acc_str = input_str.strip().split("@")
        return cls(int(pos_str.split(", ")[0]), int(pos_str.split(", ")[1]),int(pos_str.split(", ")[2]), int(acc_str.split(", ")[0]), int(acc_str.split(", ")[1]), int(acc_str.split(", ")[2]))

    def __repr__(self):
        return f"({self.X}, {self.Y}, {self.Z}) @ ({self.vX}, {self.vY}, {self.vZ})"
    
    def posAndVelVecs(self):
        return self.positionVec(), self.velocityVec()

    def positionVec(self):
        return [self.X, self.Y, self.Z]

    def velocityVec(self):
        return [self.vX, self.vY, self.vZ]

    def PathConverge2DXY(self, B, min=200000000000000, max=400000000000000):
        # calculate slopes of paths
        m_self = self.vY / self.vX
        m_B = B.vY / B.vX

        # calculate x intersection
        x_num = m_self*self.X - m_B*B.X + B.Y - self.Y
        x_den = m_self - m_B

        if x_den == 0: # lines have the same slope
            if x_num != 0: #parallel
                return False
            return True # same path
        
        x_conv = x_num / x_den
        if x_conv < min or x_conv > max: # fail if not in limits
            return False
        
        # calculate y intersection
        y_conv = m_self*(x_conv - self.X) + self.Y
        if y_conv < min or y_conv > max: # fail if not in limits
            return False
        
        # check if forward in time
        t_self = (1 / self.vY) * (y_conv - self.Y)
        t_B = (1 / B.vY) * (y_conv - B.Y)
        if t_self < 0 or t_B < 0:
            return False

        return True
    
    def findConvergePoint3D(self, B, min=200000000000000, max=400000000000000):
        x, y = self.findConvergePoint2DXY(B, min, max)
        x, z = self.findConvergePoint2DXZ(B, min, max)
        return (round(x), round(y), round(z))

    def findConvergePoint2DXY(self, B, min, max):
        # calculate slopes of paths
        m_self = self.vY / self.vX
        m_B = B.vY / B.vX

        # calculate x intersection
        x_num = m_self*self.X - m_B*B.X + B.Y - self.Y
        x_den = m_self - m_B

        if x_den == 0: # lines have the same slope
            if x_num != 0: #parallel
                return (-1, -1)
            return (self.X, self.Y) # same path
        
        x_conv = x_num / x_den
        # if x_conv < min or x_conv > max: # fail if not in limits
        #     return (-1, -1)
        
        # calculate y intersection
        y_conv = m_self*(x_conv - self.X) + self.Y
        # if y_conv < min or y_conv > max: # fail if not in limits
        #     return (-1, -1)

        return (x_conv, y_conv)
    
    def findConvergePoint2DXZ(self, B, min, max):
        # calculate slopes of paths
        m_self = self.vZ / self.vX
        m_B = B.vZ / B.vX

        # calculate x intersection
        x_num = m_self*self.X - m_B*B.X + B.Z - self.Z
        x_den = m_self - m_B

        if x_den == 0: # lines have the same slope
            if x_num != 0: #parallel
                return (-1, -1)
            return (self.X, self.Z) # same path
        
        x_conv = x_num / x_den
        # if x_conv < min or x_conv > max: # fail if not in limits
        #     return (-1, -1)
        
        # calculate z intersection
        z_conv = m_self*(x_conv - self.X) + self.Z
        # if z_conv < min or z_conv > max: # fail if not in limits
        #     return (-1, -1)

        return (x_conv, z_conv)
    

def findRockVelocity(h1, h2, h3):
    #source: https://www.reddit.com/r/adventofcode/comments/1994lfw/comment/kjlm9br/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    s1, v1 = h1.posAndVelVecs()
    s2, v2 = h2.posAndVelVecs()
    s3, v3 = h3.posAndVelVecs()

    g1 = np.cross(np.subtract(s1, s2), np.subtract(v1, v2))
    g2 = np.cross(np.subtract(s2, s3), np.subtract(v2, v3))
    g3 = np.cross(np.subtract(s3, s1), np.subtract(v3, v1))
    f1 = np.dot(g1, v1)
    f2 = np.dot(g2, v2)
    f3 = np.dot(g3, v3)
    
    G = np.array([g1, g2, g3])
    w = np.matmul(np.linalg.inv(G), [[f1], [f2], [f3]])
    return w
    

hailstones_str = open("input.txt").read().strip().split("\n")
hail = []
for line in hailstones_str:
    hail.append(Hailstone.fromString(line))

count = 0
crossed = []
for i in range(len(hail)):
    h= hail[i]
    for stone in hail[i+1:]:
        if h.PathConverge2DXY(stone):
            count += 1
            crossed.append((h, stone))

print("Part 1:", count)

w = findRockVelocity(hail[0], hail[1], hail[2])
print(w)

H0 = hail[0]
H1 = hail[1]
A = Hailstone(H0.X, H0.Y, H0.Z, round(H0.vX - w.item(0)), round(H0.vY - w.item(1)), round(H0.vZ - w.item(2)))
B = Hailstone(H1.X, H1.Y, H1.Z, round(H1.vX - w.item(0)), round(H1.vY - w.item(1)), round(H1.vZ - w.item(2)))

# 757031940316990 = too low
r = A.findConvergePoint3D(B)
print(r, A, B)
print(r[0] + r[1] + r[2])