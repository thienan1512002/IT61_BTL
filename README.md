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

- `Raw_Data/`
  - `facebook_combined.txt`: Dữ liệu thô đầu vào, chứa thông tin kết nối mạng xã hội.
- `Data_Result/`
  - `DataExample/`
  - `Rules/`

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

## Ví dụ sử dụng

```powershell
python snap_apriori.py
```

Sau khi chạy xong, kiểm tra file kết quả tại `Data_Result/Rules/association_rules.json`.

# 📊 Social Network Association Rules Mining - ASP.NET Core MVC

Đây là hệ thống web được xây dựng bằng **ASP.NET Core MVC (.NET 8)** để trình bày kết quả khai phá luật kết hợp từ dữ liệu mạng xã hội Facebook (SNAP dataset). Hệ thống đọc dữ liệu JSON được xuất từ Python (FP-Growth) và hiển thị qua giao diện web.

---

## 🔧 Công nghệ sử dụng

- ASP.NET Core MVC **8.0**
- C# (.NET 8)
- Newtonsoft.Json (đọc JSON)
- Python 3.11 (chạy thuật toán FP-Growth - riêng biệt)

---

## 🧰 Yêu cầu hệ thống

| Thành phần        | Phiên bản yêu cầu                |
| ----------------- | -------------------------------- |
| .NET SDK          | **8.0** trở lên                  |
| Visual Studio     | 2022 (có hỗ trợ .NET 8)          |
| Python (optional) | 3.11 nếu cần chạy lại thuật toán |

---

## ▶️ Cách chạy ứng dụng

1. **Cài đặt .NET 8 SDK**  
   Tải tại: https://dotnet.microsoft.com/en-us/download/dotnet/8.0

2. **Clone dự án về máy:**

   ```bash
   git clone https://github.com/thienan1512002/IT61_BTL.git

   cd IT61_BTL
   ```
