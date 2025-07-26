using DataMiningSocialApp.Models;

namespace DataMiningSocialApp.Services
{
    public interface IRuleService
    {
        public List<AssociationRule> LoadRules(string path); // Đọc luật từ ../Data_Result/Rules/association_rules.json

        public List<string> SuggestFriends(string userId, Dictionary<string, List<string>> userBaskets, List<AssociationRule> rules);

        public Dictionary<string, List<string>> LoadUserBaskets(string path);

    }
}
