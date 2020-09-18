import http.client
from flask_restplus import Namespace, Resource
from operators_backend.models import OperatorModel
from operators_backend.db import db

admin_namespace = Namespace('admin', description='Admin operations')


@admin_namespace.route('/operators/<int:operator_id>/')
class OperatorsDelete(Resource):

    @admin_namespace.doc('delete_operator',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, operator_id):
        '''
        Delete a operator
        '''
        operator = OperatorModel.query.get(operator_id)
        if not operator:
            # The operator is not present
            return '', http.client.NO_CONTENT

        db.session.delete(operator)
        db.session.commit()

        return '', http.client.NO_CONTENT
