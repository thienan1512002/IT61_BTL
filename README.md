# IT61_BTL - Social Network Analysis System

Hệ thống khai phá và phân tích mối quan hệ trong mạng xã hội sử dụng thuật toán Apriori và FP-Growth, tích hợp Python và ASP.NET Core MVC.

## Snap_Apriori

### Giới thiệu

`Snap_Apriori` là module Python dùng để khai thác luật kết hợp (association rules) từ dữ liệu mạng xã hội, sử dụng thuật toán Apriori và FP-Growth. Dự án này phù hợp cho các bài toán phân tích dữ liệu lớn, đặc biệt là dữ liệu mạng xã hội như Facebook SNAP dataset.

## Yêu cầu hệ thống

- **Python**: Phiên bản tối thiểu 3.7
- Các thư viện cần thiết:
  - pandas
  - numpy
  - scikit-learn
  - mlxtend
  - json (có sẵn trong Python)

Cài đặt thư viện bằng lệnh:

```powershell
pip install pandas numpy scikit-learn mlxtend
```

## Cấu trúc thư mục

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

## Hướng dẫn sử dụng

### 1. Cài đặt và chuẩn bị

1. **Chuẩn bị môi trường Python**:

   ```powershell
   # Kiểm tra phiên bản
   python --version  # Phải >= 3.7

   # Cài đặt thư viện
   pip install pandas numpy scikit-learn mlxtend
   ```

2. **Chuẩn bị dữ liệu**:
   - Copy dữ liệu SNAP vào thư mục `Raw_Data/`:
     - `facebook_combined.txt`: Dữ liệu quan hệ bạn bè
     - `features.txt`: Đặc trưng người dùng (optional)
     - `circles/`: Thông tin nhóm (optional)

### 2. Khai phá luật kết hợp

1. **Chạy thuật toán**:

   ```powershell
   cd Snap_Apriori
   python snap_apriori.py
   ```

2. **Tham số có thể điều chỉnh**:

   - Trong file `snap_apriori.py`:

     ```python
     # Thuật toán: 'apriori' hoặc 'fpgrowth'
     algorithm = 'fpgrowth'

     # Ngưỡng
     min_support = 0.05
     min_confidence = 0.5
     ```

3. **Kết quả**:
   - File: `Data_Result/Rules/association_rules.json`
   - Format:
     ```json
     {
       "LHS": ["user1", "user2"],
       "RHS": ["user3"],
       "support": 0.0638,
       "confidence": 0.9961,
       "lift": 3.8186
     }
     ```

## DataMiningSocialApp - ASP.NET Core MVC

### 1. Yêu cầu hệ thống

- **.NET Core SDK**: 6.0 trở lên
- **IDE**: VS Code với C# Dev Kit extension
- **Database**: SQL Server (LocalDB/Express)
- **Packages**:
  - Microsoft.EntityFrameworkCore.SqlServer
  - Dapper
  - Newtonsoft.Json

### 2. Cài đặt

1. **Cài đặt .NET SDK**:

   - Tải từ: https://dotnet.microsoft.com/download
   - Kiểm tra:
     ```powershell
     dotnet --version  # Phải >= 6.0
     ```

2. **Chuẩn bị database**:

   ```powershell
   # Chạy script tạo database
   cd Database
   sqlcmd -S .(LocalDB) -i schema.sql
   ```

3. **Cấu hình ứng dụng**:
   - Mở `DataMiningSocialApp/appsettings.json`
   - Cập nhật connection string

### 3. Chạy ứng dụng

1. **Build và run**:

   ```powershell
   cd DataMiningSocialApp

   # Restore dependencies
   dotnet restore

   # Build
   dotnet build

   # Run
   dotnet run
   ```

2. **Truy cập**:
   - URL: https://localhost:5001
   - Các trang chính:
     - Dashboard: `/Home/Index`
     - Luật kết hợp: `/Home/Rules`
     - Gợi ý bạn bè: `/Home/Suggest`

### 4. Tính năng

1. **Dashboard**

   - So sánh hiệu suất Apriori vs FP-Growth
   - Biểu đồ thống kê
   - Danh sách luật kết hợp

2. **Khai phá luật**

   - Xem tất cả luật
   - Lọc theo metrics:
     - Support >= 0.05
     - Confidence >= 0.6
     - Lift > 1

3. **Gợi ý bạn bè**
   - Dựa trên luật kết hợp
   - Hiển thị lý do gợi ý
   - Theo dõi trạng thái kết bạn

## Xử lý lỗi thường gặp

### Python

- Check PATH trong biến môi trường
- Cài đủ thư viện
- Đúng phiên bản Python

### .NET

- Xóa thư mục bin và obj
- Check connection string
- SQL Server đang chạy

### Database

- Quyền truy cập SQL Server
- Chạy lại schema.sql
- Database tồn tại

## Đóng góp

Tạo issue hoặc pull request trên GitHub.

## License

MIT License
