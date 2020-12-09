import os
import db_config as config
from exceptions import UploadProcessException
from app import app
from fastnumbers import fast_real
from collections import namedtuple
# config.set_oracle_instant_client_location()  # we set location of oracle instant client,
import cx_Oracle

db_schema = app.config['DB_SCHEMA']
DBResSpec = namedtuple('DBResSpec', 'data data_link_back sql_inserts sql_updates id_map')


def get_connection():
    return cx_Oracle.connect(config.username, config.password, config.dsn, encoding=config.encoding)


def remove_extra_ccsd_rows_R(connection):
    sql_statement = "delete from {0}.A_CCSD Where A_CCSD_ID = ANY(Select A_CCSD_ID From {0}.A_CCSD Where \"Side\" = 'R' AND \"CRD-revision-side ID\" Not in (Select \"CRD-revision-side ID\" from  {0}.B_Tests ))".format(db_schema)
    execute_oracle_queries(connection, sql_statement)

def remove_extra_ccsd_rows_L(connection):
        sql_statement = "delete from {0}.A_CCSD Where A_CCSD_ID = ANY(Select A_CCSD_ID From {0}.A_CCSD Where \"Side\" = 'L' AND \"CRD\" Not in (Select \"CRD\" from  {0}.A_CCSD WHERE \"Side\" = 'R'))".format(db_schema)
        execute_oracle_queries(connection, sql_statement)


def get_test_id(connection, test_id):
    sql_statement = "select  B_TESTS_ID from {0}.B_TESTS where\"Test ID\"='{1}'".format(db_schema, test_id)
    try:
        # create a cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            while True:
                rows = cursor.fetchone()
                if not rows:
                    return 0
                else:
                    return 1
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not allocate sequence ID: {0}".format(e)) from e


def get_user_id(connection, uid):
    sql_statement = "select  B_TESTS_ID from {0}.B_TESTS where \"User\"='{1}'".format(db_schema, uid)
    try:
        # create a cursor
        with connection.cursor() as cursor:

            cursor.execute(sql_statement)
            while True:
                rows = cursor.fetchone()
                if not rows:
                    return 0
                else:
                    return 1
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not allocate sequence ID: {0}".format(e)) from e


def read_b_row_and_check_if_same_user(connection, rows):
    for i in range(0, len(rows)):
        first_value = str(rows[i][0])
        user_id = str(rows[i][2])
        if get_test_id(connection, first_value) == 1:
            if get_user_id(connection, user_id) == 0:
                #app.logger.info("user id doesn't match")
                raise UploadProcessException("user id doesn't match. You are not authorized to make these changes.")




def convert_number_or_into_string(str_input, col):
    """Optimizes the Data Types. If VARCHAR type is defined in SQL for any value, it saves the similar value by adding quotation marks.
    However, if not, then by default it's a Number. In the later case, if the value is NULL, convert it to 0 else save the number."""

    if (col == "CRD-revision-side ID") or (col == "CRD") or \
            (col == "CRD revision") or (col == "Folder name") or (col == "Symmetric") or (col == "Side") or (
            col == "User") or (col == "Origin") or (col == "Tire size") or \
            (col == "CTC revision") or (col == "ERD-ARD") or (col == "Design manual") or (col == "Design code") or \
            (col == "Rim flange protector") or (col == "Apex 3 layup") or (col == "Ply layu") or (
            col == "Flipper layup") or \
            (col == "Stiffener inside layup") or (col == "First chipper layup") or (col == "Toeguard layup") or (
            col == "Sidewall layup") or \
            (col == "Overlay layup") or (col == "Tread layup") or (col == "Bead configuration") or (col == "Type") or (
            col == "Description") or \
            (col == "Construction") or (col == "Material model") or (col == "DEW version") or (
            col == "Rolling surface") or (col == "Cooldown") or \
            (col == "Unit system") or (col == "Rim contour") or (col == "Test-component ID") or (
            col == "Component") or (col == "Compound") or (
            col == "Sample ID") or \
            (col == "Cord code") or (col == "Cord serial") or (
            col == "Treatment code") or \
            (col == "Test-load-pressure ID") or (col == "TD") or (
            col == "FP") or (col == "SR") or (col == "RR") or \
            (col == "FM") or (col == "COSTGV") or (col == "COSBO") or (col == "Groove contact") or (col == "Sipe contact") \
            or (col == "Test-load-pressure-component I") or (col == "Test-load-pressure-component I") or (col == "Test ID")\
            or (col == "Test path"):
        return "'" + str_input + "'"

    if str_input == 'null' or str_input == 'None':
        return 0
    elif str_input.isdigit() or (str_input.replace('.', '', 1).isdigit() and str_input.count('.') < 2) or (
            str_input.replace('-', '', 1).replace('.', '', 1).isdigit()):
        return fast_real(str_input)
    else:
        return "'" + str_input + "'"


