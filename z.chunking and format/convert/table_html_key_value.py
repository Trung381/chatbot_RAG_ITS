from bs4 import BeautifulSoup

def convert_html_table_to_key_value_string(html_string):
    """
    Chuyển đổi một bảng HTML từ một chuỗi thành một chuỗi có định dạng key:value cho mỗi hàng.

    Args:
        html_string: Chuỗi chứa mã HTML của bảng.

    Returns:
        Một chuỗi đã định dạng, mỗi hàng của bảng được biểu diễn dưới dạng key:value.

    For example:
        example table data:
        STT | Name | Date of birth | Address
        1   | John | 20/01/2000    | Hanoi
        2   | Jane | 21/02/2001    | Haiphong
        
        string output: [TABLE]STT: 1, Name: John, Date of birth: 20/01/2000, Address: Hanoi\n[TABLE]STT: 2, Name: Jane, Date of birth: 21/02/2001, Address: Haiphong"

    """
    soup = BeautifulSoup(html_string, 'html.parser', from_encoding='utf-8')
    
    # Tìm bảng đầu tiên trong HTML
    table = soup.find('table')
    
    if not table:
        return "Không tìm thấy bảng nào trong chuỗi HTML."

    output_strings = []
    
    # Lấy các thẻ <tr> (hàng) trong bảng
    rows = table.find_all('tr')
    
    if len(rows) < 2:
        return "Bảng không có đủ hàng (tiêu đề và dữ liệu)."

    # Hàng đầu tiên được coi là hàng tiêu đề
    header_row = rows[0]
    headers = [header.get_text(strip=True) for header in header_row.find_all(['th', 'td'])]
    
    # Các hàng còn lại là hàng dữ liệu
    data_rows = rows[1:]
    
    for row in data_rows:
        columns = row.find_all(['th', 'td'])
        
        # Bỏ qua các hàng trống
        if not any(col.get_text(strip=True) for col in columns):
            continue

        row_data = {}
        for i, col in enumerate(columns):
            if i < len(headers):
                row_data[headers[i]] = col.get_text(strip=True)
        
        # Tạo chuỗi key:value cho mỗi hàng
        key_value_pairs = [f"{key}: {value}" for key, value in row_data.items()]
        output_strings.append("[TABLE]" + ", ".join(key_value_pairs))
        
    return "\\n".join(output_strings)


