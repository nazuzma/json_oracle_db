import os
import crypto as cr
import uuid
import cx_Oracle

username = 'lda5148'
password = cr.decrypt(cr.lda5148_gds187)


dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ora')
dsn = dsn_tns
port = 1521
encoding = 'UTF-8'

# here fix the length of columns from json
a_ccsd_column = 139
b_tests_column = 31
c_components_column = 9
d_reinforcements_column = 14
e_indicators_column = 46
appendix_fp_column = 16
appendix_rr_column = 5

connection_string = 'oracle://{user}:{password}@{sid}'.format(
    user=username,
    password=password,
    sid=dsn_tns
)


def generate_uuid():
    return str(uuid.uuid4())


table_spec = {
    # '[TABLE_NAME]': {
    #   'number_of_columns': [Number of columns in the data table],
    #   'primary_key_column': [Primary column ID in the data table],
    #   'link_back_key_column': [Column hosting the natural key column] ,
    #   'parent_key_column': [Parent's primary key ID],
    #   'parent_link_back_key_column': [Parent's natural key column],
    # },
    'A_CCSD': {
        'number_of_columns': a_ccsd_column,
        'primary_key_column': 'A_CCSD_ID',
        'link_back_key_column': 'CRD-revision-side ID',
        'parent_key_column': 'A_CCSD_ID',
        'parent_link_back_key_column': 'CRD-revision-side ID',
    },
    'B_TESTS': {
        'number_of_columns': b_tests_column,
        'primary_key_column': 'B_TESTS_ID',
        'link_back_key_column': 'Test ID',
        'parent_key_column': 'A_CCSD_ID',
        'parent_link_back_key_column': 'CRD-revision-side ID',
    },
    'C_COMPONENTS': {
        'number_of_columns': c_components_column,
        'primary_key_column': 'C_COMPONENTS_ID',
        'link_back_key_column': 'Test-component ID',
        'parent_key_column': 'B_TESTS_ID',
        'parent_link_back_key_column': 'Test ID',
    },
    'D_REINFORCEMENTS': {
        'number_of_columns': d_reinforcements_column,
        'primary_key_column': 'D_REINFORCEMENTS_ID',
        'link_back_key_column': 'Test-component ID',
        'parent_key_column': 'B_TESTS_ID',
        'parent_link_back_key_column': 'Test ID',
    },
    'E_INDICATORS': {
        'number_of_columns': e_indicators_column,
        'primary_key_column': 'E_INDICATORS_ID',
        'link_back_key_column': 'Test-load-pressure ID',
        'parent_key_column': 'B_TESTS_ID',
        'parent_link_back_key_column': 'Test ID',
    },
    'APPENDIX_FP': {
        'number_of_columns': appendix_fp_column,
        'primary_key_column': 'APPENDIX_FP_ID',
        'link_back_key_column': 'Test-load-pressure-rib ID',
        'parent_key_column': 'E_INDICATORS_ID',
        'parent_link_back_key_column': 'Test-load-pressure ID',
    },
    'APPENDIX_RR': {
        'number_of_columns': appendix_rr_column,
        'primary_key_column': 'APPENDIX_RR_ID',
        'link_back_key_column': 'Test-load-pressure-component ID',
        'parent_key_column': 'E_INDICATORS_ID',
        'parent_link_back_key_column': 'Test-load-pressure ID',
    },
    'A_CCSD_EXTRA': {
        'primary_key_column': 'A_CCSD_EXTRA_ID',
    },
    'B_TESTS_EXTRA': {
        'primary_key_column': 'B_TESTS_EXTRA_ID',
    },
    'C_COMPONENTS_EXTRA': {
        'primary_key_column': 'C_COMPONENTS_EXTRA_ID',
    },
    'D_REINFORCEMENTS_EXTRA': {
        'primary_key_column': 'D_REINFORCEMENTS_EXTRA_ID',
    },
    'E_INDICATORS_EXTRA': {
        'primary_key_column': 'E_INDICATORS_EXTRA_ID',
    },
    'APPENDIX_FP_EXTRA': {
        'primary_key_column': 'APPENDIX_FP_Extra_ID',
    },
    'APPENDIX_RR_EXTRA': {
        'primary_key_column': 'APPENDIX_RR_EXTRA_ID',
    },
}


def get_table_total_cols(table_name):
    """Returns the total number of columns in each table of JSON"""
    return table_spec[table_name]['number_of_columns']


def get_table_primary_key(table_name):
    """Returns the primary key associated to each table of JSON"""
    return table_spec[table_name]['primary_key_column']


def get_table_link_back_key(table_name):
    """Returns the foreign key of each table of JSON"""
    return table_spec[table_name]['link_back_key_column']


def get_parent_table_primary_key(table_name):
    """Returns the primary key of main tables from DB"""
    return table_spec[table_name]['parent_key_column']


def get_parent_link_back_key(table_name):
    """Returns the parent's natural key column"""
    return table_spec[table_name]['parent_link_back_key_column']


def get_key_by_value(dict_of_elements, value_to_find):
    try:
        for key, value in dict_of_elements.items():
            if value == value_to_find:
                return key
    except KeyError:
        print('seems no key value pair', KeyError)


def get_connection_string():
    return "%s/%s@%s" % (username, password, dsn)  # connection format username/password@oracleServer


# on windows there was problem of oracle instant client so we set up manually path
def set_oracle_instant_client_location():
    LOCATION = r"C:\app\instantclient_19_5"
    # print("ARCH:", platform.architecture())
    # print("FILES AT LOCATION:")
    # for name in os.listdir(LOCATION):
    # print(name)
    os.environ["PATH"] = LOCATION
