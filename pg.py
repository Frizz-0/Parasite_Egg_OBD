import psycopg2
import os
import json

conn = psycopg2.connect(host = 'localhost', password='6999', dbname = 'postgres', user = 'postgres')

cur = conn.cursor()
def add_tables_pg():
    # Drop tables if they exist (in reverse order due to foreign keys)
    cur.execute('''DROP TABLE IF EXISTS parasite_app.species CASCADE''')
    cur.execute('''DROP TABLE IF EXISTS parasite_app.treatments CASCADE''')
    cur.execute('''DROP TABLE IF EXISTS parasite_app.taxonomy CASCADE''')

    cur.execute('''CREATE SCHEMA IF NOT EXISTS parasite_app''')

    cur.execute('''CREATE TABLE IF NOT EXISTS parasite_app.taxonomy (
                taxonomy_id SERIAL PRIMARY KEY,
                kingdom VARCHAR(50),
                phylum VARCHAR(50),
                class VARCHAR(50),
                family VARCHAR(50),
                order_rank VARCHAR(50)
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS parasite_app.treatments (
                treatments_id SERIAL PRIMARY KEY,
                drug_name VARCHAR(100) NOT NULL,
                dosage_instruction TEXT,
                notes TEXT
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS parasite_app.species(
                species_id SERIAL PRIMARY KEY,
                scientific_name VARCHAR(50) UNIQUE NOT NULL,
                common_name VARCHAR(50),
                habitat TEXT,
                description TEXT,
                taxonomy_id INT REFERENCES parasite_app.taxonomy(taxonomy_id),
                treatments_id INT REFERENCES parasite_app.treatments(treatments_id)
                )''')
    conn.commit()
    cur.close()
    conn.close()
    


def add_new_parasite(species_data, tax_data, treat_data):

    cur = conn.cursor()
    try:
        cur.execute(""" 
        INSERT INTO parasite_app.taxonomy(kingdom,phylum,class, family,order_rank)
        VALUES(%s,%s,%s,%s,%s ) RETURNING taxonomy_id;""",(tax_data['kingdom'], tax_data['phylum'],tax_data['class'], tax_data['family'], tax_data['order']))

        tax_id = cur.fetchone()[0]

        cur.execute(""" 
        INSERT INTO parasite_app.treatments(drug_name, dosage_instruction, notes)
        VALUES(%s,%s,%s ) RETURNING treatments_id;""",(treat_data['drug'], treat_data['dosage'],treat_data['notes']))

        treat_id = cur.fetchone()[0]

        cur.execute(""" 
        INSERT INTO parasite_app.species(scientific_name,common_name, habitat, description, taxonomy_id, treatments_id)
        VALUES(%s,%s,%s,%s,%s,%s ) ;
        """,(species_data['name'],species_data['common'],species_data['habitat'], species_data['desc'],tax_id,treat_id))

        conn.commit()

        print(f"Successfully added {species_data['name']} to the database!") 

    except Exception as e:
        conn.rollback()
        print(f'error {e}')

    finally:
        cur.close()
        conn.close()

# add_tables_pg()

species = {'name': 'Ascaris lumbricoides', 'common': 'Giant Roundworm', 'habitat': 'Soil', 'desc': 'Large nematode'}
taxanomy = {'kingdom':'Animalia','phylum': 'Nematoda', 'class': 'Chromadorea','family': 'Ascarididae', 'order': 'Rhabditida'}
treatments = {'drug': 'Albendazole', 'dosage': '400mg single dose', 'notes': 'Standard WHO treatment'}

# add_new_parasite(species,taxanomy,treatments)

