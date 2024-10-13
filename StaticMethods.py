from encryption import RSAEncryption

class StaticMethods:
    
    @staticmethod
    def get_user_role(self, username):
        sql = 'SELECT username, password, role FROM users'
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        for encrypted_username,passw, role in users:
            try:
                decrypted_username = RSAEncryption.decrypt_data(encrypted_username)
            except Exception as e:
                print(f"Decryption failed: {str(e)}")
                continue
            
            if decrypted_username == username:
                return role
            
        return None

    @staticmethod
    def GetRowIDUsers(cursor, username):
        sql = 'SELECT rowid, username FROM users'
        cursor.execute(sql)
        rowids = cursor.fetchall()
        for rowid, encrypted_username in rowids:
            try:
                decrypted_username = RSAEncryption.decrypt_data(encrypted_username)
            except Exception as e:
                print(f"Decryption failed: {str(e)}")
                continue 
            if decrypted_username == username:
                return rowid
            
        return None

    @staticmethod
    def GetRowIDRole(cursor, username, table):
        sql = f'SELECT rowid, username FROM {table}'
        cursor.execute(sql)
        rowids = cursor.fetchall()
        for rowid, encrypted_username in rowids:
            try:
                decrypted_username = RSAEncryption.decrypt_data(encrypted_username)
            except Exception as e:
                print(f"Decryption failed: {str(e)}")
                continue
            if decrypted_username == username:
                return rowid