from pyexpat import features

from cfmtoolbox import app, CFM, Feature


@app.command()
def encode_to_smt(cfm: CFM) -> str:
    print("Encoding CFM...")
    encoding = ""

    encoding += declare_constants(cfm.features)
    encoding += create_assert_child_parent_connection(cfm.root.children)

    print(encoding)
    return encoding


def create_assert_child_parent_connection(features: list) -> str:
    childrenAssert = ""


    if len(features) != 0:
        if features.__getitem__(0).parent.parent is None:
            childrenAssert += "(assert "
        else:
            childrenAssert += "(and "
            for feature in features:
                childrenAssert += "(and "
                childrenAssert += "(ite "
                childrenAssert += "(= " + create_const_name(feature.parent) + " 0)"
                childrenAssert += "(= " + create_const_name(feature) + " 0)"
                childrenAssert += "(>= " + create_const_name(feature) + " 0)"
                childrenAssert += ")"
                childrenAssert += create_assert_child_parent_connection(feature.children)
                childrenAssert += ")"
            childrenAssert += " )"

    if len(features) != 0:
        if features.__getitem__(0).parent.parent is None:
            childrenAssert += " )"

    return childrenAssert

def declare_constants(features: list) -> str:
    constants = ""

    for feature in features:
        constants += "(declare-const " + create_const_name(feature) +  " int)\n"

    return constants


def create_const_name(feature: Feature) -> str:
    return "Feature_" + feature.name