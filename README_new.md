# IT61_BTL - Social Network Analysis System

Hệ thống khai phá và phân tích mối quan hệ trong mạng xã hội sử dụng thuật toán Apriori và FP-Growth, tích hợp Python và ASP.NET Core MVC.

## Cấu trúc dự án

```
IT61_BTL/
├── Snap_Apriori/           # Module Python xử lý dữ liệu
│   └── snap_apriori.py     # Script khai phá luật kết hợp
├── Database/               # Scripts và schema SQL Server
│   └── schema.sql         # Cấu trúc database
├── DataMiningSocialApp/   # Ứng dụng ASP.NET Core MVC
├── Raw_Data/              # Dữ liệu thô từ SNAP
│   ├── facebook_combined.txt
│   ├── features.txt
│   └── circles/
└── Data_Result/          # Dữ liệu đã xử lý
    └── Rules/
        └── association_rules.json
```

## Yêu cầu hệ thống

### 1. Python (Xử lý dữ liệu)

- Python 3.7 trở lên
- Các thư viện cần thiết:
  ```powershell
  pip install pandas numpy scikit-learn mlxtend
  ```

### 2. .NET Core (Web Application)

- .NET 6.0 SDK trở lên
- VS Code với C# Dev Kit extension
- SQL Server (LocalDB hoặc Express)
- Các NuGet packages:
  - Microsoft.EntityFrameworkCore.SqlServer
  - Dapper
  - Newtonsoft.Json

## Hướng dẫn cài đặt và chạy

### 1. Chuẩn bị môi trường

1. **Cài đặt Python và pip**:

   ```powershell
   # Kiểm tra Python
   python --version  # Phải >= 3.7

   # Cài đặt thư viện
   pip install pandas numpy scikit-learn mlxtend
   ```

2. **Cài đặt .NET SDK**:

   - Tải từ: https://dotnet.microsoft.com/download
   - Kiểm tra:
     ```powershell
     dotnet --version  # Phải >= 6.0
     ```

   ```

   ```

### 2. Khai phá luật kết hợp (Python)

1. **Chuẩn bị dữ liệu**:

   ```powershell
   # Copy dữ liệu SNAP vào thư mục Raw_Data
   cp facebook_combined.txt Raw_Data/
   ```

2. **Chạy thuật toán**:
   ```powershell
   cd Snap_Apriori
   python snap_apriori.py
   ```
   - Kết quả lưu trong: `Data_Result/Rules/association_rules.json`
   - Có thể điều chỉnh tham số trong file:
     - minSupport = 0.05
     - minConfidence = 0.5

### 3. Chạy ứng dụng web (ASP.NET Core MVC)

1. **Restore và build**:

   ```powershell
   cd DataMiningSocialApp
   dotnet restore
   dotnet build
   ```

2. **Cấu hình database**:

   - Mở `appsettings.json`
   - Cập nhật connection string

3. **Khởi chạy**:
   ```powershell
   dotnet run
   ```
   Truy cập: https://localhost:5001

## Sử dụng hệ thống

### 1. Dashboard

- So sánh hiệu suất Apriori vs FP-Growth
- Xem thống kê và biểu đồ
- URL: `/Home/Index`

### 2. Khai phá luật kết hợp

- Xem danh sách luật
- Lọc theo metrics
- URL: `/Home/Rules`

### 3. Gợi ý bạn bè

- Đăng nhập để xem gợi ý
- Dựa trên luật kết hợp chất lượng cao
- URL: `/Home/Suggest`

## Xử lý lỗi thường gặp

1. **Lỗi Python**:

   - Kiểm tra PATH
   - Cài đủ thư viện
   - Đúng phiên bản Python

2. **Lỗi .NET**:
   - Xóa bin/obj, build lại
   - Check connection string
   - SQL Server đang chạy
