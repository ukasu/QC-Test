import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import math 
import scipy.ndimage
from scipy.signal import convolve2d
import cv2
from convolve import convolve 
import numpy as np
from scipy.ndimage.filters import convolve

class Filter:
   def __init__(self, I,theta,sigma,resize=1):
      self.I = I
      #print(self.I.shape)
      if len(self.I.shape) == 3: 
         self.I_gray = cv2.cvtColor(self.I, cv2.COLOR_BGR2GRAY)
      else:
         self.I_gray = self.I
      self.I_w =  len(self.I[0,:])
      self.I_h = len(self.I)
      self.theta = theta
      self.sigma = sigma
      self.J = 0;
      #resim boyutu küçültülebilir
      self.img = self.I_gray
      width = int(self.img.shape[1] / resize )
      height = int(self.img.shape[0]/ resize )
      dim = (width, height)
      
      #img = Image.fromarray(img)
      #img.resize(size=dim)
      self.img_resized = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
      
      #img = img.reshape(dim) 

   def SteerableDigitalFilter(self):
      #  1. I: input image
      #  2. theta: the orientation
      #  3. sigma: standard deviation of the Gaussian template   
      #  Output:
      #  J. The response of derivative in theta direction
      #  Implemented from Jincheng Pang, Tufts University, Dec. 2013.
      
      #self.I = self.I[:,:,None]
      
      #self.I = np.mean(self.I.astype(float)); # Burada matlabda 3 parametresi var. Onu araştır.
      # for i in range(self.I_w):
      #    for j in range(self.I_h):
      #       self.I()

      self.theta = -self.theta*(math.pi/180);
      #self.sigma = 1;

      Wx = math.floor((8/2)*self.sigma); 
      if Wx < 1:
        Wx = 1
      x = np.arange(-Wx,(Wx+1));
      xx,yy = np.meshgrid(x,x)
      
      g0 = np.exp(-((pow(xx,2)+pow(yy,2))/(2*pow(self.sigma,2))))/(self.sigma*math.sqrt(2*math.pi)) # Matlab ile aynı değerler
      G2a = -g0/pow(self.sigma,2)+g0*pow(xx,2)/pow(self.sigma,4);# Matlab ile aynı değerler
      G2b =  g0*xx*yy/pow(self.sigma,4);# Matlab ile aynı değerler
      G2c = -g0/pow(self.sigma,2)+g0*pow(yy,2)/pow(self.sigma,4);# Matlab ile aynı değerler
      #I2a = imfilter(I,G2a,'same','replicate');
      # I2b = imfilter(I,G2b,'same','replicate');
      # I2c = imfilter(I,G2c,'same','replicate');
      #print(str(self.I_gray.shape))

      #I2c = scipy.ndimage.convolve(self.I_gray, G2c, mode='reflect')
      #print(np.sum(I2c))
      J = pow(math.cos(self.theta),2)*I2a+math.pow(math.sin(self.theta),2)*I2c-2*math.cos(self.theta)*math.sin(self.theta)*I2b
      self.J = J;
      return self.J
      


   def conv2(self,x,y,mode='same'):
       """
       Emulate the function conv2 from Mathworks.

       Usage:

       z = conv2(x,y,mode='same')

       TODO: 
        - Support other modes than 'same' (see conv2.m)
       """

       if not(mode == 'same'):
           raise Exception("Mode not supported")

       # Add singleton dimensions
       if (len(x.shape) < len(y.shape)):
           dim = x.shape
           for i in range(len(x.shape),len(y.shape)):
               dim = (1,) + dim
           x = x.reshape(dim)
       elif (len(y.shape) < len(x.shape)):
           dim = y.shape
           for i in range(len(y.shape),len(x.shape)):
               dim = (1,) + dim
           y = y.reshape(dim)

       origin = ()

       # Apparently, the origin must be set in a special way to reproduce
       # the results of scipy.signal.convolve and Matlab
       for i in range(len(x.shape)):
           if ( (x.shape[i] - y.shape[i]) % 2 == 0 and
                x.shape[i] > 1 and
                y.shape[i] > 1):
               origin = origin + (-1,)
           else:
               origin = origin + (0,)

       z = convolve(x,y, mode='constant', origin=origin)

       return z