def get_parasite_details(name):
    
    query = '''
    SELECT s.description, s.scientific_name,s.common_name, s.habitat, t.kingdom, t.phylum, t.class, t.order_rank, t.family, tr.drug_name, tr.dosage_instruction
    FROM parasite_app.species s
    JOIN parasite_app.taxonomy t ON s.taxonomy_id = t.taxonomy_id
    JOIN parasite_app.treatments tr ON s.treatments_id = tr.treatments_id
    WHERE s.scientific_name = %s;

    '''

    cur.execute(query,(name,))
    result = cur.fetchone()

    if result:
        # print(f"--- Medical Report for {result[0]} ---")
        # print(f"Taxonomy: {result[1]}")
        # print(f"Treatment: {result[2]} ({result[3]})")
        # print(result)
        print(f"(Species)\nName: {result[1]}\nCommonly Called: {result[2]}\nFound in: {result[3]}\n")
        print(f"(Taxonomy)\nKingdom: {result[4]}\nPhylum: {result[5]}\nClass: {result[6]}\nOrder: {result[7]}\nFamily: {result[8]}\n")
        print(f"(Treatment)\nTreatment : {result[9]} ({result[10]})\n")
        print(f"Description: {result[0]}")
    
    else:
        print("Parasite not found in database.")
    
    cur.close()
    conn.close()

# get_parasite_details('Ascaris lumbricoides')

def backup_table_to_csv(table_name, output_file):
    try:
        cur = conn.cursor()

        # 2. Define the 'Universal' CSV Export command
        # 'WITH CSV HEADER' ensures your column names are saved at the top
        sql = f"COPY parasite_app.{table_name} TO STDOUT WITH CSV HEADER"

        # 3. Stream the data directly to a file
        with open(output_file, 'w', encoding='utf-8') as f:
            cur.copy_expert(sql, f)

        print(f"✅ Success! {table_name} backed up to {output_file}")

    except Exception as e:
        print(f"❌ Error during backup: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

# --- Run the Backup ---
# This creates a 'backups' folder if it doesn't exist
# os.makedirs("backups", exist_ok=True)

# backup_table_to_csv("species", "backups/species_backup.csv")

def ingest_parasite_json(file_path):
    # 1. Load the JSON data
    with open(file_path, 'r') as f:
        parasites = json.load(f)

    try:
        for p in parasites:
            # --- STEP A: Insert Taxonomy & Get ID ---
            cur.execute("""
                INSERT INTO parasite_app.taxonomy (kingdom,phylum, class, order_rank, family)
                VALUES (%s, %s, %s, %s, %s) RETURNING taxonomy_id;
            """, (p['taxonomy']['kingdom'],p['taxonomy']['phylum'], p['taxonomy']['class'], 
                  p['taxonomy']['order'], p['taxonomy']['family']))
            tax_id = cur.fetchone()[0]

            # --- STEP B: Insert Treatment & Get ID ---
            cur.execute("""
                INSERT INTO parasite_app.treatments (drug_name, dosage_instruction, notes)
                VALUES (%s, %s, %s) RETURNING treatments_id;
            """, (p['medical_info']['treatment'], p['medical_info']['dosage'], "Imported via JSON"))
            treat_id = cur.fetchone()[0]

            # --- STEP C: Insert Species using the new IDs ---
            cur.execute("""
                INSERT INTO parasite_app.species 
                (scientific_name, common_name, habitat, description, taxonomy_id, treatments_id)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (p['species_name'], p['common_name'], p['medical_info']['habitat'], 
                  p['description'], tax_id, treat_id))

        # 3. Permanent Save
        conn.commit()
        print(f"✅ Success! {len(parasites)} parasites imported with all links.")

    except Exception as e:
        conn.rollback() # If any error happens, undo EVERYTHING
        print(f"❌ Error during import: {e}")

    finally:
        cur.close()
        conn.close()

# Run the ingestion

if __name__=='__main__':

    # add_tables_pg()
    # add_new_parasite(species,taxanomy,treatments)
    get_parasite_details('Ascaris lumbricoides')
 
    # ingest_parasite_json(r'data\species_data.json')

    # backup_table_to_csv("species", "backups/species_backup.csv")
