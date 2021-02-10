import re
import subprocess
from datetime import datetime

from config import CLASSPATH, ORACLE_BASE_URL, ORACLE_USERNAME, \
    ORACLE_PASSWORD, ORACLE_POLICY


def upload_fbdi_csv_to_ucm(file_name):
    print(f'upload process started at: {datetime.now()}')
    process = subprocess.Popen(
        ['java', '-classpath', CLASSPATH,
         'oracle.ucm.idcws.client.UploadTool',
         f'-url={ORACLE_BASE_URL}',
         f'-username={ORACLE_USERNAME}', f'-password={ORACLE_PASSWORD}',
         f'-policy={ORACLE_POLICY}',
         f'-primaryFile={file_name}',
         '-dDocAccount=fin/generalLedger/import'],
        stdout=subprocess.PIPE
    )
    byte_output, err = process.communicate()
    output = byte_output.decode('utf-8')
    if process.returncode != 0:
        error_message = 'an error occurred while uploading the file to UCM'
        if 'Error ' in output:
            error_index = output.index('Error ')
            error_message = output[error_index:]
        raise Exception(error_message)

    print(f'upload process completed at: {datetime.now()}')
    response = re.findall('\[(.*)(?=\])', output)
    d_id = None
    d_doc_name = None
    if response:
        response_list = response[0].split('|')
        d_id = response_list[0].split('=')[1]
        d_doc_name = response_list[1].split('=')[1]
    return d_id, d_doc_name


if __name__ == '__main__':
    # file = '/home/bharath/Downloads/axis1_gl_journal_composite.csv'
    file = '/home/bharath/Downloads/MOCK_DATA.zip'
    ucm_id, doc_name = upload_fbdi_csv_to_ucm(file)
    print(f'dID is: {int(ucm_id)} and dDocName is : {str(doc_name)}')
