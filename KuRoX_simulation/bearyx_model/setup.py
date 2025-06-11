import os
from glob import glob
from setuptools import setup

package_name = 'bearyx_model'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name + '/launch'), glob('launch/*.launch.py')),
        (os.path.join('share/' + package_name + '/meshes/stl'), glob('meshes/stl/*.STL')),
        (os.path.join('share/' + package_name + '/meshes/dae'), glob('meshes/dae/*.dae')),
        (os.path.join('share/' + package_name + '/urdf'), glob('urdf/*.urdf')),
        (os.path.join('share/' + package_name + '/rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='TESR',
    maintainer_email='tesrshop@gmail.com',
    description='TESR Beary-x model',
    license='TESR',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
