from owlready2 import *
import requests
import json
import string


onto = get_ontology("http://test.org/onto.owl")
Hapsah = get_ontology("file://Hapsah-ontology.owl").load()


def parse_name(name):
    name = string.capwords(name)
    name = name.replace(" ", "")
    return name


def parse_attribution(attribution_name):
    name = parse_name(attribution_name)
    name = name[0].lower() + name[1:]
    return name


def declare_element(identifier, name, super_element, definition, namespace):
    constructed_element = type(identifier, (super_element, ), {'namespace': namespace})
    constructed_element.label = name
    constructed_element.isDefinedBy = definition
    if super_element == ObjectProperty or super_element == DataProperty:
        constructed_element.python_name = name
    return constructed_element


def declare_attribution(attribution, instance, predicate_counter, ontology):
    predicate_identifier = attribution["attribution"]["identifier"]["type"] +\
                           str(attribution["attribution"]["identifier"]["number"])
    predicate = ontology[predicate_identifier]
    if attribution["instance"]["identifier"]["instanceType"] == "Descriptor":
        predicate = declare_element(predicate_identifier + "A",
                                    attribution["attribution"]["names"][0]["nameSingular"],
                                    ObjectProperty, attribution["attribution"]["definition"]["definition"], ontology)
        undergoer = ontology["D" + str(attribution["instance"]["identifier"]["instanceNumber"])]
    else:
        undergoer = attribution["instance"]["value"]["value"]
    predicate_name = predicate.python_name
    predicate.python_name = "predicate" + str(predicate_counter)
    if predicate.python_name == "predicate1":
        instance.predicate1.append(undergoer)
    if predicate.python_name == "predicate2":
        instance.predicate2.append(undergoer)
    if predicate.python_name == "predicate3":
        instance.predicate3.append(undergoer)
    if predicate.python_name == "predicate4":
        instance.predicate4.append(undergoer)
    if predicate.python_name == "predicate5":
        instance.predicate5.append(undergoer)
    if predicate.python_name == "predicate6":
        instance.predicate6.append(undergoer)
    if predicate.python_name == "predicate7":
        instance.predicate7.append(undergoer)
    if predicate.python_name == "predicate8":
        instance.predicate8.append(undergoer)
    if predicate.python_name == "predicate9":
        instance.predicate9.append(undergoer)
    if predicate.python_name == "predicate10":
        instance.predicate10.append(undergoer)

    predicate.python_name = predicate_name


def declare_association(association, instance, predicate_counter, ontology):
    predicate_identifier = "Association" + str(association["association"]["identifier"]["number"])
    predicate = ontology[predicate_identifier]
    predicate_name = predicate.python_name
    predicate.python_name = "predicate" + str(predicate_counter)
    undergoer = ontology["E" + str(association["instance"]["identifier"]["instanceNumber"])]
    if predicate.python_name == "predicate1":
        instance.predicate1.append(undergoer)
    if predicate.python_name == "predicate2":
        instance.predicate2.append(undergoer)
    if predicate.python_name == "predicate3":
        instance.predicate3.append(undergoer)
    if predicate.python_name == "predicate4":
        instance.predicate4.append(undergoer)
    if predicate.python_name == "predicate5":
        instance.predicate5.append(undergoer)
    if predicate.python_name == "predicate6":
        instance.predicate6.append(undergoer)
    if predicate.python_name == "predicate7":
        instance.predicate7.append(undergoer)
    if predicate.python_name == "predicate8":
        instance.predicate8.append(undergoer)
    if predicate.python_name == "predicate9":
        instance.predicate9.append(undergoer)
    if predicate.python_name == "predicate10":
        instance.predicate10.append(undergoer)

    predicate.python_name = predicate_name


