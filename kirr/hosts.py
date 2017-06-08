from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'(?!www).*', 'kirr.hostsconf.urls', name='wildcard'),
)
'''
from kirr.hostsconf import urls as redirect_urls

host_patterns = patterns['',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'(?!www).*', redirect_urls, name='wildcard'),
]
'''