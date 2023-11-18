# -*- coding: utf-8 -*-
import math
import npy as np 
 
# MAG = WMM(latitude=MUNICH_LATITUDE, longitude=MUNICH_LONGITUDE, height=MUNICH_HEIGHT).magnetic_elements
class TRIAD:
    def __init__(self, w1:list=[0.0,0,0,0], w2:list=[0.0,0,0,0], v1:list=[0,0,1], v2:list=[0.5,0,0.5], representation='rotmat', frame='NED'):
        self.w1 = np.copy(w1) 
        self.w2 = np.copy(w2) 
        self.representation = representation
        if representation.lower() not in ['rotmat', 'quaternion']:
            raise ValueError("Wrong representation type. Try 'rotmat' or 'quaternion'")
        if frame.upper() not in ['NED', 'ENU']:
            raise ValueError(f"Given frame {frame} is NOT valid. Try 'NED' or 'ENU'")
        # Reference frames
        #TODO Set the refernce frames as a custom.
        self.v1 = self._set_first_triad_reference(v1, frame)
        self.v2 = self._set_second_triad_reference(v2, frame)
        # # Compute values if samples given
        # if all([self.w1, self.w2]):
        #     self.A = self._compute_all(self.representation)

    def _set_first_triad_reference(self, value, frame:str):
        if value is None:
            ref = np.array([0.0, 0.0, 1.0]) if frame.upper() == 'NED' else np.array([0.0, 0.0, -1.0])
        else:
            ref = np.copy(value)
            ref_norm = math.sqrt(sum(x ** 2 for x in ref))
            ref = [x / ref_norm for x in ref]
        return ref

    def _set_second_triad_reference(self, value, frame:str):
        ref=[0,0,0]
        if isinstance(value, float):
            if abs(value) > 90:
                raise ValueError("Dip Angle must be within range [-90, 90]. Got {}".format(value))
            
            if frame.upper() == 'NED':
                ref = [math.cos(math.radians(value)), 0.0, math.sin(math.radians(value))]
            else:
                ref = [0.0, math.cos(math.radians(value)), -math.sin(math.radians(value))]

        if isinstance(value, (list, tuple)):
            ref = value[:]
            ref_norm = np.norm(ref)
            ref = [x / ref_norm for x in ref]
            print("Normalised Mag As v2 : "+str(ref))
        return ref 

    def _compute_all(self, representation:str):
        if len(self.w1) != len(self.w2):
            raise ValueError("w1 and w2 are not the same size")
        
        if isinstance(self.w1[0], (int, float)):
            return self.estimate(self.w1, self.w2, representation)
        
        num_samples = len(self.w1)
        if representation.lower() == 'quaternion':
            A = [[0.0, 0.0, 0.0, 0.0] for _ in range(num_samples)]
        else:
            A = [[[0.0, 0.0, 0.0] for _ in range(3)] for _ in range(num_samples)]
        
        for t in range(num_samples):
            A[t] = self.estimate(self.w1[t], self.w2[t], representation)
        
        return A



    def estimate(self, w1:list, w2:list, representation: str = 'rotmat') -> list:
        '''
        Returns a direction cosine matrix by taking the mag field (v2) and gravity (v1) as reference.
        '''
        if representation.lower() not in ['rotmat', 'quaternion']:
            raise ValueError("Wrong representation type. Try 'rotmat', or 'quaternion'")
        w1, w2 = np.copy(w1), np.copy(w2) 
 
        w1 = np.normalise(w1)
        w2 = np.normalise(w2)
        print(str(w2))
        w1xw2 = np.cross(w1, w2)
        s2 = np.normalise(w1xw2)                     
        s3 = np.normaliseAVectorWithAnotherNorm(np.cross(w1, w1xw2),np.norm(w1xw2))

        v1xv2 = np.cross(self.v1, self.v2)
        r2 = np.normalise(v1xv2)
        r3 = np.normaliseAVectorWithAnotherNorm(np.cross(self.v1, v1xv2), np.norm(v1xv2) )

        Mb = np.c_(w1, s2, s3)                             
        Mr = np.c_(self.v1, r2, r3)                          
        #A = Mb@Mr.T                 
        A=np.matmul(Mb,np.transpose(Mr))                      
        if representation.lower() == 'quaternion':
            return np.chiaverini(A)
        print(A)
        return A
        
    
    def orientTo(self, euler:tuple|list):
        #send in the order roll pitch yaw
        # roll,pitch,yaw = euler
        # momentx = math.cos(math.radians(yaw))
        # momenty = math.sin(math.radians(yaw))
        #moments = np.matmul(dcm,[[1],[1],[1]]) 
        return np.matmul(np.euler_to_dcm(euler),[1,1,1])
