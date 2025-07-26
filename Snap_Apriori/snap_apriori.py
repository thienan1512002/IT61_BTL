
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
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from collections import defaultdict
import json

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
    # Bước 4: Khai phá luật kết hợp bằng FP-Growth
    # Chuyển DataFrame về dạng bool (True/False)
    df_bool = df.astype(bool)

    user_freq = df_bool.sum(axis=0)
    # Lọc các user xuất hiện ít nhất 1 lần (có thể chỉnh ngưỡng nếu muốn)
    top_users = user_freq[user_freq >= 1].index
    df_bool = df_bool[top_users]
    print(f"✅ Lọc còn {len(top_users):,} người dùng có >1 lần xuất hiện.")

    # Sử dụng toàn bộ transaction để khai phá luật
    print(f"✅ Sử dụng toàn bộ {df_bool.shape[0]:,} transaction để khai phá.")

    # Khai phá các itemset thường xuyên bằng FP-Growth
    freq_items = fpgrowth(df_bool, min_support=min_support, use_colnames=True)
    print(f"✅ Tìm được {len(freq_items):,} itemset thường xuyên.")

    # Sinh các luật kết hợp từ các itemset thường xuyên
    rules = association_rules(freq_items, metric="confidence", min_threshold=min_confidence)
    print(f"✅ Khai phá được {len(rules):,} luật kết hợp.")
    return rules

# BƯỚC 5: Xuất luật ra file JSON
def save_rules_json(rules, path):
    # Bước 5: Lưu các luật kết hợp ra file JSON
    output = []
    for _, row in rules.iterrows():
        output.append({
            "LHS": list(row['antecedents']),
            "RHS": list(row['consequents']),
            "support": round(row['support'], 4),
            "confidence": round(row['confidence'], 4),
            "lift": round(row['lift'], 4)
        })
    with open(path, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Lưu luật kết hợp vào: {path}")

# CHẠY TOÀN BỘ QUY TRÌNH
if __name__ == '__main__':
    # Chạy toàn bộ quy trình khai phá luật kết hợp
    snap_path = './Raw_Data/facebook_combined.txt'  # Đường dẫn file SNAP
    graph = load_snap_data(snap_path)                # Đọc dữ liệu mạng xã hội

    baskets = convert_to_baskets(graph)              # Tạo các giỏ hàng từ dữ liệu mạng
    df = baskets_to_df(baskets)                      # Chuyển thành DataFrame nhị phân

    rules = mine_association_rules(df, min_support=0.05, min_confidence=0.6)  # Khai phá luật kết hợp
    save_rules_json(rules, './Data_Result/Rules/association_rules.json')       # Lưu luật ra file JSON
