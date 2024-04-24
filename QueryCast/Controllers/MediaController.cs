using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using QueryCast;
namespace QueryCast.Controllers
{
    public class MediaController : Controller
    {
        private readonly BusinessAccess _businessAccess;

        public MediaController()
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
            var floatEmbeddings = doubleEmbeddings.Select(d => (float)d).ToList();

            if (!string.IsNullOrEmpty(model.SelectedCategory))
            {
                model.MediaFiles = _businessAccess.FetchEntriesByCategoryAndScore(floatEmbeddings, model.SelectedCategory);
            }
            else
            {
                model.MediaFiles = _businessAccess.FetchAllEntries(floatEmbeddings);
            }

            if (model.MediaFiles.Any())
            {
                var context = model.MediaFiles.First().Transcript; // Assuming you want to use the transcript of the first media file
                //var answer = await _businessAccess.GetAnswerFromContext(question, context);
                var answer = await _businessAccess.GenerateAnswerFromTranscript(question, context);



                model.Answer = answer; // Ensure your ViewModel has a property to hold this answer
            }

            // Repopulate categories for the dropdown
            model.Categories = _businessAccess.FetchCategories();

            return View(model);
        }
        //public async Task<IActionResult> Index(MediaSearchViewModel model)
        //{

        //    string? question = model.UserQuestion;


        //    var doubleEmbeddings = await _businessAccess.GenerateQuestionEmbedding(question);
        //    var floatEmbeddings = doubleEmbeddings.Select(d => (float)d).ToList(); // Conversion
        //                                                                           // model.MediaFiles =  _businessAccess.FetchAllEntries(floatEmbeddings);


        //    // Fetch entries either by category (if selected) or all entries
        //    if (!string.IsNullOrEmpty(model.SelectedCategory))
        //    {
        //        model.MediaFiles = _businessAccess.FetchEntriesByCategoryAndScore(floatEmbeddings, model.SelectedCategory);
        //    }
        //    else
        //    {
        //        model.MediaFiles = _businessAccess.FetchAllEntries(floatEmbeddings);
        //    }

        //    // Repopulate categories for the dropdown
        //    model.Categories = _businessAccess.FetchCategories();

        //    return View(model);
        //}
    }
}
