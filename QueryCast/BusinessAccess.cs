using MySql.Data.MySqlClient;
using System.Text.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using QueryCast;
using Newtonsoft.Json;
using System.Text;

namespace QueryCast
{
    public class BusinessAccess
    {
                                                  
        private string connectionString = "{insert connection string}";

        public MySqlConnection GetDatabaseConnection()
        {
            return new MySqlConnection(connectionString);
        }

        public async Task<List<double>> GenerateQuestionEmbedding(string? questionText, string model = "text-embedding-ada-002")
        {
            using var httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Add("Authorization", "Bearer {insert open AI Api key}");

            var response = await httpClient.PostAsync(
                $"https://api.openai.com/v1/embeddings",
                new StringContent(System.Text.Json.JsonSerializer.Serialize(new { model = model, input = questionText }), System.Text.Encoding.UTF8, "application/json"));

            var content = await response.Content.ReadAsStringAsync();
            var jsonElement = JsonDocument.Parse(content).RootElement;
            var embedding = jsonElement.GetProperty("data")[0].GetProperty("embedding").Deserialize<List<double>>();

            return embedding;
        }

       
        public List<MediaFile> FetchAllEntries(List<float> questionEmbedding, double threshold = 0.8)
        {
            List<MediaFile> similarEntries = new List<MediaFile>();
            try
            {
                using (var connection = new MySqlConnection(connectionString))
                {
                    connection.Open();
                    string embeddingsJson = JsonConvert.SerializeObject(questionEmbedding);

                    string sql = $@"
            SELECT filename, filetype, category, transcript, summary, enhancedTranscript,
                   (dot_product(contentVector, JSON_ARRAY_PACK('{embeddingsJson}'))) AS score
            FROM MediaFile
            ORDER BY score DESC LIMIT 1";

                    using (var command = new MySqlCommand(sql, connection))
                    {
                        using (var reader = command.ExecuteReader())
                        {
                            while (reader.Read())
                            {
                                var mediaFile = new MediaFile
                                {
                                    Filename = reader.GetString(reader.GetOrdinal("filename")),
                                    Filetype = reader.GetString(reader.GetOrdinal("filetype")),
                                    Category = reader.GetString(reader.GetOrdinal("category")),
                                    Transcript = reader.GetString(reader.GetOrdinal("transcript")),
                                    EnhancedTranscript = reader.GetString(reader.GetOrdinal("enhancedTranscript")),
                                    Summary = reader.GetString(reader.GetOrdinal("summary")),
                                    Score = reader.GetDouble(reader.GetOrdinal("score"))
                                };
                                similarEntries.Add(mediaFile);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                // Handle exception
            }
            return similarEntries;
        }

        public List<MediaFile> FetchEntriesByCategoryAndScore(List<float> questionEmbedding, string category, double threshold = 0.8)
        {
            List<MediaFile> similarEntries = new List<MediaFile>();
            
            try
            {
                using (var connection = new MySqlConnection(connectionString))
                {
                    connection.Open();
                    string embeddingsJson = JsonConvert.SerializeObject(questionEmbedding);

                    string sql = $@"
                    SELECT filename, filetype, category, transcript, summary, 
                           (dot_product(contentVector, JSON_ARRAY_PACK('{embeddingsJson}'))) AS score
                    FROM MediaFile
                    WHERE category = @category
                    ORDER BY score DESC";

                    using (var command = new MySqlCommand(sql, connection))
                    {
                        command.Parameters.AddWithValue("@category", category);
                        using (var reader = command.ExecuteReader())
                        {
                            while (reader.Read())
                            {
                                var mediaFile = new MediaFile
                                {
                                    Filename = reader.GetString(reader.GetOrdinal("filename")),
                                    Filetype = reader.GetString(reader.GetOrdinal("filetype")),
                                    Category = reader.GetString(reader.GetOrdinal("category")),
                                    Transcript = reader.GetString(reader.GetOrdinal("transcript")),
                                    Summary = reader.GetString(reader.GetOrdinal("summary")),
                                    Score = reader.GetDouble(reader.GetOrdinal("score"))
                                };
                                similarEntries.Add(mediaFile);
                            }
                        }
                    }

                }
            }
            catch (Exception ex)
            {

            }
            return similarEntries;
        }


        public List<string> FetchCategories()
        {
            List<string> categories = new List<string>();
            try
            {
                using (var connection = new MySqlConnection(connectionString))
                {
                    connection.Open();
                    string sql = "SELECT DISTINCT category FROM MediaFile ORDER BY category";
                    using (var command = new MySqlCommand(sql, connection))
                    {
                        using (var reader = command.ExecuteReader())
                        {
                            while (reader.Read())
                            {
                                categories.Add(reader.GetString("category"));
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            return categories;
        }
        //New Code Implementation 
        public async Task<string> GetAnswerFromContext(string question, string context)
        {
            using var httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", "{insert open AI Api key}");

            var prompt = $"Answer the question based on the given context:\nContext: {context}\nQuestion: {question}";
            var data = new
            {
                model = "gpt-3.5-turbo-instruct",
                prompt = prompt,
                max_tokens = 150
            };

            var response = await httpClient.PostAsync(
                "https://api.openai.com/v1/completions",
                new StringContent(JsonConvert.SerializeObject(data), Encoding.UTF8, "application/json"));

            if (response.IsSuccessStatusCode)
            {
                var content = await response.Content.ReadAsStringAsync();
                var jsonElement = JsonDocument.Parse(content).RootElement;
                var answer = jsonElement.GetProperty("choices")[0].GetProperty("text").GetString();
                return answer;
            }
            else
            {
                var error = await response.Content.ReadAsStringAsync();
                throw new Exception($"Failed to retrieve answer from OpenAI: {error}");
            }
        }

       


        public async Task<string> GenerateAnswerFromTranscript(string question, string transcript)
        {
            using var httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", "{insert open AI Api key}");

            // Calculate the available tokens for the transcript
            int maxTranscriptTokens = 4000 - question.Length; // Adjust based on typical question length
            string shortenedTranscript = TruncateTranscript(transcript, maxTranscriptTokens); // Implement this method based on tokenization

            var prompt = $"Question: {question}\nTranscript: {shortenedTranscript}\nAnswer the question based strictly on the information available in the transcript. Do not infer or add information beyond what is provided.";
            var data = new
            {
                model = "gpt-3.5-turbo-instruct",
                prompt = prompt,
                max_tokens = 150
            };

            var response = await httpClient.PostAsync(
                "https://api.openai.com/v1/completions",
                new StringContent(JsonConvert.SerializeObject(data), Encoding.UTF8, "application/json"));

            var content = await response.Content.ReadAsStringAsync();
            var jsonElement = JsonDocument.Parse(content);
            if (jsonElement.RootElement.TryGetProperty("choices", out var choices) && choices.GetArrayLength() > 0)
            {
                var answer = choices[0].GetProperty("text").GetString();
                return answer;
            }
            else
            {
                return "No answer generated or an error occurred.";
            }
        }

        private string TruncateTranscript(string transcript, int maxTokens)
        {
            // Simple truncation logic (could be improved with actual tokenization)
            var words = transcript.Split(' ');
            var truncatedWords = words.Take(maxTokens).ToArray(); // This is an oversimplification
            return string.Join(" ", truncatedWords);
        }


    }

}
