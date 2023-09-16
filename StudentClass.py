import sqlite3 as sql
from itertools import groupby

class Students:

    def __init__(self, db_path : str):
        self._connection_database = sql.connect(db_path)
        self._students_db = self._connection_database.cursor()
    
    def add(self, surname : str,name : str, subject : str, subgroup : str) -> None:
        self._students_db.execute('SELECT * FROM Queue WHERE subject_name = ? AND subgroup_id = ?', (subject, subgroup))
        if self._students_db.fetchone() is not None:
             self._students_db.execute('UPDATE Queue SET student_surname = ?, student_name  = ? WHERE subject_name = ? AND subgroup_id = ?', (surname, name,subject,subgroup))
        else:
            self._students_db.execute('INSERT INTO Queue (student_surname, student_name, subject_name, subgroup_id) VALUES(?,?,?,?)', (surname, name, subject, subgroup))
        self._connection_database.commit()


    #NO IMPLEMENTATION
    def remove(self, subject : str, stud_union : str, student : str) -> None:
        raise NotImplementedError("remove_student not implemented")

    def find(self, student_name : str) -> tuple:
        result_execute = self._students_db.execute(f"SELECT * FROM Queue WHERE student_name = '{student_name}'")
        result : tuple = result_execute.fetchone()
        if result is None:
            raise ValueError("Empthy result exception")
        return result

    def show_all(self) -> tuple:
        result_execute = self._students_db.execute('SELECT * FROM Queue')
        result : tuple = result_execute.fetchall()
        if type(result) == tuple:
            counter : int = 0
            for sub_str in result:
                counter += len(sub_str)
                if counter >= 4096:
                    raise ValueError("show_all : string's contains too much chars (over 4095)")
        return result

    #NOT TESTED
    def find(self, student_id : int) -> tuple:
        result_execute = self._students_db.execute(f"SELECT * FROM Queue WHERE student_id = " + "% d" % student_id)
        result = result_execute.fetchone()
        if result is None:
            raise ValueError("Empthy result exception")
        return result

    def __del__(self):
        self._students_db.close()

if __name__ == '__main__':
    stud = Students("D:\Tg_Bots\QueueBot\DataBase\StudentsTest.db")
    print(stud.show_all())