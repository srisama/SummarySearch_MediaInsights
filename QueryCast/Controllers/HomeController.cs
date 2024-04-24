using Microsoft.AspNetCore.Mvc;

namespace QueryCast.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
