# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_helm' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

from packaging.requirements import Requirement


def main():
    """Calculate the lower bound of dependencies where possible."""
    with open("requirements.txt") as req_file:
        for line in req_file:
            try:
                requirement = Requirement(line)
            except ValueError:
                print(line.strip())
            else:
                for spec in requirement.specifier:
                    if spec.operator == ">=":
                        if requirement.name == "pulpcore":
                            operator = "~="
                        else:
                            operator = "=="
                        min_version = str(spec)[2:]
                        print(f"{requirement.name}{operator}{min_version}")
                        break
                else:
                    print(line.strip())


if __name__ == "__main__":
    main()
