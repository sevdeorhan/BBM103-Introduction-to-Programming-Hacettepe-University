import sys
def create_table(database, table_name, columns):
    if table_name in database:
        print(f"Error: Table '{table_name}' already exists")
        return
    columns_list = columns.split(',')
    database[table_name] = {"columns": columns_list, "rows": []}
    print(f"Table '{table_name}' created with columns: {database[table_name]['columns']}")

def insert(database, table_name, data):
    data_list = data.split(',')
    if table_name not in database:
        print(f"Table {table_name} not found")
        print(f"Inserted into '{table_name}': {tuple(data_list)}")
        return
    columns = database[table_name]["columns"]
    if len(data_list) != len(columns):
        print(f"Error: Number of data elements does not match number of columns in table '{table_name}'.")
        return
    database[table_name]["rows"].append(data_list)
    print(f"Inserted into '{table_name}': {tuple(data_list)}")
    print( )
    table(database, table_name)

def table(database, table_name):
    if table_name not in database:
        print(f"Table '{table_name}' does not exist.")
        return
    columns = database[table_name]["columns"]
    rows = database[table_name]["rows"]
    column_width = [len(column) for column in columns]
    for row in rows:
        for i, data in enumerate(row):
            column_width[i] = max(column_width[i],len(str(data))) #the larger of the column and row value
    print(f"Table: {table_name}")
    for i, column in enumerate(columns):
        print('+' + '-'* (column_width[i]+2) ,end='')
    print('+')
    header_row = '| '
    for i in range(len(columns)):
        header_row += columns[i].ljust(column_width[i])
        if i < len(columns)-1:
            header_row += ' | '
        else:
            header_row += ' |'
    print(header_row)
    for i,column in enumerate(columns):
        print('+' + '-'* (column_width[i]+2) ,end='')
    print('+')
    for row in rows:
        row_print = '| '
        for i in range(len(row)):
            row_print += str(row[i]).ljust(column_width[i])
            if i < len(row) - 1:
                row_print += ' | '
            else:
                row_print += ' |'
        print(row_print)
    for i,column in enumerate(columns):
        print('+' + '-'* (column_width[i]+2) ,end='')
    print('+')

def select(database, table_name, columns, conditions):
    formatted_conditions = (conditions.replace('"', "'") if conditions.startswith('{') and conditions.endswith('}') else conditions)
    if table_name not in database:
        print(f"Table {table_name} not found")
        print(f"Condition: {formatted_conditions}")
        print(f"Select result from '{table_name}': None")
        return
    table = database[table_name]
    table_columns = table["columns"]
    rows = table["rows"]
    if columns == '*':
        selected_columns = table_columns
    else:
        selected_columns = []
        for column in columns.split(','):
            column = column.strip()
            if column in table_columns:
                selected_columns.append(column)
            else:
                print(f"Column {column} does not exist.")
                print(f"Condition: {formatted_conditions}")
                print(f"Select result from '{table_name}': None")
                return
    conditions = conditions.strip('{}')
    conditions_list = []
    try:
        conditions_pairs = conditions.split(',')
        for condition in conditions_pairs:
            key, value = condition.split(':', 1)
            conditions_list.append((key.strip().strip('"').strip("'"), value.strip().strip('"').strip("'")))
    except ValueError:
        print(f"Invalid condition format: {conditions}")
        print(f"Select result from '{table_name}': None")
        return
    conditions= dict(conditions_list)
    filtered_rows = []
    for row in rows:
        add_row = True
        for column, value in conditions_list:
            if column in table_columns:
                column_index = table_columns.index(column)
                if str(row[column_index]) != str(value):
                    add_row = False
                    break
            else:
                print(f"Column {column} does not exist.")
                print(f"Condition: {formatted_conditions}")
                print(f"Select result from '{table_name}': None")
                return
        if add_row:
            filtered_rows.append(row)
    result = []
    for row in filtered_rows:
        if selected_columns == table_columns:
            result.append(row)
        else:
            selected_row = []
            for column in selected_columns:
                if column in table_columns:
                    index = table_columns.index(column)
                    selected_row.append(row[index])
            result.append(tuple(selected_row))
    if result:
        print(f"Condition: {formatted_conditions}")
        print(f"Select result from '{table_name}': {result}")
    else:
        print(f"Select result from '{table_name}': None")

