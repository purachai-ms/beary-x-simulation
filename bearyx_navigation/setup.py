import os
from glob import glob
from setuptools import setup
from setuptools import find_packages

package_name = 'bearyx_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share/'+ package_name + '/launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name), glob('map/*')),
        (os.path.join('share/' + package_name + '/config'), glob('config/*')),
        (os.path.join('share/' + package_name + '/rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tesr',
    maintainer_email='tesrshop@gmail.com',
    description='TESR Navigation',
    license='TESR',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_position_tracking = bearyx_navigation.robot_position:main',
        ],
    },
)
