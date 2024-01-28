import cv2 # OpenCV kütüphanesini içe aktarır
import pickle # pickle kütüphanesini içe aktarır
import numpy as np # numpy kütüphanesini içe aktarır

def checkParkSpace(imgg): # Park alanını kontrol etmek için bir fonksiyon tanımlar
    boslukSayaci = 0 # Boş park alanlarını saymak için bir sayaç başlatır
    
    for pos in posList: # Pozisyon listesindeki her pozisyon için döngü başlatır
        x, y = pos # Pozisyondaki x ve y koordinatlarını alır
        
        img_kırp = imgg[y: y + height, x:x + width]  # Görüntüyü belirli bir pozisyonda kırpma
        sayac = cv2.countNonZero(img_kırp) # Kırpılmış görüntüdeki sıfır olmayan piksel sayısını hesaplama
        
        # print("count: ", count)
        
        if sayac < 150: # Eğer sıfır olmayan piksel sayısı 150'den az ise
            renk = (0, 255, 0) # Rengi yeşil yap python opencv BGR blue green default ayar.
            boslukSayaci += 1 # Boş park alanı sayısını artır
        else: # Eğer sıfır olmayan piksel sayısı 150'den fazla ise
            renk = (0, 0, 255) # Rengi kırmızı yap
     # Görüntü üzerine bir dikdörtgen çizme ve piksel sayısını üzerine yazma 
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), renk, 2) 
        cv2.putText(img, str(sayac), (x, y + height - 2), cv2.FONT_HERSHEY_PLAIN, 1,renk,1)
    # Görüntü üzerine boş park alanı sayısını yaz sayfanın en yukarısında olacak.renk kodu araştırdım koyu mavi yaptım.
    cv2.putText(img, f"FREE: {boslukSayaci}/{len(posList)}", (15,24), cv2.FONT_HERSHEY_PLAIN, 2,(191,0,25),4)
    cv2.putText(img, f"bedirhan durmus", (7,330), cv2.FONT_HERSHEY_PLAIN, 1,(191,0,25),1)
    cv2.putText(img, f" 210208049", (7,340), cv2.FONT_HERSHEY_PLAIN, 1,(191,0,25),1)
# kırpılacak görüntü için dikdörtgenin boyut bilgileri
width = 27
height = 15

cap = cv2.VideoCapture("video.mp4") # Videoyu okumak için bir VideoCapture nesnesi oluşturur

with open("CarParkPos", "rb") as f: # Dosyayı okuma modunda açar
    posList = pickle.load(f) # Dosyadan pozisyon listesini yükler

while True: # Sonsuz bir döngü başlatır
    success, img = cap.read() # Videodan bir kare okur.
    
    # Görüntüyü sırasıyla griye dönüştürür , gaussian blur ile bulanıklaştırır
    # adaptivethreshhold ile mantıklı bir şekilde görüntüyü ikili (binary) hale getirir
    # median blur filtresiyle görüntüyü düzeltir gürültülerden arındırır
    # dilate ile genişletir.
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3)), iterations = 1)
    
    checkParkSpace(imgDilate) # Park alanını kontrol eder
    
    cv2.imshow("img", img) # Görüntüyü gösterir
    cv2.imshow("img_gray", imgGray)
    cv2.imshow("imgBlur", imgBlur)
    cv2.imshow("imgThreshold", imgThreshold)
    cv2.imshow("imgMedian", imgMedian)
    cv2.imshow("imgDilate", imgDilate)
    cv2.waitKey(200) 
    if cv2.waitKey(200)& 0xFF ==ord("q"):
        cap.release()
        cv2.destroyAllWindows()
    # Belirli bir süre bekler 1 yazarsak yavaş 200 yazarsak hızlı değer bize bağlı.
    # Oluşturduğum koşul kısmında da video açıldığında q ya bastığım zaman direk videoyu kapatacak.
    
    
    
    
    
    
    