from dotmap import DotMap

from unittest import TestCase
from unittest.mock import patch, MagicMock

from rancon.backends import consul

TEST_SERVICES = [DotMap({
    'name': sname,
    'host': 'host_{}'.format(sname),
    'port': str(10001 + i),
}) for i, sname in enumerate(('one', 'two', 'three'))]


class TestConsulStatic(TestCase):

    def setUp(self):
        self.consul = consul.ConsulBackend(url="http://loglhost:7500")

    @patch('rancon.backends.consul.consul')
    def test_register(self, mock):
        con = self.consul.register(TEST_SERVICES[0])
        consul_mock = mock.Consul
        self.assertTrue(consul_mock.called)
        consul_mock.assert_called_with(host="loglhost", port=7500, scheme='http')


class TestConsulDynamic(TestCase):

    def setUp(self):
        self.consul = consul.ConsulBackend(url="http://%HOST%")

    @patch('rancon.backends.consul.consul')
    def test_register(self, mock):
        def register_mock(*args, **kwargs):
            return args[1]
        # prepare side effect
        consul_mock = mock.Consul
        mock_agent = consul_mock.return_value.agent.service.register
        mock_agent.side_effect = register_mock
        _, con0 = self.consul.register(TEST_SERVICES[0])
        self.assertEqual(1, len(self.consul.consul_inst_cache))
        _, con1 = self.consul.register(TEST_SERVICES[1])
        self.assertEqual(2, len(self.consul.consul_inst_cache))
        # check return values
        self.assertEqual('one-host-one-10001', con0)
        self.assertEqual('two-host-two-10002', con1)
        # check calls
        self.assertTrue(consul_mock.called)
        # nice:
        # http://stackoverflow.com/questions/7242433/asserting-successive-calls-to-a-mock-method
        consul_mock.assert_any_call(host="host_one", port=8500, scheme='http')
        consul_mock.assert_any_call(host="host_two", port=8500, scheme='http')
        self.assertEqual(2, consul_mock.call_count)
        self.assertTrue(mock_agent.called)
        mock_agent.assert_any_call('one', 'one-host-one-10001',
                             address='host_one',
                             port=10001,
                             tags=['rancon-cleanup-id-default', 'rancon'])
        mock_agent.assert_any_call('two', 'two-host-two-10002',
                             address='host_two',
                             port=10002,
                             tags=['rancon-cleanup-id-default', 'rancon'])
