using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace QueryCast.Controllers
{
    public class MediaOldController : Controller
    {
        private readonly BusinessAccess _businessAccess;

        public MediaOldController()
        {
            _businessAccess = new BusinessAccess();
        }




        // GET: Display the initial form
        public IActionResult Index()
        {
            var viewModel = new MediaSearchViewModel
            {
                Categories = _businessAccess.FetchCategories()
            };
            viewModel.CategorySelectList = new SelectList(viewModel.Categories);
            System.Diagnostics.Debug.WriteLine(viewModel.Categories);
            return View(viewModel);
        }

        [HttpPost]
        public async Task<IActionResult> Index(MediaSearchViewModel model)
        {

            string? question = model.UserQuestion;


            var doubleEmbeddings = await _businessAccess.GenerateQuestionEmbedding(question);
            var floatEmbeddings = doubleEmbeddings.Select(d => (float)d).ToList(); // Conversion
                                                                                   // model.MediaFiles =  _businessAccess.FetchAllEntries(floatEmbeddings);


            // Fetch entries either by category (if selected) or all entries
            if (!string.IsNullOrEmpty(model.SelectedCategory))
            {
                model.MediaFiles = _businessAccess.FetchEntriesByCategoryAndScore(floatEmbeddings, model.SelectedCategory);
            }
            else
            {
                model.MediaFiles = _businessAccess.FetchAllEntries(floatEmbeddings);
            }

            // Repopulate categories for the dropdown
            model.Categories = _businessAccess.FetchCategories();

            return View(model);
        }
    }
}
