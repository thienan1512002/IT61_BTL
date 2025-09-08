using DataMiningSocialApp.Models;
using System.Text.Json;


namespace DataMiningSocialApp.Services
{
    /// <summary>
    /// Service để load luật kết hợp và gợi ý bạn bè dựa trên các luật này
    /// </summary>
    public class RuleService : IRuleService
    {
        /// <summary>
        /// Hàm khởi tạo RuleService
        /// </summary>
        public RuleService()
        {
        }
        /// <summary>
        /// Đọc file JSON chứa các luật kết hợp và chuyển thành danh sách AssociationRule
        /// </summary>
        /// <param name="path">Đường dẫn tới file luật</param>
        /// <returns>Danh sách các luật kết hợp</returns>
        public List<AssociationRule> LoadRules(string path)
        {
            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };
            var json = File.ReadAllText(path); // Đọc nội dung file JSON

            // Đọc dữ liệu từ JSON với cấu trúc mới chung
            var jsonData = JsonSerializer.Deserialize<RuleData>(json, options);
            if (jsonData?.Rules == null) return new List<AssociationRule>();

            string algorithm = jsonData.Metadata?.Algorithm ?? "Unknown";

            return jsonData.Rules.Select(r => new AssociationRule
            {
                LHS = r.Antecedents ?? new List<string>(),
                RHS = r.Consequents ?? new List<string>(),
                Support = r.Support,
                Confidence = r.Confidence,
                Lift = r.Lift,
                Algorithm = algorithm
            }).ToList();
        }

        private class RuleData
        {
            public MetaData? Metadata { get; set; }
            public List<Rule>? Rules { get; set; }
        }

        private class MetaData
        {
            public string Algorithm { get; set; } = string.Empty;
            public double ExecutionTime { get; set; }
            public double MemoryUsage { get; set; }
            public double CpuUsage { get; set; }
            public int TotalRules { get; set; }
            public string Timestamp { get; set; } = string.Empty;
        }

        private class Rule
        {
            public List<string> Antecedents { get; set; } = new List<string>();
            public List<string> Consequents { get; set; } = new List<string>();
            public double Support { get; set; }
            public double Confidence { get; set; }
            public double Lift { get; set; }
            public double? Leverage { get; set; }
            public double? Conviction { get; set; }
        }

        /// <summary>
        /// Đọc file txt chứa danh sách bạn bè của từng user và chuyển thành Dictionary
        /// Mỗi dòng có dạng: userId,friend1,friend2,...
        /// </summary>
        /// <param name="path">Đường dẫn tới file txt dữ liệu bạn bè</param>
        /// <returns>Dictionary với key là userId, value là danh sách bạn bè</returns>
        public Dictionary<string, List<string>> LoadUserBaskets(string path)
        {
            var dict = new Dictionary<string, List<string>>();
            foreach (var line in System.IO.File.ReadLines(path))
            {
                var parts = line.Split(','); // Tách các phần tử trên dòng bằng dấu phẩy
                var userId = parts[0];
                var friends = parts.Skip(1);
                if (!dict.ContainsKey(userId))
                {
                    dict[userId] = new List<string>(friends);
                }
                else
                {
                    // Gộp thêm bạn mới, tránh trùng lặp
                    dict[userId].AddRange(friends.Where(f => !dict[userId].Contains(f)));
                }
            }
            return dict;
        }

        /// <summary>
        /// Gợi ý bạn bè cho một user dựa trên các luật kết hợp
        /// </summary>
        /// <param name="userId">ID của user cần gợi ý</param>
        /// <param name="userBaskets">Dictionary chứa danh sách bạn bè của từng user</param>
        /// <param name="rules">Danh sách các luật kết hợp</param>
        /// <returns>Danh sách userId được gợi ý kết bạn</returns>
        public List<string> SuggestFriends(string userId, Dictionary<string, List<string>> userBaskets, List<AssociationRule> rules)
        {
            // Nếu user không tồn tại trong dữ liệu thì trả về rỗng
            if (!userBaskets.ContainsKey(userId)) return new List<string>();

            var userFriends = userBaskets[userId]; // Danh sách bạn bè hiện tại của user
            var suggestions = new HashSet<string>(); // Dùng HashSet để tránh trùng lặp

            // Duyệt qua từng luật kết hợp
            foreach (var rule in rules)
            {
                if (rule.LHS != null && rule.RHS != null)
                {
                    // Nếu tất cả phần tử bên trái luật đều có trong danh sách bạn bè của user
                    if (rule.LHS.All(x => userFriends.Contains(x)))
                    {
                        // Duyệt qua các phần tử bên phải luật
                        foreach (var f in rule.RHS)
                        {
                            // Nếu chưa là bạn và không phải chính user thì thêm vào gợi ý
                            if (!userFriends.Contains(f) && f != userId)
                            {
                                suggestions.Add(f);
                            }
                        }
                    }
                }
            }

            return suggestions.ToList(); // Trả về danh sách gợi ý
        }
    }
}
