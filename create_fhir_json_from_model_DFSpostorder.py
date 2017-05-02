# do a level first search of structure to find all props adn create a dict

#imports

import logging
import fhirclient.models.patient as p # import python resource
from json import dumps
import pprint
pp = pprint.PrettyPrinter(indent=4)

# ========= logging ============
# logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format= ' %(asctime)s - %(levelname)s- %(message)s')
logging.info('Start of program')
logging.info('The logging module is working.')


#=========== variables=============
L = []
D = {}  # dictionary we are going to build
ignore_me = ["extension","modifierExtension","contained","id", "assigner"]  # ignore these prop properties -assigner and extension will cause an infinite loop can add to this to remove prop you don't want ( for primitives see below)


# =============code ================

def get_props(props):
    nested_dict = {}
    for prop in props:
        if prop[0] not in ignore_me:
            try:
                logging.info('key in resource = {}' .format(prop[0]))
                new_properties = prop[2]().elementProperties()
                logging.info('current_prop_expansion = {!s}' .format(new_properties))
                logging.info('D[{}] = is a an nested dict' .format(prop[0]))
                if prop[3]: #  if list
                    val = [get_props(new_properties)]
                else:
                    val = get_props(new_properties)
                nested_dict.setdefault(prop[0],val)
            except AttributeError:
                logging.info('exception = is a primitive')
                if prop[3]: #  if list
                    val = [prop[2].__name__]
                else:
                    val = prop[2].__name__
                nested_dict.setdefault(prop[0],val)
                logging.info("D[{!r}] = {!r}" .format(prop[0],nested_dict[prop[0]]))
    return nested_dict


def get_dots(l, e_name, klass='str'):
    try:
        for i in l.elementProperties():  # iterate over all elements in resources
            k = i[0]  # get the element name
            j = i[2]  # get the class
            if k not in ignore_me:  # if element class not = extension or contained
                logging.info('current_prop_expansion = {!s}' .format(j))
                logging.info('key in resource = {}' .format(k))
                if i[3]:
                    k = k + "_0"
                get_dots(j(), e_name + "." + k, j.__name__)
    except AttributeError:
        L.append(e_name + "=" + klass)  # catch the primitive types and put the dot notation in list
    return


def main():

    patient = p.Patient({'id': 'patient-1'})
    resource = patient.elementProperties()
    logging.info('resource = ' + str(resource))
#  e.g.  ("birthDate", "birthDate", fhirdate.FHIRDate, False, None, False)
    get_dots(patient, "patient")

    D = get_props(resource)
    print('dot list = ')
    pp.pprint(L)
    D.setdefault("ResourceType",patient.resource_type)
    print('resource = {}' .format(dumps(D, sort_keys=True, indent=4)))
    return


if __name__ == '__main__':

    main()
    logging.info('End of program')
