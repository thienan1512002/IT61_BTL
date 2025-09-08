
# snap_apriori.py
# ---------------------------------------------
# QUY TRÌNH KHAI PHÁ LUẬT KẾT HỢP TỪ DỮ LIỆU MẠNG XÃ HỘI FACEBOOK (SNAP)
# Các bước:
# 1. Đọc dữ liệu mạng xã hội từ file SNAP (facebook_combined.txt)
# 2. Chuyển đổi dữ liệu thành các giỏ hàng (baskets) - mỗi giỏ là danh sách bạn bè của một người dùng
# 3. Chuyển đổi các giỏ hàng thành DataFrame nhị phân (mỗi cột là một người dùng, mỗi dòng là một transaction)
# 4. Khai phá luật kết hợp bằng thuật toán FP-Growth
# 5. Lưu các luật kết hợp ra file JSON để phục vụ phân tích, trực quan hóa hoặc đề xuất
# ---------------------------------------------

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from collections import defaultdict
import json
import time
import psutil
import datetime

# BƯỚC 1: Đọc dữ liệu SNAP Facebook và hiển thị tiến trình
def load_snap_data(path):
    # Bước 1: Đọc dữ liệu SNAP Facebook
    # Đếm tổng số dòng để hiển thị tiến trình
    total_lines = sum(1 for _ in open(path))

    # Tạo đồ thị: mỗi user là một node, các cạnh là quan hệ bạn bè
    graph = defaultdict(set)
    with open(path, 'r') as f:
        for i, line in enumerate(f, 1):
            u1, u2 = line.strip().split()
            graph[u1].add(u2)
            graph[u2].add(u1)

            if i % 10000 == 0 or i == total_lines:
                print(f"Đang đọc dòng {i:,} / {total_lines:,}")
    print("✅ Đọc hoàn tất.")
    return graph

# BƯỚC 2: Chuyển đổi thành giỏ hàng người dùng
def convert_to_baskets(graph):
    # Bước 2: Chuyển đổi thành giỏ hàng người dùng
    baskets = []
    # Mỗi giỏ hàng là danh sách bạn bè của một user (chỉ lấy user có >=2 bạn)
    for user, friends in graph.items():
        if len(friends) >= 2:
            baskets.append(list(friends))
    print(f"✅ Tạo {len(baskets):,} giỏ hàng từ dữ liệu mạng.")
    return baskets

# BƯỚC 3: Chuyển thành DataFrame nhị phân
def baskets_to_df(baskets):
    # Bước 3: Chuyển thành DataFrame nhị phân
    # Tạo danh sách tất cả người dùng xuất hiện trong các giỏ hàng
    all_items = sorted({item for basket in baskets for item in basket})
    # Tạo DataFrame: mỗi dòng là một transaction, mỗi cột là một user, giá trị 1 nếu user xuất hiện trong transaction
    df = pd.DataFrame(0, index=range(len(baskets)), columns=all_items)
    for i, basket in enumerate(baskets):
        df.loc[i, basket] = 1
    print(f"✅ DataFrame nhị phân có kích thước: {df.shape}")
    return df

# BƯỚC 4: Khai phá luật kết hợp bằng FP-Growth
def mine_association_rules(df, min_support=0.05, min_confidence=0.7):
    # Bước 4: Khai phá luật kết hợp bằng Apriori
    # Chuyển DataFrame về dạng bool (True/False)
    df_bool = df.astype(bool)

    user_freq = df_bool.sum(axis=0)
    # Lọc các user xuất hiện ít nhất 1 lần (có thể chỉnh ngưỡng nếu muốn)
    top_users = user_freq[user_freq >= 1].index
    df_bool = df_bool[top_users]
    print(f"✅ Lọc còn {len(top_users):,} người dùng có >1 lần xuất hiện.")

    # Sử dụng toàn bộ transaction để khai phá luật
    print(f"✅ Sử dụng toàn bộ {df_bool.shape[0]:,} transaction để khai phá.")

    # Khai phá các itemset thường xuyên bằng Apriori
    freq_items = apriori(df_bool, min_support=min_support, use_colnames=True)
    print(f"✅ Tìm được {len(freq_items):,} itemset thường xuyên.")

    # Sinh các luật kết hợp từ các itemset thường xuyên
    rules = association_rules(freq_items, metric="confidence", min_threshold=min_confidence)
    print(f"✅ Khai phá được {len(rules):,} luật kết hợp.")
    return rules, len(rules)

# BƯỚC 5: Xuất luật ra file JSON
def save_rules_json(rules, total_rules, start_time, path):
    # Tính toán metrics
    end_time = time.time()
    execution_time = end_time - start_time
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024  # Convert to MB
    cpu_percent = psutil.cpu_percent()

    # Tạo metadata
    metadata = {
        "algorithm": "Apriori",
        "execution_time": round(execution_time, 2),
        "total_rules": total_rules,
        "memory_usage": round(memory_usage, 2),
        "cpu_usage": round(cpu_percent, 2),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Chuyển đổi rules thành list các dict
    rules_list = []
    for _, row in rules.iterrows():
        rules_list.append({
            "antecedents": list(row['antecedents']),
            "consequents": list(row['consequents']),
            "support": round(row['support'], 4),
            "confidence": round(row['confidence'], 4),
            "lift": round(row['lift'], 4)
        })

    # Tạo output JSON với metadata
    output = {
        "metadata": metadata,
        "rules": rules_list
    }

    # Lưu vào file
    with open(path, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Lưu luật kết hợp vào: {path}")
    print(f"✅ Thời gian thực thi: {execution_time:.2f}s")
    print(f"✅ Bộ nhớ sử dụng: {memory_usage:.2f}MB")
    print(f"✅ CPU usage: {cpu_percent}%")

# CHẠY TOÀN BỘ QUY TRÌNH
if __name__ == '__main__':
    start_time = time.time()
    
    # Lấy đường dẫn tuyệt đối đến thư mục gốc dự án
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Tạo đường dẫn đến các file
    snap_path = os.path.join(project_root, 'Raw_Data', 'facebook_combined.txt')
    print(f"📂 Đường dẫn file dữ liệu: {snap_path}")
    
    # Kiểm tra file tồn tại
    if not os.path.exists(snap_path):
        print("❌ Lỗi: Không tìm thấy file dữ liệu!")
        print("💡 Hãy chạy combine_edges.py trước để tạo file facebook_combined.txt")
        exit(1)
        
    # Đọc dữ liệu mạng xã hội
    graph = load_snap_data(snap_path)

    baskets = convert_to_baskets(graph)              # Tạo các giỏ hàng từ dữ liệu mạng
    df = baskets_to_df(baskets)                      # Chuyển thành DataFrame nhị phân

    rules, total_rules = mine_association_rules(df, min_support=0.05, min_confidence=0.6)  # Khai phá luật kết hợp
    
    # Tạo thư mục Data_Result/Rules nếu chưa tồn tại
    output_dir = os.path.join(project_root, 'Data_Result', 'Rules')
    os.makedirs(output_dir, exist_ok=True)
    
    # Lưu luật ra file JSON
    output_path = os.path.join(output_dir, 'association_rules.json')
    save_rules_json(rules, total_rules, start_time, output_path)
