class ModelUser():

    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql="""SELECT id, username, password, fullname FROM user 
                    WHERE username = '{}' """.format(user.username)
            cursor.execute(sql)
        except Exception as ex:
            raise Exception(ex)