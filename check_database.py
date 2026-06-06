from SQLLITE3_DataBase import medi_data_base

# Create object
db = medi_data_base()

# Get saved data
data = db.display_table()

# Print data
print("\n===== SAVED DATABASE DATA =====\n")
print(data)
