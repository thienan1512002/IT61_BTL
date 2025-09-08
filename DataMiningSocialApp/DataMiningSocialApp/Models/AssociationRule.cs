namespace DataMiningSocialApp.Models
{
    public class AssociationRule
    {
        public List<string>? LHS { get; set; }
        public List<string>? RHS { get; set; }
        public double Support { get; set; }
        public double Confidence { get; set; }
        public double Lift { get; set; }
        public string Algorithm { get; set; } = "Apriori"; // Default to Apriori
    }
}
