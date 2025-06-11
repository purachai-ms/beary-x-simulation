import os
from glob import glob
from setuptools import setup

package_name = 'bearyx_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        (os.path.join('share/' + package_name + '/models/beary_x/meshes'), glob('models/beary_x/meshes/*.dae')),
        (os.path.join('share/' + package_name + '/models/bearyx_world/meshes'), glob('models/bearyx_world/meshes/*.dae')),
        (os.path.join('share/' + package_name + '/worlds/bearyx_empty'), glob('worlds/bearyx_empty/*.model')),
        (os.path.join('share/' + package_name + '/worlds/bearyx_worlds'), glob('worlds/bearyx_worlds/*.model')),
               
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='TESR',
    maintainer_email='tesrshop@gmail.com',
    description='TESR Beary-x Gazebo',
    license='TESR',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
