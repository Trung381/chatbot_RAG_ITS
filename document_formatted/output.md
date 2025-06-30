## **LỜI NÓI ĐẦU**

Tài liệu này được biên soạn với mục đích cung cấp một nguồn dữ liệu thô, phức tạp và đa dạng về cấu trúc để phục vụ cho việc thử nghiệm và phát triển các hệ thống xử lý ngôn ngữ tự nhiên, đặc biệt là các mô hình RAG (Retrieval-Augmented Generation). Nội dung trong tài liệu là sự kết hợp của các thông tin được tạo ra ngẫu nhiên và các kiến thức phổ thông, được trình bày theo một cấu trúc phân cấp sâu nhằm thách thức khả năng phân đoạn (chunking) và hiểu cấu trúc của các thuật toán.

## **PHẦN A: CÔNG NGHỆ VÀ KHOA HỌC MÁY TÍNH**

### **CHƯƠNG 1: TRÍ TUỆ NHÂN TẠO (AI)**

Đây là chương giới thiệu tổng quan về lĩnh vực Trítuệ nhân tạo, từ lịch sử hình thành đến các ứng dụng hiện đại.

#### **1.1 Lịch sử phát triển của AI**

Lịch sử của AI là một hành trình dài với nhiều dấu mốc quan trọng, từ những ý tưởng triết học sơ khai đến những đột phá công nghệ gần đây.

#### **1.1.1 Giai đoạn sơ khai (1940 - 1956)**

- Năm 1943: Warren McCulloch và Walter Pitts đề xuất mô hình mạng nơ-ron nhân tạo đầu tiên.
- Năm 1950: Alan Turing công bố bài báo "Computing Machinery and Intelligence", giới thiệu Phép thử Turing (Turing Test) để đánh giá tríthông minh của máy móc.
- Năm 1956: Hội thảo Dartmouth, được coi là sự kiện khai sinh ra lĩnh vực AI.John McCarthy lần đầu tiên sử dụng thuật ngữ "Artificial Intelligence".

### **1.1.2 Kỷ nguyên vàng và mùa đông AI (1956 - 1980)**

- Giai đoạn phát triển ban đầu đầy lạc quan với các chương trình như Logic Theorist và General Problem Solver.
- Sau đó là "Mùa đông AI" lần thứ nhất vào giữa những năm 1970 do sự cắt giảm tài trợ
- và những kỳ vọng không được đáp ứng.● Các hệ chuyên gia (Expert Systems) bắt đầu xuất hiện và đạt được một số thành công thương mại vào những năm 1980.

### **1.1.3 Sự trỗi dậy của Học máy (1980 - nay)**

- Mạng nơ-ron lan truyền ngược (Backpropagation) được phổ biến rộng rãi vào những năm 1980.
- Học máy (Machine Learning) trở thành phương pháp tiếp cận chủ đạo, thay thế dần các hệ chuyên gia dựa trên luật.

● Sự bùng nổ của dữ liệu lớn (Big Data) và sức mạnh tính toán (GPU) đã thúc đẩy sự phát triển của Học sâu (Deep Learning).

### **1.2 Các phân ngành chính của AI**

Trí tuệ nhân tạo là một lĩnh vực rộng lớn bao gồm nhiều phânngành khác nhau, mỗi phân ngành tập trung vào một khía cạnh cụ thể của trí thông minh.

## **1.2.1 Học máy (Machine Learning)**

Học máy là nhánh cốt lõi của AI, tập trung vào việc phát triển các thuật toán cho phép máy tính học hỏi từ dữ liệu mà không cần được lập trình tường minh.

## **1.2.1.1 Học có giám sát (Supervised Learning)**

Sử dụng dữ liệu đã được gán nhãn để huấn luyện mô hình.

Các thuật toán phổ biến: Hồi quy tuyến tính, Hồi quy logistic, Máy vector hỗ trợ (SVM), Cây quyết định.

## **1.2.1.2 Học không giám sát (Unsupervised Learning)**

Tự tìm ra các mẫuvà cấu trúc trong dữ liệu không được gán nhãn.

Các thuật toán phổ biến: Phân cụm K-means, Phân tích thành phần chính (PCA), Apriori.