def get_unique_id(connection):
    """Getting unique primary id from SQL"""
    sql_statement = 'select {0}.shared_sequence.nextval from dual'.format(db_schema)
    try:
        # create a cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            return int(cursor.fetchone()[0])
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not allocate sequence ID: {0}".format(e)) from e


def get_crd_id(connection, crd):
    """Getting unique primary id from SQL"""
    sql_statement = "select  A_CCSD_ID from {0}.A_CCSD where \"CRD-revision-side ID\"=\'{1}\'".format(db_schema, crd)
    try:
        # create a cursor
        with connection.cursor() as cursor:
            cursor.execute(sql_statement)
            while True:
                rows = cursor.fetchone()
                resp = 0
                if not rows:
                    resp = 0
                else:
                    resp = int(rows[0])
                #      app.logger.info('executed ' + sql_statement + 'response> ' + str(resp))
                return resp
    except cx_Oracle.Error as e:
        raise UploadProcessException("Could not find CCSD ID: {0}".format(e)) from e


def search_and_delete(connection, first_value):
    sql_statement = 'delete from {0}.B_TESTS where B_TESTS_ID=ANY(select B_TESTS_ID from {0}.B_TESTS where \"Test ID\"=\'{1}\')'.format(db_schema, first_value)
    execute_oracle_queries(connection, sql_statement)


def delete_a_extra_columns(connection, a_table_id):
    sql_statement = 'delete from {0}.A_CCSD_EXTRA where "A_CCSD_ID"={1}'.format(db_schema, a_table_id)
    execute_oracle_queries(connection, sql_statement)



def put_double_quote_if_space_between_col_name_and_length_30(col_name):

    """As the Oracle only allows maximum 30 characters for columns names, we limit the names of the columns to 30 from JSON"""

    str = col_name
    if len(col_name) > 30:
        return '"' + truncate_30_chars(str) + '"'
    return '"' + col_name + '"'


