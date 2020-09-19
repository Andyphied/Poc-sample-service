import http.client
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource, fields
from operators_backend import config
from operators_backend.models import OperatorModel
from operators_backend.collections import OperatorCollection
from operators_backend.token_validation import validate_token_header
from operators_backend.db import db
from mongoengine.queryset.visitor import Q
from flask import abort

WELCOME_MSG_URL = "http://165.22.116.11:7058/api/messages/welcome/"

api_namespace = Namespace('api', description='API operations')


def authentication_header_parser(value):
    username = validate_token_header(value, config.PUBLIC_KEY)
    if username is None:
        abort(401)
    return username


# Input and output formats for operator
authentication_parser = api_namespace.parser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')

operator_parser = authentication_parser.copy()
operator_parser.add_argument('pin', type=str, required=True,
                             help='The operator zeno pin')
operator_parser.add_argument('name', type=str, required=True,
                             help='The operators Name')
operator_parser.add_argument('usernameMain', type=str, required=True,
                             help='The operators usrname')
operator_parser.add_argument('email', type=str, required=True,
                             help='The email address of the operator')
operator_parser.add_argument('phoneNo', type=str, required=True,
                             help='The operators Phone Number')
operator_parser.add_argument('contactName', type=str, required=False,
                             help='The operators Name')
operator_parser.add_argument('contactPhoneNo', type=str, required=False,
                             help='The operators Name')
operator_parser.add_argument('contactEmail', type=str, required=False,
                             help='The operators Name')
operator_parser.add_argument('officeAddress', type=str, required=True,
                             help='The office address of the operator')
operator_parser.add_argument('status', type=str, required=True,
                             help="status of operator, '0' or '1'")
operator_parser.add_argument('numberOfVehicle', type=str, required=True,
                             help='The operators Bank Account Number')

model = {
    'id': fields.Integer(),
    'username': fields.String(),
    'usernameMain': fields.String(),
    'pin': fields.String(),
    'name': fields.String(),
    'phoneNo': fields.String(),
    'email': fields.String(),
    'contactName': fields.String(),
    'contactPhoneNo': fields.String(),
    'contactEmail': fields.String(),
    'officeAddress': fields.String(),
    'numberOfVehicle': fields.String(),
    'status': fields.String(),
    'statusTimestamp': fields.DateTime(),
    'timestamp': fields.DateTime(),
}
operator_model = api_namespace.model('Operator', model)


