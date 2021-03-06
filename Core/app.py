import pprint
from abc import ABCMeta

import Core.DB


class Entity(object):
    __metaclass__ = ABCMeta

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.__dict__))

    def persist(self):
        """for all variable in the (respective) class,
        it checks if not None and fires
        an SQL INSERT query to persist (or rollback and
        some custom Exception)"""
        # print ("inside Entity.persist()")
        # raise NotImplementedError("Class %s does not (yet) implement"
        #                           "method persist()" %
        #                           (self.__class__.__name__))

        # def prettyPrint(self):
        #     # After thought: should be replaced by overriding __str__
        #     """Optional function.
        #     Should return a pretty String to be displayed to the user"""

    def from_dict(self, init_dict):
        for key in init_dict:
            setattr(self, key, init_dict[key])
        return self

    def print_item(self):
        pprint.pprint(self.__dict__)


class Customer(Entity):
    def __init__(self, name=None):
        self.name = name
        self.id = None

    def print_item(self):
        print "\nWelcome %s!" % self.name


class Employee(Entity):
    def __init__(self, name=None, franchise_id=None, manager_id=None):
        self.id = None
        self.name = name
        self.manager_id = manager_id
        self.franchise_id = franchise_id

    def print_employee_entity(self):
        print self.name, "  manager id : ", self.manager_id, " franchise id : ", self.franchise_id


class Franchise(Entity):
    def __init__(self, name=None, st_address=None, address=None, city=None, state=None, zip=None,
                 manager_id=None):
        self.id = None
        self.name = name
        self.st_address = st_address
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.manager_id = manager_id


class Product(Entity):
    def __init__(self, name=None):
        self.id = None
        self.name = name


class Service(Entity):
    def __init__(self, name=None):
        self.id = None
        self.name = name


class Feedback(Entity):
    def __init__(self, rating=None, comments=None, customer_id=None, item_id=None, franchise_id=None):
        self.rating = rating
        self.comments = comments
        self.customer_id = customer_id
        self.item_id = item_id
        self.franchise_id = franchise_id


class ProductFeedback(Feedback):
    def __init__(self, rating=0, comments="", customer_id=0, item_id=0,
                 franchise_id=0):
        self.product_feedback_id = None
        super(ProductFeedback, self).__init__(rating, comments, customer_id,
                                              item_id, franchise_id)

    def from_dict(self, init_dict):
        if 'product_feedback_id' in init_dict:
            self.product_feedback_id = init_dict['product_feedback_id']
        if 'ratings' in init_dict:
            self.rating = init_dict['ratings']
        if 'customer_id' in init_dict:
            self.customer_id = init_dict['customer_id']
        if 'product_id' in init_dict:
            self.item_id = init_dict['product_id']
        if 'comments' in init_dict:
            self.comments = init_dict['comments']
        if 'franchise_id' in init_dict:
            self.franchise_id = init_dict['franchise_id']
        return self

    def __eq__(self, other):
        if isinstance(other, ProductFeedback):
            return self.__dict__ == other.__dict__
        else:
            return False

    def print_item(self):
        print "product feedback id : ", self.product_feedback_id, " rating : ", self.rating, "comments ", self.comments, "product id ", self.item_id

    def persist(self):
        db = Core.DB.DB()
        db.insert_feedback_record("product",
                                  (self.rating, self.customer_id, self.item_id,
                                   self.comments, self.franchise_id))


class ServiceFeedback(Feedback):
    def __init__(self, rating=0, comments="", customer_id=0, item_id=0,
                 franchise_id=0):
        self.service_feedback_id = None
        super(ServiceFeedback, self).__init__(rating, comments, customer_id,
                                              item_id, franchise_id)

    def print_item(self):
        print "service feedback id : ", self.service_feedback_id, " rating : ", self.rating, "comments ", self.comments, "service id ", self.item_id

    def from_dict(self, init_dict):
        if 'service_feedback_id' in init_dict:
            self.service_feedback_id = init_dict['service_feedback_id']
        if 'ratings' in init_dict:
            self.rating = init_dict['ratings']
        if 'customer_id' in init_dict:
            self.customer_id = init_dict['customer_id']
        if 'service_id' in init_dict:
            self.item_id = init_dict['service_id']
        if 'comments' in init_dict:
            self.comments = init_dict['comments']
        if 'franchise_id' in init_dict:
            self.franchise_id = init_dict['franchise_id']
        return self

    def __eq__(self, other):
        if isinstance(other, ServiceFeedback):
            return self.__dict__ == other.__dict__
        else:
            return False

    def persist(self):
        db = Core.DB.DB()
        db.insert_feedback_record("service",
                                  (self.rating, self.customer_id, self.item_id,
                                   self.comments, self.franchise_id))


class ActionItems(Entity):
    def __init__(self, action_item_id=None, start_date=None, end_date=None, action_status=None, assigned_to=None,
                 created_by=None, comments=None, service_feedback_id=None, product_feedback_id=None):
        self.assigned_to = assigned_to
        self.action_item_id = action_item_id
        self.start_date = start_date
        self.end_date = end_date
        self.service_feedback_id = service_feedback_id
        self.product_feedback_id = product_feedback_id
        self.comments = comments
        self.created_by = created_by
        self.action_status = action_status

    def __eq__(self, other):
        if isinstance(other, ActionItems):
            return self.__dict__ == other.__dict__
        else:
            return False

    def print_item(self):
        print "ID : %s, comments : %s, start date : %s, end date : %s" % \
            (self.action_item_id, self.comments,
                self.start_date.strftime("%m-%d-%y %H:%M:%S"),
                self.end_date.strftime("%m-%d-%y %H:%M:%S"))

    def persist(self):
        pass  # TODO implement


class Logins(Entity):
    def __init__(self, entity_type=None, id=None, pswd=None):
        self.entity_type = entity_type
        self.id = id
        self.pswd = pswd


class SoldBy(Entity):
    def __init__(self, product_id=None, franchise_id=None):
        self.product_id = product_id
        self.franchise_id = franchise_id


class ServiceProvidedBy(Entity):
    def __init__(self, service_id, employee_id):
        self.service_id = service_id
        self.employee_id = employee_id
