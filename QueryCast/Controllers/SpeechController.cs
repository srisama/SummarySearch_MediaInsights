using Microsoft.AspNetCore.Mvc;

namespace QueryCast.Controllers
{
    [Route("api/Speech/playsound")]
    [ApiController]
    public class SpeechController : ControllerBase
    {
        

        private readonly TextToSpeechService _textToSpeechService;

        public SpeechController(TextToSpeechService textToSpeechService)
        {
            _textToSpeechService = textToSpeechService;
        }

        [HttpPost]
        public async Task<IActionResult> playsound([FromBody] string text)
        {
            try
            {
                var speechData = await _textToSpeechService.SynthesizeSpeechAsync(text);
                return File(speechData, "audio/mp3");
            }
            catch (Exception ex)
            {
                return BadRequest(ex.Message);  // It’s better to log this exception
            }
        }
    }
}
