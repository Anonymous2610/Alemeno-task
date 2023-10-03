from django.shortcuts import render
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from django.http import HttpResponse 

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


#Extracts Color. Copied from internet
def extract_colors(file_path: str):
    image = Image.open(file_path)
    image_array = np.array(image)
    num_pixels = image_array.shape[0] * image_array.shape[1]
    image_array_reshaped = image_array.reshape(num_pixels, -1)
    num_colors = 10
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(image_array_reshaped)
    colors = kmeans.cluster_centers_
    colors = colors.astype(int)
    result = []
    for color in colors:
        result.append(color.tolist())
    return result

#API for ananlyzing urine_stripes
class Result(APIView):
    def post(self,request):
        uploaded_file = request.FILES.get('file')
        if(uploaded_file is None):
            return Response({'Please upload a image'},status.HTTP_204_NO_CONTENT)
        try:
            color = extract_colors(uploaded_file)
            context ={
                'URO': color[0],
                'BIL': color[1],
                'KET': color[2],
                'BLD': color[3],
                'PRO': color[4],
                'NIT': color[5],
                'LEU': color[6],
                'GLU': color[7],
                'SG': color[8],
                'PH': color[9]
            }
            return Response(context,status.HTTP_200_OK)
        except:
            return Response({"Something went wrong"})

