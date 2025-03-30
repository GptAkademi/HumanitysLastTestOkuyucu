# Soru-Cevap Gösterici

Bu program, parquet dosyasındaki soru ve cevapları görüntülemek için tasarlanmıştır. Base64 formatında kodlanmış resimleri de gösterebilir.

## Gereksinimler

### Veri Dosyası

Programın çalışması için gerekli olan parquet dosyasını aşağıdaki adresten indirebilirsiniz:
[https://huggingface.co/datasets/cais/hle/tree/main/data](https://huggingface.co/datasets/cais/hle/tree/main/data)

İndirdiğiniz `test-00000-of-00001.parquet` dosyasını programın çalıştığı dizine koymanız gerekmektedir.

Şimdilik program "test-00000-of-00001.parquet" dosyasını arıyor, bu yüzden eğer yeni bir versiyon varsa ve dosya adı farklıysa, dosya adını test-00000-of-00001.parquet olarak değiştirmeniz gerekiyor.

### Kütüphaneler

Aşağıdaki kütüphanelerin yüklü olması gerekir:

```
pip install -r requirements.txt
```

## Çalıştırma

### GUI Versiyonu

GUI versiyonunu aşağıdaki komutla çalıştırabilirsiniz:

```
python display_qa.py
```

### Konsol Versiyonu

Eğer GUI versiyonunda sorun yaşarsanız, konsol versiyonunu kullanabilirsiniz:

```
python display_qa_console.py
```

Konsol versiyonu, base64 formatındaki resimleri geçici dosyalara kaydedip varsayılan görüntüleyici ile açacaktır.

## Kullanım

### GUI Versiyonu
- "Sonraki" ve "Önceki" butonlarını kullanarak sorular arasında gezinebilirsiniz.
- Metin ve resim olarak kodlanmış içerikler otomatik olarak görüntülenir.
- İki sekme bulunmaktadır: "Soru-Cevap" ve "Açıklama (Rationale)".
- Soru-Cevap sekmesinde soru, ilave görsel ve cevap görüntülenir.
- Açıklama sekmesinde rationale metni ve varsa rationale görseli görüntülenir.

### Konsol Versiyonu
- 'n' tuşuyla sonraki soruya, 'p' tuşuyla önceki soruya geçebilir, 'q' tuşuyla programdan çıkabilirsiniz.
- Resimler otomatik olarak tarayıcıda açılacaktır.
- Program şu alanları görüntüler: Soru, İlave Görsel (varsa), Cevap, Açıklama (varsa) ve Açıklama Görseli (varsa).

## Görüntülenen Alanlar

Program aşağıdaki alanları görüntüler:
- `question`: Soru metni veya görseli
- `image`: İlave soru görseli (varsa)
- `answer`: Cevap metni veya görseli
- `rationale`: Açıklama/gerekçe metni (varsa)
- `rationale_image`: Açıklama/gerekçe görseli (varsa)

## Not

Program, `test-00000-of-00001.parquet` dosyasını çalıştığı dizinde aramaktadır. 