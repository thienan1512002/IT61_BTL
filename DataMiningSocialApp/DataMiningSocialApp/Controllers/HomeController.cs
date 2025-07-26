using System.Diagnostics;
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
        private readonly string RULE_PATH = "E://UNI//Source Code//IT61_BTL//Data_Result//Rules//association_rules.json";
        private readonly string BASKET_PATH = "E://UNI//Source Code//IT61_BTL//Data_Result//DataExample//facebook_combined.csv";

        public HomeController(ILogger<HomeController> logger, IRuleService ruleService)
        {
            _ruleService = ruleService;
            _rules = _ruleService.LoadRules(RULE_PATH); // Tải luật kết hợp từ file
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