html_string = """
<table><tr><td>Tênga</td><td>SE2</td><td>SE4</td><td>SE6</td><td>SE8</td><td>SE10</td><td>SE12</td><td>SE20</td><td>SE18</td><td>QB2</td><td>QB4</td><td>NA2</td></tr><tr><td>SÀI</td><td>20:35</td><td>19:00</td><td>15:00</td><td>6:00</td><td>12:20</td><td>19:25</td><td/><td/><td/><td/><td/></tr><tr><td>GÒN</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>DĨAN</td><td>21:05</td><td>19:32</td><td>15:32</td><td>6:32</td><td>12:52</td><td>19:59</td><td/><td/><td/><td/><td/></tr><tr><td>BIÊN</td><td>21:21</td><td>19:48</td><td>15:48</td><td>6:48</td><td>13:08</td><td>20:18</td><td/><td/><td/><td/><td/></tr><tr><td>HÒA</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>LONG</td><td/><td>20:51</td><td>16:51</td><td>7:51</td><td>14:11</td><td>21:20</td><td/><td/><td/><td/><td/></tr><tr><td>KHÁNH</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>SUỐI</td><td/><td/><td>17:42</td><td>8:43</td><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>KIẾT</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>BÌNH</td><td>0:04</td><td>22:41</td><td>18:46</td><td>9:46</td><td>16:08</td><td>23:08</td><td/><td/><td/><td/><td/></tr><tr><td>THUẬN</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>SÔNG</td><td/><td/><td>19:52</td><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>MAO</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>THÁP</td><td/><td/><td>21:09</td><td>12:04</td><td>18:26</td><td>2:36</td><td/><td/><td/><td/><td/></tr><tr><td>CHÀM</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>NHA</td><td>3:56</td><td>2:36</td><td>23:28</td><td>13:59</td><td>21:45</td><td>4:26</td><td/><td/><td/><td/><td/></tr><tr><td>TRANG</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>NINH</td><td/><td/><td>0:13</td><td>14:44</td><td>22:51</td><td>5:11</td><td/><td/><td/><td/><td/></tr><tr><td>HÒA</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>GIÃ</td><td/><td/><td/><td>15:15</td><td/><td>5:42</td><td/><td/><td/><td/><td/></tr><tr><td>TUY</td><td>6:06</td><td>4:47</td><td>1:52</td><td>16:21</td><td>0:23</td><td>6:47</td><td/><td/><td/><td/><td/></tr><tr><td>HÒA</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>LAHAI</td><td/><td/><td/><td>17:20</td><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>DIÊU</td><td>8:17</td><td>6:52</td><td>3:57</td><td>18:41</td><td>2:28</td><td>9:06</td><td/><td/><td/><td/><td/></tr><tr><td>TRÌ</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>BỒNG</td><td/><td>8:16</td><td>5:30</td><td>20:06</td><td>4:18</td><td>10:33</td><td/><td/><td/><td/><td/></tr><tr><td>SƠN</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>ĐỨC</td><td/><td/><td>6:22</td><td/><td>5:10</td><td>11:25</td><td/><td/><td/><td/><td/></tr><tr><td>PHÓ</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr></table>\n\n<table><tr><td>QUÃNG</td><td>11:07</td><td>9:53</td><td>7:12</td><td>21:53</td><td>6:00</td><td>12:21</td><td/><td/><td/><td/><td/></tr><tr><td>NGÃI</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>NÚI</td><td/><td/><td>7:56</td><td/><td>6:44</td><td>13:05</td><td/><td/><td/><td/><td/></tr><tr><td>THÀNH</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>TAM</td><td>12:15</td><td>11:12</td><td>8:30</td><td>23:05</td><td>7:17</td><td>13:47</td><td/><td/><td/><td/><td/></tr><tr><td>KỲ</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>TRÀ</td><td/><td>11:54</td><td>9:23</td><td/><td>7:58</td><td>14:43</td><td/><td/><td/><td/><td/></tr><tr><td>KIỆU</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>ĐÃ</td><td>13:55</td><td>12:57</td><td>10:30</td><td>0:56</td><td>9:04</td><td>15:43</td><td>18:05</td><td>19:25</td><td/><td/><td/></tr><tr><td>NẴNG</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>HUẾ</td><td>16:24</td><td>15:32</td><td>13:43</td><td>3:34</td><td>12:42</td><td>18:28</td><td>20:41</td><td>22:13</td><td/><td/><td/></tr><tr><td>ĐÔNG</td><td>17:35</td><td>16:47</td><td>14:56</td><td>4:49</td><td>13:57</td><td>19:52</td><td>21:54</td><td>23:41</td><td/><td/><td/></tr><tr><td>HÀ</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>MỸ</td><td/><td/><td>15:58</td><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>TRẠCH</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>MỸ</td><td/><td/><td/><td>6:15</td><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>ĐỨC</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>ĐỒNG</td><td>19:30</td><td>18:49</td><td>17:05</td><td>7:02</td><td>15:59</td><td>21:52</td><td>23:55</td><td>1:52</td><td>15:20</td><td>13:05</td><td/></tr><tr><td>HỚI</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>MINH</td><td/><td/><td/><td>7:51</td><td>16:59</td><td>22:41</td><td/><td/><td/><td/><td/></tr><tr><td>LỆ</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>ĐÔNG</td><td>21:10</td><td>20:31</td><td>18:47</td><td>8:49</td><td>17:57</td><td/><td/><td/><td>17:10</td><td/><td/></tr><tr><td>LÊ</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>HƯƠNG</td><td>22:16</td><td>21:39</td><td>19:55</td><td>9:57</td><td>19:05</td><td/><td/><td>6:10</td><td>18:20</td><td>17:10</td><td/></tr><tr><td>PHỐ</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>YÊN</td><td>23:14</td><td>22:38</td><td>20:54</td><td>10:56</td><td>20:16</td><td/><td/><td>7:08</td><td>19:20</td><td>18:08</td><td/></tr><tr><td>TRUNG</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>VINH</td><td>23:47</td><td>23:11</td><td>21:33</td><td>11:29</td><td>20:49</td><td>3:18</td><td>5:18</td><td>7:39</td><td>19:54</td><td>18:41</td><td>22:15</td></tr><tr><td>CHỢSI</td><td/><td/><td>22:20</td><td>12:35</td><td>21:54</td><td>4:32</td><td/><td/><td/><td/><td>23:03</td></tr><tr><td>MINH</td><td/><td/><td>0:11</td><td>14:15</td><td/><td>6:01</td><td/><td>10:01</td><td/><td/><td/></tr><tr><td>KHÔI</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>THANH</td><td>2:40</td><td>2:03</td><td>0:47</td><td>14:41</td><td>1:25</td><td>6:27</td><td>7:50</td><td>10:25</td><td/><td/><td/></tr><tr><td>HÓA</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>BỈM</td><td/><td/><td>1:25</td><td>15:19</td><td/><td>7:05</td><td/><td>11:06</td><td/><td/><td/></tr><tr><td>SƠN</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>NINH</td><td>3:46</td><td>3:12</td><td>2:01</td><td>16:12</td><td/><td>7:41</td><td>9:17</td><td>11:42</td><td/><td/><td/></tr><tr><td>BÌNH</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>NAM</td><td>4:21</td><td>3:50</td><td>2:38</td><td>17:08</td><td>3:06</td><td>8:29</td><td>9:54</td><td>12:19</td><td/><td/><td/></tr><tr><td>ĐỊNH</td><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/><td/></tr><tr><td>PHỦLÝ</td><td>4:56</td><td>4:31</td><td>3:14</td><td>17:52</td><td>3:49</td><td>9:05</td><td>10:30</td><td>12:55</td><td/><td/><td/></tr><tr><td>HÀNỘI</td><td>6:00</td><td>5:40</td><td>4:35</td><td>19:12</td><td>4:55</td><td>10:10</td><td>11:40</td><td>14:20</td><td>3:55</td><td>3:00</td><td>5:20</td></tr></table>
"""

# Chuyển đổi và in kết quả
formatted_string = convert_html_table_to_key_value_string(html_string)
print(formatted_string)