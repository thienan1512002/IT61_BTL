using System.Diagnostics;
using System.Text.Json;
using DataMiningSocialApp.Models;
using DataMiningSocialApp.Services;
using Microsoft.AspNetCore.Mvc;

namespace DataMiningSocialApp.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly IRuleService _ruleService;
        private readonly Dictionary<string, List<string>> _baskets;
        private readonly List<AssociationRule> _rules;
        private readonly string APRIORI_RULE_PATH = "E://UNI//Source Code//IT61_BTL//Data_Result//Rules//association_rules.json";
        private readonly string FP_GROWTH_RULE_PATH = "E://UNI//Source Code//IT61_BTL//Data_Result//Rules//fp_growth_rules.json";
        private readonly string BASKET_PATH = "E://UNI//Source Code//IT61_BTL//Data_Result//DataExample//facebook_combined.csv";

        public HomeController(ILogger<HomeController> logger, IRuleService ruleService)
        {
            _ruleService = ruleService;

            // Tải luật từ cả hai file
            var aprioriRules = _ruleService.LoadRules(APRIORI_RULE_PATH);
            var fpGrowthRules = _ruleService.LoadRules(FP_GROWTH_RULE_PATH);
            _rules = aprioriRules.Concat(fpGrowthRules).ToList();
            //_rules = fpGrowthRules;


            _baskets = _ruleService.LoadUserBaskets(BASKET_PATH); // Tải dữ liệu bạn bè từ file
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Rules()
        {
            return View(_rules);
        }

        public IActionResult Dashboard()
        {
            return View();
        }

        [HttpGet]
        public IActionResult GetRules()
        {
            try
            {
                // Đọc trực tiếp từ file để lấy metadata
                var aprioriJson = System.IO.File.ReadAllText(APRIORI_RULE_PATH);
                var fpGrowthJson = System.IO.File.ReadAllText(FP_GROWTH_RULE_PATH);

                var aprioriData = System.Text.Json.JsonDocument.Parse(aprioriJson);
                var fpGrowthData = System.Text.Json.JsonDocument.Parse(fpGrowthJson);

                // Parse rules from JSON data directly
                var aprioriRules = aprioriData.RootElement.GetProperty("rules")
                    .EnumerateArray()
                    .Select(r => new
                    {
                        antecedent = string.Join(", ", r.GetProperty("antecedents").EnumerateArray().Select(x => x.GetString())),
                        consequent = string.Join(", ", r.GetProperty("consequents").EnumerateArray().Select(x => x.GetString())),
                        support = r.GetProperty("support").GetDouble(),
                        confidence = r.GetProperty("confidence").GetDouble(),
                        lift = r.GetProperty("lift").GetDouble()
                    }).ToList();

                var fpGrowthRules = fpGrowthData.RootElement.GetProperty("rules")
                    .EnumerateArray()
                    .Select(r => new
                    {
                        antecedent = string.Join(", ", r.GetProperty("antecedents").EnumerateArray().Select(x => x.GetString())),
                        consequent = string.Join(", ", r.GetProperty("consequents").EnumerateArray().Select(x => x.GetString())),
                        support = r.GetProperty("support").GetDouble(),
                        confidence = r.GetProperty("confidence").GetDouble(),
                        lift = r.GetProperty("lift").GetDouble()
                    }).ToList();

                // Helper function to safely get metadata value
                double SafeGetMetadataDouble(JsonDocument doc, string property, double defaultValue = 0)
                {
                    try
                    {
                        var metadata = doc.RootElement.GetProperty("metadata");
                        if (metadata.TryGetProperty(property, out JsonElement value))
                        {
                            return value.GetDouble();
                        }
                        return defaultValue;
                    }
                    catch
                    {
                        return defaultValue;
                    }
                }

                int SafeGetMetadataInt(JsonDocument doc, string property, int defaultValue = 0)
                {
                    try
                    {
                        var metadata = doc.RootElement.GetProperty("metadata");
                        if (metadata.TryGetProperty(property, out JsonElement value))
                        {
                            return value.GetInt32();
                        }
                        return defaultValue;
                    }
                    catch
                    {
                        return defaultValue;
                    }
                }

                var metadata = new
                {
                    apriori = new
                    {
                        execution_time = SafeGetMetadataDouble(aprioriData, "execution_time"),
                        memory_usage = SafeGetMetadataDouble(aprioriData, "memory_usage"),
                        cpu_usage = SafeGetMetadataDouble(aprioriData, "cpu_usage"),
                        total_rules = SafeGetMetadataInt(aprioriData, "total_rules")
                    },
                    fpGrowth = new
                    {
                        execution_time = SafeGetMetadataDouble(fpGrowthData, "execution_time"),
                        memory_usage = 0.0, // Default value since FP-Growth doesn't provide memory usage
                        cpu_usage = 0.0,    // Default value since FP-Growth doesn't provide CPU usage
                        total_rules = SafeGetMetadataInt(fpGrowthData, "total_rules")
                    }
                };

                return Json(new
                {
                    aprioriRules = aprioriRules,
                    fpGrowthRules = fpGrowthRules,
                    metadata = metadata
                });
            }
            catch (Exception ex)
            {
                _logger.LogError($"Error in GetRules: {ex.Message}");
                return Json(new { error = "Failed to load rules data" });
            }
        }

        [HttpPost]
        public IActionResult Suggest(string userId)
        {
            var suggestions = _ruleService.SuggestFriends(userId, _baskets, _rules);
            ViewBag.UserId = userId;
            return View(suggestions);
        }


        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
