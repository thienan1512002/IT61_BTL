import os
import glob

def combine_edges_files():
    # Đường dẫn đến thư mục chứa dữ liệu
    raw_data_dir = '../Raw_Data'
    output_file = os.path.join(raw_data_dir, 'facebook_combined.txt')
    
    print(f"\n📂 Thư mục dữ liệu: {os.path.abspath(raw_data_dir)}")
    
    # Kiểm tra thư mục tồn tại
    if not os.path.exists(raw_data_dir):
        print("❌ Lỗi: Không tìm thấy thư mục Raw_Data!")
        return
    
    # Tìm tất cả file .edges
    edge_files = glob.glob(os.path.join(raw_data_dir, '*.edges'))
    
    if not edge_files:
        print("❌ Lỗi: Không tìm thấy file .edges nào!")
        print("💡 Hãy đảm bảo các file .edges đã được copy vào thư mục Raw_Data")
        return
    
    print(f"\n🔍 Tìm thấy {len(edge_files)} file .edges:")
    for f in edge_files:
        print(f"   - {os.path.basename(f)}")
    
    # Tập hợp để lưu các cạnh unique (tránh trùng lặp)
    edges_set = set()
    total_edges = 0
    
    print("\n📖 Bắt đầu đọc dữ liệu:")
    # Đọc từng file .edges
    for edge_file in edge_files:
        file_edges = 0
        print(f"\n⏳ Đang xử lý: {os.path.basename(edge_file)}")
        
        try:
            with open(edge_file, 'r') as f:
                for line in f:
                    edge = line.strip()
                    if edge:  # Bỏ qua dòng trống
                        # Sắp xếp node để chuẩn hóa cạnh (1-2 và 2-1 là như nhau)
                        n1, n2 = sorted(map(int, edge.split()))
                        edges_set.add(f"{n1} {n2}")
                        file_edges += 1
                        total_edges += 1
            
            print(f"   ✓ Đọc được {file_edges:,} cạnh")
            
        except Exception as e:
            print(f"❌ Lỗi khi đọc file {edge_file}: {str(e)}")
            continue
    
    if not edges_set:
        print("\n❌ Không tìm thấy cạnh nào để xử lý!")
        return
    
    # Tạo thư mục chứa kết quả nếu chưa tồn tại
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Ghi ra file kết quả
    try:
        with open(output_file, 'w') as f:
            for edge in sorted(edges_set, key=lambda x: tuple(map(int, x.split()))):
                f.write(f"{edge}\n")
        
        print(f"\n✅ Hoàn tất! Kết quả:")
        print(f"   📊 Tổng số cạnh đọc được: {total_edges:,}")
        print(f"   📊 Số cạnh unique: {len(edges_set):,}")
        print(f"   📄 File kết quả: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Lỗi khi ghi file kết quả: {str(e)}")

if __name__ == '__main__':
    print("🚀 Bắt đầu kết hợp các file edges...")
    combine_edges_files()
    print("\n⌛ Kết thúc chương trình.")
