import pymysql.cursors
import requests

# Loading legacy accessions from file
legacy_file = "legacy_final_list.csv"
legacy_list = {}
with open(legacy_file, "r") as fh:
    for line in fh:
        ln = line.rstrip().split(',')
        if ln[3].startswith("ERZ") and ln[4].startswith("ERZ"):
            legacy_list[ ln[3] ] = ln[4]

# Connect to the database
connection = pymysql.connect(host='HOST',
                             user='USER',
                             password='PASSWORD',
                             port=PORT,
                             database='emg_backlog_2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def getLastUpdate(acc):
    url = 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=' + acc + '&fields=last_updated&format=json&result=analysis'
    res = requests.get(url)
    d = res.json()
    if 'last_updated' in d[0]:
        return d[0]['last_updated']
    else:
        return None

with connection:
    with connection.cursor() as cursor:
        for old_acc in legacy_list:
            new_acc = legacy_list[old_acc]
            new_date = getLastUpdate(new_acc)

            print("Processing {} - {}".format(old_acc, new_acc))

            # Read assembly record from Assembly table
            search_assembly = "SELECT * FROM Assembly WHERE primary_accession=%s"
            cursor.execute(search_assembly, (old_acc,))
            data = cursor.fetchone()

            # Update old assembly to be Legacy
            try:
                update_assembly = "UPDATE Assembly SET assembly_type_id=6 WHERE primary_accession=%s"
                cursor.execute(update_assembly, (old_acc,))
                connection.commit()
            except:
                print("cannot set assembly_type_id for {}".format(old_acc))

            # Create new assembly record
            try:
                insert_assembly = "INSERT INTO Assembly (primary_accession, study_id, ena_last_update, public, biome_id, inferred_biome_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_assembly, (new_acc, data['study_id'], new_date, data['public'], data['biome_id'], data['inferred_biome_id'],))
                connection.commit()
            except:
                print("cannot insert new assembly {}".format(new_acc))

            # Get new id for new assembly
            search_id = "SELECT id FROM Assembly WHERE primary_accession=%s"
            cursor.execute(search_id, (new_acc,))
            new_id = cursor.fetchone()

            # Search Run Id linked to the old assembly
            search_run = "SELECT run_id FROM RunAssembly WHERE assembly_id=%s"
            cursor.execute(search_run, (data['id'],))
            run_id = cursor.fetchone()

            # Insert new link between Run Id and New Assembly
            try:
                insert_run_link = "INSERT INTO RunAssembly (assembly_id, run_id) VALUES (%s, %s)"
                cursor.execute(insert_run_link, (new_id['id'], run_id['run_id'],))
                connection.commit()
            except:
                print("cannot link assembly and run {}".format(new_id['id']))

            # Search old assembly job data
            search_job = "SELECT * FROM AssemblyJob WHERE new_ena_assembly=%s"
            cursor.execute(search_job, (old_acc,))
            job = cursor.fetchone()

            # Create new assemblyjob
            try:
                insert_job = "INSERT INTO AssemblyJob (input_size, reason, priority, uploaded_to_ena, new_ena_assembly, assembler_id, result_id, status_id, submission_id, directory, estimated_peak_mem, requester_id, request_id, bam_uploaded) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_job, (job['input_size'], job['reason'], job['priority'], job['uploaded_to_ena'], new_acc, job['assembler_id'], job['result_id'], job['status_id'], job['submission_id'], job['directory'], job['estimated_peak_mem'], job['requester_id'], job['request_id'], job['bam_uploaded'],))
                connection.commit()
            except:
                print("cannot insert new assembly job for {}".format(new_acc))