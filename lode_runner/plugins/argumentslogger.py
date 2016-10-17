# coding: utf-8

import logging
import inspect

from nose.plugins import Plugin
from functools import wraps

log = logging.getLogger('nose.plugins.argumentslogger')


class ArgumentsLogger(Plugin):
    name = 'argumentslogger'
    enabled = True

    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option('--log-test-arguments', action="store_true",
                          default=env.get('LOG_TEST_ARGUMENTS', False),
                          dest="log_test_arguments",
                          help="Enable logging for test attributes."
                               "[LOG_TEST_ATTRIBUTES]")

    def configure(self, options, conf):
        super(ArgumentsLogger, self).configure(options, conf)
        self.enabled = True
        if not self.enabled:
            return

    def prepareTest(self, test):
        test_method = getattr(test.test, test.test._testMethodName)
        setattr(test.test, test.test._testMethodName, _log_test_arguments(test_method))


def _log_test_arguments(test):
    @wraps(test)
    def wrapper(*args, **kwargs):
        try:
            argspecs = inspect.getargspec(test).args
            argslist = map(lambda x, y: '%s=%s' % (x, y), argspecs, args)[1:]
            log.info('Test arguments: ' + ', '.join(argslist))
        finally:
            log.info('Run test:  %s' % test.__name__)
            return test(*args, **kwargs)
    return wrapper