def declare_composition(composition, instance, predicate_counter, ontology):
    for i in ontology.data_properties():
        if i.label[0] == composition["typeNames"][0]["nameSingular"]:
            predicate = i
    predicate_identifier = predicate.python_name
    predicate.python_name = "predicate" + str(predicate_counter)
    undergoer = composition["value"]["value"]
    if predicate.python_name == "predicate1":
        instance.predicate1.append(undergoer)
    if predicate.python_name == "predicate2":
        instance.predicate2.append(undergoer)
    if predicate.python_name == "predicate3":
        instance.predicate3.append(undergoer)
    if predicate.python_name == "predicate4":
        instance.predicate4.append(undergoer)
    if predicate.python_name == "predicate5":
        instance.predicate5.append(undergoer)
    if predicate.python_name == "predicate6":
        instance.predicate6.append(undergoer)
    if predicate.python_name == "predicate7":
        instance.predicate7.append(undergoer)
    if predicate.python_name == "predicate8":
        instance.predicate8.append(undergoer)
    if predicate.python_name == "predicate9":
        instance.predicate9.append(undergoer)
    if predicate.python_name == "predicate10":
        instance.predicate10.append(undergoer)

    predicate.python_name = predicate_identifier


def declare_all_elements(ontology):
    url = "http://localhost:7777/api/type/by-id"
    element_types = ["Association", "Attribute", "Attribution", "Descriptor", "Entity"]
    for element_type in element_types:
        test = True
        i = 1
        while test:
            parameters = {"identifier": json.dumps({
                "type": element_type,
                "number": i,
                "version": 1
            })
            }
            response = requests.get(url, params=parameters)
            if response.status_code != 200:
                test = False
            else:
                data = response.json()
                identifier = data["identifier"]["type"] + str(data["identifier"]["number"])
                name = data["names"][0]["nameSingular"]
                definition = data["definition"]["definition"]
                if element_type == "Entity":
                    declare_element(identifier, name, Thing, definition, ontology)
                if element_type == "Descriptor":
                    declare_element(identifier, name, Hapsah.Descriptor, definition, ontology)
                if element_type == "Attribute":
                    declare_element(identifier, name, DataProperty, definition, ontology)
                if element_type == "Association":
                    association = declare_element(identifier, name, ObjectProperty, definition, ontology)
                    inverse_association = declare_element(identifier + "Inverse",
                                                          data["names"][0]["nameSingularBackward"], ObjectProperty,
                                                          definition, ontology)
                    association.inverse_property = inverse_association
                if element_type == "Attribution":
                    name = name[0].lower() + name[1:]
                    if ontology[identifier] is None:
                        declare_element(identifier, name, DataProperty, definition, ontology)

                i += 1
        if element_type == "Entity":
            declare_all_entities(ontology)
            declare_all_associations(ontology)
        if element_type == "Descriptor":
            declare_all_descriptors(ontology)


def declare_all_entities(ontology):
    url = "http://localhost:7777/api/entity-instance/by-number"
    test = True
    instance_number = 1
    while test is True:
        parameters = {"instanceNumber": instance_number}
        response = requests.get(url, params=parameters)
        if response.status_code != 200:
            print("Fail")
            test = False
        else:
            data = response.json()
            super_class = ontology[data["identifier"]["instanceType"] + str(data["identifier"]["typeNumber"])]
            instance = super_class("E" + str(instance_number))
            instance_number += 1


def declare_all_descriptors(ontology):
    url = "http://localhost:7777/api/descriptor-instance/by-number"
    test = True
    instance_number = 1
    while test is True:
        parameters = {"instanceNumber": instance_number}
        response = requests.get(url, params=parameters)
        if response.status_code != 200:
            print("Fail")
            test = False
        else:
            data = response.json()
            super_class = ontology[data["identifier"]["instanceType"] + str(data["identifier"]["typeNumber"])]
            descriptor = super_class("D" + str(instance_number))
            predicate_counter = 1
            for composition in data["compositions"]:
                declare_composition(composition, descriptor, predicate_counter, ontology)
                predicate_counter += 1
            instance_number += 1


def declare_all_associations(ontology):
    url = "http://localhost:7777/api/entity-instance/by-number"
    test = True
    instance_number = 1
    while test is True:
        parameters = {"instanceNumber": instance_number}
        response = requests.get(url, params=parameters)
        if response.status_code != 200:
            print("Fail")
            test = False
        else:
            data = response.json()
            instance = onto["E" + str(data["identifier"]["instanceNumber"])]
            predicate_counter = 1
            for attribution in data["attributions"]:
                declare_attribution(attribution, instance, predicate_counter, ontology)
                predicate_counter += 1
            for association in data["outgoingAssociations"]:
                declare_association(association, instance, predicate_counter, ontology)
                predicate_counter += 1
            instance_number += 1


declare_all_elements(onto)

onto.save(file="prototype1.5.owl")