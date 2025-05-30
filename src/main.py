import sys
import qdarkstyle
import csv
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QFileDialog
from PySide6.QtCore import QSettings, QDate
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Dialog as about_ui
import redis
from cryptography.fernet import Fernet
import uuid

class MainWindow(QMainWindow, main_ui): # used to display the main user interface
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # loads main_ui
        self.settings_manager = SettingsManager(self)  # Initializes SettingsManager
        self.settings_manager.load_settings()  # Load settings when the app starts
        self.redis_cloud = None

        # Populate the department combo box
        departments = [
            "Executive",
            "Human Resources",
            "Engineering",
            "Sales",
            "Marketing",
            "Finance",
            "IT",
            "Operations"
        ]
        self.combobox_department.addItems(departments)

        # menubar
        self.action_dark_mode.toggled.connect(self.dark_mode)
        self.action_about_qt.triggered.connect(lambda: QApplication.aboutQt())
        self.action_about.triggered.connect(lambda: AboutWindow(dark_mode=self.action_dark_mode.isChecked()).exec())

        # buttons
        self.button_connect.clicked.connect(self.redis_connection) # Connect button is pressed
        self.button_send.clicked.connect(self.redis_send) # Send button is pressed
        self.button_update.clicked.connect(self.redis_update) # Update button is pressed
        self.button_delete.clicked.connect(self.redis_delete) # Delete button is pressed
        self.button_query.clicked.connect(self.redis_query) # Query button is pressed
        self.button_search.clicked.connect(self.redis_search) # Search button is pressed
        self.button_import_csv.clicked.connect(self.import_csv) # Import CSV button is pressed
        self.button_export_csv.clicked.connect(self.export_to_csv) # Export to CSV button is pressed

        self.label_connection.setText("Not connected to RedisCloud")

        self.clear_fields()  # Clear input fields on startup

    def redis_send(self): # send data to RedisCloud (send button is pressed)
        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        id = str(uuid.uuid4()) # Generate a unique ID for the person

        # Get the values from the QLineEdits
        firstname = self.line_firstname.text().strip()
        middlename = self.line_middlename.text().strip()
        lastname = self.line_lastname.text().strip()
        age = self.line_age.text().strip()
        title = self.line_title.text().strip()
        joindate = self.join_date.date().toString("MM-dd-yyyy")
        department = self.combobox_department.currentText()
        address1 = self.line_address1.text().strip()
        address2 = self.line_address2.text().strip()
        country = self.line_country.text().strip()
        misc = self.line_misc.text().strip()

        row = self.table.rowCount()
        self.populate_table(row, id, firstname, middlename, lastname, age, title, joindate, department, address1, address2, country, misc)

        # Prepare the data dictionary
        data = {
            "_id": id,
            "First Name": firstname,    # Using dot notation for nested fields
            "Middle Name": middlename,
            "Last Name": lastname,
            "Age": age,
            "Title": title,
            "Join Date": joindate,
            "Department": department,
            "Address 1": address1,
            "Address 2": address2,
            "Country": country,
            "Misc": misc
        }

        try:
            # Get Redis client and store the data as a hash
            redis_client = self.redis_cloud.get_client()
            # Using HSET to store the dictionary with the ID as the key
            redis_client.hset(f"person:{id}", mapping=data)
            
            # Optional: Keep track of all person IDs in a set
            redis_client.sadd("person_ids", id)
            
            QMessageBox.information(self, "Success", "Data successfully sent to Redis")
        except redis.RedisError as e:
            QMessageBox.critical(self, "Redis Error", f"Failed to send data to Redis: {str(e)}")

        self.clear_fields()

    def redis_update(self): # update information in RedisCloud (update button is pressed)
        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        # Get selected rows
        selected_rows = set(index.row() for index in self.table.selectedIndexes())
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select at least one row to update")
            return

        try:
            redis_client = self.redis_cloud.get_client()
            updated_count = 0

            # Process each selected row
            for row in selected_rows:
                # Get all items from the row
                id_item = self.table.item(row, 0)  # ID column
                if not id_item:
                    continue

                id = id_item.text()
                
                # Create updated data dictionary from table
                data = {
                    "_id": id,
                    "First Name": self.table.item(row, 1).text() if self.table.item(row, 1) else "",
                    "Middle Name": self.table.item(row, 2).text() if self.table.item(row, 2) else "",
                    "Last Name": self.table.item(row, 3).text() if self.table.item(row, 3) else "",
                    "Age": self.table.item(row, 4).text() if self.table.item(row, 4) else "",
                    "Title": self.table.item(row, 5).text() if self.table.item(row, 5) else "",
                    "Join Date": self.table.item(row, 6).text() if self.table.item(row, 6) else "",
                    "Department": self.table.item(row, 7).text() if self.table.item(row, 7) else "",
                    "Address 1": self.table.item(row, 8).text() if self.table.item(row, 6) else "",
                    "Address 2": self.table.item(row, 9).text() if self.table.item(row, 7) else "",
                    "Country": self.table.item(row, 10).text() if self.table.item(row, 8) else "",
                    "Misc": self.table.item(row, 11).text() if self.table.item(row, 9) else ""
                }

                # Update the Redis hash
                redis_client.hset(f"person:{id}", mapping=data)
                updated_count += 1

            QMessageBox.information(self, "Success", f"Successfully updated {updated_count} record(s) in Redis")
            
        except redis.RedisError as e:
            QMessageBox.critical(self, "Redis Error", f"Failed to update Redis: {str(e)}")
        except AttributeError as e:
            QMessageBox.critical(self, "Table Error", f"Error reading table data: {str(e)}")

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def redis_delete(self): # delete information from RedisCloud (delete button is pressed)
        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        # Get selected rows
        selected_rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select at least one row to delete")
            return

        # Confirm deletion
        reply = QMessageBox.question(self, "Confirm Deletion",
                                   f"Are you sure you want to delete {len(selected_rows)} record(s)?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            redis_client = self.redis_cloud.get_client()
            deleted_count = 0

            # Process each selected row
            for row in selected_rows:
                # Get the person_id from the first column
                id_item = self.table.item(row, 0)  # ID column
                if not id_item:
                    continue

                person_id = id_item.text()
                
                # Delete from Redis
                redis_client.delete(f"person:{person_id}")  # Delete the hash
                redis_client.srem("person_ids", person_id)  # Remove from set
                
                # Remove row from table
                self.table.removeRow(row)
                deleted_count += 1

            QMessageBox.information(self, "Success", f"Successfully deleted {deleted_count} record(s) from Redis and table")
            
        except redis.RedisError as e:
            QMessageBox.critical(self, "Redis Error", f"Failed to delete from Redis: {str(e)}")
        except AttributeError as e:
            QMessageBox.critical(self, "Table Error", f"Error reading table data: {str(e)}")

    def redis_query(self): # query information in RedisCloud (query button is pressed)
        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        try:
            redis_client = self.redis_cloud.get_client()
            
            # Get all person IDs from the set
            person_ids = redis_client.smembers("person_ids")
            if not person_ids:
                QMessageBox.information(self, "Query Result", "No records found in Redis")
                self.table.setRowCount(0)  # Clear the table
                return

            # Clear existing table content
            self.table.setRowCount(0)
            
            # Populate table with data from Redis
            row = 0
            for person_id in person_ids:
                # Get all fields for this person
                person_data = redis_client.hgetall(f"person:{person_id}")
                
                # Extract values with defaults if fields are missing
                id = person_data.get("_id", person_id)
                firstname = person_data.get("First Name", "")
                middlename = person_data.get("Middle Name", "")
                lastname = person_data.get("Last Name", "")
                age = person_data.get("Age", "")
                title = person_data.get("Title", "")
                joindate = person_data.get("Join Date", "")
                department = person_data.get("Department", "")
                address1 = person_data.get("Address 1", "")
                address2 = person_data.get("Address 2", "")
                country = person_data.get("Country", "")
                misc = person_data.get("Misc", "")
                
                # Add to table
                self.populate_table(row, id, firstname, middlename, lastname, age, title, joindate, department, address1, address2, country, misc)
                row += 1

            QMessageBox.information(self, "Success", f"Retrieved {row} record(s) from Redis")
            
        except redis.RedisError as e:
            QMessageBox.critical(self, "Redis Error", f"Failed to query Redis: {str(e)}")

    def redis_search(self):  # Search information in RedisCloud
        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        # Get search criteria (no need to lowercase here, we'll handle it in comparison)
        firstname_search = self.line_firstname_search.text().strip()
        lastname_search = self.line_lastname_search.text().strip()

        try:
            redis_client = self.redis_cloud.get_client()
            
            # Get all person IDs
            person_ids = redis_client.smembers("person_ids")
            if not person_ids:
                QMessageBox.information(self, "Search Result", "No records found in Redis")
                self.table.setRowCount(0)
                return

            # Clear existing table content
            self.table.setRowCount(0)
            
            row = 0
            matches = 0
            
            # If both fields are empty, show all records (same as query)
            if not firstname_search and not lastname_search:
                for person_id in person_ids:
                    person_data = redis_client.hgetall(f"person:{person_id}")
                    self._populate_search_result(row, person_data)
                    row += 1
                    matches += 1
            else:
                # Search through all records
                for person_id in person_ids:
                    person_data = redis_client.hgetall(f"person:{person_id}")
                    
                    # Get name fields for comparison
                    firstname = person_data.get("First Name", "")
                    lastname = person_data.get("Last Name", "")
                    
                    # Case-insensitive comparison using lower() or re.IGNORECASE
                    import re
                    firstname_match = not firstname_search or re.search(re.escape(firstname_search), firstname, re.IGNORECASE)
                    lastname_match = not lastname_search or re.search(re.escape(lastname_search), lastname, re.IGNORECASE)
                    
                    if firstname_match and lastname_match:
                        self._populate_search_result(row, person_data)
                        row += 1
                        matches += 1

                if matches == 0:
                    QMessageBox.information(self, "Search Result", "No matching records found")
                else:
                    QMessageBox.information(self, "Search Result", f"Found {matches} matching record(s)")

        except redis.RedisError as e:
            QMessageBox.critical(self, "Redis Error", f"Failed to search Redis: {str(e)}")

    def _populate_search_result(self, row, person_data): # populates the table after searching
        id = person_data.get("_id", "")
        firstname = person_data.get("First Name", "")
        middlename = person_data.get("Middle Name", "")
        lastname = person_data.get("Last Name", "")
        age = person_data.get("Age", "")
        title = person_data.get("Title", "")
        joindate = person_data.get("Join Date", "")
        department = person_data.get("Department", "")
        address1 = person_data.get("Address 1", "")
        address2 = person_data.get("Address 2", "")
        country = person_data.get("Country", "")
        misc = person_data.get("Misc", "")
        
        self.populate_table(row, id, firstname, middlename, lastname, age, title, joindate, department, address1, address2, country, misc)

    def export_to_csv(self):  # exports data to CSV (export to CSV button is pressed)
        self.filename = QFileDialog.getSaveFileName(self, 'Export File', '', 'Data File (*.csv)')

        if not self.filename[0]:
            return

        try:
            with open(self.filename[0], 'w', newline='') as file:
                writer = csv.writer(file)
                
                # Write the header row (column names from the table)
                headers = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
                writer.writerow(headers)

                # Write the data rows from the table
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        # Append the text if the item exists, otherwise append an empty string
                        row_data.append(item.text() if item else '')
                    writer.writerow(row_data)

            QMessageBox.information(self, "Export Successful", f"Table data exported to {self.filename[0]}")
        
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export to CSV: {str(e)}")

    def import_csv(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Import CSV File', '', 'CSV Files (*.csv)')
        
        if not filename:
            return

        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        try:
            redis_client = self.redis_cloud.get_client()
            imported_count = 0
            
            with open(filename, 'r', newline='') as file:
                reader = csv.DictReader(file)
                
                expected_headers = {'ID', 'First Name', 'Middle Name', 'Last Name', 'Age', 'Title', 'Join Date', 'Department', 'Address 1', 'Address 2', 'Country', 'Misc'}
                if not all(header in reader.fieldnames for header in expected_headers):
                    QMessageBox.warning(self, "CSV Format Error", 
                                        "CSV file must contain all required headers:"
                                         "ID, First Name, Middle Name, Last Name, Age, Title, Join Date, Department, Address 1, Address 2, Country, Misc")
                    return

                self.table.setRowCount(0)
                
                for row_num, row in enumerate(reader):
                    id = row['ID'] if row['ID'] else str(uuid.uuid4())  # Generate a new ID if not provided
                    
                    data = {
                        "_id": id,
                        "First Name": row['First Name'] or "",
                        "Middle Name": row['Middle Name'] or "",
                        "Last Name": row['Last Name'] or "",
                        "Age": row['Age'] or "",
                        "Title": row['Title'] or "",
                        "Join Date": row['Join Date'] or "",
                        "Department": row['Department'] or "",
                        "Address 1": row['Address 1'] or "",
                        "Address 2": row['Address 2'] or "",
                        "Country": row['Country'] or "",
                        "Misc": row['Misc'] or ""
                    }
                    
                    redis_client.hset(f"person:{id}", mapping=data)
                    redis_client.sadd("person_ids", id)
                    
                    self.populate_table(row_num, 
                                        id, 
                                        data["First Name"], 
                                        data["Middle Name"],
                                        data["Last Name"], 
                                        data["Age"], 
                                        data["Title"], 
                                        data["Join Date"], 
                                        data["Department"],
                                        data["Address 1"], 
                                        data["Address 2"], 
                                        data["Country"],
                                        data["Misc"])
                    
                    imported_count += 1

            QMessageBox.information(self, "Import Successful", 
                                    f"Successfully imported {imported_count} record(s) from CSV")
            
        except FileNotFoundError:
            QMessageBox.critical(self, "File Error", "Could not find the specified CSV file")
        except redis.RedisError as e:
            QMessageBox.critical(self, "Redis Error", f"Failed to import to Redis: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Failed to import CSV: {str(e)}")

    def redis_connection(self):
        redis_url = self.line_redis_url.text().strip()
        redis_port = self.line_redis_port.text().strip()
        redis_user = self.line_redis_user.text().strip()
        if redis_user == '':
            redis_user = 'default'  # Default username if not provided
        redis_password = self.line_redis_password.text().strip()


        if any(not field for field in [redis_url, redis_port, redis_user, redis_password]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return

        try:
            # Create RedisCloud instance with provided details
            self.redis_cloud = RedisCloud(redis_url, redis_port, redis_user, redis_password)
            self.update_connection_status()
            self.initialize_table()
            self.redis_query()

        except redis.ConnectionError as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to Redis: {str(e)}")
            self.redis_cloud = None
            self.update_connection_status()

    def initialize_table(self):
        self.table.setRowCount(0) # clears the table
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(['ID', 'First Name', 'Middle Name', 'Last Name', 'Age', 'Title', 'Join Date', 'Department', 'Address 1', 'Address 2', 'Country', 'Misc'])
        self.table.setSelectionMode(QTableWidget.MultiSelection)

    def populate_table(self, row, id, firstname, middlename, lastname, age, title, joindate, department, address1, address2, country, misc):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(firstname))
        self.table.setItem(row, 2, QTableWidgetItem(middlename))
        self.table.setItem(row, 3, QTableWidgetItem(lastname))
        self.table.setItem(row, 4, QTableWidgetItem(age))
        self.table.setItem(row, 5, QTableWidgetItem(title))
        self.table.setItem(row, 6, QTableWidgetItem(joindate))
        self.table.setItem(row, 7, QTableWidgetItem(department))
        self.table.setItem(row, 8, QTableWidgetItem(address1))
        self.table.setItem(row, 9, QTableWidgetItem(address2))
        self.table.setItem(row, 10, QTableWidgetItem(country))
        self.table.setItem(row, 11, QTableWidgetItem(misc))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_fields(self):
        self.join_date.setDate(QDate.currentDate())
        self.combobox_department.setCurrentIndex(0)
        self.line_firstname.clear()
        self.line_middlename.clear()
        self.line_lastname.clear()
        self.line_age.clear()
        self.line_title.clear()
        self.line_address1.clear()
        self.line_address2.clear()
        self.line_country.clear()
        self.line_misc.clear()

    def update_connection_status(self):
        if self.redis_cloud is None:
            self.label_connection.setText("Not connected to RedisCloud")
        else:
            is_connected = self.redis_cloud.check_connection()
            if is_connected:
                self.label_connection.setText("Connected to RedisCloud")
            else:
                self.label_connection.setText("Failed to connect to RedisCloud")

    def dark_mode(self, checked):
        if checked:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        else:
            self.setStyleSheet('')

    def closeEvent(self, event):  # Save settings when closing the app
        self.settings_manager.save_settings()  # Save settings using the manager
        event.accept()

class RedisCloud:
    def __init__(self, redis_url, redis_port, redis_user, redis_password):
        try:
            self.client = redis.Redis(
                host=redis_url,
                port=int(redis_port),  # Convert port to integer
                username=redis_user,
                password=redis_password,
                decode_responses=True
            )
            # Test the connection immediately
            self.client.ping()
            self.connected = True
        except (redis.ConnectionError, ValueError) as e:
            self.connected = False
            raise redis.ConnectionError(f"Connection failed: {str(e)}")

    def get_client(self):
        return self.client
    
    def check_connection(self):
        try:
            self.client.ping()
            self.connected = True
            return True
        except redis.ConnectionError:
            self.connected = False
            return False

class SettingsManager: # used to load and save settings when opening and closing the app
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.key = self.settings.value('encryption_key', None)
        if self.key is None:
            self.key = Fernet.generate_key()
            self.settings.setValue('encryption_key', self.key.decode())
        self.cipher = Fernet(self.key)

    def encrypt_text(self, text):
        if not text:
            return None
        return self.cipher.encrypt(text.encode()).decode()
    
    def decrypt_text(self, encrypted_text):
        if not encrypted_text:
            return None
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

    def load_settings(self):
        size = self.settings.value('window_size', None)
        pos = self.settings.value('window_pos', None)
        dark = self.settings.value('dark_mode')
        redis_url = self.settings.value('redis_url')
        redis_port = self.settings.value('redis_port')
        redis_user = self.settings.value('redis_user')
        encrypted_redis_password = self.settings.value('redis_password')
        
        if size is not None:
            self.main_window.resize(size)
        if pos is not None:
            self.main_window.move(pos)
        if dark == 'true':
            self.main_window.action_dark_mode.setChecked(True)
            self.main_window.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        if redis_url is not None:
            self.main_window.line_redis_url.setText(redis_url)
        if redis_port is not None:
            self.main_window.line_redis_port.setText(redis_port)
        if redis_user is not None:
            self.main_window.line_redis_user.setText(redis_user)
        if encrypted_redis_password is not None:
            redis_password = self.decrypt_text(encrypted_redis_password)
            if redis_password:
                self.main_window.line_redis_password.setText(redis_password)
            else:
                self.main_window.line_redis_password.setText("")

    def save_settings(self):
        self.settings.setValue('window_size', self.main_window.size())
        self.settings.setValue('window_pos', self.main_window.pos())
        self.settings.setValue('dark_mode', self.main_window.action_dark_mode.isChecked())
        self.settings.setValue('redis_url', self.main_window.line_redis_url.text())
        self.settings.setValue('redis_port', self.main_window.line_redis_port.text())
        self.settings.setValue('redis_user', self.main_window.line_redis_user.text())

        redis_password = self.main_window.line_redis_password.text()
        self.settings.setValue('redis_password', self.encrypt_text(redis_password))

class AboutWindow(QDialog, about_ui): # this is the About Window
    def __init__(self, dark_mode=False):
        super().__init__()
        self.setupUi(self)
        if dark_mode:
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
        self.button_ok.clicked.connect(self.accept)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # needs to run first
    main_window = MainWindow()  # Instance of MainWindow
    main_window.show()
    sys.exit(app.exec())
