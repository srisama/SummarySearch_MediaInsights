using Microsoft.AspNetCore.Mvc.Rendering;

namespace QueryCast
{
    public class MediaFile
    {
        public string? Filename { get; set; }
        public string? Filetype { get; set; }
        public string? Category { get; set; }
        public string? Transcript { get; set; }
        public string? EnhancedTranscript { get; set; }
     
        public string? Summary { get; set; }
        public double? Score { get; set; }
        public List<double>? ContentVector { get; set; }
    }

    public class MediaSearchViewModel
    {
        public List<MediaFile> MediaFiles { get; set; } = new List<MediaFile>();
        public string? UserQuestion { get; set; }
        public List<string>? Categories { get; set; }
        public string? SelectedCategory { get; set; }
        public SelectList? CategorySelectList { get; set; }  // Add this property
        public string? Answer { get; set; }
    }


}
