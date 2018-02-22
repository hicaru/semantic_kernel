"""Module for working with data shell."""
import main
import sys


def valid(method, project_id):
    """Test on method.
    :param method: Method valid.
    :param project_id: Project id in DB.
    :return: None.
    """
    if method == 'auto':
        """Collects semantics from domain."""

        main.auto_sem(project_id)

    elif method == 'query':
        """Collects semantics from query word"""

        query = sys.argv[3]

        # This magic number, limits the max result.
        main.query_sem(project_id, query, 300)

    elif method == 'cr':
        """Collects semantics from competitors in yandex"""

        query = sys.argv[3]

        main.cr_sem(project_id, query)

    elif method == 'form':
        """Can work with large amounts of data and minus words"""

        minus_id_array = sys.argv[3:]
        main.form_sem(project_id, minus_id_array)


if __name__ == '__main__':
    # Project id from DB.
    project_id = int(sys.argv[1])

    # Method received shell.
    method = sys.argv[2]
    valid(method, project_id)
