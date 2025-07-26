# IT61_BTL

# Snap_Apriori

## Giới thiệu

`Snap_Apriori` là module Python dùng để khai thác luật kết hợp (association rules) từ dữ liệu mạng xã hội, sử dụng thuật toán Apriori. Dự án này phù hợp cho các bài toán phân tích dữ liệu lớn, đặc biệt là dữ liệu mạng xã hội như Facebook.

## Yêu cầu hệ thống

- **Python**: Phiên bản tối thiểu 3.7
- Các thư viện cần thiết:
  - pandas
  - numpy
  - json (có sẵn trong Python)

Cài đặt thư viện bằng lệnh:

```powershell
pip install pandas numpy
```

## Cấu trúc thư mục

- `Snap_Apriori/`
  - `snap_apriori.py`: File chính thực thi thuật toán Apriori và sinh luật kết hợp.
- `Raw_Data/`
  - `facebook_combined.txt`: Dữ liệu thô đầu vào, chứa thông tin kết nối mạng xã hội.
- `Data_Result/`
  - `DataExample/`
    - `facebook_combined.csv`: Dữ liệu đã được xử lý, chuyển đổi từ dữ liệu thô.
  - `Rules/`
    - `association_rules.json`: File lưu kết quả các luật kết hợp được sinh ra từ thuật toán Apriori.

## Hướng dẫn sử dụng

1. **Chuẩn bị dữ liệu**  
   Đảm bảo dữ liệu thô đã được đặt trong `Raw_Data/facebook_combined.txt`.

2. **Cài đặt thư viện**  
   Chạy lệnh sau trong terminal:

   ```powershell
   pip install pandas numpy
   ```

3. **Chạy thuật toán Apriori**  
   Mở terminal tại thư mục gốc dự án và chạy lệnh sau:

   ```powershell
   cd "e:\UNI\Source Code\IT61_BTL\Snap_Apriori"
   python snap_apriori.py
   ```

   Kết quả các luật kết hợp sẽ được lưu tại `Data_Result/Rules/association_rules.json`.

## Ví dụ sử dụng

Giả sử bạn đã có dữ liệu đầu vào và đã cài đặt các thư viện cần thiết, chỉ cần chạy:

```powershell
cd "e:\UNI\Source Code\IT61_BTL\Snap_Apriori"
python snap_apriori.py
```

Sau khi chạy xong, kiểm tra file kết quả tại `Data_Result/Rules/association_rules.json`.
