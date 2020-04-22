from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class GQLClient(Client):
    """ Patches execute method to return error object instead of stringified version """
    def execute(self, document, *args, **kwargs):
        if self.schema:
            self.validate(document)

        result = self._get_result(document, *args, **kwargs)
        if result.errors:
            raise Exception(result.errors[0])

        return result.data

class InvalidAuth(Exception):
    pass

class NotifyBoxApi:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = None
        self._create_client()
        self._authenticate()

    def _create_client(self):
        headers = {
            "Content-type": "application/json",
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        sample_transport=RequestsHTTPTransport(
            url='http://localhost:8080/v1/graphql',
            use_json=True,
            headers=headers,
            verify=False
        )

        self.client = GQLClient(
            retries=3,
            transport=sample_transport,
            fetch_schema_from_transport=True,
        )

    def _authenticate(self):
        self.token = self.createToken()['createToken']
        self._create_client()

    def createToken(self):
        data = {
            "access_key": self.access_key,
            "secret_key": self.secret_key,
        }
        query = gql('''
            mutation CreateToken($access_key: String!, $secret_key: String!) {
              createToken(access_key: $access_key, secret: $secret_key)
            }
        ''')

        try:
            result = self.client.execute(query, variable_values=data)
        except Exception as e:
            if e.args[0]['message'] == 'The provided secret is invalid':
                raise InvalidAuth()

            raise

        return result

    ########
    # Kind #
    ########
    def createKind(self, value):
        data = {
            "value": value
        }
        query = gql('''
            mutation CreateKind($value: String!) {
              insert_notificationKind_one(object: {value: $value}) {
                id,
                value
              }
            }
        ''')
        result = self.client.execute(query, variable_values=data)

        return result

    def getKind(self, value):
        data = {
            "value": value
        }
        query = gql('''
            query getKind($value: String!) {
              notificationKind(where: {value: {_eq: $value}}) {
                id,
                value
              }
            }
        ''')
        result = self.client.execute(query, variable_values=data)

        return result

    def getOrCreateKind(self, value):
        try:
            return self.createKind(value)['insert_notificationKind_one']
        except Exception as e:
            if e.args[0]['message'].startswith('Uniqueness violation'):
                return self.getKind(value)['notificationKind'][0]
            raise e

    ############
    # Template #
    ############
    def createTemplate(self, kind_id, via, recipient_type, locale, data_string, body, version=1):
        data = {
            "kind_id": kind_id,
            "locale": locale,
            "data": data_string,
            "value": body,
            "via": via,
            "recipient_type": recipient_type,
            "version": version
        }
        query = gql('''
            mutation CreateTemplate(
                $kind_id: Int!,
                $version: Int!,
                $recipient_type: String!
                $locale: String!,
                $data: CreateMessagetemplateJsonb!,
                $value: String!,
                $via: _notificationVia_enum!,
            ) {
                create_messageTemplate(data: $data, kind_id: $kind_id, locale: $locale, value: $value, version: $version, via: $via, recipient_type: $recipient_type) {
                    id,
                    data,
                    value,
                    via,
                    locale,
                    version,
                    recipient_type
                }
            }
        ''')
        result = self.client.execute(query, variable_values=data)

        return result

    def getLatestTemplate(self, kind_id, via, recipient_type):
        data = {
            "kind_id": kind_id,
            "via": via,
            "recipient_type": recipient_type
        }
        query = gql('''
            query getTemplate(
                $kind_id: bigint!,
                $recipient_type: String!,
                $via: notificationVia_enum!
            ) {
              messageTemplate(
                 order_by: { version: desc },
                 limit: 1,
                 where: {
                    kind_id: {_eq: $kind_id},
                    via: {_eq: $via},
                    recipient_type: {_eq: $recipient_type}
                 }
              ) {
                id,
                data,
                value,
                via,
                locale,
                version,
                recipient_type
              }
            }
        ''')
        result = self.client.execute(query, variable_values=data)

        return result

    def createOrUpdateTemplate(self, kind_id, via, recipient_type, locale, data_string, body):
        try:
            return self.createTemplate(kind_id, via, recipient_type, locale, data_string, body)['create_messageTemplate']
        except Exception as e:
            if e.args[0]['message'].endswith('unique constraint "messageTemplate_via_kind_id_version_recipient_type_key"'):
                version = self.getLatestTemplate(kind_id, via, recipient_type)['messageTemplate'][0]["version"]
                return self.createTemplate(kind_id, via, recipient_type, locale, data_string, body, version+1)['create_messageTemplate']
            raise e

    ###########
    # Trigger #
    ###########
    def getTrigger(self, kind_id, recipient_type):
        data = {
            "kind_id": kind_id,
            "recipient_type": recipient_type,
        }
        query = gql('''
            query GetTrigger(
                $kind_id: bigint!,
                $recipient_type: String!
            ) {
                notificationTrigger(where: {
                    kind_id: {_eq: $kind_id},
                    recipient_type: {_eq: $recipient_type}
                }) {
                    id,
                    kind_id,
                    message_template_id,
                    recipient_type
                }
            }
        ''')
        result = self.client.execute(query, variable_values=data)

        return result

    def createTrigger(self, kind_id, message_template_id, recipient_type):
        data = {
            "kind_id": kind_id,
            "message_template_id": message_template_id,
            "recipient_type": recipient_type,
        }
        query = gql('''
            mutation CreateTrigger(
                $kind_id: bigint!,
                $message_template_id: bigint!,
                $recipient_type: String!
            ) {
                insert_notificationTrigger_one(object: {kind_id: $kind_id, message_template_id: $message_template_id, recipient_type: $recipient_type}) {
                    id,
                    kind_id,
                    message_template_id,
                    recipient_type
                }
            }
        ''')
        result = self.client.execute(query, variable_values=data)

        return result

    def updateTrigger(self, kind_id, message_template_id, recipient_type):
        data = {
            "kind_id": kind_id,
            "message_template_id": message_template_id,
            "recipient_type": recipient_type,
        }
        query = gql('''
            mutation UpdateTrigger(
                $kind_id: bigint!,
                $message_template_id: bigint!,
                $recipient_type: String!
            ) {
                update_notificationTrigger(
                    _set: {kind_id: $kind_id, message_template_id: $message_template_id, recipient_type: $recipient_type},
                    where: {kind_id: {_eq: $kind_id}, recipient_type: {_eq: $recipient_type}}
                ) {
                    returning {
                        id,
                        kind_id,
                        message_template_id,
                        recipient_type
                    }
                }
            }
        ''')
        result = self.client.execute(query, variable_values=data)

        return result

    def createOrUpdateTrigger(self, kind_id, message_template_id, recipient_type):
        triggers = self.getTrigger(kind_id, recipient_type)['notificationTrigger']

        if len(triggers):
            return self.updateTrigger(kind_id, message_template_id, recipient_type)['update_notificationTrigger']['returning'][0]
        else:
            return self.createTrigger(kind_id, message_template_id, recipient_type)['insert_notificationTrigger_one']
