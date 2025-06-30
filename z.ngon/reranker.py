chunks = [
    # Relevant
    "Đại Nội Huế là quần thể di tích nổi bật, từng là trung tâm hành chính – chính trị của triều Nguyễn, gồm Hoàng thành, Tử Cấm Thành và các cung điện cổ.",
    "Chùa Thiên Mụ, nằm bên bờ sông Hương, là một trong những biểu tượng văn hóa lâu đời và nổi tiếng nhất của cố đô Huế.",
    "Lăng Khải Định là công trình kiến trúc độc đáo kết hợp giữa phong cách Á – Âu, là điểm đến thu hút du khách yêu lịch sử và nghệ thuật.",
    "Đồi Thiên An và Tu viện Thiên An mang vẻ đẹp cổ kính, yên bình, là điểm đến hấp dẫn cho những ai yêu thích khám phá không gian tĩnh lặng và tâm linh.",
    "Cầu Trường Tiền bắc qua sông Hương là cây cầu gắn liền với hình ảnh Huế thơ mộng và được xem là một biểu tượng văn hóa của thành phố.",

    # Noisy
    "Huế có khí hậu nhiệt đới gió mùa, với mùa mưa kéo dài từ tháng 9 đến tháng 12, thích hợp để du lịch từ tháng 3 đến tháng 8.",
    "Ẩm thực Huế nổi tiếng với các món như bún bò Huế, bánh bèo, bánh bột lọc – phản ánh sự tinh tế trong văn hóa ẩm thực cung đình.",
    "Lễ hội Festival Huế được tổ chức định kỳ với các chương trình nghệ thuật, trình diễn áo dài, thuyền hoa và nhạc cung đình.",
    "Huế là nơi có nhiều làng nghề truyền thống như nón lá Phú Cam, tranh làng Sình, góp phần làm phong phú sản phẩm du lịch địa phương.",
    "Nhiều du khách thích chèo thuyền trên sông Hương vào buổi tối để thưởng thức ca Huế, một loại hình nghệ thuật truyền thống đặc sắc.",

    # Irrelevant
    "Đà Nẵng là một thành phố biển năng động với các điểm đến nổi tiếng như Bà Nà Hills, cầu Rồng, và bãi biển Mỹ Khê.",
    "Hội An, cách Huế khoảng 120km, là phố cổ được UNESCO công nhận, nổi bật với kiến trúc cổ và đèn lồng nhiều màu sắc.",
    "Sapa là một địa điểm du lịch nổi tiếng ở miền Bắc, hấp dẫn du khách bởi cảnh quan núi non và văn hóa dân tộc thiểu số.",
    "Phở Hà Nội thường được phục vụ với nước dùng trong, thịt bò tái và bánh phở mềm – là món ăn đặc trưng của miền Bắc.",
    "Thành phố Hồ Chí Minh là trung tâm kinh tế lớn nhất cả nước, với nhiều tòa nhà cao tầng và cuộc sống nhộn nhịp."
]

questions = [
    # Truy vấn rõ ràng → nên trả lại chunk 1, 2, 3...
    "Huế có những địa điểm du lịch văn hóa – lịch sử nổi bật nào?",
    "Lăng tẩm và đền đài nổi tiếng ở Huế là gì?",

    # Truy vấn hẹp → chỉ 1–2 chunk thật sự đúng
    "Chùa nào nổi tiếng ở Huế?",
    "Có công trình kiến trúc nào kết hợp phong cách Á – Âu tại Huế không?",

    # Truy vấn có thể gây nhầm lẫn với noisy chunk
    "Huế có những lễ hội truyền thống đặc sắc nào?",
    "Ca Huế được biểu diễn ở đâu và vào lúc nào?",

    # Truy vấn từ khóa giống irrelevant → kiểm tra khả năng chống lệch hướng
    "Những điểm du lịch nổi bật tại Đà Nẵng?",
    "Ẩm thực đặc trưng của miền Bắc là gì?",

    # Truy vấn ngắn gọn, cần hiểu ngữ nghĩa
    "Biểu tượng của Huế là gì?",
    "Cầu nào bắc qua sông Hương?",

    # Truy vấn rộng, mô hình phải chọn lọc
    "Đi đâu, chơi gì khi đến Huế?",
    "Giới thiệu các địa điểm nổi bật ở Huế dành cho người yêu văn hóa"
]

from sentence_transformers import CrossEncoder

# Load model
model = CrossEncoder("cross-encoder/ms-marco-electra-base")

# Tạo cặp (query, passage)
pairs = [(questions[0], doc) for doc in chunks]

# Tính điểm relevance
scores = model.predict(pairs)

# Sắp xếp và chọn top-n
reranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
top_docs = [[doc, score] for doc, score in reranked[:len(chunks)]]  # chọn top 3
for doc in top_docs:
    print(f"{doc[1]} - {doc[0]}")
