import sys
import qdarkstyle
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QDialog
from PySide6.QtCore import QSettings
from main_ui import Ui_MainWindow as main_ui
from about_ui import Ui_Dialog as about_ui
import redis
import datetime
from cryptography.fernet import Fernet

class MainWindow(QMainWindow, main_ui): # used to display the main user interface
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # loads main_ui
        self.settings_manager = SettingsManager(self)  # Initializes SettingsManager
        self.settings_manager.load_settings()  # Load settings when the app starts
        self.redis_cloud = None

        # menubar
        self.action_dark_mode.toggled.connect(self.dark_mode)
        self.action_about_qt.triggered.connect(lambda: QApplication.aboutQt())
        self.action_about.triggered.connect(lambda: AboutWindow(dark_mode=self.action_dark_mode.isChecked()).exec())

        # buttons
        self.button_connect.clicked.connect(self.redis_connection)
        self.button_send.clicked.connect(self.redis_send)
        self.button_update.clicked.connect(self.redis_update)
        self.button_delete.clicked.connect(self.redis_delete)
        self.button_query.clicked.connect(self.redis_query)
        self.button_search.clicked.connect(self.redis_search)

        self.label_connection.setText("Not connected to RedisCloud")

    def redis_send(self):
        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        id = datetime.datetime.now().strftime("%m%d%Y%H%M%S")

        # Get the values from the QLineEdits
        firstname = self.line_firstname.text()
        middlename = self.line_middlename.text()
        lastname = self.line_lastname.text()
        age = self.line_age.text()
        title = self.line_title.text()
        address1 = self.line_address1.text()
        address2 = self.line_address2.text()
        country = self.line_country.text()
        misc = self.line_misc.text()

        row = self.table.rowCount()
        self.populate_table(row, id, firstname, middlename, lastname, age, title, address1, address2, country, misc)

        # Prepare the data dictionary
        data = {
            "_id": id,
            "First Name": firstname,    # Using dot notation for nested fields
            "Middle Name": middlename,
            "Last Name": lastname,
            "Age": age,
            "Title": title,
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

    def redis_update(self):
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
                    "Address 1": self.table.item(row, 6).text() if self.table.item(row, 6) else "",
                    "Address 2": self.table.item(row, 7).text() if self.table.item(row, 7) else "",
                    "Country": self.table.item(row, 8).text() if self.table.item(row, 8) else "",
                    "Misc": self.table.item(row, 9).text() if self.table.item(row, 9) else ""
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

    def redis_delete(self):
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

    def redis_query(self):
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
                address1 = person_data.get("Address 1", "")
                address2 = person_data.get("Address 2", "")
                country = person_data.get("Country", "")
                misc = person_data.get("Misc", "")
                
                # Add to table
                self.populate_table(row, id, firstname, middlename, lastname, age, title, address1, address2, country, misc)
                row += 1

            QMessageBox.information(self, "Success", f"Retrieved {row} record(s) from Redis")
            
        except redis.RedisError as e:
            QMessageBox.critical(self, "Redis Error", f"Failed to query Redis: {str(e)}")

    def redis_search(self):
        if self.redis_cloud is None or not self.redis_cloud.check_connection():
            QMessageBox.warning(self, "Connection Error", "Please connect to Redis first")
            return

        # Get search criteria
        firstname_search = self.line_firstname_search.text().strip().lower()
        lastname_search = self.line_lastname_search.text().strip().lower()

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
                    firstname = person_data.get("First Name", "").lower()
                    lastname = person_data.get("Last Name", "").lower()
                    
                    # Check if record matches search criteria
                    firstname_match = not firstname_search or firstname_search in firstname
                    lastname_match = not lastname_search or lastname_search in lastname
                    
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

    def _populate_search_result(self, row, person_data):
        id = person_data.get("_id", "")
        firstname = person_data.get("First Name", "")
        middlename = person_data.get("Middle Name", "")
        lastname = person_data.get("Last Name", "")
        age = person_data.get("Age", "")
        title = person_data.get("Title", "")
        address1 = person_data.get("Address 1", "")
        address2 = person_data.get("Address 2", "")
        country = person_data.get("Country", "")
        misc = person_data.get("Misc", "")
        
        self.populate_table(row, id, firstname, middlename, lastname, age, title, address1, address2, country, misc)

    def redis_connection(self):
        redis_url = self.line_redis_url.text()
        redis_port = self.line_redis_port.text()
        redis_user = self.line_redis_user.text()
        redis_password = self.line_redis_password.text()

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
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(['ID', 'First Name', 'Middle Name', 'Last Name', 'Age', 'Title', 'Address 1', 'Address 2', 'Country', 'Misc'])
        self.table.setSelectionMode(QTableWidget.MultiSelection)

    def populate_table(self, row, id, firstname, middlename, lastname, age, title, address1, address2, country, misc):
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(id)))
        self.table.setItem(row, 1, QTableWidgetItem(firstname))
        self.table.setItem(row, 2, QTableWidgetItem(middlename))
        self.table.setItem(row, 3, QTableWidgetItem(lastname))
        self.table.setItem(row, 4, QTableWidgetItem(age))
        self.table.setItem(row, 5, QTableWidgetItem(title))
        self.table.setItem(row, 6, QTableWidgetItem(address1))
        self.table.setItem(row, 7, QTableWidgetItem(address2))
        self.table.setItem(row, 8, QTableWidgetItem(country))
        self.table.setItem(row, 9, QTableWidgetItem(misc))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def clear_fields(self):
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
