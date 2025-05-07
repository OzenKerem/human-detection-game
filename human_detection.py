import cv2
import torch
import numpy as np
import os
import random
import pygame
from datetime import datetime

# Pygame ses modülünü başlat
pygame.mixer.init()

# Çıktı klasörünü oluştur
output_dir = "output_frames"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# YOLOv5 modelini yükle
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Webcam'i başlat
cap = cv2.VideoCapture(0)

# Ekran penceresini oluştur
cv2.namedWindow("Insan Tespit Oyunu", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Insan Tespit Oyunu", 1280, 720)

# Ses dosyasını yükle
ses_dosyasi = 'ses.mp3'
pygame.mixer.music.load(ses_dosyasi)

# Oyun değişkenleri
frame_count = 0
oyun_modu = "tarama"  # "tarama" veya "secim"
secilen_kisi = None
secilen_kisi_bbox = None
secim_beklemesi = 0
kisi_listesi = []
secilen_kisi_goruntu = None
animasyon_adimi = 0
tam_frame = None
ses_calindi = False

while True:
    # Frame'i oku
    ret, frame = cap.read()
    if not ret:
        break
    
    # Görüntünün kopyasını al
    display_frame = frame.copy() 
    
    # YOLOv5 ile tespit yap
    results = model(frame)
    
    # İnsan detaylarını al
    detections = results.pandas().xyxy[0]
    persons = detections[detections['name'] == 'person']
    person_count = len(persons)
    
    # Tarama modunda, tespit edilen kişileri listele ve göster
    if oyun_modu == "tarama":
        # Müzik çalıyorsa durdur ve ses_calindi bayrağını sıfırla
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        ses_calindi = False
            
        # Tespit sonuçlarını çiz
        annotated_frame = np.array(results.render()[0])
        
        # Kamera sabit kalma uyarısı
        cv2.putText(annotated_frame, "Lutfen kamerayi sabit tutun!", 
                    (int(annotated_frame.shape[1]/2) - 250, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # İnsan sayısını ekranın sağ üstüne yaz
        cv2.putText(annotated_frame, f'Insan Sayisi: {person_count}', 
                    (annotated_frame.shape[1] - 250, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Bulunan kişilerin listesini sol tarafa yaz
        cv2.putText(annotated_frame, "Tespit Edilen Kisiler:", 
                    (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        for i, (index, person) in enumerate(persons.iterrows()):
            kisi_adi = f"Kisi {i+1}"
            cv2.putText(annotated_frame, kisi_adi, 
                        (10, 90 + i*30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Kişi listesini güncelle
        kisi_listesi = []
        for index, person in persons.iterrows():
            x1, y1, x2, y2 = int(person['xmin']), int(person['ymin']), int(person['xmax']), int(person['ymax'])
            # Ayrıca görüntüyü de sakla
            face_img = frame[y1:y2, x1:x2].copy() if y2 > y1 and x2 > x1 else None
            kisi_listesi.append((x1, y1, x2, y2, face_img))
        
        # En az 1 kişi tespit edildiğinde ve belirli bir süre tarama yaptıktan sonra seçim moduna geç
        if person_count > 0 and frame_count > 90:  # 3 saniye sonra (30fps varsayımıyla)
            oyun_modu = "secim"
            # Rastgele bir kişi seç
            secilen_kisi_indeks = random.randint(0, person_count - 1)
            secilen_kisi_bbox = kisi_listesi[secilen_kisi_indeks][:4]  # (x1, y1, x2, y2)
            secilen_kisi_goruntu = kisi_listesi[secilen_kisi_indeks][4]  # Kişinin görüntüsü
            tam_frame = frame.copy()  # Tam kareyi sakla
            secim_beklemesi = 0
            animasyon_adimi = 0
            
            # Ses dosyasını çal
            pygame.mixer.music.play()
            ses_calindi = True
            print("Ses çalınıyor: ses.mp3")
        
        display_frame = annotated_frame
    
    # Seçim modunda, SADECE seçilen kişiyi göster
    elif oyun_modu == "secim":
        secim_beklemesi += 1
        animasyon_adimi = (animasyon_adimi + 1) % 20  # 0-19 arası değişen animasyon adımı
        
        # Yeni bir siyah arka plan oluştur
        h, w = frame.shape[:2]
        black_bg = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Animasyon için renk değişimi (kırmızı tonları)
        blue = 0
        green = 0
        red = 155 + abs(animasyon_adimi - 10) * 10  # 155-255 arası kırmızı tonları
        
        # Seçilen kişiyi göster
        if secilen_kisi_bbox and secilen_kisi_goruntu is not None:
            x1, y1, x2, y2 = secilen_kisi_bbox
            
            try:
                # Görüntünün boyutlarını al
                person_h, person_w = secilen_kisi_goruntu.shape[:2]
                
                # Büyütme faktörü (ekranın yüksekliğinin %70'i kadar)
                scale_factor = (h * 0.7) / person_h
                new_height = int(person_h * scale_factor)
                new_width = int(person_w * scale_factor)
                
                # Görüntüyü yeniden boyutlandır
                enlarged_person = cv2.resize(secilen_kisi_goruntu, (new_width, new_height))
                
                # Ekranın ortasında konumlandır
                center_x = w // 2
                center_y = h // 2
                
                # Yerleştirme için koordinatları hesapla
                x_offset = center_x - new_width // 2
                y_offset = center_y - new_height // 2
                
                # Animasyonlu çerçeve kalınlığı
                frame_thickness = 8 + abs(animasyon_adimi - 10)
                
                # Çerçeve çiz (siyah arka plana)
                cv2.rectangle(
                    black_bg, 
                    (x_offset - frame_thickness, y_offset - frame_thickness), 
                    (x_offset + new_width + frame_thickness, y_offset + new_height + frame_thickness), 
                    (blue, green, red), 
                    frame_thickness
                )
                
                # Kişinin görüntüsünü yerleştir
                black_bg[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = enlarged_person
                
                # "SEÇİLEN!" yazısını ekranın alt kısmına ekle
                kazanan_text = "SEÇİLEN!"
                text_size = cv2.getTextSize(kazanan_text, cv2.FONT_HERSHEY_TRIPLEX, 2.5, 3)[0]
                text_x = center_x - text_size[0] // 2
                text_y = y_offset + new_height + 70
                
                cv2.putText(
                    black_bg, 
                    kazanan_text, 
                    (text_x, text_y), 
                    cv2.FONT_HERSHEY_TRIPLEX, 
                    2.5, 
                    (blue, green, red), 
                    3
                )
                
                # Ekran üst kısmına "SEÇİLEN KİŞİ!" yazısı ekle
                title_text = "SECILEN KISI!"
                title_size = cv2.getTextSize(title_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
                title_x = center_x - title_size[0] // 2
                title_y = y_offset - 20
                
                cv2.putText(
                    black_bg, 
                    title_text, 
                    (title_x, title_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1.5, 
                    (blue, green, red), 
                    3
                )
                
            except Exception as e:
                print(f"Hata: {e}")
                oyun_modu = "tarama"
                frame_count = 0
        
        display_frame = black_bg
        
        # 5 saniye sonra tarama moduna geri dön
        if secim_beklemesi > 150:  # 5 saniye (30fps varsayımıyla)
            oyun_modu = "tarama"
            frame_count = 0
    
    # Frame sayacını artır
    frame_count += 1
    
    # Görüntüyü göster
    cv2.imshow("Insan Tespit Oyunu", display_frame)
    
    # Çıkış için 'q' tuşuna basılmasını bekle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizlik
cap.release()
cv2.destroyAllWindows()
