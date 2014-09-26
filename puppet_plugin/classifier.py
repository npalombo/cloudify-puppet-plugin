from manager import PuppetParamsError
from puppet_classifier.groups import GroupClient, Group

class PuppetClassifier(object):

    def __init__(self, ctx):
        self.ctx = ctx
        self.props = self.ctx.properties['puppet_config']

        self.set_properties()

        server=self.props['server']
        scheme = 'http'
        port = '1261'
        cert=key=cacert = None
        if self.use_ssl:
            scheme = 'https'
            port = '1262'
            # the location of these files is platform dependent.
            #TODO: set defaults based on platform
            config_certname = ctx['config_certname']
            default_cert = '/var/lib/puppet/ssl/certs/%s.pem' % config_certname
            default_key = '/var/lib/puppet/ssl/private_keys/%s.pem' % config_certname
            default_cacert = '/var/lib/puppet/ssl/certs/ca.pem'
            cert = self.group.get('cert', default_cert)
            key = self.group.get('key', default_key)
            cacert = self.group.get('cacert', default_cacert)

        puppet_endpoint_url = '{scheme}://{server}:{port}'.format(scheme=scheme, server=server, port=port)
        self.group_client = GroupClient(puppet_endpoint_url, cert, key, cacert)

    def set_properties(self):
        self.environment = self.props['environment']
        self.group = self.props.get('group')
        self.use_ssl = self.group.get('use_ssl')
        if self.group is not None:
            self.parent_id = self.group.get('parent_id')
            if self.parent_id is None:
                raise PuppetParamsError("parent_id value of group must be set.")
            self.classes = self.group.get('classes')
            if self.classes is None:
                raise PuppetParamsError("classes value of group must be set.")

    def classify(self):
        if self.group is not None:
            config_node_name = self.ctx['config_node_name']
            group_name = 'cloudify_%s' % config_node_name
            match = "^%s.*$" % config_node_name
            rule = ["and",["~","name",match]]
            variables = self.group.get('variables')
            new_group =  Group(
                    group_name,
                    self.parent_id,
                    rule,
                    self.classes,
                    variables=variables,
                    environment=self.environment
                )
            self.group_client.create(new_group)