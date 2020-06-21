from setuptools import find_packages, setup

from paypalv2 import VERSION

install_requires = [
    'django-oscar==2.0.4',
    'paypal-checkout-serversdk',
    'django>=2.2,<2.3',
]


# @todo: license...
setup(
    name='oscar-paypalcheckout',  # @todo: this right?
    version=VERSION,
    url='https://github.com/ThorstenMauch/oscar-paypalcheckout',
    description="Updated version of paypal checkout.",  # @todo: like this?
    long_description=open('README.md').read(),
    keywords='Payment, PayPal, Oscar',
    platforms=['windows'],  # @todo: this right?
    find_packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'oscar': ['django-oscar>=2.0,<2.1']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8', # @todo: we can expand on this once tox with multiple versions is setup
        'Topic :: Other/Nonlisted Topic'],
)
