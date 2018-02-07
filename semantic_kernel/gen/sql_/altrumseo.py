'''
This module is completely
devoted to work with the database.
'''
import pymysql.cursors


class Sql_pool:

    def __init__( self ):
        self.connection = pymysql.connect(
            host = 'localhost', user = '',
            password = '',
            db = '', charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor
        )

    def sql_exc( self, sql_command ):
        temp = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute( sql_command )
                temp = cursor.fetchall()
            self.connection.commit()
        except Exception:
            pass
        finally:
            return temp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class Pattern(Sql_pool):
    '''This class contains patterns with sql queries.'''

    def select_id( self, idP ):
        '''
        :param idP: Project id.
        :return: Project domain.
        '''

        # Sql request.
        sql = 'SELECT `domain` FROM `projects` ' \
              'WHERE id = %i'

        # Request.
        temp = self.sql_exc(sql % int(idP))
        return temp[0]['domain']

    def select_requests(self, idP):
        '''
        :param idP: Project id.
        :return: Array query.
        '''

        # Sql request.
        sql = 'SELECT `request`, `position` FROM ' \
              '`requests_promoted` WHERE `projectId` = {0}'

        # Request.
        temp = [i["request"] for i in self.sql_exc(sql.format(idP))]
        return temp

    def select_minus_word(self, id_word):
        '''
        :param id_word: Show minus word.
        :return: Array minus word.
        '''

        ids = ''

        for i in id_word:
            ids += str(i) + ","

        ids = ids[:-1]

        # Sql request.
        sql = "SELECT id, subjects, word, subjects_id" \
              " FROM minus_word WHERE " \
              "subjects_id IN(%s)" % ids

        # Request.
        temp = [i["word"] for i in self.sql_exc(sql)]
        return temp

    def add_from_base( self, id, r, f, p ):
        '''
        :param id: Project id.
        :param r: Query word.
        :param f: Frequency this word.
        :param p: Json string with position query word.
        :return: None.
        '''

        # Sql request.
        sql = "INSERT INTO `requests_promoted` " \
              "(`projectId`, `request`, `frequency`, `position`, `competitors`)" \
              " VALUES ({0}, '{1}' , '{2}' ,'{3}' , ' ' )"

        # Request.
        self.sql_exc(sql.format(str(id), r, str(f), p))

    def delite(self, project):
        '''
        :param project: Project id.
        :return: None.
        '''

        # Sql request.
        sql = "DELETE FROM `altrumseo`.`requests_promoted` " \
              "WHERE `requests_promoted`.`projectId` = %i"

        # Request.
        self.sql_exc( sql % project)

    def select_region(self, p_id):
        '''
        :param p_id: Project id.
        :return: If do't in stock region id 0.
        '''

        # Sql request.
        sql = 'SELECT `region_id_list` FROM' \
              ' `projects` WHERE `id` = %i'

        # Request.
        lr = self.sql_exc(sql % p_id)[0]['region_id_list']
        lr = lr.split(',')[0]

        # If do't id region return 0.
        # else return region id.
        if lr:
            return lr
        else:
            return 0