def update(database, table_name, updates, conditions):
    formatted_conditions = (conditions.replace('"', "'") if conditions.startswith('{') and conditions.endswith('}') else conditions)
    formatted_updates = (updates.replace('"', "'") if updates.startswith('{') and updates.endswith('}') else updates)
    print(f"Updated '{table_name}' with {formatted_updates} where {formatted_conditions}")
    if table_name not in database:
        print(f"Table {table_name} not found.")
        print(f"0 rows updated.")
        return
    table = database[table_name]
    table_columns = table["columns"]
    rows = table["rows"]
    update_dict = {}
    updates = updates.strip('{}').split(',')
    for update in updates:
        if ':' in update:
            key, value = update.split(':', 1)
            key = key.strip().strip('"').strip("'")
            value = value.strip().strip('"').strip("'")
            update_dict[key] = value
        else:
            print(f"Column {update} does not exist.")
            print(f"0 rows updated.\n")
            updated_table(table_name)
            return
    for column in update_dict:
        if column not in table_columns:
            print(f"Column {column} does not exist.")
            print(f"0 rows updated.\n")
            updated_table(database, table_name)
            return
    condition_dict = {}
    conditions = conditions.strip('{}').split(',')
    for condition in conditions:
        if ':' in condition:
            key, value = condition.split(':', 1)
            key = key.strip().strip('"').strip("'")
            value = value.strip().strip('"').strip("'")
            condition_dict[key] = value
        else:
            print(f"Column {condition} does not exist.")
            print(f"0 rows updated.\n")
            updated_table(table_name)
            return
    for column in condition_dict:
        if column not in table_columns:
            print(f"Column {column} does not exist.")
            print(f"0 rows updated.\n")
            updated_table(database, table_name)
            return
    rows_updated = 0
    for row in rows:
        condition_met = True
        for column, value in condition_dict.items():
            if column in table_columns:
                column_index = table_columns.index(column)
                if str(row[column_index]) != str(value):
                    condition_met = False
                    break
            else:
                print(f"Column {column} does not exist.")
                condition_met = False
                break
        if condition_met:
            for column, value in update_dict.items():
                if column in table_columns:
                    column_index = table_columns.index(column)
                    row[column_index] = value
            rows_updated += 1
    print(f"{rows_updated} rows updated.\n")
    updated_table(database, table_name)

def updated_table(database, table_name):
    if table_name not in database:
        print(f"Table '{table_name}' not found.")
        return
    columns = database[table_name]["columns"]
    rows = database[table_name]["rows"]
    column_width = [len(column) for column in columns]
    for row in rows:
        for i, data in enumerate(row):
            column_width[i] = max(column_width[i], len(str(data)))  # the larger of the column and row value
    print(f"Table: {table_name}")
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')
    header_row = '| '
    for i in range(len(columns)):
        header_row += columns[i].ljust(column_width[i])
        if i < len(columns) - 1:
            header_row += ' | '
        else:
            header_row += ' |'
    print(header_row)
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')
    for row in rows:
        row_print = '| '
        for i in range(len(row)):
            row_print += str(row[i]).ljust(column_width[i])
            if i < len(row) - 1:
                row_print += ' | '
            else:
                row_print += ' |'
        print(row_print)
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')

def delete(database, table_name, conditions):
    formatted_conditions = (conditions.replace('"', "'") if conditions.startswith('{') and conditions.endswith('}') else conditions)
    print(f"Deleted from '{table_name}' where {formatted_conditions}")
    if table_name not in database:
        print(f"Table {table_name} not found.")
        print(f"0 rows deleted.")
        return
    table = database[table_name]
    table_columns = table["columns"]
    rows = table["rows"]
    condition_dict = {}
    conditions = conditions.strip('{}').split(',')
    for condition in conditions:
        if ':' in condition:
            key, value = condition.split(':', 1)
            key = key.strip().strip('"').strip("'")
            value = value.strip().strip('"').strip("'")
            condition_dict[key] = value
        else:
            print(f"Column {condition} does not exist.")
            print(f"0 rows deleted.\n")
            deleted_table(database, table_name)
            return
    for column in condition_dict:
        if column not in table_columns:
            print(f"Column {column} does not exist.")
            print(f"0 rows deleted.\n")
            deleted_table(database, table_name)
            return
    rows_deleted = 0
    rows_to_delete = []
    for row in rows:
        condition_met = True
        for column, value in condition_dict.items():
            if column in table_columns:
                column_index = table_columns.index(column)
                if str(row[column_index]) != str(value):
                    condition_met = False
                    break
            else:
                print(f"Column {column} does not exist.")
                condition_met = False
                break
        if condition_met:
            rows_to_delete.append(row)
    for row in rows_to_delete:
        rows.remove(row)
        rows_deleted += 1
    print(f"{rows_deleted} rows deleted.\n")
    deleted_table(database, table_name)

