from argparse import ArgumentParser
from pathlib import Path
import jinja2

env = jinja2.Environment()

base_cmakelist_template = env.from_string(
    "cmake_minimum_required(VERSION 3.12)\n"
    "project({{project}})\n\n"
    "# Set the output directories for all build types\n"
    "set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)\n"
    "set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)\n"
    "set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)\n"
    "set(CMAKE_CXX_STANDARD 20)\n"
    "set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n\n"
)

base_cmakelist_exe_modifier_template = env.from_string(
    "add_subdirectory({{exe}})\n\n"
)

base_cmakelist_lib_modifier_template = env.from_string(
    "add_subdirectory({{lib}})\n\n"
)

build_script = \
    "#!/bin/bash\n\n\n" \
    "cmake -S . -B build\n" \
    "cmake --build build\n" \

exe_cmakelist_template = env.from_string(
    "add_executable({{exe}} src/main.cpp)\n\n"
)

target_cmakelist_lib_modifier_template = env.from_string(
    "target_link_libraries({{target}} LINK_PUBLIC {{libs}})\n\n"
)


exe_main_cpp = \
    "#include <iostream>\n\n" \
    "using namespace std;\n\n" \
    "int main() {\n" \
    "    cout << \"hello world\" << endl;\n" \
    "}\n\n"

exe_main_cpp_for_lib_template = env.from_string(
    "#include <iostream>\n\n"
    "#include <{{lib}}.hpp>\n\n"
    "using namespace std;\n\n"
    "int main() {\n"
    "    cout << get_word() << endl;\n"
    "}\n\n"
)

lib_cmakelist_template = env.from_string(
    "add_library({{lib}} SHARED src/{{lib}}.cpp)\n\n"
    "target_include_directories ({{lib}} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)\n\n"
)

lib_header = \
    "#pragma once\n\n" \
    "#include <string>\n\n" \
    "std::string get_word();\n\n"

lib_cpp_template = env.from_string(
    "#include \"{{lib}}.hpp\"\n\n"
    "std::string get_word() {\n" \
    "   return \"word\";\n" \
    "}\n\n"
)

def target_link_libs(target, libs=[], link_sfml=False, link_eigen=False):
    if link_sfml:
        libs.append("sfml-graphics")

    if link_eigen:
        libs.append("Eigen3::Eigen")

    if not libs:
        return None
    
    return target_cmakelist_lib_modifier_template.render(target=target, libs=" ".join(libs))

def main(args):
    destination = Path(args.destination)
    project = args.project if args.project is not None else destination.name

    if destination.exists():
        print("Can't initialize a project in a folder that already exists!")
        return

    destination.mkdir(parents=True)

    base_cmakelist = destination / "CMakeLists.txt"

    with open(base_cmakelist, "w") as f:
        f.write(base_cmakelist_template.render(project=project))
        if args.sfml:
            f.write("find_package(SFML 2.5 COMPONENTS graphics REQUIRED)\n\n")
        if args.eigen:
            f.write("find_package(Eigen3 3.4 REQUIRED NO_MODULE)\n\n")

    script = destination / "run_build"
    with open(script, "w") as f:
        f.write(build_script)
    script.chmod(0o0777)

    exe = args.exe if args.exe else project 
    exe_dir = destination / exe
    exe_dir.mkdir()

    with open(base_cmakelist, "a") as f:
        f.write(base_cmakelist_exe_modifier_template.render(exe=exe_dir.name))
    
    exe_cmakelist = exe_dir / "CMakeLists.txt"
    with open(exe_cmakelist, "w") as f:
        f.write(exe_cmakelist_template.render(exe=exe))
    
    src_dir = exe_dir / "src"
    src_dir.mkdir()
    exe_main = src_dir / "main.cpp"
    with open(exe_main, "w") as f:
        if args.sfml:
            with open("./templates/sfml_main.cpp", "r") as ft:
                f.write(ft.read())
        else:
            f.write(exe_main_cpp)

    if args.lib:
        lib = args.lib
        lib_dir = destination / lib
        lib_dir.mkdir()

        include_dir = lib_dir / "include"
        include_dir.mkdir()

        src_dir = lib_dir / "src"
        src_dir.mkdir()

        with open(base_cmakelist, "a") as f:
            f.write(base_cmakelist_lib_modifier_template.render(lib=lib))

        with open(lib_dir / "CMakeLists.txt", "w") as f:
            f.write(lib_cmakelist_template.render(lib=lib))
            link_libs = target_link_libs(lib, link_sfml=args.sfml, link_eigen=args.eigen)
            if link_libs is not None:
                f.write(link_libs)

        with open(include_dir / f"{lib}.hpp", "w") as f:
            f.write(lib_header)

        with open(src_dir / f"{lib}.cpp", "w") as f:
            f.write(lib_cpp_template.render(lib=lib))

        # we overwrite the main exe logic for example lib call
        with open(exe_main, "w") as f:
            f.write(exe_main_cpp_for_lib_template.render(lib=lib))

        with open(exe_cmakelist, "a") as f:
            f.write(target_cmakelist_lib_modifier_template.render(target=exe, libs=lib))
    else:
        # if we didn't add the lib with deps above, we check if we should add them
        # directly to exe cmakelist here
        link_libs = target_link_libs(exe, link_sfml=args.sfml, link_eigen=args.eigen)
        if link_libs is not None:
            with open(exe_cmakelist, "a") as f:
                f.write(link_libs)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("destination")
    parser.add_argument("--project", help="if provided, will be used as project name, otherwise destination is used.")
    parser.add_argument("--lib", help="if provided, it will initialize a library subfolder.")
    parser.add_argument("--exe", help="if provided, will be used as executable folder name.")
    parser.add_argument("--sfml", help="if set, will add sfml flags", action="store_true", default=False)
    parser.add_argument("--eigen", help="if set, will add eigen flags", action="store_true", default=False)

    main(parser.parse_args())
