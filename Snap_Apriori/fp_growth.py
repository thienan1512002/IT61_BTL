import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import fpgrowth, association_rules
from collections import defaultdict
import json
import os
import time

def load_data(path):
    """Đọc dữ liệu từ file facebook_combined.txt"""
    print("\n1️⃣ Đang đọc dữ liệu...")
    
    # Đếm tổng số dòng
    total_lines = sum(1 for _ in open(path))
    
    # Tạo đồ thị
    graph = defaultdict(set)
    with open(path, 'r') as f:
        for i, line in enumerate(f, 1):
            u1, u2 = line.strip().split()
            graph[u1].add(u2)
            graph[u2].add(u1)
            
            if i % 10000 == 0:
                print(f"   Đã đọc: {i:,}/{total_lines:,} dòng")
    
    print(f"✅ Đã đọc xong {len(graph):,} nodes và {total_lines:,} edges")
    return graph

def create_transactions(graph):
    """Chuyển đổi graph thành các transactions"""
    print("\n2️⃣ Tạo transactions...")
    
    transactions = []
    for user, friends in graph.items():
        if len(friends) >= 2:  # Chỉ lấy user có từ 2 bạn trở lên
            transactions.append(list(friends))
    
    print(f"✅ Đã tạo {len(transactions):,} transactions")
    return transactions

def create_binary_matrix(transactions):
    """Chuyển transactions thành ma trận nhị phân"""
    print("\n3️⃣ Tạo ma trận nhị phân...")
    
    # Lấy danh sách tất cả users
    all_users = sorted(set(user for trans in transactions for user in trans))
    
    # Tạo DataFrame
    df = pd.DataFrame(0, index=range(len(transactions)), columns=all_users)
    for i, trans in enumerate(transactions):
        df.loc[i, trans] = 1
    
    print(f"✅ Ma trận có kích thước: {df.shape}")
    return df

def mine_fp_growth(df, min_support=0.05, min_confidence=0.5, min_lift=1.0):
    """Khai phá luật kết hợp bằng FP-Growth"""
    print("\n4️⃣ Bắt đầu khai phá luật...")
    start_time = time.time()
    
    # Chuyển về kiểu bool
    df_bool = df.astype(bool)
    
    # Tìm frequent itemsets
    print("   🔍 Tìm frequent itemsets...")
    frequent_itemsets = fpgrowth(df_bool, 
                                min_support=min_support,
                                use_colnames=True)
    print(f"   ✓ Tìm thấy {len(frequent_itemsets):,} itemsets")
    
    # Tạo luật kết hợp
    print("   🔍 Tạo luật kết hợp...")
    rules = association_rules(frequent_itemsets,
                            metric="confidence",
                            min_threshold=min_confidence)
    
    # Lọc luật theo lift
    quality_rules = rules[rules['lift'] >= min_lift].copy()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ Hoàn tất khai phá trong {duration:.2f} giây")
    print(f"   - Tổng số luật: {len(rules):,}")
    print(f"   - Số luật chất lượng (lift >= {min_lift}): {len(quality_rules):,}")
    
    return quality_rules, duration

def save_results(rules, duration, output_path):
    """Lưu kết quả ra file JSON"""
    print("\n5️⃣ Lưu kết quả...")
    
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Chuyển rules thành JSON
    results = {
        "metadata": {
            "algorithm": "FP-Growth",
            "execution_time": duration,
            "total_rules": len(rules),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "rules": []
    }
    
    for _, rule in rules.iterrows():
        results["rules"].append({
            "antecedents": list(rule['antecedents']),
            "consequents": list(rule['consequents']),
            "support": float(rule['support']),
            "confidence": float(rule['confidence']),
            "lift": float(rule['lift']),
            "leverage": float(rule['leverage']),
            "conviction": float(rule['conviction'])
        })
    
    # Lưu file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Đã lưu kết quả vào: {output_path}")

def main():
    # Thiết lập đường dẫn
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, 'Raw_Data', 'facebook_combined.txt')
    output_path = os.path.join(project_root, 'Data_Result', 'Rules', 'fp_growth_rules.json')
    
    print("🚀 Bắt đầu khai phá luật kết hợp bằng FP-Growth...")
    
    # Kiểm tra file đầu vào
    if not os.path.exists(input_path):
        print(f"❌ Không tìm thấy file dữ liệu: {input_path}")
        return
    
    # Các bước xử lý
    graph = load_data(input_path)
    transactions = create_transactions(graph)
    df = create_binary_matrix(transactions)
    rules, duration = mine_fp_growth(df)
    save_results(rules, duration, output_path)
    
    print("\n✨ Hoàn tất quá trình khai phá!")

if __name__ == "__main__":
    main()
