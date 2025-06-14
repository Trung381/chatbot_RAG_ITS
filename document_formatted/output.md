# **Working Directory → Staging → Commit**

Để sử dụng Git hiệu quả, điều quan trọng đầu tiên là phải hiểu rõ quy trình làm việc cơ bản của nó. Git quản lý các thay đổi trong dự án của bạn thông qua ba khu vực chính, tạo thành một quy trình 3 bước:

- 1. **Working Directory (Thư mục làm việc)**
- 2. **Staging Area (Khu vực chuẩn bị hay Index)**
- 3. **Git Repository (Kho chứa Git thường là thư mục .git )**

![](_page_0_Figure_5.jpeg)

## **Working Directory (Thư mục làm việc)**

Đây chính là thư mục chứa toàn bộ các tệp tin và thư mục con của dự án mà bạn đang làm việc trực tiếp trên máy tính của mình.

- Bạn có thể tự do tạo, sửa đổi, xóa các tệp tin trong thư mục này bằng trình soạn thảo code hoặc các công cụ khác.
- Các tệp tin ở đây có thể ở trạng thái "untracked" (Git chưa theo dõi) hoặc "modified" (đã được Git theo dõi nhưng có sự thay đổi so với lần commit

cuối cùng).

**Ví dụ:** Khi bạn mở dự án bằng VSCode và sửa một file index.html hay tạo một file style.css mới, bạn đang thao tác trực tiếp trên Working Directory.

## **Staging Area (Khu vực chuẩn bị / Index)**

Đây là một khu vực trung gian, hoạt động như một "bản nháp" cho lần commit tiếp theo của bạn. Nó chứa thông tin về những thay đổi cụ thể mà bạn *muốn* đưa vào commit kế tiếp.

Nó cho phép bạn chọn lọc chính xác những thay đổi nào từ Working Directory sẽ được ghi nhận vào lịch sử dự án. Bạn có thể sửa nhiều file nhưng chỉ chọn một vài thay đổi quan trọng để commit.

#### **Cách đưa thay đổi vào:** Sử dụng lệnh git add

- git add [tên\_file] : Đưa thay đổi của một file cụ thể vào Staging Area.
- git add . : Đưa tất cả các thay đổi (file mới, file đã sửa, file đã xóa) trong thư mục hiện tại và các thư mục con vào Staging Area.

Hành động này gọi là "staging" hoặc "đưa vào khu vực chuẩn bị".

## **Git Repository (Kho chứa Git / Thư mục .git )**

Đây là nơi Git lưu trữ toàn bộ lịch sử thay đổi của dự án dưới dạng các "snapshots" (ảnh chụp nhanh) gọi là **commits**. Thông thường, kho chứa này nằm trong một thư mục ẩn có tên là .git tại thư mục gốc của dự án.

- Mỗi commit là một bản ghi vĩnh viễn về trạng thái của dự án tại một thời điểm nhất định.
- Lịch sử commit cho phép bạn xem lại các thay đổi, quay lại các phiên bản cũ, và hợp nhất công việc của nhiều người.

### **Cách lưu thay đổi từ Staging Area vào Repository:** Sử dụng lệnh git commit

git commit -m "Thông điệp mô tả commit" : Lệnh này sẽ lấy tất cả những gì đang có trong Staging Area, tạo một commit mới với những thay đổi đó, và lưu

commit này vào Repository kèm theo một thông điệp mô tả (rất quan trọng để ghi rõ ràng, dễ hiểu).

Hành động này gọi là "**committing**" hoặc "**cam kết thay đổi**".

## **Tổng kết**

Luồng công việc phổ biến nhất khi làm việc với Git là:

- 1. **Sửa đổi:** Bạn thực hiện các thay đổi (thêm, sửa, xóa file) trong **Working Directory**.
- 2. **Chuẩn bị (Stage):** Bạn chọn lọc những thay đổi muốn lưu và đưa chúng vào **Staging Area** bằng lệnh git add . Bạn có thể lặp lại bước 1 và 2 nhiều lần cho đến khi Staging Area chứa đúng những gì bạn muốn cho lần commit tới.
- 3. **Cam kết (Commit):** Bạn ghi lại vĩnh viễn các thay đổi đã có trong Staging Area vào **Git Repository** bằng lệnh git commit -m "Thông điệp" .