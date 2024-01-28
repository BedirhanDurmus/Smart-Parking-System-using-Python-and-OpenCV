import cv2 # OpenCV kütüphanesini içe aktarır, görüntü işleme için kullanılır
import pickle 
# pickle modülünü içe aktarır, Python nesnelerini dosyalara kaydetmek ve yüklemek için kullanılır
import numpy as np


# kırpılacak görüntü için dikdörtgenin boyut bilgileri
width = 27
height = 15

try: # Aşağıdaki kod bloğunu dener
    with open("CarParkPos", "rb") as f: # "CarParkPos" adlı dosyayı okuma modunda açar
        posList = pickle.load(f) # Dosyadan Python nesnesini yükler
except: # Yukarıdaki kod bloğunda hata oluşursa
    posList = [] # posList'i boş bir liste olarak başlatır


def mouseClick(events, x, y, flags, params):
    # Fare tıklama olaylarını işleyen bir fonksiyon tanımlar clickle seçicez bölgeyi.
    
    if events == cv2.EVENT_LBUTTONDOWN: # Eğer sol fare tuşuna basılırsa
        posList.append((x, y)) # Tıklanan konumu listeye ekler
    
    
    if events == cv2.EVENT_RBUTTONDOWN: # Eğer sağ fare tuşuna basılırsa
        for i, pos in enumerate(posList): # Listede her pozisyon için
            x1, y1 = pos # Pozisyon koordinatlarını alır
           
            if x1 < x < x1 + width and y1 < y < y1 + height: 
                posList.pop(i) 
   # Eğer tıklanan konum belirli bir alanın içindeyse Bu pozisyonu listeden çıkarır
    with open("CarParkPos","wb") as f: # "CarParkPos" adlı dosyayı yazma modunda açar
        pickle.dump(posList, f) # Python nesnesini dosyaya yazar

while True: # sonsuz döngü başlatır.
    img = cv2.imread("first_frame.png") # first frame dosyasını okur .
    
    # Listede her pozisyon için görüntü üzerine bir dikdörtgen çizer mavi ve 2 kalınlığında.
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255,0,0),2)
    # print("poslist: ",posList)
    
    cv2.imshow("img", img)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("img_gray", imgGray)

    # Prewitt operatörünü tanımla
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    
    # Prewitt operatörünü görüntüye uygula
    img_prewittx = cv2.filter2D(img, -1, kernelx)
    img_prewitty = cv2.filter2D(img, -1, kernely)

    # Sonuçları göster
    cv2.imshow("Prewitt X", img_prewittx)
    cv2.imshow("Prewitt Y", img_prewitty)
    cv2.imshow("Prewitt", img_prewittx + img_prewitty)
    
     
    # Fare olaylarını işlemek için bir geri çağırma fonksiyonu belirler
    cv2.setMouseCallback("img", mouseClick) 
    cv2.waitKey(1) # Belirli bir süre boyunca bir tuşa basılmasını bekler
    
    
    
    
    
    
    
    
    
    