def get_cols(cols, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name_and_length_30(primary_key)
    parent_primary_key = config.get_parent_table_primary_key(table_name)
    if not table_name == 'A_CCSD':
        col_string += ",{0}".format(put_double_quote_if_space_between_col_name_and_length_30(parent_primary_key))
    for i in range(0, col_length):
        col_string += ',' + put_double_quote_if_space_between_col_name_and_length_30(str(cols[i]))
    return col_string + ')'


def get_col_list(cols, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_length = len(cols)
    col_list = []
    for i in range(0, col_length):
        col_list.append(put_double_quote_if_space_between_col_name_and_length_30(str(cols[i])))
    return col_list


def get_extra_cols(cols, allowed_col_length, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_list = []
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name_and_length_30(primary_key)
    parent_primary_key = config.get_parent_table_primary_key(table_name)
    if not table_name == 'A_CCSD':
        col_string += ",{0}".format(put_double_quote_if_space_between_col_name_and_length_30(parent_primary_key))
    for i in range(0, col_length):
        if i >= allowed_col_length:
            col_list.append(truncate_30_chars(str(cols[i])))
            continue
        col_string += ',' + put_double_quote_if_space_between_col_name_and_length_30(str(cols[i]))
    return col_string + ')', col_list


def get_extra_cols_a_table(cols, allowed_col_length, table_name):
    primary_key = config.get_table_primary_key(table_name)
    col_length = len(cols)
    col_string = '(' + put_double_quote_if_space_between_col_name_and_length_30(primary_key)
    for i in range(0, col_length):
        if i >= allowed_col_length:
            continue
        col_string += ',' + put_double_quote_if_space_between_col_name_and_length_30(str(cols[i]))
    return col_string + ')'


def read_all_rows_and_save_extra(connection, table_name, cols, rows, allowed_col_length, link_dict):
    sql_list = []
    id_map = dict()
    col_string, col_list = get_extra_cols(cols, allowed_col_length, table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    link_key = config.get_parent_link_back_key(table_name)
    link_back_key_index = cols.index(link_key)
    row_string = ''
    extra_row_string = []
    id_map_col = cols.index(config.get_table_link_back_key(table_name))
    for i in range(0, len(rows)):
        actual_row_cols = len(rows[i])
        uid = get_unique_id(connection)
        first_value = str(rows[i][0])
        link_back_fk_from_db = -1
        if table_name == 'B_TESTS':
            search_and_delete(connection, str(first_value))
            link_back_fk_from_db = get_crd_id(connection, str(rows[i][1]))

        link_back_value = str(rows[i][link_back_key_index])

        id_map[str(rows[i][id_map_col])] = uid
        dict_data.update({uid: first_value})
        dict_data_link_back.update({uid: link_back_value})
        row_string += 'INTO {0}.{1} {2} VALUES({3}'.format(db_schema, table_name, col_string, uid)
        if not table_name == 'A_CCSD':
            if link_back_fk_from_db != 0 and link_back_fk_from_db != -1:
                link_fk_key = link_back_fk_from_db
            else:
                link_fk_key = config.get_key_by_value(link_dict, link_back_value)

            row_string += ",{0}".format(link_fk_key)
        row_string += ",'{0}'".format(first_value)
        for j in range(1, actual_row_cols):
            if j >= allowed_col_length:
                statement = prepare_extra_column_sql(table_name, uid, str(cols[j]), str(rows[i][j]))
                extra_row_string.append(statement)
                continue
            val = convert_number_or_into_string(str(rows[i][j]), cols[j])
            row_string += ",{0}".format(val)
        row_string += ')'
        sql_list.append(row_string)  # save normal columns
        row_string = ''
    # iterate through all extra col
    for sql_stmt in extra_row_string:
        extraid = get_unique_id(connection)
        sql_list.append(sql_stmt.replace('REPLACE_ID', str(extraid)))
    return DBResSpec(dict_data, dict_data_link_back, sql_list, None, id_map)


def read_all_rows_and_save(connection, table_name, cols, rows, link_dict):
    sql_list = []
    id_map = dict()
    allowed_col_length = config.get_table_total_cols(table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    if len(cols) > allowed_col_length:
        return read_all_rows_and_save_extra(connection, table_name, cols, rows, allowed_col_length, link_dict)
    else:
        col_string = get_cols(cols, table_name)
        link_key = config.get_parent_link_back_key(table_name)
        link_back_key_index = cols.index(link_key)
        id_map_col = cols.index(config.get_table_link_back_key(table_name))
        row_string = ''
        for i in range(0, len(rows)):
            actual_row_cols = len(rows[i])
            uid = get_unique_id(connection)
            first_value = str(rows[i][0])
            link_back_fk_from_db = -1
            if table_name == 'B_TESTS':
                search_and_delete(connection, str(first_value))
                link_back_fk_from_db = get_crd_id(connection, str(rows[i][1]))

            link_back_value = str(rows[i][link_back_key_index])

            id_map[str(rows[i][id_map_col])] = uid
            dict_data.update({uid: first_value})
            dict_data_link_back.update({uid: link_back_value})
            row_string += 'INTO {0}.{1} {2} VALUES({3}'.format(db_schema, table_name, col_string, uid)
            if not table_name == 'A_CCSD':
                if link_back_fk_from_db != 0 and link_back_fk_from_db != -1:
                    link_fk_key = link_back_fk_from_db
                else:
                    link_fk_key = config.get_key_by_value(link_dict, link_back_value)

                row_string += ",{0}".format(link_fk_key)
            row_string += ",'{0}'".format(first_value)
            for j in range(1, actual_row_cols):
                val = convert_number_or_into_string(str(rows[i][j]), cols[j])
                row_string += ",{0}".format(val)
            row_string += ')'
            sql_list.append(row_string)  # save normal columns
            row_string = ''
    return DBResSpec(dict_data, dict_data_link_back, sql_list, None, id_map)


def read_all_rows_and_save_a_table_extra(connection, table_name, cols, rows, allowed_col_length, link_dict):
    sql_list = []
    id_map = dict()
    allowed_col_length = config.get_table_total_cols(table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    extra_row_string = []
    col_list = get_col_list(cols, table_name)
    col_string, clist = get_extra_cols(cols, allowed_col_length, table_name)
    link_key = config.get_parent_link_back_key(table_name)
    link_back_key_index = cols.index(link_key)
    id_map_col = cols.index(config.get_table_link_back_key(table_name))
    update_sql_list = []
    insert_sql_list = []
    for i in range(0, len(rows)):
        actual_row_cols = len(rows[i])
        crd_revision_id = str(rows[i][0])
        link_pk_from_db = get_crd_id(connection, str(crd_revision_id))
        link_back_value = str(rows[i][link_back_key_index])
        uid = link_pk_from_db if link_pk_from_db != 0 else get_unique_id(connection)
        if link_pk_from_db != 0:
            update_sql_query = 'UPDATE {0}.{1} SET {2}= \'{3}\''.format(db_schema, table_name, col_list[0], crd_revision_id)
            # here we are deleting all existing extra columns for the specific crd record
            delete_a_extra_columns(connection, link_pk_from_db)
            for j in range(1, actual_row_cols):
                if j >= allowed_col_length:
                    # if there exist any extra in updated json file, we insert it as new record with existing crd record
                    statement = 'INSERT ' + prepare_extra_column_sql(table_name, link_pk_from_db, str(cols[j]), str(rows[i][j]))
                    extra_row_string.append(statement)
                    continue
                val = convert_number_or_into_string(str(rows[i][j]), cols[j])
                update_sql_query += ",{0}={1}".format(col_list[j], val)
            update_sql_query += " WHERE {0}='{1}'".format(col_list[0], crd_revision_id)
            update_sql_list.append(update_sql_query)
        else:
            # here we need to create insert because crd already does not exist.
            insert_sql_query = 'INSERT INTO {0}.{1} {2} VALUES({3}'.format(db_schema, table_name, col_string, uid)
            insert_sql_query += ",'{0}'".format(crd_revision_id)
            for j in range(1, actual_row_cols):
                if j >= allowed_col_length:
                    statement = 'INSERT ' + prepare_extra_column_sql(table_name, uid, str(cols[j]), str(rows[i][j]))
                    extra_row_string.append(statement)
                    continue
                val = convert_number_or_into_string(str(rows[i][j]), cols[j])
                insert_sql_query += ",{0}".format(val)
            insert_sql_query += ')'
            insert_sql_list.append(insert_sql_query)
        id_map[str(rows[i][id_map_col])] = uid
        dict_data.update({uid: crd_revision_id})
        dict_data_link_back.update({uid: link_back_value})
        # iterate through all extra col
    for sql_stmt in extra_row_string:
        extra_id = get_unique_id(connection)
        insert_sql_list.append(sql_stmt.replace('REPLACE_ID', str(extra_id)))
    return DBResSpec(dict_data, dict_data_link_back, insert_sql_list, update_sql_list, id_map)


def read_all_rows_and_save_a_table(connection, table_name, cols, rows, link_dict):
    sql_list = []
    id_map = dict()
    allowed_col_length = config.get_table_total_cols(table_name)
    dict_data = dict()
    dict_data_link_back = dict()
    if len(cols) > allowed_col_length:
        return read_all_rows_and_save_a_table_extra(connection, table_name, cols, rows, allowed_col_length, link_dict)
    else:
        col_list = get_col_list(cols, table_name)
        col_string = get_cols(cols, table_name)
        link_key = config.get_parent_link_back_key(table_name)
        link_back_key_index = cols.index(link_key)
        id_map_col = cols.index(config.get_table_link_back_key(table_name))
        update_sql_list = []
        insert_sql_list = []
        for i in range(0, len(rows)):
            actual_row_cols = len(rows[i])
            crd_revision_id = str(rows[i][0])
            link_pk_from_db = get_crd_id(connection, str(crd_revision_id))
            link_back_value = str(rows[i][link_back_key_index])
            uid = link_pk_from_db if link_pk_from_db != 0 else get_unique_id(connection)

            if link_pk_from_db != 0:
                # if we r here that mean crd already exist, so we need to update it
                update_sql_query = 'UPDATE {0}.{1} SET {2}= \'{3}\''.format(db_schema, table_name, col_list[0],
                                                                            crd_revision_id)
                # here we r deleting all existed extra columns for this specific existing crd record
                delete_a_extra_columns(connection, link_pk_from_db)
                for j in range(1, actual_row_cols):
                    val = convert_number_or_into_string(str(rows[i][j]), cols[j])
                    update_sql_query += ",{0}={1}".format(col_list[j], val)
                update_sql_query += " WHERE {0}='{1}'".format(col_list[0], crd_revision_id)
                update_sql_list.append(update_sql_query)
            else:
                # here we need to create insert because crd already does not exist.
                insert_sql_query = 'INSERT INTO {0}.{1} {2} VALUES({3}'.format(db_schema, table_name, col_string, uid)
                insert_sql_query += ",'{0}'".format(crd_revision_id)
                for j in range(1, actual_row_cols):
                    val = convert_number_or_into_string(str(rows[i][j]), cols[j])
                    insert_sql_query += ",{0}".format(val)
                insert_sql_query += ')'
                insert_sql_list.append(insert_sql_query)
            id_map[str(rows[i][id_map_col])] = uid
            dict_data.update({uid: crd_revision_id})
            dict_data_link_back.update({uid: link_back_value})

    return DBResSpec(dict_data, dict_data_link_back, insert_sql_list, update_sql_list, id_map)


def prepare_extra_column_sql(table_name, primary_key_value, col_name, col_value):
    primary_key = config.get_table_primary_key(table_name)
    primary_key_extra = config.get_table_primary_key(table_name + '_EXTRA')
    sql_string = ''
    sql_string += 'INTO {0}.{1}_EXTRA '.format(db_schema, table_name)
    sql_string += '("{0}","{1}","Column name","Column value") '.format(primary_key_extra, primary_key)
    sql_string += "VALUES (REPLACE_ID,{0},'{1}','{2}')".format(primary_key_value, col_name, col_value)
    return sql_string


def execute_oracle_queries(connection, sql_statements):
    try:
        with connection.cursor() as cursor:
            if isinstance(sql_statements, list):
                for sql_statement in sql_statements:
                    cursor.execute(sql_statement)
            else:
                cursor.execute(sql_statements)
            connection.commit()
    except cx_Oracle.Error as e:
        raise UploadProcessException('Could not save data!: {0} -> {1}'.format(e, sql_statement)) from e


def delete_all_rows(connection, table_name):
    sql_statement = 'Truncate Table ' + table_name
    try:
        # create a cursor
        with connection.cursor() as cursor:
            # execute the insert statement
            cursor.execute(sql_statement)
            print('delete completed:' + table_name)
    except cx_Oracle.Error as error:
        print('Error occurred while deleting:' + table_name)
        print(error)


def delete_table(connection, table_name):
    sql_statement = 'DROP TABLE "' + table_name + '" CASCADE CONSTRAINTS'
    try:
        # create a cursor
        with connection.cursor() as cursor:
            # execute the insert statement
            cursor.execute(sql_statement)
            print('delete table:' + table_name)
    except cx_Oracle.Error as error:
        print('Error occurred while deleting:' + table_name)
        print(error)


def delete_all_tables(connection):
    delete_table(connection, 'E_INDICATORS_EXTRA')
    delete_table(connection, 'E_INDICATORS')
    delete_table(connection, 'D_REINFORCEMENTS_EXTRA')
    delete_table(connection, 'D_REINFORCEMENTS')
    delete_table(connection, 'C_COMPONENTS_EXTRA')
    delete_table(connection, 'C_COMPONENTS')
    delete_table(connection, 'B_TESTS_EXTRA')
    delete_table(connection, 'B_TESTS')
    delete_table(connection, 'A_CCSD_EXTRA')
    delete_table(connection, 'A_CCSD')


def delete_all_tables_data(connection):
    delete_all_rows(connection, 'E_INDICATORS_EXTRA')
    delete_all_rows(connection, 'E_INDICATORS')
    delete_all_rows(connection, 'D_REINFORCEMENTS_EXTRA')
    delete_all_rows(connection, 'D_REINFORCEMENTS')
    delete_all_rows(connection, 'C_COMPONENTS_EXTRA')
    delete_all_rows(connection, 'C_COMPONENTS')
    delete_all_rows(connection, 'B_TESTS_EXTRA')
    delete_all_rows(connection, 'B_TESTS')
    delete_all_rows(connection, 'A_CCSD_EXTRA')
    delete_all_rows(connection, 'A_CCSD')


def truncate_30_chars(input_string):
    return input_string[:30]


def upsert_cloud_upload_status(connection, file_id, parent_id, file_name, object_name, new_status):
    with connection.cursor() as cursor:
        # Does a record already exists for that file?
        sqlcmd = 'select count(*) from {0}.attached_file where parent_id=:parent_id and file_name=:file_name'.format(db_schema)
        cursor.execute(sqlcmd, parent_id=parent_id, file_name=file_name)
        exists = int(cursor.fetchone()[0]) > 0
        # Insert or update the status record accordingly
        sqlcmd = """ 
            update {0}.attached_file set 
              cloud_upload_status = :status 
            , object_name = :object_name
            , updated_on = systimestamp
            , file_id = :file_id
            where parent_id=:parent_id and file_name=:file_name
            """.format(db_schema) if exists else """
            insert into {0}.attached_file 
            (cloud_upload_status, object_name, inserted_on, file_id, parent_id, file_name) 
            values (:status, :object_name, systimestamp, :file_id, :parent_id, :file_name)
            """.format(db_schema)
        cursor.execute(sqlcmd, status=new_status, object_name=object_name, file_id=file_id, parent_id=parent_id, file_name=file_name)
        connection.commit()


def insert_ccsd_status(connection, file_id, id_map, a_ccsd_cols, c_ccsd_rows):
    key_col_index = a_ccsd_cols.index(config.get_table_link_back_key('A_CCSD'))
    user_col_index = a_ccsd_cols.index('User')
    row_map = {ccsd_id: [r[key_col_index] for r in c_ccsd_rows].index(back_key) for back_key, ccsd_id in id_map.items()}
    with connection.cursor() as cursor:
        # Reset all related status records
        cursor.execute('delete {0}.a_ccsd_status where a_ccsd_id in ({1})'.format(db_schema, ','.join(str(i) for i in id_map.values())))
        sqlcmd = """insert into {0}.a_ccsd_status (a_ccsd_id, source_file_id, created_on, created_by) 
            values(:a_ccsd_id, :file_id, systimestamp, :created_by)""".format(db_schema)
        for a_ccsd_id in id_map.values():
            user = c_ccsd_rows[row_map[a_ccsd_id]][user_col_index]
            cursor.execute(sqlcmd, a_ccsd_id=a_ccsd_id, file_id=file_id, created_by=user)
        connection.commit()