def deleted_table(database, table_name):
    if table_name not in database:
        print(f"Table '{table_name}' not found.")
        return
    columns = database[table_name]["columns"]
    rows = database[table_name]["rows"]
    column_width = [len(column) for column in columns]
    for row in rows:
        for i, data in enumerate(row):
            column_width[i] = max(column_width[i], len(str(data)))  # the larger of the column and row value
    print(f"Table: {table_name}")
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')
    header_row = '| '
    for i in range(len(columns)):
        header_row += columns[i].ljust(column_width[i])
        if i < len(columns) - 1:
            header_row += ' | '
        else:
            header_row += ' |'
    print(header_row)
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')
    for row in rows:
        row_print = '| '
        for i in range(len(row)):
            row_print += str(row[i]).ljust(column_width[i])
            if i < len(row) - 1:
                row_print += ' | '
            else:
                row_print += ' |'
        print(row_print)
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')

def join(database, table1, table2, column):
    print(f"Join tables {table1} and {table2}")
    if table1 not in database:
        print(f"Table {table1} does not exist")
        return
    if table2 not in database:
        print(f"Table {table2} does not exist")
        return
    table1_name = database[table1]
    table2_name = database[table2]
    if column not in table1_name["columns"] or column not in table2_name["columns"]:
        print(f"Column {column} does not exist")
        return
    table1_name_column_index = table1_name["columns"].index(column)
    table2_name_column_index = table2_name["columns"].index(column)
    joined_rows = []
    for row1 in table1_name["rows"]:
        for row2 in table2_name["rows"]:
            if row1[table1_name_column_index] == row2[table2_name_column_index]:
                joined_row = row1 + row2
                joined_rows.append(joined_row)
    if joined_rows:
        print(f"Join result ({len(joined_rows)} rows):\n")
        all_columns = table1_name["columns"] + table2_name["columns"]
        joined_table_name = f"{table1}_{table2}_joined"
        database[joined_table_name] = {
            "columns": all_columns,
            "rows": joined_rows
        }
        joined_table(database, joined_table_name)
    else:
        print(f"No matching rows found for the join operation.")

def joined_table(database, table_name):
    if table_name not in database:
        print(f"Table '{table_name}' does not exist")
        return
    columns = database[table_name]["columns"]
    rows = database[table_name]["rows"]
    column_width = [len(column) for column in columns]
    for row in rows:
        for i, data in enumerate(row):
            column_width[i] = max(column_width[i], len(str(data)))
    print(f"Table: Joined Table")
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')
    header_row = '| '
    for i in range(len(columns)):
        header_row += columns[i].ljust(column_width[i])
        if i < len(columns) - 1:
            header_row += ' | '
        else:
            header_row += ' |'
    print(header_row)
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')
    for row in rows:
        row_print = '| '
        for i in range(len(row)):
            row_print += str(row[i]).ljust(column_width[i])
            if i < len(row) - 1:
                row_print += ' | '
            else:
                row_print += ' |'
        print(row_print)
    for i, column in enumerate(columns):
        print('+' + '-' * (column_width[i] + 2), end='')
    print('+')