@api_namespace.route('/me/operators/')
class MeOperatorListCreate(Resource):

    @api_namespace.doc('list_operators')
    @api_namespace.expect(authentication_parser)
    @api_namespace.marshal_with(operator_model, as_list=True)
    def get(self):
        '''
        Retrieves all the operators added by an admin
        '''
        args = authentication_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        operators = OperatorCollection.objects(username=username)

        result = [operator for operator in operators]

        return result

    @api_namespace.doc('create_operator')
    @api_namespace.expect(operator_parser)
    @api_namespace.marshal_with(operator_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new operator
        '''
        args = operator_parser.parse_args()
        username = authentication_header_parser(args['Authorization'])

        new_operator = OperatorModel(
            username=username,
            officeAddress=args['officeAddress'],
            usernameMain=args['usernameMain'],
            email=args['email'],
            status=args['status'],
            pin=args['pin'],
            name=args['name'],
            phoneNo=args['phoneNo'],
            contactName=args['contactName'],
            contactPhoneNo=args['contactPhoneNo'],
            contactEmail=args['contactEmail'],
            numberOfVehicle=args['numberOfVehicle'],
            timestamp=datetime.utcnow()
        )
        db.session.add(new_operator)
        db.session.commit()

        result = api_namespace.marshal(new_operator, operator_model)

        return result, http.client.CREATED


search_parser = api_namespace.parser()
search_parser.add_argument('search', type=str, required=False,
                           help='Search in the text of the operators')


@api_namespace.route('/operators/')
class OperatorList(Resource):

    @api_namespace.doc('list_operators')
    @api_namespace.marshal_with(operator_model, as_list=True)
    @api_namespace.expect(search_parser)
    def get(self):
        '''
        Searches all for operators by name
        '''
        args = search_parser.parse_args()
        param = args['search']

        if param:

            queries = OperatorCollection.objects(name__icontains=param)
            result = [query for query in queries]

            return result

        query = []

        return query


@api_namespace.route('/all/operators/')
class AllOperatorList(Resource):

    @api_namespace.doc('list all_operators')
    @api_namespace.marshal_with(operator_model, as_list=True)
    @api_namespace.expect(authentication_parser)
    def get(self):
        '''
        Retrieves all the operators
        '''
        args = authentication_parser.parse_args()
        authentication_header_parser(args['Authorization'])
        operators = OperatorCollection.objects()

        result = [operator for operator in operators]

        return result


update_parser = authentication_parser.copy()
update_parser.add_argument('name', type=str, required=False,
                           help='The operators Name')
update_parser.add_argument('usernameMain', type=str, required=False,
                           help='The operators user name')
update_parser.add_argument('email', type=str, required=False,
                           help='The email address of the operator')
update_parser.add_argument('phoneNo', type=str, required=False,
                           help='The operators Phone Number')
update_parser.add_argument('officeAddress', type=str, required=False,
                           help='The office address of the operator')
update_parser.add_argument('numberOfVehicle', type=str, required=False,
                           help='The operators Bank Account Number')
update_parser.add_argument('contactName', type=str, required=False,
                           help='The operators Name')
update_parser.add_argument('contactPhoneNo', type=str, required=False,
                           help='The operators Name')
update_parser.add_argument('contactEmail', type=str, required=False,
                           help='The operators Name')


@api_namespace.route('/operators/<int:operator_id>/')
class OperatorsRetrieve(Resource):

    @api_namespace.doc('retrieve_operator')
    @api_namespace.marshal_with(operator_model)
    def get(self, operator_id):
        '''
        Retrieve a operator
        '''
        operator = OperatorCollection.objects(id=operator_id).first()
        if not operator:
            # The operator is not present
            return '', http.client.NOT_FOUND
        print(operator)
        return operator

    @api_namespace.doc('update_operator')
    @api_namespace.marshal_with(operator_model)
    @api_namespace.expect(update_parser)
    def put(self, operator_id):
        '''
        update a operator
        '''
        args = update_parser.parse_args()
        operator = (
            OperatorModel
            .query
            .filter(OperatorModel.id == operator_id)
            .first()
        )
        if not operator:
            # The operator is not present
            return '', http.client.NOT_FOUND

        operator.officeAddress = args['officeAddress']
        operator.usernameMain = args['usernameMain']
        operator.email = args['email']
        operator.name = args['name']
        operator.phoneNo = args['phoneNo']
        operator.numberOfVehicle = args['numberOfVehicle']
        operator.timestamp = datetime.utcnow()
        operator.contactName = args['contactName']
        operator.contactPhoneNo = args['contactPhoneNo']
        operator.contactEmail = args['contactEmail']
        operator.move = 2

        db.session.add(operator)
        db.session.commit()

        return operator


status_parser = api_namespace.parser()
status_parser.add_argument('status', type=str, required=True,
                           help='The Operator status')


class OperatorsStatus(Resource):

    @api_namespace.doc('retrieve_operator')
    @api_namespace.marshal_with(operator_model, as_list=True)
    @api_namespace.expect(status_parser)
    def get(self):
        '''
        retrive operator with specified status
        '''
        args = status_parser.parse_args()
        status = args['status']
        operators = OperatorCollection.objects(status=status)
        if not operators:
            # The operator is not present
            return '', http.client.NOT_FOUND

        result = [operator for operator in operators]

        return result


@api_namespace.route('/status/<int:operator_id>/')
class OperatorsStatusUpdate(Resource):

    @api_namespace.doc('retrieve_operator')
    @api_namespace.marshal_with(operator_model)
    @api_namespace.expect(status_parser)
    def put(self, operator_id):
        '''
        set the operator status
        '''
        args = status_parser.parse_args()
        status = args['status']
        operator = (OperatorCollection
                    .objects(
                        id=operator_id
                        )
                    .first())
        if not operator:
            # The operator is not present
            return '', http.client.NOT_FOUND

        operator.status = status
        operator.updated = 1
        operator.statusTimestamp = datetime.now()

        operator.save()

        return operator


operatorpin_parser = authentication_parser.copy()
operatorpin_parser.add_argument('pin', type=str, required=True,
                                help='The Operator pin')


@api_namespace.route('/pin/<int:operator_id>/')
class OperatorsPinUpdate(Resource):

    @api_namespace.doc('retrieve_operator')
    @api_namespace.marshal_with(operator_model)
    @api_namespace.expect(operatorpin_parser)
    def put(self, operator_id):
        '''
        set the operator pin
        '''
        args = operatorpin_parser.parse_args()
        authentication_header_parser(args['Authorization'])

        pin = args['pin']
        operator = (OperatorCollection
                    .objects(
                        id=operator_id
                        )
                    .first())

        if not operator:
            # The operator is not present
            return '', http.client.NOT_FOUND

        operator.pin = pin
        operator.updated = 1
        operator.timestamp = datetime.now()

        operator.save()

        return operator


email_parser = api_namespace.parser()
email_parser.add_argument('email', type=str, required=True,
                          help='The Operator email')


@api_namespace.route('/email/')
class OperatorsEmail(Resource):

    @api_namespace.doc('retrieve_operator')
    @api_namespace.marshal_with(operator_model, as_list=True)
    @api_namespace.expect(email_parser)
    def get(self):
        '''
        retrive operator with specified email
        '''
        args = email_parser.parse_args()
        email = args['email']
        operators = OperatorCollection.objects(email=email)

        if not operators:
            # The operator is not present
            return '', http.client.NOT_FOUND

        result = [operator for operator in operators]

        return result


dateQuery_parser = authentication_parser.copy()
dateQuery_parser.add_argument('startdate', type=str, required=True,
                              help="The start date format '%d/%m/%Y'")
dateQuery_parser.add_argument('enddate', type=str, required=True,
                              help="The end date format '%d/%m/%Y'")


@api_namespace.route('/datequery/')
class OperatorsDateQuery(Resource):

    @api_namespace.doc('query count in db')
    @api_namespace.expect(dateQuery_parser)
    def get(self):
        '''
        Help find  the daily signup within a range of dates
        '''
        args = dateQuery_parser.parse_args()
        authentication_header_parser(args['Authorization'])

        start_date_str = args['startdate']
        end_date_str = args['enddate']

        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")

        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")

        result = {}

        if start_date > end_date:
            return '', http.client.BAD_REQUEST

        while start_date <= end_date:

            interval = start_date + timedelta(days=1)

            operator = (OperatorCollection
                        .objects(Q(timestamp__gte=start_date)
                                 &
                                 Q(timestamp__lt=interval))
                        .count())
            date = start_date.strftime("%d/%m/%Y")
            result[date] = operator

            start_date = start_date + timedelta(days=1)

        return result


@api_namespace.route('/sumquery/')
class OperatorsSummaryQuery(Resource):

    @api_namespace.doc('query count in db')
    @api_namespace.expect(authentication_parser)
    def get(self):
        '''
        Help find the sum of records in database
        '''
        args = authentication_parser.parse_args()
        authentication_header_parser(args['Authorization'])
        operator = OperatorCollection.objects.count()

        return operator
