# %%
import os
import re
import spacy
import fitz  # PyMuPDF
import easyocr
import docx2txt
# import pandas as pd
from datetime import datetime
import datetime

from dateutil.relativedelta import relativedelta
from datetime import datetime

# %%
def pdf_to_text(pdf_path, txt_output_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Initialize an empty string for the extracted text
    text = ""
    
    # Loop through the pages and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")  # Extract text in plain text format

    # Write the extracted text to a .txt file
    with open(txt_output_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    
    # Close the PDF file
    pdf_document.close()

    print(f"Text extracted and saved to {txt_output_path}")
    
    # Return the extracted text so it can be used later
    return text

def jpg_to_text(jpg_path, txt_output_path):
       # Initialize the reader for Romanian language
    reader = easyocr.Reader(['ro'])
    
    # Perform OCR on the image
    results = reader.readtext(jpg_path)
    
    # Extract the text from the OCR results
    text = "\n".join([res[1] for res in results])  # res[1] contains the recognized text
    
    # Write the extracted text to a .txt file
    with open(txt_output_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    
    print(f"Text extracted and saved to {txt_output_path}")
    
    return text

def docx_to_text(docx_path, txt_output_path):
    # Process the docx file and extract text
    text = docx2txt.process(docx_path)
    
    # Write the extracted text to the output .txt file
    with open(txt_output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(text)
    
    return text    


# %%
# Function to read both txt and pdf files by checking the file's extension
def read_file(file_path):
    
    # Check file extension
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        # For text files, simply read and return the content
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    elif ext == '.pdf':
        # For PDFs, extract text using pdf_to_text and save it to a .txt file
        txt_output_path = os.path.splitext(file_path)[0] + '.txt'  # Replace .pdf with .txt
        return pdf_to_text(file_path, txt_output_path)  # Return the extracted text
    
    elif ext == '.jpg':
        txt_output_path = os.path.splitext(file_path)[0] + '.txt'
        return jpg_to_text(file_path, txt_output_path)
    
    elif ext == 'docx':
        txt_output_path = os.path.splitext(file_path)[0] + 'txt'
        return docx_to_text(file_path, txt_output_path)
    else:
        return "File could not be read because the format is unsupported"


# %%
# Keywords
# Create dictionary for ages
varste = {
    '18-25' : (18, 25),
    '26-30' : (26, 30),
    '31-35' : (31, 35),
    '36-40' : (36, 40),
    '41-45' : (41, 45),
    '46-50' : (46, 50),
    '51-55' : (51, 55),
    '56-60' : (56, 60)
}

pozitii = [
    'Agent', 'Programator', 'Event Manager', 'Specialist',
    'Manager', 'Reprezentant', 'Consultant', 'Controlor', 'Casier', 'Șofer',
    'Coordonator', 'Tehnolog', 'Contabil', 'Analist', 'Asistent','Operator','Lucrător',
    'Tehnician','Inginer','Muncitor','Vânzător'
]

domeniu = ['Event', 'Marketing', 'Resurse Umane', 'Vânzări', 'Vin', 'Bere', 'Financiar', 'Relatii Clienți',
           'Producție', 'Mașini', 'Îmbuteliere', 'IT', 'Recrutare', 'Logistică', 'Mentenanță', 'HR']

competente = [
    'Python', 'Java', 'Management de proiect', 'Învățare automată', 'Deep Learning',
    'Analiză de date', 'Leadership', 'Munca în echipă', 'Agile', 'Scrum', 'Cloud Computing',
    'AWS', 'Azure', 'SQL', 'React', 'JavaScript', 'HTML', 'CSS', 'Marketing',
    'Marketing digital', 'SEO', 'Creare de conținut', 'Public Speaking', 'Analiză financiară',
    'Bugetare', 'Managementul timpului', 'Rezolvarea problemelor', 'Comunicare',
    'Vizualizarea datelor', 'Design grafic', 'Serviciu pentru clienți', 'Salesforce',
    'Google Analytics', 'DevOps', '1C', 'Excel', 'Word', 'PowerPoint', 'Jira', 'Trello'
]

studii = {
    'licență' : 'licențiat',
    'liceu' : 'bacalaureat',
    'masterat' : 'masterat',
    'doctorat' : 'doctorat',
    'colegiu' : 'colegiu'
}

sex = ['bărbat', 'femeie']

limbi = ['română', 'rusă', 'engleză', 'germană', 'franceză', 'ucraineană', 'turcă', 'italiană', 'spaniolă', 'găgăuză', 'poloneză', 'cehă', 'slovacă', 'ungară']

permis_de_conducere = {
    'Categoria' : ['A', 'B', 'C', 'D']
}

experienta_dist = {
    "Începător": {"ani_minimi": 0, "ani_maximi": 2},
    "Junior": {"ani_minimi": 1, "ani_maximi": 3},
    "Mediu": {"ani_minimi": 3, "ani_maximi": 5},
    "Senior": {"ani_minimi": 5, "ani_maximi": 10},
    "Lider/Management": {"ani_minimi": 8, "ani_maximi": 15},
    "Executiv": {"ani_minimi": 15, "ani_maximi": None}  # None pentru fără limită superioară
}
experienta_dist_lista = [
    ("Începător", 0, 2),
    ("Junior", 1, 3),
    ("Mediu", 3, 5),
    ("Senior", 5, 10),
    ("Lider/Management", 8, 15),
    ("Executiv", 15, None)  # None pentru fără limită superioară
]
experienta_totala = {
    '0-1' : (0,1),
    '1-3' : (1,3),
    '3-5' : (3,5),
    '5-10' : (5,10),
    '10-15' : (10,15),
    '15+' : (15,None)
}

# %%
patterns = {
        'Nume': re.compile(r'Nume:', re.IGNORECASE | re.DOTALL),
        'Vârstă': re.compile(r'Vârstă:', re.IGNORECASE | re.DOTALL),
        'Sex': re.compile(r'Sex:', re.IGNORECASE | re.DOTALL),
        'Stare Civilă': re.compile(r'Stare Civilă:', re.IGNORECASE | re.DOTALL),
        'Experiență Profesională': re.compile(r'Experiență Profesională:(.*?)(?=Educație:)', re.IGNORECASE | re.DOTALL),
        'Educație': re.compile(r'Educație:', re.IGNORECASE | re.DOTALL),
        'Limbi Străine': re.compile(r'Limbi Străine:', re.IGNORECASE | re.DOTALL),
        'Competențe': re.compile(r'Competențe:', re.IGNORECASE),   }

# %%
def segmentation(content):
    # Define patterns for different sections of the CV
    # Initialize a list to store segments
    matches = []

    # Iterate over the patterns and find matches for each section
    for section, pattern in patterns.items():
        section_matches = list(pattern.finditer(content))
        matches.extend(section_matches)  # Add the found matches to the main list

    # Initialize a list to store segments
    segments = []

    # Process the matches and extract content between sections
    for i in range(len(matches) - 1):
        segment_name = matches[i].group()
        start_index = matches[i].end()
        end_index = matches[i + 1].start()
        
        segment_content = content[start_index:end_index].strip()
        segments.append((segment_name, segment_content))

    # Handle the last segment after the last match
    if matches:
        last_segment_name = matches[-1].group()
        last_segment_content = content[matches[-1].end():].strip()
        segments.append((last_segment_name, last_segment_content))

    # Print the segments
    #for i, (name, segment) in enumerate(segments):
        #print(f"Segment {i + 1} - {name}")
        #print(segment)

# %%
def exp_def(content):
    experience = patterns['Experiență Profesională'].findall(content)
    def job_title_matches(experience):
        experience = ' '.join(experience)
 # Regex patterns to match job positions and domains
        pozitii_pattern = '|'.join(pozitii)
        domenii_pattern = '|'.join(domeniu)
        job_pattern = rf'{pozitii_pattern}\s*?{domenii_pattern}'

    # Find all job experience matches in the content
        job_matches = re.findall(job_pattern, experience)

    # Print found job matches
        print(job_matches)
    job_title_matches(experience)
    period_pattern = re.compile(r'Perioadă:\s*(\d{4})\s*-\s*(\d{4}|prezent)', re.IGNORECASE)

    matches = period_pattern.findall(experience[0])
    job_durations = []

# Function to determine experience level
    def determine_experience_level(job_duration):
        for level, min_years, max_years in experienta_dist_lista:
            if max_years is None:  # For "Executiv" with no upper limit
                if job_duration >= min_years:
                    return level
            elif min_years <= job_duration < max_years:
                return level
        return "Unknown" 

# Iterate through the matches and calculate job durations
    for i, match in enumerate(reversed(matches), start=1):
        start_year, end_year = match
    
    # Convert start_year to a datetime object
        start_date = datetime(year=int(start_year), month=1, day=1)

    # Handle the "prezent" case
        if end_year == "prezent":
            end_date = datetime.now()  
        else:
            end_date = datetime(year=int(end_year), month=1, day=1)

        job_duration = relativedelta(end_date, start_date).years
        job_durations.append(job_duration)
    
    # Experience level
        experience_level = determine_experience_level(job_duration)

# Total experience after the loop
    total_experience = sum(job_durations)

# Print total experience
    print(f"Total Experience: {total_experience} ani") 

# %%
def kword_finder(content, user_input):
    # Tokenization
    content = content.replace("\n", "").replace("\t", "")
    nlp = spacy.load('ro_core_news_lg')

    doc = nlp(content)
    tokens = [token.text for token in doc]

    possible_keywords = (varste, pozitii, domeniu, competente, studii, sex, limbi, permis_de_conducere)

    all_possible_keywords = []

    for item in possible_keywords:
        if isinstance(item, dict):
            all_possible_keywords.extend(item.keys())  # Add dictionary keys (if needed)
            all_possible_keywords.extend(item.values())  # Add dictionary values
        elif isinstance(item, list):
            all_possible_keywords.extend(item)
        elif isinstance(item, tuple):
            all_possible_keywords.extend(item)

    # Create the 'keywords' list by selecting words present in 'all_possible_keywords' (case-insensitive match)
    keywords = [word for word in all_possible_keywords if isinstance(word, str) and word.lower() in [input_word.lower() for input_word in user_input]]

    print(f'Cuvintele cheie introduse: {keywords}')

    keyword_match = []
    matched_keywords = set()  # A set to keep track of already matched keywords

    # Find matches in the tokens
    for token in tokens:
        for keyword in keywords:
            if token.lower() == keyword.lower() and keyword not in matched_keywords:
                keyword_match.append(keyword)
                matched_keywords.add(keyword)  # Mark the keyword as found
                break  # Move to the next token after a match is found

    return tokens, keywords, keyword_match


# %%
def varste_cat(content):

    # Example regex to match ages (you may need to refine this pattern)
    age_pattern = re.compile(r'\b\d{1,2}\b')  # Matches ages from 0 to 99
    ages = age_pattern.findall(content)

    for age_str in ages:
        age = int(age_str)  # Convert to integer
        if 18 <= age <= 25:
            varste['18-25'].append(age)
        elif 26 <= age <= 30:
            varste['26-30'].append(age)
        elif 31 <= age <= 35:
            varste['31-35'].append(age)
        elif 36 <= age <= 40:
            varste['36-40'].append(age)
        elif 41 <= age <= 45:
            varste['41-45'].append(age)
        elif 46 <= age <= 50:
            varste['46-50'].append(age)
        elif 51 <= age <= 55:
            varste['51-55'].append(age)
        elif 56 <= age <= 65:
            varste['56-65'].append(age)
        else:
            varste['66+'].append(age)

    return varste


# %%
# Directory path
folder_path = '/Users/valeriacabac/Desktop/try2/new2'
cv_match = {}

# User-provided keywords (for example, this could be taken from input)
user_input = input("Enter keywords separated by commas: ").split(',')

    # Strip whitespace from the user's input
user_input = [word.strip() for word in user_input]
    
# Iterate through all files in the directory
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # Skip hidden system files
    if filename.startswith('.'):
        continue
    # Check if it's a file (not a directory)
    if os.path.isfile(file_path):
        print(f'Processing file: {file_path}')
        content = read_file(file_path)
        content = content.replace("•", "").replace("Abilități", "Competențe")
        segmentation(content)
        exp_def(content)

        tokens, keywords, keyword_match = kword_finder(content, user_input)

        keyword_count = len(keyword_match)  # Number of matched keywords
        total_keywords = len(keywords)      # Total keywords looked up

        if keyword_count > 0:
            # Calculate percentage of matched keywords
            percentage_matched = (keyword_count / total_keywords) * 100 if total_keywords > 0 else 0
            cv_match[filename] = {
                'keyword_count': keyword_count,
                'percentage_matched': percentage_matched,
                'matched_keywords': keyword_match
            }

        # Extract ages and categorize
        # varste = varste_cat(content)  # This will call the function and categorize ages
        # print(f'Ages categorized from {filename}: {varste}')

# Print results
print("\nCV-uri cu cuvinte cheie prezente:")
for cv, info in cv_match.items():
    print(f"{cv}: {info['keyword_count']} cuvinte cheie găsite, {info['percentage_matched']:.2f}% potrivire. Cuvinte cheie: {info['matched_keywords']}")