def count(database, table_name, conditions):
    if table_name not in database:
        print(f"Table {table_name} not found.")
        print(f"Total number of entries in '{table_name}' is 0")
        return
    columns = database[table_name]["columns"]
    rows = database[table_name]["rows"]
    table = database[table_name]
    row_count = len(table["rows"])
    condition_dict = {}
    if conditions:
        conditions = conditions.strip('{}').split(',')
        for condition in conditions:
            if ':' in condition:
                key, value = condition.split(':', 1)
                key = key.strip().strip('"').strip("'")
                value = value.strip().strip('"').strip("'")
                condition_dict[key] = value
            else:
                print(f"Column {condition} does not exist")
                print(f"Total number of entries in '{table_name}' is 0")
                return
    for column in condition_dict:
        if column not in columns:
            print(f"Column {column} does not exist")
            print(f"Total number of entries in '{table_name}' is 0")
            return
    matching_rows = rows
    for column, value in condition_dict.items():
            column_index = columns.index(column)
            matching_rows = [row for row in matching_rows if str(row[column_index]) == str(value)]
    count_result = len(matching_rows)
    print(f"Count: {count_result}")
    print(f"Total number of entries in '{table_name}' is {count_result}")
    return

def main():
    database = {}
    with open(sys.argv[1], 'r') as file:
        for line in file:
            line=line.strip()
            if line.startswith('CREATE_TABLE'):
                print('#' * 22 + ' ' + 'CREATE' + ' ' + '#' * 25)
                parts = line.split(maxsplit=2)
                table_name = parts[1]
                columns = parts[2]
                create_table(database, table_name, columns)
                print('#' * 55)
                print( )
            elif line.startswith('INSERT'):
                print('#' * 22 + ' ' + 'INSERT' + ' ' + '#' * 25)
                parts = line.split(maxsplit=2)
                table_name = parts[1]
                data = parts[2]
                insert(database, table_name, data)
                print('#' * 55)
                print( )
            elif line.startswith('SELECT'):
                print('#' * 22 + ' ' + 'SELECT' + ' ' + '#' * 25)
                parts = line.split(maxsplit=2)
                table_name = parts[1]
                continued = parts[2] #columns WHERE conditions
                if 'WHERE' in continued:
                    columns = continued.split('WHERE')[0].strip()
                    conditions = continued.split('WHERE')[1].strip()
                else:
                    columns = continued.strip()
                    conditions = None
                select(database, table_name, columns, conditions)
                print('#' * 55)
                print()
            elif line.startswith('UPDATE'):
                print('#' * 22 + ' ' + 'UPDATE' + ' ' + '#' * 25)
                parts = line.split(maxsplit=2)
                table_name = parts[1]
                continued = parts[2]
                if 'WHERE' in continued:
                    columns = continued.split('WHERE')[0].strip()
                    conditions = continued.split('WHERE')[1].strip()
                else:
                    columns = continued.strip()
                    conditions = None
                update(database, table_name, columns, conditions)
                print('#' * 55)
                print( )
            elif line.startswith('DELETE'):
                print('#' * 22 + ' ' + 'DELETE' + ' ' + '#' * 25)
                parts = line.split(maxsplit=2)
                table_name = parts[1]
                continued= parts[2]
                if 'WHERE' in continued:
                    columns = continued.split('WHERE')[0].strip()
                    conditions = continued.split('WHERE')[1].strip()
                else:
                    columns = continued.strip()
                    conditions = None
                delete(database, table_name, conditions)
                print('#' * 55)
                print()
            elif line.startswith('JOIN'):
                print('#' * 23 + ' ' + 'JOIN' + ' ' + '#' * 26)
                parts = line.split(maxsplit=2)
                tables = parts[1]
                if 'ON' in parts[2]:
                    column = parts[2].split('ON')[1].strip()
                    if ',' in tables:
                        table1 = tables.split(',')[0].strip()
                        table2 = tables.split(',')[1].strip()
                join(database, table1, table2, column)
                print('#' * 55)
                print()
            elif line.startswith('COUNT'):
                print('#' * 22 + ' ' + 'COUNT' + ' ' + '#' * 25)
                parts = line.split(maxsplit=2)
                table_name = parts[1]
                continued= parts[2]
                if 'WHERE' in continued:
                    columns = continued.split('WHERE')[0].strip()
                    conditions = continued.split('WHERE')[1].strip()
                count(database, table_name, conditions)
                print('#' * 55)
                print()

if __name__ == "__main__":
    main()