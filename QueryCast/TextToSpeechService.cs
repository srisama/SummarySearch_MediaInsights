using Newtonsoft.Json;
using System.Net.Http;
using System.Threading.Tasks;

namespace QueryCast
{
    public class TextToSpeechService
    {
        private readonly HttpClient _httpClient;

        public TextToSpeechService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<byte[]> SynthesizeSpeechAsync(string text)
        {
            var apiKey = "{insert api  key}"; // Replace with your actual API key
            var url = $"https://texttospeech.googleapis.com/v1/text:synthesize?key={apiKey}";
            var requestData = new
            {
                input = new { text = text },
                voice = new { languageCode = "en-US", ssmlGender = "NEUTRAL" },
                audioConfig = new { audioEncoding = "MP3" }
            };

            var response = await _httpClient.PostAsJsonAsync(url, requestData);
            response.EnsureSuccessStatusCode();
            var jsonContent = await response.Content.ReadAsStringAsync(); // Use ReadAsStringAsync here
            var jsonResponse = JsonConvert.DeserializeObject<dynamic>(jsonContent); // Deserialize the JSON content
            var audioContent = jsonResponse.audioContent;
            return Convert.FromBase64String(audioContent.ToString()); // Make sure to convert to string if necessary
        }
    }
}
