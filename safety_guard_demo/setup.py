from setuptools import setup
package_name='safety_guard_demo'
setup(name=package_name,version='0.0.1',packages=[package_name],
    data_files=[('share/ament_index/resource_index/packages',['resource/'+package_name]),
                ('share/'+package_name,['package.xml'])],
    install_requires=['setuptools'],zip_safe=True,maintainer='Demo Maintainer',
    maintainer_email='example@example.invalid',description='Non-certified ROS 2 guard monitor demonstration',
    license='Apache-2.0',entry_points={'console_scripts':['guard_demo = safety_guard_demo.guard_node:main']})