## **1.2.1.3 Học tăng cường (Reinforcement Learning)**

Mô hình học bằng cách tương tác với một môi trường và nhận phần thưởng hoặc hình phạt.

Ứng dụng: Xe tự lái, robot, chơi game (AlphaGo).

## **1.2.2 Xử lý ngôn ngữ tự nhiên (Natural Language Processing - NLP)**

NLP giúp máy tính hiểu, diễn giải và tạo ra ngôn ngữ của con người.

- Các tác vụ chính:
	- a. Phân loại văn bản
	- b. Nhận dạng thực thể có tên (NER)
	- c. Dịch máy
	- d. Tóm tắt văn bản
	- e. Hỏi đáp

#### **1.2.3 Thị giác máy tính (Computer Vision)**

Lĩnh vực này cho phép máy tính "nhìn" và hiểu được nội dung của hình ảnh và video.

- Ứng dụng:
	- Nhận dạng khuôn mặt
	- Phân tích hình ảnh y tế
	- Xe tự lái
	- Giám sát an ninh

### **CHƯƠNG 2: MẠNG MÁY TÍNH VÀ AN NINH MẠNG**

#### **2.1 Mô hình OSI và TCP/IP**

### **2.1.1 Mô hình 7 lớp OSI**

Mô hình tham chiếu OSI (Open Systems Interconnection) là một mô hình khái niệm chia giao thức mạng thành bảy lớp riêng biệt.

- 1. Lớp Vật lý (Physical Layer)
- 2. Lớp Liên kết dữ liệu (Data Link Layer)
- 3. Lớp Mạng (Network Layer)
- 4. Lớp Giao vận (Transport Layer)
- 5. Lớp Phiên (Session Layer)
- 6. Lớp Trình diễn (Presentation Layer)
- 7. Lớp Ứng dụng (Application Layer)

## **2.1.2 Bảng so sánh OSI và TCP/IP (có viền)**

Dưới đây là một bảng so sánh cấu trúc các lớp giữa hai mô hình phổ biến.

| LớpOSI | TênLớpOSI | LớpTCP/IPtươngứng |
|------------|-------------------|-------------------------------|
| 7          | Application       | Application                   |
| 6          | Presentation      | Application                   |

| 5 | Session      | Application       |  |
|---|--------------|-------------------|--|
| 4 | Transport    | Transport         |  |
| 3 | Network      | Internet          |  |
| 2 | DataLink | NetworkAccess |  |
| 1 | Physical     | NetworkAccess |  |

### **2.2 Các loại tấn công mạng phổ biến**

An ninh mạng là một cuộc chiến không ngừng nghỉ giữa những người bảo vệ hệ thống và những kẻ tấn công.

## **2.2.1 Tấn công từ chốidịch vụ (DoS/DDoS)**

❖ Mục tiêu: Làm chotài nguyên máy tính hoặc mạng không khả dụng cho người dùng hợp pháp.

❖ Phương thức: Gửi một lượng lớn yêu cầu đến máy chủ mục tiêu, làm cạn kiệt tài nguyên của nó.

## **2.2.2 Phishing (Tấn công giả mạo)**

❖ Mục tiêu: Lừa người dùng tiết lộ thông tin nhạy cảm như tên đăng nhập,mật khẩu, thông tin thẻ tín dụng.

❖ Phương thức: Gửi email hoặc tin nhắn giả mạo, trông giống như từ một nguồn đáng tin cậy.

# **2.2.3 Malware**

Là một thuật ngữ chung cho các phần mềm độc hại.

-> Virus: Gắn vào các tệp tin sạch và lây lan sang các máy tính khác.

-> Worm: Tương tự virus nhưng có thể tự nhân bản và lây lan mà không cần sự can thiệp của con người.

- -> Ransomware: Mã hóa dữ liệu của nạn nhân và đòi tiền chuộc để giải mã.
- -> Spyware: Bí mật thu thập thông tin về người dùng.

### **2.3 Bảng phân loại Malware (không có viền)**

Bảng dưới đây trình bày một cách trực quan về các loại phần mềm độc hại và mục đích chính của chúng, được định dạng để kiểm thử khả năng nhận dạng bảng không có đường kẻ. lorem lorem