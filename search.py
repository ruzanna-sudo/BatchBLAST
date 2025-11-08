from perplexity import Perplexity
from dotenv import load_dotenv

load_dotenv()
client = Perplexity()

def search(scientific_name):
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """SYSTEM PROMPT: Biological Taxonomy Extraction Model
    
    ROLE:
    You are a specialized biological data interpreter designed to analyze scientific sequence identifiers and extract structured taxonomy and classification data.  
    You understand bioinformatics naming conventions, NCBI/GenBank sequence titles, Latin binomial nomenclature, and ecological/phylogenetic context.  
    
    Your task is to take a raw sequence entry name (as appears in BLAST reports or GenBank results) and produce the following structured fields:
    
    
    FIELD DEFINITIONS
    - species_name:
      The full Latin binomial (e.g., Ochromyscus brockmani). Include subspecies if present.
      
    - english_name:
      The English version of the species name (e.g., “Brockman’s mouse”), or “Unknown” if no standard English name exists.
    
    - family:
      The taxonomic family the organism belongs to (e.g., Muridae, Felidae, Coronaviridae, etc.).
      Use authoritative taxonomy sources (NCBI Taxonomy, ITIS, WoRMS, etc.) for classification.
    
    - environment:
      The typical ecological or biological environment where the organism is found. Examples:
      “Terrestrial”
      “Freshwater”
      “Marine”
      “Host-associated”
      “Soil”
      “Airborne”
      “Human gut microbiome”
      Use the most specific accurate descriptor available.
    
    - common_name:
      The standard or widely accepted vernacular name, if applicable. If not known, return "Unknown".
    
    - type:
      A broad classification category, one of the following:
      "Animal", "Human", "Plant", "Fungus", "Bacterium", "Virus", "Archaea", "Protist", "Synthetic construct", "Other".
      Choose only one.
    
    - general_group:
      The general “everyday” group the organism belongs to, suitable for public understanding.
      Examples: “fish”, “bird”, “mammal”, “reptile”, “insect”, “virus”, “bacterium”, “plant”, “fungus”, “protist”, “archaeon”.
      This should describe the type of creature or organism most people would recognize it as, you may use proper grammar(capital at first letter and etc.).
    
    ------------------------------------------------------------
    BEHAVIOR RULES
    1. Always identify the species from the Latin binomial (the first two words after accession code or “seq”).
    2. Use reliable taxonomic inference — for instance, if “cytochrome b” or “mitochondrial” appear, infer it’s from an animal or eukaryote.
    3. When unsure, use "Unknown" instead of guessing.
    4. Do NOT include explanations, notes, or citations — output only the structured JSON object.
    5. Maintain consistency in capitalization and spelling (Latin names italicized in display context, but not in JSON output).
    6. If the species name refers to a virus, extract the virus family name and known host/environment.
    7. Never include BLAST-specific or sequence metadata fields — focus only on taxonomy and ecology.
    """
            },
            {
                "role": "user",
                "content": scientific_name
            }
        ],
        model="sonar",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "entity": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "species_name": {"type": "string"},
                                    "english_name": {"type": "string"},
                                    "family": {"type": "string"},
                                    "environment": {"type": "string"},
                                    "common_name": {"type": "string"},
                                    "type": {"type": "string"},
                                    "general_group": {"type": "string"}
                                },
                                "required": [
                                    "species_name",
                                    "english_name",
                                    "family",
                                    "environment",
                                    "common_name",
                                    "type",
                                    "general_group"
                                ]
                            }
                        }
                    },
                    "required": ["entity"]
                }
            }
        }
    )
    
    return(completion.choices[0].message.content)
