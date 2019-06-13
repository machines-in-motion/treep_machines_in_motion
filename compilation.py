#! /usr/bin/python2.7

def dynamic_graph(workspace_path, package_name, package_path,
        log=True, clean=False,  multiprocess=True, build_type="Debug"):
    """
    this function allows to use the tag "compilation: dynamic_graph"
    in repositories.yaml. If you want to compile in release, set the default
    argument of build_type.
    """

    # similar to tree.cmake but destination folder is workspace/devel/

    from treep.coloring import green,dim
    import multiprocessing,os
    
    if log:
        print("\tusing custom compilation script for compiling: "+green(package_name))

    catkin_workspace_path = workspace_path + "workspace"
    devel = os.path.abspath(catkin_workspace_path + os.sep + "devel")
    cmake_suffix = ("-DCMAKE_INSTALL_PREFIX=" + devel +
                    " -DCMAKE_BUILD_TYPE=" + build_type)


    s = ["# calling customized cmake for "+str(package_name)+"\n"]

    s.append("mkdir -p "+devel)
    
    s.append("cd "+package_path)

    build_folder = package_path + os.sep + "build"
    setup_bash = devel + os.sep + "dynamic_graph_setup.bash"
    devel_bin_folder = devel + os.sep + "bin"
    devel_lib_folder = devel + os.sep + "lib"
    devel_plugin_folder = devel_lib_folder + os.sep + "plugin"
    devel_pkgconfig_folder = devel_lib_folder + os.sep + "pkgconfig"
    devel_python_folder = devel_lib_folder + os.sep + "python2.7" + os.sep + "site-packages"
    devel_ros_folder = devel + os.sep + "share"

    s.append("echo \"#! /bin/bash\" > " + setup_bash)
    s.append("echo \"\" >> " + setup_bash)
    s.append("echo \"export PATH=" + devel_bin_folder + ":\$PATH\" >> " + setup_bash)
    s.append("echo \"export PKG_CONFIG_PATH=" + devel_pkgconfig_folder + ":\$PKG_CONFIG_PATH\" >> " + setup_bash)
    s.append("echo \"export LD_LIBRARY_PATH=" + devel_lib_folder + ":\$LD_LIBRARY_PATH\" >> " + setup_bash)
    s.append("echo \"export LD_LIBRARY_PATH=" + devel_plugin_folder + ":\$LD_LIBRARY_PATH\" >> " + setup_bash)
    s.append("echo \"export PYTHONPATH=" + devel_python_folder + ":\$PYTHONPATH\" >> " + setup_bash)
    s.append("echo \"export ROS_PACKAGE_PATH=" + devel_ros_folder + ":\$ROS_PACKAGE_PATH\" >> " + setup_bash)

    s.append("source " + setup_bash)

    if clean:
        if os.path.isdir(build_folder):
            s.append("rm -rf build")
            s.append("mkdir build")

    if not os.path.isdir(build_folder):
        s.append("mkdir build")
        
    s.append("cd build")
    s.append("cmake .. "+cmake_suffix)

    j=""
    if multiprocess:
        cpus = multiprocessing.cpu_count()
        cpus = cpus-1
        if cpus<=0 : cpus = 1
        j = " -j"+str(cpus)

    s.append("make "+j)

    s.append("make install")

    return "\n".join(s)
