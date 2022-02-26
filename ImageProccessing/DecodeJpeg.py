#!/usr/bin/env python
# coding: utf-8

# In[35]:


import simplejpeg as jpeg
import serial as s
#ser = s.Serial()
#ser = s.Serial('COM3', 9600)
#data = s.read(1024)
data = open('pythonOutEdit.dat', 'rb').read()
data


# In[36]:


print("Is JPEG: "+ str(jpeg.is_jpeg(data)))
print("Header info: "+ str(jpeg.decode_jpeg_header(data)))
jpeg.decode_jpeg(data)


# In[ ]:




